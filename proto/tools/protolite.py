#!/usr/bin/env python3
"""protolite: a minimal proto3 toolchain for the Leaf wire protocol.

protoc and buf are not installed in this environment, so this module does
the three jobs the round-trip test needs:

1. parse()       reads the subset of proto3 that leaf.proto uses
                 (top-level enums and messages, scalar/enum/message fields,
                 repeated, one oneof per message, comments).
2. descriptor()  turns the parse into a google.protobuf FileDescriptorProto,
                 so the official python runtime builds real message classes.
3. encode()/decode()  an independent, hand-rolled canonical codec that works
                 from plain dicts. The test checks that both stacks produce
                 identical bytes, so neither one is trusted alone.

Canonical encoding (proto/VERSIONING.md): fields in ascending number order,
minimal varints, proto3 defaults omitted (except a set oneof member),
packed repeated scalars.
"""
import re
import struct

SCALARS = {
    # name: (wire type, FieldDescriptorProto.Type number)
    "double": (1, 1), "float": (5, 2), "int64": (0, 3), "uint64": (0, 4),
    "int32": (0, 5), "fixed64": (1, 6), "fixed32": (5, 7), "bool": (0, 8),
    "string": (2, 9), "bytes": (2, 12), "uint32": (0, 13),
    "sfixed32": (5, 15), "sfixed64": (1, 16), "sint32": (0, 17), "sint64": (0, 18),
}
TYPE_MESSAGE, TYPE_ENUM = 11, 14


class Field:
    def __init__(self, name, type_name, number, repeated, oneof):
        self.name, self.type_name, self.number = name, type_name, number
        self.repeated, self.oneof = repeated, oneof
        self.kind = None  # "scalar" | "enum" | "message", resolved later

    def __repr__(self):
        return f"Field({self.name}:{self.type_name}={self.number})"


class Schema:
    def __init__(self, package):
        self.package = package
        self.enums = {}      # name -> {value_name: number}
        self.messages = {}   # name -> [Field] sorted by number

    def fields(self, msg):
        return self.messages[msg]


def _strip_comments(text):
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"//[^\n]*", "", text)


def parse(path):
    text = _strip_comments(open(path, encoding="utf-8").read())
    toks = re.findall(r"[A-Za-z_][\w.]*|\d+|[{}=;]|\"[^\"]*\"", text)
    i = 0
    schema = None

    def expect(t):
        nonlocal i
        if toks[i] != t:
            raise SyntaxError(f"expected {t!r}, got {toks[i]!r} at token {i}")
        i += 1

    while i < len(toks):
        t = toks[i]
        if t == "syntax":
            i += 1; expect("="); expect('"proto3"'); expect(";")
        elif t == "package":
            schema = Schema(toks[i + 1]); i += 2; expect(";")
        elif t == "enum":
            name = toks[i + 1]; i += 2; expect("{")
            vals = {}
            while toks[i] != "}":
                vname = toks[i]; i += 1; expect("=")
                vals[vname] = int(toks[i]); i += 1; expect(";")
            i += 1
            if len(set(vals.values())) != len(vals):
                raise SyntaxError(f"duplicate value in enum {name}")
            schema.enums[name] = vals
        elif t == "message":
            name = toks[i + 1]; i += 2; expect("{")
            fields, oneof = [], None
            while True:
                t = toks[i]
                if t == "}":
                    if oneof is not None:
                        oneof = None; i += 1; continue
                    i += 1; break
                if t == "oneof":
                    oneof = toks[i + 1]; i += 2; expect("{"); continue
                rep = t == "repeated"
                if rep:
                    i += 1
                ftype, fname = toks[i], toks[i + 1]; i += 2; expect("=")
                fnum = int(toks[i]); i += 1; expect(";")
                fields.append(Field(fname, ftype, fnum, rep, oneof))
            nums = [f.number for f in fields]
            if len(set(nums)) != len(nums):
                raise SyntaxError(f"duplicate field number in {name}")
            schema.messages[name] = sorted(fields, key=lambda f: f.number)
        else:
            raise SyntaxError(f"unexpected token {t!r}")
    for msg, fields in schema.messages.items():
        for f in fields:
            if f.type_name in SCALARS:
                f.kind = "scalar"
            elif f.type_name in schema.enums:
                f.kind = "enum"
            elif f.type_name in schema.messages:
                f.kind = "message"
            else:
                raise SyntaxError(f"{msg}.{f.name}: unknown type {f.type_name}")
    return schema


# ------------------------------------------------------------ descriptor ---

