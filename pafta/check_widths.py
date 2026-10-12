#!/usr/bin/env python3
"""Pafta QA: flag any text line whose rendered width leaves its panel or the sheet.

Font metrics: DejaVu Sans (the rasterizer font). DejaVu is wider than Helvetica,
so a pass here is a pass in every viewer that has Helvetica or Arial.
"""
import sys, glob, xml.etree.ElementTree as ET
from PIL import ImageFont

NS = "{http://www.w3.org/2000/svg}"
SHEET_W = 1600
SHEET_LIMIT = SHEET_W - 40          # 40 px outer margin
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

def width(text, size, bold):
    return font(size, bold).getlength(text) / 4.0

def main(paths):
    bad = 0
    for path in paths:
        root = ET.parse(path).getroot()
        panels = []
        for el in root.iter():
            if el.get("class") in ("panel", "tb") and el.tag.endswith("rect"):
                x, y = float(el.get("x", 0)), float(el.get("y", 0))
                panels.append((x, y, x + float(el.get("width", 0)), y + float(el.get("height", 0))))
        for el in root.iter(NS + "text"):
            if el.get("transform"):
                continue
            cls = (el.get("class") or "lbls").split()[0]
            raw = "".join(el.itertext())
            if not raw.strip():
                continue
            size, bold = SIZE.get(cls, 10), cls in BOLD
            w = width(raw, size, bold)
            x, y = float(el.get("x", 0)), float(el.get("y", 0))
            right = x + w
            # innermost panel that contains the start point
            limit = SHEET_LIMIT
            for px, py, pr, pb in panels:
                if px - 1 <= x <= pr + 1 and py - 1 <= y <= pb + 1:
                    limit = min(limit, pr - 8)
            if right > limit + 0.5:
                bad += 1
                print(f"{path.split('/')[-1]:34s} y={y:5.0f} x={x:5.0f} right={right:6.0f} limit={limit:5.0f} "
                      f"over={right-limit:5.1f}  {cls}: {raw[:64]}")
    print(f"\n{bad} line(s) over the limit")
    return 0 if bad == 0 else 1

if __name__ == "__main__":
    files = sys.argv[1:] or sorted(glob.glob("/home/user/LEAF/pafta/*.svg"))
    sys.exit(main(files))
