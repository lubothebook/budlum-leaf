#!/usr/bin/env python3
# BUDLUM LEAF · pafta/make_l3e_sheets.py · revision L.5.0 · 2026-10-12
# Emits P17-ENERJI-LEVHASI-PARCA-PARCA.svg:
#   All 52 internal parts across the 4-Quadrant (+) Snap-Together Polycarbonate Screen-Battery Tiles
#   (4 x 40.0 x 80.0 x 2.00 mm = 68.0 g, 4 x 3.0 Wh = 12.0 Wh LLZO/PEO all-solid-state battery,
#   ISO 10993 medical polycarbonate, orthotropic graphene/Mu-metal ocular shield, universal Qi2.2/Qi coils).
# Gate: pafta/check_sheets.py -> OVER 0, COVERED 0, COLLIDE 0.

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_l3_sheets import head, lines

HERE = os.path.dirname(os.path.abspath(__file__))


def sheet_p17():
    w, h = 1400, 1000
    o = [
        head(
            w,
            h,
            "BUDLUM LEAF · 4-PARÇALI (+) POLİKARBONAT KATI-HAL PİL VE Qİ2 KAROLARI (52 İÇ PARÇA)",
            "4 ceyrek polikarbonat ekran-batarya karosu (52 ic parca): yanmaz LLZO kati-hal pil, gozluk saglik kalkani ve Qi2 kablosuz sarj",
        )
    ]
    o.append('<text class="t h1" x="40" y="52">4-PARÇALI (+) POLİKARBONAT KATI-HAL PİL VE Qİ2 KAROLARI · 52 İÇ PARÇA</text>')
    body, _ = lines(
        "Kaba alt batarya modülü kaldırılmıştır: telefon ortasından artı (+) şeklinde 4 eşit tak-çıkar polikarbonat ekran-batarya "
        "karosuna (Q1-Q4; 40x80x2.00 mm, 4x 17 g = 68 g) bölünmüştür. Her karoda gözlük/el/cep sağlığına uygun yanmaz LLZO/PEO "
        "katı-hal pil (3.0 Wh x 4 = 12.0 Wh), Mu-metal/grafen göz kalkanı ve evrensel Qi2.2/Qi kablosuz şarj bobini yer alır.",
        40,
        78,
        150,
    )
    o += body
    o.append('<line class="rule" x1="40" y1="136" x2="1360" y2="136"/>')

    # ---------- A: Internal Blueprint of the 4-Quadrant (+) Polycarbonate Screen-Battery Body
    o.append('<rect class="glass" x="40" y="152" width="820" height="340" rx="6"/>')
    o.append('<text class="t h2" x="60" y="180">A · 4-KARO (+) İÇ KESİTİ · LLZO KATI-HAL PİL, GÖZ KALKANI VE Qİ2 BOBİNLERİ</text>')
    ox, oy, kw, kh = 84.0, 200.0, 4.4, 2.7
    o.append('<rect fill="#dcecff" stroke="#18507e" stroke-width="2.0" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="14"/>'
             % (ox, oy, 160.0 * kw, 80.0 * kh))
    for (qx, qy, lbl) in ((4.0, 4.0, "Q1 · 3.0 Wh LLZO"), (82.0, 4.0, "Q3 · 3.0 Wh LLZO"),
                          (4.0, 42.0, "Q2 · 3.0 Wh LLZO"), (82.0, 42.0, "Q4 · 3.0 Wh LLZO")):
        o.append('<rect fill="#b8ebd8" stroke="#1b8a6b" stroke-width="1.3" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="6"/>'
                 % (ox + qx * kw, oy + qy * kh, 74.0 * kw, 34.0 * kh))
        o.append('<circle cx="%.1f" cy="%.1f" r="24" fill="none" stroke="#c88a18" stroke-width="1.4" stroke-dasharray="4 2"/>'
                 % (ox + (qx + 37.0) * kw, oy + (qy + 17.0) * kh))
        o.append('<text class="lbls" x="%.1f" y="%.1f">%s</text>' % (ox + (qx + 7.0) * kw, oy + (qy + 18.0) * kh, lbl))
    cx_p, cy_p = ox + 80.0 * kw, oy + 40.0 * kh
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#1b8a6b" stroke-width="2.2"/>' % (cx_p, oy, cx_p, oy + 80.0 * kh))
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#1b8a6b" stroke-width="2.2"/>' % (ox, cy_p, ox + 160.0 * kw, cy_p))
    o.append('<circle cx="%.1f" cy="%.1f" r="54" fill="none" stroke="#d89818" stroke-width="2.6" stroke-dasharray="10 4"/>' % (cx_p, cy_p))
    o.append('<rect fill="#d8dbe0" stroke="#181816" stroke-width="1.4" x="%.1f" y="%.1f" width="20" height="20" rx="3"/>' % (cx_p - 10, cy_p - 10))

    o.append('<text class="lbls" x="60" y="446">• Gözlük ve İnsan Sağlığı: Yanmaz LLZO/PEO katı-hal pil (%0 sıvı, 0 ppm HF gazı), &lt;=36.2 C göz sıcaklığı ve SAR 0.054 W/kg.</text>')
    o.append('<text class="lbls" x="60" y="464">• Çiziksiz (+) Ekran: 12 µm n=1.585 optik elastomer dudak + Corning kenar-sarımlı elektrotlar ile sıfır görünür birleşim izi.</text>')
    o.append('<text class="lbls" x="60" y="482">• Portsuz Evrensel Şarj: Gövdede Type-C yoktur; Ø54 mm Qi2.2 MPP + 4x Ø22 mm Qi bobin ile her kablosuz pedde şarj olur.</text>')

    # ---------- B: Capacities and Biocompatibility Physics
    o.append('<rect class="glass" x="880" y="152" width="480" height="340" rx="6"/>')
    o.append('<text class="t h2" x="900" y="180">B · KARO HACMİ, ENERJİ VE SAĞLIK HESABI</text>')
    rows = [
        ("birim", "kalınlık", "yoğunluk", "enerji", "kapasite", "kütle"),
        ("Tek Karo (Q)", "2.00 mm", "750 Wh/L", "3.0 Wh", "800 mAh", "17 g"),
        ("4-Karo (+)", "2.00 mm", "750 Wh/L", "12.0 Wh", "3.20 Ah", "68 g"),
        ("+ B Modülü", "4.00 mm", "Sıfır-CPU", "12.0 Wh", "3.20 Ah", "88 g"),
        ("Leaf 240/480", "2.40 mm", "850 Wh/L", "48.0 Wh", "12.8 Ah", "240 g"),
    ]
    for i, r in enumerate(rows):
        cls = "lblb" if i == 0 else "lbls"
        yy = 208 + i * 20
        for j, cell in enumerate(r):
            o.append('<text class="%s" x="%d" y="%d">%s</text>' % (cls, 900 + j * 74, yy, cell))
    caps = (
        "Sıfır-CPU mimarisinde CPU ve RAM bulut/hub düğümündedir; 4 karo + B modülü toplam gücü yalnız 0.85 W'tır. "
        "Polikarbonat karoların içindeki 4 x 3.0 Wh = 12.0 Wh (3 200 mAh) yanmaz LLZO katı-hal pil >14.1 saat kesintisiz "
        "ekran süresi verir. AB 2023/1542 Md. 11 uyarınca her karo 3 saniyede aletsiz takılıp çıkarılabilir."
    )
    body, _ = lines(caps, 900, 326, 52)
    o += body
    o.append('<text class="lbls" x="900" y="472">ENR-11..21 kapıları biyouyumlu LLZO katı-hal pili ve Qi2 şarjı doğrular.</text>')

    # ---------- C: The 52 internal parts of the 4-Quadrant (+) Screen-Battery Body (13 per quadrant x 4)
    o.append('<rect class="glass" x="40" y="508" width="820" height="330" rx="6"/>')
    o.append('<text class="t h2" x="60" y="536">C · 4 ÇEYREK KARONUN 52 İÇ PARÇASI (HER KARODA 13 PARÇA × 4)</text>')
    parts = [
        "1 (x4) ön 0.20 mm ISO 10993 tıbbi polikarbonat + SiO2 kaplama",
        "2 (x4) arka 0.20 mm ISO 10993 tıbbi polikarbonat + R 0.55 kenar",
        "3 (x4) 12 µm n=1.585 fenil-florosilikon çiziksiz (+) optik dudak",
        "4 (x4) 8 oluklu dış polikarbonat esnek omurga (toplam 32 diş)",
        "5 (x4) ön/arka 0.05 mm silikon OCA kayma katmanı (%0.38 gerinim)",
        "6 (x4) ön/arka 0.14 mm DC-dimming T-OLED + kenar-sarımlı elektrot",
        "7 (x4) 0.09 mm PDLC gizlilik + ortotropik grafen/Mu-metal kalkan",
        "8 (x4) 35x75x1.08 mm yanmaz LLZO/PEO-Seramik katı-hal pil (3 Wh)",
        "9 (x4) çift-telli (bifilar) akım-iptalli folyo kulaklar + NTC (&lt;=36.2 C)",
        "10 (x4) 90° merkez Qi2.2 MPP bobin sektörü (birleşince Ø54 mm)",
        "11 (x4) Ø22.0 mm bağımsız çeyrek Qi alıcı bobini + nanokristal zırh",
        "12 (x4) U_QI yerel kablosuz şarj düzeltici + 3 ms Dead-Pad BMS çipi",
        "13 (x4) Ti Artı (+) göbek çeyreği + 2 kırlangıç pim + 6 N52H + 16 yaprak",
        "Toplam: 4 çeyrek karo × 13 iç alt-montaj = 52 modellenmiş iç parça",
    ]
    for i, t in enumerate(parts):
        cx = 60 if i < 7 else 452
        cy = 564 + (i if i < 7 else i - 7) * 36
        o.append('<text class="lbls" x="%d" y="%d">%s</text>' % (cx, cy, t))

    # ---------- D: Biocompatibility, Ocular Safety & Qi2 Numbers
    o.append('<rect class="glass" x="880" y="508" width="480" height="180" rx="6"/>')
    o.append('<text class="t h2" x="900" y="536">D · GÖZLÜK SAĞLIĞI VE Qİ2 ŞARJ SAYILARI</text>')
    bend = [
        "katı-hal pil kimyası      LLZO oksit-seramik + PEO (%0 sıvı)",
        "zehirli gaz / yanma       0.0 ppm HF gazı · UL94 V-0 yanmaz",
        "göz yüzeyi sıcaklığı      &lt;=36.2 °C (donanım NTC + grafen kalkan)",
        "manyetik alan (ELF)       &lt;0.08 µT (bifilar akım iptali + Mu-metal)",
        "özgül soğurma (SAR)       0.054 W/kg (90° B çubukta uzak anten)",
        "biyouyumluluk             ISO 10993-5/-10 tıbbi polikarbonat",
        "kablosuz şarj             Qi2.2 MPP Ø54 mm (15-25W) + 4x Ø22 mm Qi",
        "gövde port / buton        0 adet (Type-C yalnız 90° B çubuğunda)",
        "AB 2023/1542 Md. 11       &lt;3 saniyede aletsiz tak-çıkar karo değişimi",
    ]
    for i, t in enumerate(bend):
        o.append('<text class="lbls" x="900" y="%d">%s</text>' % (562 + i * 14, t))

    # ---------- E: Six tool-free Quadrant Hot-Swap steps
    o.append('<rect class="glass" x="880" y="704" width="480" height="134" rx="6"/>')
    o.append('<text class="t h2" x="900" y="730">E · 3 SN KESİNTİSİZ KARO HOT-SWAP · ALTI ADIM</text>')
    steps = [
        "1 değiştirilecek çeyrek karoyu + hattından çek",
        "2 Dead-Pad IC o karonun 16 altın yaprağını 0.1 ms keser",
        "3 kalan 3 karo (9.0 Wh) sistemi kesintisiz besler",
        "4 ekran ve UWB/mmWave oturumu hiç kapanmaz",
        "5 dolu karo Ti kırlangıç pim ve N52H ile + hatta oturur",
        "6 n=1.585 dudak çiziksiz kapanır, 3 ms sonra güç birleşir",
    ]
    for i, t in enumerate(steps):
        o.append('<text class="lbls" x="900" y="%d">%s</text>' % (752 + i * 14, t))

    # ---------- F: Gates
    o.append('<rect class="glass" x="40" y="854" width="1320" height="122" rx="6"/>')
    o.append('<text class="t h2" x="60" y="882">F · KAPILAR ENR-11 … ENR-21 VE F-01 … F-10 (REV L.5.0)</text>')
    g1 = "ENR-11 4x 3.0 Wh = 12.0 Wh yanmaz LLZO katı-hal pil · ENR-12 ISO 10993 tıbbi PC · ENR-13 &lt;=36.2 C göz kalkanı · ENR-14 0 ppm HF"
    g2 = "ENR-15 AB 2023/1542 &lt;3 sn Hot-Swap · ENR-16 3 ms Dead-Pad · ENR-17 Evrensel Qi/Qi2.2 şarj · ENR-18..21 SAR 0.054 W/kg + IP68"
    o.append('<text class="lbls" x="60" y="910">%s</text>' % g1)
    o.append('<text class="lbls" x="60" y="930">%s</text>' % g2)
    o.append('<text class="lbls" x="60" y="954">4 çeyrek ekran-batarya karosunun tüm 52 iç parçası ve 90° B modülünün 32 iç parçası (toplam 84 parça) 3B CAD modelindedir.</text>')
    return "\n".join(o) + "\n</svg>\n"


def main():
    for name, fn in (("P17-ENERJI-LEVHASI-PARCA-PARCA.svg", sheet_p17),):
        svg = fn()
        with open(os.path.join(HERE, name), "w") as fh:
            fh.write(svg)
        print("wrote", name.split("-")[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