def descriptor(schema, filename="budlum/leaf/v1/leaf.proto"):
    from google.protobuf import descriptor_pb2 as d
    fdp = d.FileDescriptorProto(name=filename, package=schema.package, syntax="proto3")
    for ename, vals in schema.enums.items():
        e = fdp.enum_type.add(name=ename)
        for vn, num in vals.items():
            e.value.add(name=vn, number=num)
    for mname, fields in schema.messages.items():
        m = fdp.message_type.add(name=mname)
        oneofs = []
        for f in fields:
            fd = m.field.add(name=f.name, number=f.number, json_name=_camel(f.name))
            fd.label = 3 if f.repeated else 1
            if f.kind == "scalar":
                fd.type = SCALARS[f.type_name][1]
            elif f.kind == "enum":
                fd.type = TYPE_ENUM; fd.type_name = f".{schema.package}.{f.type_name}"
            else:
                fd.type = TYPE_MESSAGE; fd.type_name = f".{schema.package}.{f.type_name}"
            if f.oneof:
                if f.oneof not in oneofs:
                    oneofs.append(f.oneof); m.oneof_decl.add(name=f.oneof)
                fd.oneof_index = oneofs.index(f.oneof)
    return fdp


def _camel(s):
    parts = s.split("_")
    return parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:])


def message_classes(schema):
    from google.protobuf import descriptor_pool, message_factory
    pool = descriptor_pool.DescriptorPool()
    fd = pool.Add(descriptor(schema))
    return {name: message_factory.GetMessageClass(fd.message_types_by_name[name])
            for name in schema.messages}


# ------------------------------------------------------- hand-rolled codec ---

def _varint(n):
    if n < 0:
        n &= (1 << 64) - 1
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def _zigzag(n):
    return (n << 1) ^ (n >> 63)


def _unzigzag(n):
    return (n >> 1) ^ -(n & 1)


def _scalar_bytes(type_name, v):
    if type_name in ("sint32", "sint64"):
        return _varint(_zigzag(v))
    if type_name == "bool":
        return _varint(1 if v else 0)
    if type_name in ("int32", "int64", "uint32", "uint64"):
        return _varint(v)
    if type_name == "double":
        return struct.pack("<d", v)
    if type_name == "float":
        return struct.pack("<f", v)
    if type_name in ("fixed32",):
        return struct.pack("<I", v)
    if type_name in ("sfixed32",):
        return struct.pack("<i", v)
    if type_name in ("fixed64",):
        return struct.pack("<Q", v)
    if type_name in ("sfixed64",):
        return struct.pack("<q", v)
    raise TypeError(type_name)


def _is_default(f, v):
    if f.kind == "message":
        return v is None
    if f.type_name in ("string",):
        return v == ""
    if f.type_name in ("bytes",):
        return v == b""
    if f.type_name == "bool":
        return v is False
    return v == 0


def _enum_num(schema, f, v):
    return schema.enums[f.type_name][v] if isinstance(v, str) else int(v)


def encode(schema, msg, obj):
    """Encode a dict to canonical proto3 bytes. Enum values may be names."""
    out = bytearray()
    known = {f.name for f in schema.fields(msg)}
    extra = set(obj) - known
    if extra:
        raise KeyError(f"{msg}: unknown fields {sorted(extra)}")
    for f in schema.fields(msg):
        if f.name not in obj:
            continue
        v = obj[f.name]
        key_ld = _varint((f.number << 3) | 2)
        if f.repeated:
            if not v:
                continue
            if f.kind == "message":
                for item in v:
                    b = encode(schema, f.type_name, item)
                    out += key_ld + _varint(len(b)) + b
            elif f.type_name in ("string", "bytes"):
                for item in v:
                    b = item.encode() if f.type_name == "string" else bytes(item)
                    out += key_ld + _varint(len(b)) + b
            else:
                if f.kind == "enum":
                    body = b"".join(_varint(_enum_num(schema, f, x)) for x in v)
                else:
                    body = b"".join(_scalar_bytes(f.type_name, x) for x in v)
                out += key_ld + _varint(len(body)) + body
            continue
        if f.oneof is None and _is_default(f, v if f.kind != "enum" else _enum_num(schema, f, v)):
            continue
        if f.kind == "message":
            b = encode(schema, f.type_name, v)
            out += key_ld + _varint(len(b)) + b
        elif f.type_name in ("string", "bytes"):
            b = v.encode() if f.type_name == "string" else bytes(v)
            out += key_ld + _varint(len(b)) + b
        elif f.kind == "enum":
            out += _varint(f.number << 3) + _varint(_enum_num(schema, f, v))
        else:
            wt = SCALARS[f.type_name][0]
            out += _varint((f.number << 3) | wt) + _scalar_bytes(f.type_name, v)
    return bytes(out)


