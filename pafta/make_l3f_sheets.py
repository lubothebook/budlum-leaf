#!/usr/bin/env python3
# BUDLUM LEAF · pafta/make_l3f_sheets.py · revision L.5.0 · 2026-10-12
# Emits P18-EKRAN-PARCA-PARCA.svg:
#   The 4-Quadrant (+) Seamless Snap-Together Polycarbonate Screen-Battery Body (80 x 160 x 2.00 mm, 68 g,
#   52 internal parts): <15 um n=1.585 self-healing optical seam lip, Corning edge-wrapped zero-bezel
#   conductors, flicker-free DC-dimming T-OLED, PDLC, orthotropic graphene/Mu-metal shield, LLZO solid-state cell.
# Gate: pafta/check_sheets.py -> OVER 0, COVERED 0, COLLIDE 0.

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_l3_sheets import head, lines

HERE = os.path.dirname(os.path.abspath(__file__))


def sheet_p18():
    w, h = 1400, 1000
    o = [
        head(
            w,
            h,
            "BUDLUM LEAF · 4-PARÇALI (+) ÇİZİKSİZ EKRAN-BATARYA KAROLARI (52 İÇ PARÇA)",
            "Ortadan + bolunmus 4 parcali ciziksiz polikarbonat ekran-batarya govdesi: n=1.585 optik dudak, T-OLED, PDLC ve LLZO kati-hal pil",
        )
    ]
    o.append('<text class="t h1" x="40" y="52">4-PARÇALI (+) ÇİZİKSİZ EKRAN-BATARYA · n=1.585 OPTİK DUDAK VE 52 İÇ PARÇA</text>')
    body, _ = lines(
        "80.0 x 160.0 x 2.00 mm (68.0 g) ekran gövdesi ortadan artı (+) şeklinde 4 eşit tak-çıkar polikarbonat karoya (Q1-Q4; "
        "40x80x2.00 mm) bölünür. İç + kenarlarındaki 12 µm n=1.585 kendi kendini onaran optik dudak ve Corning kenar-sarımlı "
        "elektrotlar sayesinde 4 parça birleştiğinde hiçbir çizik veya sınır görünmez; her karoda 3.0 Wh katı-hal pil bulunur.",
        40,
        78,
        150,
    )
    o += body
    o.append('<line class="rule" x1="40" y1="136" x2="1360" y2="136"/>')

    # ---------- A: The 2.00 mm Quadrant Stack
    o.append('<rect class="glass" x="40" y="152" width="700" height="340" rx="6"/>')
    o.append('<text class="t h2" x="60" y="180">A · 2.20 MM KARO İSTİFİ · PC, OCA, T-OLED, PDLC, KALKAN VE KATI-HAL PİL</text>')
    stack = [
        ("ön ISO 10993 tıbbi polikarbonat + SiO2 kaplama · 200 µm", 2.4, "#e6d6f2"),
        ("ön silikon elastomer OCA kayma katmanı · 50 µm", 1.1, "#f7dcae"),
        ("ön titreşimsiz DC-dimming T-OLED + kenar sarım · 140 µm", 2.0, "#eef4ff"),
        ("ön AgNW/ITO + PDLC + grafen/Mu-metal kalkan · 130 µm", 1.4, "#dcecff"),
        ("MERKEZ YANMAZ LLZO KATI-HAL PİL (3 Wh) + Qİ2 BOBİN · 1160 µm", 3.6, "#b8ebd8"),
        ("arka AgNW/ITO + PDLC + grafen/Mu-metal kalkan · 130 µm", 1.4, "#dcecff"),
        ("arka titreşimsiz DC-dimming T-OLED + GIP sürücü · 140 µm", 2.0, "#eef4ff"),
        ("arka silikon OCA kayma katmanı + esnek omurga · 50 µm", 1.1, "#f7dcae"),
        ("arka ISO 10993 tıbbi polikarbonat + R 0.55 kenar · 200 µm", 2.4, "#e6d6f2"),
    ]
    y0 = 200.0
    for i, (t, th, col) in enumerate(stack):
        yy = y0 + i * 28
        wid = 90.0 + th * 25.0
        o.append(
            '<rect x="70" y="%.1f" width="%.1f" height="15.0" rx="2" fill="%s" stroke="#5b6169" stroke-width="1.2"/>'
            % (yy, wid, col)
        )
        o.append('<text class="lbls" x="280" y="%.1f">%s</text>' % (yy + 12, t))
    o.append('<text class="lbls" x="70" y="462">12 µm n=1.585 optik dudak polikarbonat (n=1.586) ile kırılma indisi eşleşmelidir (&lt;%0.0001 yansıma).</text>')
    o.append('<text class="lbls" x="70" y="480">Toplam kalınlık 2.00 mm, kütle 4 x 17.0 g = 68.0 g; B modülü arkasında Ø22.4 mm AMOLED vardır.</text>')

    # ---------- B: The panel numbers
    o.append('<rect class="glass" x="760" y="152" width="600" height="340" rx="6"/>')
    o.append('<text class="t h2" x="780" y="180">B · 4-KARO (+) ÇİZİKSİZ EKRAN SAYILARI</text>')
    rows = [
        ("tam ekran ölçüsü", "80.0 x 160.0 x 2.00 mm (4 x 40x80 mm karo)"),
        ("orta (+) optik derz", "&lt;15 µm n=1.585 elastomer · sıfır çizik / sıfır iz"),
        ("iç çerçeve (bezel)", "0.00 mm (Corning kenar-sarımlı elektrotlar)"),
        ("çözünürlük", "3 128 x 1 528 px · 508 ppi · 120 Hz DC-dimming"),
        ("göz ışık güvenliği", "IEC 62471 Grup 0 · &lt;415 nm mavi ışık kesimli"),
        ("dokunma ve kalem", "240 Hz AgNW/ITO · + derzinde kesintisiz izleme"),
        ("katı-hal batarya", "4 x 3.0 Wh = 12.0 Wh (3 200 mAh) yanmaz LLZO"),
        ("kablosuz şarj", "Ø54 mm Qi2.2 MPP (15-25W) + 4x Ø22 mm Qi"),
        ("gövdede Type-C", "yoktur (cihazdaki TEK Type-C 90° B çubuğunda)"),
        ("B modülü yerleşimi", "yuvarlak halka ekran üstünde, 90° çubuk dik"),
    ]
    for i, (a, b) in enumerate(rows):
        yy = 208 + i * 21
        o.append('<text class="lbls" x="780" y="%d">%s</text>' % (yy, a))
        o.append('<text class="lbls" x="935" y="%d">%s</text>' % (yy, b))
    o.append('<text class="lbls" x="780" y="456">B modülündeki 4-Karo Ana TCON + derz sınırındaki pikselleri</text>')
    o.append('<text class="lbls" x="780" y="474">gerçek zamanlı LUT ile kalibre ederek parlaklık farkını sıfırlar.</text>')

    # ---------- C: Internal Architecture of the 4 Quadrants (+ Seam, Ti Hub, Qi2 Ring)
    o.append('<rect class="glass" x="40" y="508" width="700" height="292" rx="6"/>')
    o.append('<text class="t h2" x="60" y="536">C · İÇ YAPI: (+) OPTİK DERZ, Ti ARTl GÖBEK VE Qİ2 HALKASI</text>')
    s = 2.0
    ox, oy = 74.0, 588.0
    o.append(
        '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="#dcecff" stroke="#18507e" stroke-width="2.0"/>'
        % (ox, oy, 160 * s, 80 * s, 3.2 * s)
    )
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#1b8a6b" stroke-width="2.0"/>'
             % (ox + 80 * s, oy, ox + 80 * s, oy + 80 * s))
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#1b8a6b" stroke-width="2.0"/>'
             % (ox, oy + 40 * s, ox + 160 * s, oy + 40 * s))
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#d89818" stroke-width="2.2" stroke-dasharray="6 3"/>'
             % (ox + 80 * s, oy + 40 * s, 24 * s))
    o.append('<rect fill="#d8dbe0" stroke="#181816" stroke-width="1.3" x="%.1f" y="%.1f" width="16" height="16" rx="3"/>'
             % (ox + 80 * s - 8, oy + 40 * s - 8))
    c_lines = [
        "Ortadan + şeklinde 4 eşit tak-çıkar karo (Q1..Q4).",
        "12 µm n=1.585 kendi kendini onaran optik dudak.",
        "Merkez (0,0) Grade-5 Titanyum Artı (+) kilit göbeği.",
        "8 konik Ti kırlangıç pim (&lt;2.5 µm Z-eşdüzlemliliği).",
        "24 N52H mıknatıs + 64 altın mikro-yaprak kontak.",
        "Merkezde Ø54 mm Qi2.2 + her karoda Ø22 mm Qi bobin.",
    ]
    for i, t in enumerate(c_lines):
        o.append('<text class="lbls" x="410" y="%d">%s</text>' % (594 + i * 22, t))
    o.append('<text class="lbls" x="410" y="742">Gövde: 2.00 mm · 68.0 g · 12.0 Wh katı-hal pil.</text>')

    # ---------- D: Flexion states
    o.append('<rect class="glass" x="760" y="508" width="600" height="292" rx="6"/>')
    o.append('<text class="t h2" x="780" y="536">D · POLİKARBONAT + KATI-HAL PİL ESNEMESİ · ÜÇ DURUM</text>')
    o.append('<text class="lbls" x="790" y="566">1 · düz tam ekran · 160.0 x 80.0 x 2.00 mm · sıfır çizik (+)</text>')
    o.append('<line x1="790" y1="582" x2="1320" y2="582" stroke="#18507e" stroke-width="6" stroke-linecap="round"/>')
    o.append('<text class="lbls" x="790" y="622">2 · gözlük vizör kavisi · R 60 mm · göz sıcaklığı &lt;=36.2 °C</text>')
    o.append('<path d="M 790 656 Q 1055 616 1320 656" fill="none" stroke="#18507e" stroke-width="6" stroke-linecap="round"/>')
    o.append('<text class="lbls" x="790" y="696">3 · tam esneme sınırı · R 25.5 mm · OCA ile gerinim yalnız %0.38</text>')
    o.append('<path d="M 830 756 Q 1055 676 1280 756" fill="none" stroke="#18507e" stroke-width="6" stroke-linecap="round"/>')
    o.append('<text class="lbls" x="790" y="784">Esnek LLZO/PEO katı-hal pil ve OCA sayesinde 200 000 bükülmede kırılmaz.</text>')

    # ---------- E: The 13 internal parts per quadrant (x4 = 52 parts)
    o.append('<rect class="glass" x="40" y="816" width="700" height="160" rx="6"/>')
    o.append('<text class="t h2" x="60" y="844">E · HER ÇEYREK KARONUN 13 İÇ PARÇASI (×4 = 52 PARÇA)</text>')
    parts = [
        "1-2 ön/arka 0.20 mm ISO 10993 tıbbi polikarbonat + SiO2",
        "3-4 12 µm n=1.585 (+) optik dudak + 8 dişli esnek omurga",
        "5-6 ön/arka 0.05 mm silikon OCA kayma katmanı (%0.38)",
        "7-8 ön/arka 0.14 mm DC-dimming T-OLED + kenar sarım",
        "9 0.09 mm PDLC + ortotropik grafen ve Mu-metal kalkan",
    ]
    for i, t in enumerate(parts):
        o.append('<text class="lbls" x="60" y="%d">%s</text>' % (872 + i * 18, t))
    parts2 = [
        "10 35x75x1.08 mm yanmaz LLZO/PEO katı-hal pil (3.0 Wh)",
        "11 çift-telli (bifilar) akım-iptalli kulaklar + NTC (&lt;=36.2 C)",
        "12 90° Qi2.2 MPP sektör + Ø22 mm Qi bobin + U_QI PMIC",
        "13 Ti Artı (+) göbek + 2 kırlangıç + 6 N52H + 16 altın yaprak",
        "Toplam: 4 karo × 13 parça = 52 iç parça (68.0 g, 12.0 Wh)",
    ]
    for i, t in enumerate(parts2):
        o.append('<text class="lbls" x="394" y="%d">%s</text>' % (872 + i * 18, t))

    # ---------- F: Gates and thermal
    o.append('<rect class="glass" x="760" y="816" width="600" height="160" rx="6"/>')
    o.append('<text class="t h2" x="780" y="844">F · KAPILAR VE ÇİZİKSİZ (+) EKRAN DOĞRULAMASI</text>')
    g = [
        "F-01: 4 x (40x80x2.00 mm) = 80x160x2.00 mm (68 g) + ekran",
        "F-02: 12 µm n=1.585 optik dudak ile &lt;%0.0001 yansıma (0 çizik)",
        "F-03: Corning kenar-sarımlı 0.00 mm iç çerçevesiz T-OLED",
        "F-04: yanmaz LLZO katı-hal pil (12.0 Wh, 0 ppm HF, ISO 10993)",
        "F-05: gözlük güvenliği (&lt;=36.2 C, ELF &lt;0.08 µT, SAR 0.054 W/kg)",
        "F-06: portsuz gövdede Qi2.2 şarj, tek Type-C 90° B çubuğunda",
        "F-07: AB 2023/1542 Md. 11 uyumlu &lt;3 sn aletsiz karo değişimi",
    ]
    for i, t in enumerate(g):
        o.append('<text class="lbls" x="780" y="%d">%s</text>' % (866 + i * 17, t))
    return "\n".join(o) + "\n</svg>\n"


def main():
    for name, fn in (("P18-EKRAN-PARCA-PARCA.svg", sheet_p18),):
        svg = fn()
        with open(os.path.join(HERE, name), "w") as fh:
            fh.write(svg)
        print("wrote", name.split("-")[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
