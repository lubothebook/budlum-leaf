#!/usr/bin/env python3
"""Pafta QA v2 - three checks per sheet:
  OVER    text wider than the innermost rect that contains its start point (or the sheet margin)
  COVERED text whose start point falls inside a rect drawn LATER in the document (the rect hides it)
  COLLIDE two text lines whose boxes overlap
Metrics use DejaVu Sans, which is wider than Helvetica, so a pass here is a pass in any viewer.
"""
import sys, glob, xml.etree.ElementTree as ET
from PIL import ImageFont

NS = "{http://www.w3.org/2000/svg}"
SHEET_LIMIT = 1560
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SIZE = {"h1": 21, "h2": 13.5, "h3": 11.5, "lbl": 11, "lblb": 11,
        "lbls": 10, "dimt": 10, "note": 10, "mono": 10}
BOLD = {"h1", "h2", "h3", "lblb"}
cache = {}

def font(size, bold):
    key = (round(size * 4), bold)
    if key not in cache:
        cache[key] = ImageFont.truetype(FONT_B if bold else FONT, int(round(size * 4)))
    return cache[key]

def run(paths):
    n_over = n_covered = n_coll = 0
    for path in paths:
        root = ET.parse(path).getroot()
        name = path.split("/")[-1]
        rects = []            # (order, x, y, right, bottom, cls)
        for i, el in enumerate(root.iter()):
            tag = el.tag.split("}")[-1]
            if tag == "rect":
                w, h = float(el.get("width", 0)), float(el.get("height", 0))
                if w >= 1590 and h >= 1120:
                    continue    # background
                rects.append((i, float(el.get("x", 0)), float(el.get("y", 0)),
                              float(el.get("x", 0)) + w, float(el.get("y", 0)) + h, el.get("class") or "box"))
        parent = {c: p for p in root.iter() for c in p}
        texts = []
        for i, el in enumerate(root.iter()):
            if el.tag != NS + "text" or el.get("transform"):
                continue
            raw = "".join(el.itertext())
            if not raw.strip():
                continue
            node, toks = el, []
            while node is not None and not toks:
                toks = (node.get("class") or "").split()
                node = parent.get(node)
            if not toks:
                toks = ["__default__"]          # no styling ancestor: browser default, 16 px
            sizes = [SIZE[t] for t in toks if t in SIZE]
            size = max(sizes) if sizes else 16
            bold = any(t in BOLD for t in toks)
            w = font(size, bold).getlength(raw) / 4.0
            x, y = float(el.get("x", 0)), float(el.get("y", 0))
            texts.append((i, x, y, x + w, y - size * 0.78, y + size * 0.26, '+'.join(toks), raw))
        # OVER
        for i, x, y, right, t, b, cls, raw in texts:
            limit = SHEET_LIMIT
            for j, rx, ry, rr, rb, rc in rects:
                if j < i and rx - 1 <= x <= rr + 1 and ry - 1 <= y <= rb + 1:
                    limit = min(limit, rr - 6)
            if right > limit + 0.5:
                n_over += 1
                print(f"OVER    {name:32s} y={y:5.0f} x={x:5.0f} right={right:6.0f} limit={limit:5.0f} "
                      f"+{right-limit:5.1f} {cls:5s} {raw[:60]}")
        # COVERED
        for i, x, y, right, t, b, cls, raw in texts:
            for j, rx, ry, rr, rb, rc in rects:
                if j > i and rx - 2 <= x <= rr - 2 and ry - 2 <= y <= rb - 2:
                    n_covered += 1
                    print(f"COVERED {name:32s} y={y:5.0f} x={x:5.0f} by {rc} at ({rx:.0f},{ry:.0f})-({rr:.0f},{rb:.0f})  {raw[:48]}")
                    break
        # COLLIDE
        for a in range(len(texts)):
            for b2 in range(a + 1, len(texts)):
                _, x1, y1, r1, t1, bo1, c1, s1 = texts[a]
                _, x2, y2, r2, t2, bo2, c2, s2 = texts[b2]
                if x1 < r2 - 1 and x2 < r1 - 1 and t1 < bo2 - 1 and t2 < bo1 - 1:
                    n_coll += 1
                    print(f"COLLIDE {name:32s} ({x1:.0f},{y1:.0f})'{s1[:26]}' x ({x2:.0f},{y2:.0f})'{s2[:26]}'")
    print(f"\nOVER={n_over}  COVERED={n_covered}  COLLIDE={n_coll}")
    return 0

if __name__ == "__main__":
    run(sys.argv[1:] or sorted(glob.glob("/home/user/LEAF/pafta/*.svg")))