def _read_varint(buf, i):
    shift = n = 0
    start = i
    while True:
        b = buf[i]; i += 1
        n |= (b & 0x7F) << shift
        shift += 7
        if not b & 0x80:
            break
        if shift > 63:
            raise ValueError("varint too long")
    if i - start > 1 and buf[i - 1] == 0:
        raise ValueError("non-minimal varint")
    return n, i


def _signed(type_name, n):
    if type_name in ("int32",):
        n &= (1 << 64) - 1
        return n - (1 << 64) if n >= 1 << 63 else n
    if type_name == "int64":
        return n - (1 << 64) if n >= 1 << 63 else n
    return n


def decode(schema, msg, buf, strict=True):
    """Decode canonical bytes to a dict with enum names. strict=True rejects
    out-of-order fields and unknown fields, as U6 does for SliceHeader."""
    fields = {f.number: f for f in schema.fields(msg)}
    obj = {}
    i, last = 0, 0
    rev_enum = {e: {v: k for k, v in vals.items()} for e, vals in schema.enums.items()}
    while i < len(buf):
        key, i = _read_varint(buf, i)
        num, wt = key >> 3, key & 7
        f = fields.get(num)
        if f is None:
            if strict:
                raise ValueError(f"{msg}: unknown field {num}")
            raise NotImplementedError("skip of unknown fields not needed")
        if strict and num < last:
            raise ValueError(f"{msg}: field {num} out of order")
        if strict and num == last and not f.repeated:
            raise ValueError(f"{msg}: field {num} repeated")
        last = num
        if wt == 2:
            ln, i = _read_varint(buf, i)
            chunk = bytes(buf[i:i + ln]); i += ln
            if f.kind == "message":
                val = decode(schema, f.type_name, chunk, strict)
            elif f.type_name == "string":
                val = chunk.decode()
            elif f.type_name == "bytes":
                val = chunk
            else:  # packed
                vals, j = [], 0
                while j < len(chunk):
                    if SCALARS.get(f.type_name, (0,))[0] == 0 or f.kind == "enum":
                        n, j = _read_varint(chunk, j)
                        vals.append(_conv(f, n, rev_enum))
                    else:
                        size = 8 if SCALARS[f.type_name][0] == 1 else 4
                        vals.append(_fixed(f.type_name, chunk[j:j + size])); j += size
                obj[f.name] = vals
                continue
            if f.repeated:
                obj.setdefault(f.name, []).append(val)
            else:
                obj[f.name] = val
        elif wt == 0:
            n, i = _read_varint(buf, i)
            obj[f.name] = _conv(f, n, rev_enum)
        elif wt in (1, 5):
            size = 8 if wt == 1 else 4
            obj[f.name] = _fixed(f.type_name, buf[i:i + size]); i += size
        else:
            raise ValueError(f"wire type {wt}")
    return obj


def _conv(f, n, rev_enum):
    if f.kind == "enum":
        return rev_enum[f.type_name].get(n, n)
    if f.type_name in ("sint32", "sint64"):
        return _unzigzag(n)
    if f.type_name == "bool":
        return bool(n)
    return _signed(f.type_name, n)


def _fixed(type_name, b):
    fmt = {"double": "<d", "float": "<f", "fixed32": "<I", "sfixed32": "<i",
           "fixed64": "<Q", "sfixed64": "<q"}[type_name]
    return struct.unpack(fmt, b)[0]


# ----------------------------------------------- dict <-> google message ---

def to_pb(schema, classes, msg, obj):
    m = classes[msg]()
    _fill(schema, m, msg, obj)
    return m


def _fill(schema, m, msg, obj):
    fields = {f.name: f for f in schema.fields(msg)}
    for name, v in obj.items():
        f = fields[name]
        if f.kind == "message":
            if f.repeated:
                for item in v:
                    _fill(schema, getattr(m, name).add(), f.type_name, item)
            else:
                getattr(m, name).SetInParent()
                _fill(schema, getattr(m, name), f.type_name, v)
        elif f.kind == "enum":
            if f.repeated:
                getattr(m, name).extend(_enum_num(schema, f, x) for x in v)
            else:
                setattr(m, name, _enum_num(schema, f, v))
        elif f.repeated:
            getattr(m, name).extend(v)
        else:
            setattr(m, name, v)
