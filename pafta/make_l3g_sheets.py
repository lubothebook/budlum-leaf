#!/usr/bin/env python3
# BUDLUM LEAF · pafta/make_l3g_sheets.py · revision L.5.0 · 2026-10-12
# Emits P19-GOVDE-VE-SANDVIC-PARCA-PARCA.svg:
#   Complete Revision L.5.0 system architecture (84 total internal parts, 88.0 g total mass):
#   1. 4-Quadrant (+) Snap-Together Polycarbonate Screen-Battery Body (68.0 g = 4 x 17.0 g, 12.0 Wh, 52 parts)
#   2. 90°-Bent-Stem `b` Camera, Zero-CPU & Single USB-C Module (20.0 g, 32 parts)
# Gate: pafta/check_sheets.py -> OVER 0, COVERED 0, COLLIDE 0.

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_l3_sheets import head, lines

HERE = os.path.dirname(os.path.abspath(__file__))


def sheet_p19():
    w, h = 1400, 1000
    o = [
        head(
            w,
            h,
            "BUDLUM LEAF · 4-KARO (+) EKRAN-BATARYA (72 G) VE 90° BÜKÜMLÜ B MODÜLÜ (22 G) · 84 İÇ PARÇA",
            "Budlum Leaf Rev L.5.0 84 ic parca: 4-parcali (+) polikarbonat ekran-batarya (68 g, 52 parca) ve 90 derece B modulu (20 g, 32 parca)",
        )
    ]
    o.append('<text class="t h1" x="40" y="52">4-KARO (+) EKRAN-BATARYA (72 G) VE 90° B MODÜLÜ (22 G) · 84 İÇ PARÇA</text>')
    body, _ = lines(
        "Revizyon L.5.0 ile kaba alt batarya çıkıntısı kaldırılmış, pil 4 çeyrek polikarbonat ekran karosunun (4x 40x80x2.00 mm = "
        "68.0 g, 12.0 Wh yanmaz LLZO katı-hal pil, 52 iç parça) içine alınmıştır. B modülünün ise sadece anten+Type-C çubuğu 90° "
        "dik açıyla bükülür; yuvarlak kamera/AMOLED halka ekranın üstüne oturur (20.0 g, 32 iç parça; toplam 84 iç parça, 88.0 g).",
        40,
        78,
        150,
    )
    o += body
    o.append('<line class="rule" x1="40" y1="136" x2="1360" y2="136"/>')

    # ---------- A: The 2.00 mm 4-Quadrant Body + 90°-Bent-Stem B Module Layers
    o.append('<rect class="glass" x="40" y="152" width="700" height="400" rx="6"/>')
    o.append('<text class="t h2" x="60" y="180">A · 2.20 MM 4-KARO (+) GÖVDE VE 90° BÜKÜMLÜ B MODÜLÜ KATMANLARI</text>')
    layers = [
        ("karo: ön ISO 10993 tıbbi polikarbonat + SiO2 kaplama · 200 µm", 1.1, "#e6d6f2"),
        ("karo: ön silikon OCA kayma katmanı (%0.38 gerinim) · 50 µm", 0.8, "#f7dcae"),
        ("karo: ön DC-dimming T-OLED + Corning kenar sarım · 140 µm", 2.0, "#eef4ff"),
        ("karo: ön AgNW/ITO + PDLC + grafen/Mu-metal kalkan · 130 µm", 1.2, "#dcecff"),
        ("karo: MERKEZ YANMAZ LLZO KATI-HAL PİL (4x 3 Wh = 12 Wh)", 5.8, "#b8ebd8"),
        ("karo: Ø54 mm 4-sektör Qi2.2 MPP + 4x Ø22 mm Qi bobin + PMIC", 2.2, "#ffe9a8"),
        ("karo: arka PDLC + grafen/Mu-metal + AgNW + T-OLED + PC", 2.0, "#eef4ff"),
        ("(+) hat: 12 µm n=1.585 çiziksiz optik dudak + Ti Artı (+) göbek", 1.8, "#e6d6f2"),
        ("(+) hat: 8 Ti kırlangıç pim + 24 N52H mıknatıs + 64 altın yaprak", 2.0, "#c9ccd1"),
        ("B çubuk: 90° dik bükümlü çubuk + ±90° tersinir Ti boyun menteşesi", 2.6, "#d8dbe0"),
        ("B çubuk: CİHAZDAKİ TEK USB TYPE-C (40W PD 3.1, IP68) + U_PD", 2.4, "#ffe9a8"),
        ("B çubuk: 3-bant LCP anten (Wi-Fi 7/BT/UWB) + 1x4 60 GHz dizi", 2.0, "#f7dcae"),
        ("B halka: 6L Sıfır-CPU PCB (4-Karo Ana TCON + UWB/mmWave SiP)", 2.6, "#d8f0dc"),
        ("B halka: 50 MP OIS kamera + Cu-Grafit kalkan + Ø22.4 mm AMOLED", 1.8, "#8f948f"),
    ]
    yy = 200.0
    for i, (t, th, col) in enumerate(layers):
        o.append(
            '<rect x="70" y="%.1f" width="%.1f" height="15.0" rx="2" fill="%s" stroke="#5b6169" stroke-width="1.2"/>'
            % (yy, 110 + th * 20, col)
        )
        o.append('<text class="lbls" x="370" y="%.1f">%s</text>' % (yy + 12, t))
        yy += th * 2.5 + 15.2
    o.append('<text class="lbls" x="70" y="510">4 çeyrek ekran-batarya karosu birleştiğinde 80x160x2.00 mm (68 g) çiziksiz tek ekran oluşturur.</text>')
    o.append('<text class="lbls" x="70" y="528">Gövdede Type-C veya buton yoktur; her Qi / Qi2.2 şarj pedinde 15-25 W kablosuz şarj olur.</text>')
    o.append('<text class="lbls" x="70" y="546">90° bükümlü B modülü ekranın üstüne oturur; 4 yöne ve ekranın önüne/arkasına takılabilir.</text>')

    # ---------- B: The 14 groups and masses of the L.5.0 Architecture
    o.append('<rect class="glass" x="760" y="152" width="600" height="400" rx="6"/>')
    o.append('<text class="t h2" x="780" y="180">B · TÜM SİSTEMİN 14 PARÇA GRUBU VE KÜTLELERİ</text>')
    groups = [
        ("1 4x ISO 10993 PC kabuk", "11.2 g"),
        ("2 4x çift T-OLED + OCA", "8.4 g"),
        ("3 4x PDLC + AgNW ağları", "4.0 g"),
        ("4 4x grafen/Mu-metal", "3.6 g"),
        ("5 4x 3 Wh LLZO katı pil", "32.0 g"),
        ("6 Qi2.2 + 4x Qi bobin", "6.4 g"),
        ("7 (+) Ti göbek + 64 yaprak", "6.4 g"),
        ("8 90° B çubuk + halka", "7.2 g"),
        ("9 ±90° Ti boyun menteşesi", "1.2 g"),
        ("10 TEK USB-C 40W + IP68", "1.4 g"),
        ("11 LCP anten + 60GHz dizi", "0.7 g"),
        ("12 6L PCB + TCON + UWB", "3.2 g"),
        ("13 50MP OIS + 5P + prizma", "4.9 g"),
        ("14 Ø22.4 AMOLED + N52H", "3.4 g"),
    ]
    for i, (a, b) in enumerate(groups):
        col = 780 if i < 7 else 1080
        row = i if i < 7 else i - 7
        yy2 = 210 + row * 24
        o.append('<text class="lbls" x="%d" y="%d">%s</text>' % (col, yy2, a))
        o.append('<text class="lbls" x="%d" y="%d">%s</text>' % (col + 165, yy2, b))
    o.append('<text class="lbls" x="780" y="400">4-Parçalı (+) Polikarbonat Ekran-Batarya Gövdesi (Grup 1..7): 68.0 g (4 x 17.0 g, 52 parça).</text>')
    o.append('<text class="lbls" x="780" y="420">90° Dik Bükümlü B Kamera, Sıfır-CPU ve Tek Type-C Modülü (Grup 8..14): 20.0 g (32 parça).</text>')
    o.append('<text class="lbls" x="780" y="440">Tam donanımlı toplam cihaz kütlesi: 68.0 g + 20.0 g = 88.0 g (toplam 84 iç parça).</text>')
    o.append('<text class="lbls" x="780" y="460">Toplam katı-hal pil enerjisi: 4 x 3.0 Wh = 12.0 Wh (3 200 mAh) · &gt;14.1 saat aktif ekran süresi.</text>')
    o.append('<text class="lbls" x="780" y="490">AB 2023/1542 Md. 11 uyarınca her çeyrek ekran-batarya karosu 3 sn içinde elle değiştirilir.</text>')

    # ---------- C: Attachment rules
    o.append('<rect class="glass" x="40" y="568" width="700" height="250" rx="6"/>')
    o.append('<text class="t h2" x="60" y="596">C · HER İÇ PARÇA VE MODÜL NASIL BAĞLANIR</text>')
    att = [
        ("çiziksiz (+) dudak", "12 µm n=1.585 fenil-florosilikon dudak ile 4 karo arasında sıfır görünür iz"),
        ("Ti Artı (+) göbek", "merkez (0,0) 4-yollu kilit + 8 konik Ti kırlangıç pim (&lt;2.5 µm adım)"),
        ("64 altın yaprak", "her iç kenarda 16 mikro-yaprak kontak + 6 çift-kutuplu N52H mıknatıs"),
        ("LLZO katı-hal pil", "her polikarbonat karonun içinde 35x75x1.08 mm yanmaz seramik-polimer hücre"),
        ("Qi2.2 + Qi bobinler", "merkezde 4 sektörlü Ø54 mm MPP halka + her karoda bağımsız Ø22 mm bobin"),
        ("90° bükümlü B çubuk", "±90° Ti menteşe ile sadece anten+Type-C çubuğu ekran kenarında dik kalır"),
        ("yuvarlak B halkası", "ekranın 4 yönüne ve ÖN/ARKA yüzüne simetrik N52H + 12 pedle oturur"),
    ]
    for i, (a, b) in enumerate(att):
        o.append('<text class="lbls" x="60" y="%d">%s</text>' % (622 + i * 25, a))
        o.append('<text class="lbls" x="195" y="%d">%s</text>' % (622 + i * 25, b))
    o.append('<text class="lbls" x="60" y="804">Hem 4 çeyrek ekran-batarya karosu hem de 90° B modülü aletsiz takılıp çıkarılır.</text>')

    # ---------- D: Biocompatibility, Ocular Safety & Zero-Scratch Seam
    o.append('<rect class="glass" x="760" y="568" width="600" height="250" rx="6"/>')
    o.append('<text class="t h2" x="780" y="596">D · ÇİZİKSİZ (+) OPTİK FİZİĞİ, GÖZLÜK SAĞLIĞI VE B KİLİDİ</text>')
    d_lines = [
        "1. Çiziksiz (+) Ekran: n=1.585 optik elastomer dudak polikarbonatla",
        "   indis eşleşmelidir (R &lt; %0.0001); Corning kenar sarımıyla çerçeve 0 mm'dir.",
        "2. Gözlük ve Cep Sağlığı: Yanmaz LLZO katı-hal pil sıfır sıvı ve sıfır HF",
        "   gazı içerir; göz yüzeyi &lt;=36.2 °C, ELF &lt;0.08 µT ve SAR 0.054 W/kg'dır.",
        "3. Portsuz Qi2 Gövde: Gövdede Type-C yoktur, her kablosuz pedde şarj",
        "   olur; kablolu Type-C (40W) ve aktif beyin sadece 90° B modülündedir.",
        "4. Öne/Arkaya B Takımı: Sadece çubuğu 90° bükülen B modülü ekranın",
        "   4 yönüne ve ön/arka yüzüne saniyeler içinde takılır (IP68).",
    ]
    for i, t in enumerate(d_lines):
        o.append('<text class="lbls" x="780" y="%d">%s</text>' % (624 + i * 22, t))

    # ---------- E: Thermal budget in Eyewear & Hand Modes
    o.append('<rect class="glass" x="40" y="836" width="700" height="140" rx="6"/>')
    o.append('<text class="t h2" x="60" y="864">E · GÖZLÜK, EL VE CEP KULLANIMINDA ISIL VE EM GÜVENLİK</text>')
    heat = [
        "gözlük vizör modu: donanım NTC + grafen kalkan ile göz yüzeyi &lt;=36.2 °C",
        "çift-telli (bifilar) folyo + Mu-metal kalkan: ELF manyetik alan &lt;0.08 µT",
        "90° B çubuğunda uzak anten: Baş/Göz SAR = 0.054 W/kg (sınırın 37x altı)",
        "15-25 W Qi2.2 kablosuz ve 40 W B-Type-C şarjda &lt;4.2 K sıcaklık artışı",
    ]
    for i, t in enumerate(heat):
        o.append('<text class="lbls" x="60" y="%d">%s</text>' % (888 + i * 18, t))

    # ---------- F: Gates
    o.append('<rect class="glass" x="760" y="836" width="600" height="140" rx="6"/>')
    o.append('<text class="t h2" x="780" y="864">F · KAPILAR MEC-33 … MEC-38 VE F-01 … F-10 (REV L.5.0)</text>')
    g = [
        "F-01..03: 4x (40x80x2.00 mm) çiziksiz (+) ekran-batarya (n=1.585 dudak)",
        "F-04..06: 12 Wh yanmaz LLZO katı-hal pil, &lt;=36.2 C, SAR 0.054, ISO 10993",
        "F-07..10: Portsuz gövdede Qi2.2 şarj, AB 2023/1542 &lt;3 sn aletsiz değişim",
        "MON-1..20: 90° bükümlü B çubuğu (TEK Type-C + anten), halka ekran üstünde",
        "MEC-33: 68.0 g 4-karo gövde + 20.0 g 90° B modülü = 88.0 g (84 iç parça)",
        "MEC-35..38: ±90° menteşe 50 000 çevrim, 1.5 m düşme ve IP68 sızdırmazlık",
    ]
    for i, t in enumerate(g):
        o.append('<text class="lbls" x="780" y="%d">%s</text>' % (884 + i * 15, t))
    return "\n".join(o) + "\n</svg>\n"


def main():
    for name, fn in (("P19-GOVDE-VE-SANDVIC-PARCA-PARCA.svg", sheet_p19),):
        svg = fn()
        with open(os.path.join(HERE, name), "w") as fh:
            fh.write(svg)
        print("wrote", name.split("-")[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
