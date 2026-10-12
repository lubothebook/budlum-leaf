#!/usr/bin/env python3
# BUDLUM LEAF · pafta/make_l3_sheets.py · revision L.5.0 · 2026-10-12
# Emits the three Turkish explainer sheets of Revision L.5.0:
#   E01-SISTEM-KAMERA-VE-PORT.svg     whole system: 4-Quadrant (+) seamless snap screen-battery body,
#                                     biocompatible eyewear-safe solid-state battery, portless Qi2 body,
#                                     and 90°-bent-stem B module (only stem above edge, round ring ON screen)
#   E02-B-MODULU-KESIT.svg            90°-Bent-Stem B module (20 g): 90° L-stem (LCP antenna + ONLY USB-C port),
#                                     ±90° reversible Ti hinge, round ring ON screen (50MP OIS + rear AMOLED)
#   E03-PORT-RAY-KESIT.svg            (+) cross zero-scratch optical/magnetic latch, universal Qi/Qi2.2 wireless
#                                     charging in portless body, and single USB-C in the 90°-bent B stem
# Gate: pafta/check_sheets.py -> OVER 0, COVERED 0, COLLIDE 0.

import math
import os
import sys
import textwrap

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cad"))
from leaf_geom import outline, corner_cut
import monogram_letter as ML

HERE = os.path.dirname(os.path.abspath(__file__))

STYLE = """<style>
    .bg{fill:#fbfaf7}
    .t{font-family:Helvetica,Arial,sans-serif;fill:#181816}
    .h1{font-size:24px;font-weight:700}
    .h2{font-size:15px;font-weight:700}
    .h3{font-size:12.5px;font-weight:700}
    .lbl{font-size:13px}
    .lblb{font-size:13px;font-weight:700}
    .lbls{font-size:10.5px}
    .s{font-size:11.5px;fill:#4b4b47;font-family:Helvetica,Arial,sans-serif}
    .body{font-size:14px;fill:#181816;font-family:Helvetica,Arial,sans-serif}
    .glass{fill:#ffffff;stroke:#181816;stroke-width:2.4}
    .live{fill:#dcecff;stroke:#18507e;stroke-width:1.6}
    .dead{fill:#8f948f;stroke:#111;stroke-width:1.4}
    .steel{fill:#d8dbe0;stroke:#5b6169;stroke-width:1.6}
    .mod{fill:#f7dcae;stroke:#8a5a12;stroke-width:2}
    .gd{fill:#ffe9a8;stroke:#8a6a12;stroke-width:1.4}
    .mag{fill:#c9ccd1;stroke:#3b3f45;stroke-width:1.2}
    .gsk{fill:#e6d6f2;stroke:#5a3b7a;stroke-width:1.4}
    .body4{fill:#f2f1ec;stroke:#5b6169;stroke-width:1.6}
    .rule{stroke:#d5d5cf;stroke-width:1.2}
    .dim{stroke:#8a5a12;stroke-width:1.1}
    .lt{font-size:13px;font-weight:700;fill:#f6f6f4;font-family:Helvetica,Arial,sans-serif}
    .ls{font-size:11px;fill:#dcdcd8;font-family:Helvetica,Arial,sans-serif}
  </style>"""


def head(w, h, title, aria):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
        'role="img" aria-label="%s">\n  <title>%s</title>\n  %s\n  <rect class="bg" x="0" y="0" width="%d" height="%d"/>'
        % (w, h, w, h, aria, title, STYLE, w, h)
    )


def lines(txt, x, y, width_chars, dy=19, cls="s"):
    """Wrapped text, one <text> per line, and the y of the next free line."""
    out = []
    for ln in textwrap.wrap(txt, width_chars):
        ln_esc = ln.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        out.append('<text class="%s" x="%d" y="%.0f">%s</text>' % (cls, x, y, ln_esc))
        y += dy
    return out, y


def plan_path(x0, y0, bw, bh):
    """Returns rectangular prism plan path with small corner radius R = 6.35 mm."""
    c = corner_cut(80.0)
    pts = outline(160.0, 80.0, c, 0.0)
    s = min(bw / 160.0, bh / 80.0)
    ox = x0 + (bw - 160.0 * s) / 2.0
    oy = y0 + (bh - 80.0 * s) / 2.0
    d = "M " + " L ".join("%.1f %.1f" % (ox + (x + 80.0) * s, oy + (40.0 - y) * s) for (x, y) in pts) + " Z"
    return d, s, ox, oy


def sheet_e01():
    w, h = 1400, 980
    o = [
        head(
            w,
            h,
            "BUDLUM LEAF · 4-PARÇALI (+) EKRAN-BATARYA, Qİ2 GÖVDE VE 90° BÜKÜMLÜ B MODÜLÜ",
            "Ortadan + bolunmus 4 parcali ciziksiz ekran-pil, gozluk sagligina uygun kati-hal pil, portsuz Qi2 govde ve 90 derece bukumlu B modulu",
        )
    ]
    o.append('<text class="t h1" x="40" y="52">4-PARÇALI (+) TAK-ÇIKAR EKRAN-BATARYA · PORTSUZ Qİ2 GÖVDE · 90° BÜKÜMLÜ B</text>')
    body, _ = lines(
        "Revizyon L.5.0 ile kaba alt batarya çıkıntısı tamamen kaldırılmıştır: (1) 80x160x2.00 mm gövde ortadan artı (+) şeklinde 4 eşit "
        "tak-çıkar polikarbonat ekran-batarya parçasına (40x80 mm, 4x 3 Wh = 12 Wh yanmaz katı-hal pil) bölünür. (2) Gövdede Type-C yoktur, "
        "her Qi/Qi2 pedde kablosuz şarj olur. (3) B modülünün sadece anten+Type-C çubuğu 90° dik bükülür, yuvarlak kamera ekran üstüne oturur.",
        40,
        78,
        150,
    )
    o += body
    o.append('<line class="rule" x1="40" y1="120" x2="1360" y2="120"/>')

    # Panel 1: Turned & 90°-Bent-at-Gap B module (1.00 mm horizontal top çubuk on screen edge, round ring facing us)
    o.append('<rect class="glass" x="40" y="134" width="1320" height="256" rx="6"/>')
    o.append('<rect class="live" x="70" y="156" width="400" height="212" rx="6"/>')
    k1, ox1, oy1 = 3.8, 198.0, 196.0
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#18507e" stroke-width="1.8" stroke-dasharray="5 3"/>'
             % (ox1 - 12, oy1, ox1 + 36.0 * k1, oy1))
    o.append(
        '<path d="%s" fill="#8fa882" stroke="#5c6b58" stroke-width="1.5" fill-rule="evenodd"/>'
        % ML.svg_path(k1, ox1, oy1)
    )
    cx1, cy1 = ox1 + 16.0 * k1, oy1 + 20.0 * k1
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#46505a" stroke="#5c6b58" stroke-width="1.2"/>' % (cx1, cy1, 12.0 * k1))
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#183452" stroke="#8ab4d4" stroke-width="1.1"/>' % (cx1, cy1, 8.0 * k1))
    o.append('<text class="t h2" x="500" y="166">1 · BOŞLUKTAN 90° BÜKÜLEN B MODÜLÜ: 1 MM YATAY ÇUBUK ÜSTTE, YUVARLAK ÖNDE</text>')
    txt1 = (
        "Orijinal b.png tasarımı kesilmeden ve ek menteşe parçası eklenmeden ters çevrilip çubuk ile yuvarlak arasındaki doğal boşluktan "
        "90° dik açıyla bükülmüştür: böylece 1.00 mm (bir milim) çubuk yukarıda yatay olarak durur ve 2.00 mm ekranın üst kenarına tam "
        "oturur; çubuk hariç kalan yuvarlak kısım (Ø32/Ø24 mm) ise ekran yüzeyinde bize doğru bakarak durur. Ekranın 4 yönüne ve ön/arka "
        "yüzüne takılabilir. Cihazdaki TEK USB Type-C (40W PD 3.1) prizi bu 1 mm yatay üst çubuk içindedir."
    )
    body, _ = lines(txt1, 500, 192, 95)
    o += body

    # Panel 2: 4-Quadrant (+) Seamless Snap-Together Polycarbonate Screen-Battery Body
    o.append('<rect class="glass" x="40" y="406" width="1320" height="240" rx="6"/>')
    o.append('<rect class="live" x="70" y="428" width="400" height="196" rx="6"/>')
    d2, s2, ox2, oy2 = plan_path(90, 444, 360, 164)
    o.append('<path d="%s" fill="#dcecff" stroke="#18507e" stroke-width="2.0"/>' % d2)
    # 4 internal solid-state cells + + cross seam + Qi2 ring
    for (qx, qy) in ((4.0, 4.0), (82.0, 4.0), (4.0, 42.0), (82.0, 42.0)):
        o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" fill="#b8ebd8" stroke="#267862" stroke-width="1.0"/>'
                 % (ox2 + qx * s2, oy2 + qy * s2, 74.0 * s2, 34.0 * s2))
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#1b8a6b" stroke-width="1.6" stroke-dasharray="4 2"/>'
             % (ox2 + 80.0 * s2, oy2, ox2 + 80.0 * s2, oy2 + 80.0 * s2))
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#1b8a6b" stroke-width="1.6" stroke-dasharray="4 2"/>'
             % (ox2, oy2 + 40.0 * s2, ox2 + 160.0 * s2, oy2 + 40.0 * s2))
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#d89818" stroke-width="2.2" stroke-dasharray="8 3"/>'
             % (ox2 + 80.0 * s2, oy2 + 40.0 * s2, 24.0 * s2))
    o.append('<text class="t h2" x="500" y="438">2 · ORTADAN ARTI (+) 4 PARÇALI ÇİZİKSİZ EKRAN-BATARYA VE GÖZLÜK SAĞLIĞI</text>')
    txt2 = (
        "80.0 x 160.0 x 2.00 mm (68 g) gövde ortadan artı (+) şeklinde 4 eşit tak-çıkar polikarbonat karoya (Q1-Q4; 40x80 mm, 17 g) "
        "bölünür. İç + kenarında 12 µm n=1.585 kendi kendini onaran optik elastomer dudak ve Corning kenar-sarımlı elektrotlar sayesinde "
        "hiçbir çizik veya birleşim izi görünmez. Her karoda gözlük/el/cep kullanımına uygun yanmaz LLZO/PEO katı-hal pil (4x 3 Wh = 12 Wh, "
        "sıfır HF gazı, <=36.2 C göz güvenliği, ELF <0.08 µT, SAR 0.054 W/kg, ISO 10993) bulunur; AB 2023/1542 gereği 3 sn içinde değişir."
    )
    body, _ = lines(txt2, 500, 464, 95)
    o += body

    # Panel 3: Portless Qi2 Wireless Body & Mandatory Camera Module Dependency
    o.append('<rect class="glass" x="40" y="662" width="1320" height="296" rx="6"/>')
    o.append('<rect class="body4" x="70" y="706" width="180" height="80" rx="6"/>')
    o.append('<rect class="mod" x="260" y="712" width="200" height="68" rx="6"/>')
    o.append('<rect class="gsk" x="254" y="708" width="10" height="76" rx="3"/>')
    o.append('<text class="t h2" x="500" y="694">3 · PORTSUZ Qİ2 KABLOSUZ ŞARJ GÖVDESİ VE ZORUNLU B MODÜLÜ MİMARİSİ</text>')
    txt3 = (
        "Ekran gövdesinin altında veya kenarlarında kesinlikle Type-C portu veya fiziksel buton yoktur. 4 çeyrek parçanın merkezde (0,0) "
        "birleşerek oluşturduğu Ø54.0 mm Qi2.2 MPP ana bobin ve her parçanın kendi içindeki bağımsız Ø22.0 mm Qi alt-bobini sayesinde "
        "cihaz herhangi bir standart kablosuz şarj aletinde (15W-25W) şarj olur. Kablolu Type-C şarj/veri, Sıfır-CPU UWB/60GHz mmWave "
        "iletişim, 4-Karo Ana TCON ekran sürüşü, kamera ve ses için 90° bükümlü B kamera modülünün takılması zorunludur."
    )
    body, _ = lines(txt3, 500, 720, 95)
    o += body
    o.append('<text class="lbls" x="70" y="812">Sol: 4x (40x80 mm) katı-hal pilli Qi2 karo · Sağ: 90° B modülü</text>')
    o.append('<text class="lbls" x="70" y="830">Gövdede Type-C yok · Tek Type-C B çubuğunda · AB 2023/1542 uyumlu</text>')
    o.append("</svg>")
    open(os.path.join(HERE, "E01-SISTEM-KAMERA-VE-PORT.svg"), "w").write("\n".join(o))


def sheet_e02():
    w, h = 1400, 980
    o = [
        head(
            w,
            h,
            "BUDLUM LEAF · 90° DİK BÜKÜMLÜ B MODÜLÜ · L-KESİT, TEK TYPE-C, KAMERA VE PANEL",
            "Sadece cubuk kismi 90 derece dik bukulen, yuvarlak kismi ekran ustune oturan B modulu kesiti",
        )
    ]
    o.append('<text class="t h1" x="40" y="52">B MODÜLÜ (REV L.5.0) · 90° DİK L-ÇUBUK, TEK TYPE-C VE KAMERA KESİTİ</text>')
    body, _ = lines(
        "Kesit B modülünün 90° dik açıyla bükülmüş çubuk omurgasından ve ekran üstüne oturan yuvarlak halkasından geçer. Sadece anten + "
        "Type-C çubuğu yukarıda/kenarda dik kalır; yuvarlak kısım ekranın üzerine yerleşir ve ±90° menteşeyle öne/arkaya takılır.",
        40,
        78,
        150,
    )
    o += body
    o.append('<line class="rule" x1="40" y1="120" x2="1360" y2="120"/>')

    # Left panel: 90° L-section of the B module sitting on the 2.00 mm screen
    o.append('<rect class="glass" x="40" y="134" width="820" height="556" rx="6"/>')
    o.append('<text class="t h2" x="60" y="162">A · 90° DİK AÇILI L-KESİT · ÇUBUK DİK, YUVARLAK HALKA EKRAN ÜSTÜNDE</text>')

    ks, oxs, oys = 15.5, 92.0, 410.0

    def Xs(x):
        return oxs + x * ks

    def Ys(z):
        return oys - z * ks

    # Underlying 2.00 mm polycarbonate screen-battery quadrant (x=6.4..40.0, z=-2.20..0.00)
    o.append(
        '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" fill="#dcecff" stroke="#18507e" stroke-width="1.4"/>'
        % (Xs(6.4), Ys(0.0), 33.6 * ks, 2.20 * ks)
    )
    # 90°-Bent Stem section (x=0..6.4, z=-2.60..4.00) wrapping the screen edge at 90°
    o.append(
        '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="#7f927a" stroke="#5c6b58" stroke-width="1.5"/>'
        % (Xs(0.0), Ys(4.0), 6.4 * ks, 6.6 * ks, 0.55 * ks)
    )
    # ±90° Titanium Hinge at neck (x=6.4..8.0)
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#d8dbe0" stroke="#18507e" stroke-width="1.2"/>'
             % (Xs(7.2), Ys(2.0), 0.95 * ks))
    # Ring walls sitting ON the screen (x=8.0..12.0 and x=36.0..40.0, z=0..4.0)
    for (a, b) in ((8.0, 12.0), (36.0, 40.0)):
        o.append(
            '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="#93a68c" stroke="#5c6b58" stroke-width="1.5"/>'
            % (Xs(a), Ys(4.0), (b - a) * ks, 4.0 * ks, 0.55 * ks)
        )
    # Front camera bezel & folded optics inside Ø24.0 mm bore (z=1.05..3.96)
    o.append(
        '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="#687482" stroke="#48525c" stroke-width="1.3"/>'
        % (Xs(12.0), Ys(3.96), 24.0 * ks, 2.90 * ks)
    )
    o.append(
        '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" fill="#24588a"/>'
        % (Xs(15.8), Ys(3.98), 16.4 * ks, 0.50 * ks)
    )
    # Cu-Graphite shield + Rear round AMOLED panel (z=0.04..1.05)
    o.append(
        '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" fill="#203040" stroke="#48525c" stroke-width="1.3"/>'
        % (Xs(12.0), Ys(1.00), 24.0 * ks, 0.96 * ks)
    )

    for (x, y, t) in (
        (60, 206, "90° DİK BÜKÜMLÜ ÇUBUK: 32.0 x 4.0 x 1.00 mm · sadece anten çubuğu yukarıda/kenarda dik kalır"),
        (60, 228, "±90° TERSİNİR TİTANYUM MENTEŞE: çubuk ile yuvarlak halka arasında çift-yönlü L-boyun"),
        (60, 250, "CİHAZDAKİ TEK USB TYPE-C: 40 W PD 3.1 + DP 2.1 su geçirmez IP68 priz 90° çubuk içindedir"),
        (60, 272, "YUVARLAK HALKA (EKRAN ÜSTÜNDE): 32 x 32 x 4.00 mm halka doğrudan ekranın üzerine oturur"),
        (60, 310, "ÖN YÜZ (z = 1.05..4.00 mm): Ø24.0 mm açıklıkta 50 MP OIS kamera + mikrofon + hoparlör + flaş"),
        (60, 480, "ORTA VE ARKA YÜZ (z = 0.00..1.04 mm): 0.15 mm Cu-Grafit kalkan + Ø22.4 mm Yuvarlak AMOLED"),
        (60, 504, "4 YÖNE VE ÖNE/ARKAYA TAKILMA: üst, alt, sol, sağ kenarlara ve ekranın önüne/arkasına takılır"),
        (60, 528, "SIFIR-CPU SİSTEM BEYNİ: 4-Karo Ana TCON + UWB/60GHz mmWave SiP + Ses DSP halka PCB'dedir"),
        (60, 552, "GÖZLÜK GÜVENLİĞİ: anten çubuğu gözden uzakta durarak SAR değerini 0.054 W/kg altına indirir"),
    ):
        o.append('<text class="lbls" x="%d" y="%d">%s</text>' % (x, y, t))

    # Right column top: 90° Stem & Reversible specs
    o.append('<rect class="glass" x="880" y="134" width="480" height="270" rx="6"/>')
    o.append('<text class="t h2" x="900" y="164">B · 90° ÇUBUK VE ARKA AMOLED SAYILARI</text>')
    rows = [
        ("90° dik çubuk", "32x4x1 mm · ekran üst kenarında"),
        ("tek USB Type-C", "40 W PD 3.1 + DP 2.1 · IP68 contalı"),
        ("çubuk anteni", "Wi-Fi 7, BT 5.4, UWB + 60 GHz dizi"),
        ("tersinir menteşe", "±90° Grade-5 Ti · öne/arkaya takım"),
        ("arka AMOLED", "Ø22.4 mm · 220x220 px · 120 Hz"),
        ("ekran yerleşimi", "yuvarlak halka ekran üstüne oturur"),
        ("4 yöne takım", "üst, alt, sol ve sağ kenarlara uyumlu"),
        ("SAR (baş/göz)", "0.054 W/kg (ICNIRP sınırının 37x altı)"),
    ]
    for (i, (k, v)) in enumerate(rows):
        o.append('<text class="lblb" x="900" y="%d">%s</text>' % (194 + i * 24, k))
        o.append('<text class="s" x="1040" y="%d">%s</text>' % (194 + i * 24, v))

    # Right column bottom: Front camera & Zero-CPU specs
    o.append('<rect class="glass" x="880" y="420" width="480" height="270" rx="6"/>')
    o.append('<text class="t h2" x="900" y="450">C · KAMERA VE SIFIR-CPU BEYİN SAYILARI</text>')
    rows2 = [
        ("algılayıcı", "1 inç sınıfı · 50 MP · 12.8 x 9.6 mm"),
        ("optik yol", "katlanmış prizma + 5P asferik lens"),
        ("dengeleme", "4-eksen OIS bakır ses-bobini × 4"),
        ("ana TCON", "4-karo çiziksiz T-OLED + PDLC sürücü"),
        ("kablosuz SiP", "UWB + 60 GHz mmWave 0-gecikme"),
        ("mikrofon/ses", "2x MEMS + 9.0x3.2 mm hoparlör"),
        ("EM/ısı kalkanı", "0.15 mm Cu-Grafit (%0 Z-çakışması)"),
        ("toplam kütle", "20.0 g · r 0.55 mm yumuşak kenar"),
    ]
    for (i, (k, v)) in enumerate(rows2):
        o.append('<text class="lblb" x="900" y="%d">%s</text>' % (480 + i * 24, k))
        o.append('<text class="s" x="1040" y="%d">%s</text>' % (480 + i * 24, v))

    # Bottom band
    o.append('<rect class="glass" x="40" y="710" width="1320" height="248" rx="6"/>')
    o.append('<text class="t h2" x="60" y="742">D · 90° BÜKÜMLÜ B MODÜLÜ İŞ AKIŞI VE DOĞRULAMA KAPILARI</text>')
    steps = [
        ("1 · 90° ÇUBUK", "anten yukarıda dik", "tek Type-C 40W"),
        ("2 · YUVARLAK B", "ekran üstüne oturur", "simetrik N52H"),
        ("3 · ÖN/ARKA", "±90° Ti menteşe", "4 yöne takılır"),
        ("4 · 4-KARO TCON", "+ derzi sıfırlar", "120 Hz T-OLED"),
        ("5 · UWB/mmWAVE", "sıfır-CPU akış", "4.98 Gbit/s"),
        ("6 · KAMERA/SES", "50MP OIS + 5P", "Ø22.4 AMOLED"),
    ]
    for (i, (k, a, b)) in enumerate(steps):
        x = 60 + i * 216
        o.append('<rect class="live" x="%d" y="756" width="196" height="78" rx="6"/>' % x)
        o.append('<text class="lbls" x="%d" y="780">%s</text>' % (x + 12, k))
        o.append('<text class="lbls" x="%d" y="802">%s</text>' % (x + 12, a))
        o.append('<text class="lbls" x="%d" y="822">%s</text>' % (x + 12, b))
    body, y = lines(
        "Sadece çubuk kısmı 90° dik açıyla büküldüğü için çubuk ekran kenarını L-klips gibi kavrar, yuvarlak kamera ve arka AMOLED "
        "ise ekranın üzerine oturur. Böylece modül ekranın 4 yönüne ve önüne/arkasına saniyeler içinde takılıp çıkarılabilir.",
        60,
        856,
        155,
    )
    o += body
    body, y = lines(
        "Kapılar: MON-1 90° dik bükümlü çubuk · MON-2 yuvarlak kısım ekran üstünde · MON-3 ±90° öne/arkaya takım · MON-4 4 yöne uyum · MON-5 tek USB-C çubukta · MON-6..20 TCON, UWB ve IP68.",
        60,
        y + 6,
        140,
    )
    o += body
    o.append("</svg>")
    open(os.path.join(HERE, "E02-B-MODULU-KESIT.svg"), "w").write("\n".join(o))


def sheet_e03():
    w, h = 1400, 980
    o = [
        head(
            w,
            h,
            "BUDLUM LEAF · (+) ÇİZİKSİZ EKRAN-BATARYA KENETLENME, Qİ2 KABLOSUZ ŞARJ VE TEK TYPE-C",
            "Ortadan + bolunmus 4 parcali ciziksiz ekran-batarya kenetlenmesi, portsuz govdede Qi2 sarj ve B modulunde tek Type-C",
        )
    ]
    o.append('<text class="t h1" x="40" y="52">(+) ÇİZİKSİZ 4-KARO KENETLENME · PORTSUZ Qİ2 ŞARJ · B ÇUBUĞUNDA TEK TYPE-C</text>')
    body, _ = lines(
        "Kesit ortadaki artı (+) birleşim hattından geçer. 4 polikarbonat ekran-batarya parçası n=1.585 optik dudak ile sıfır çizikle "
        "birleşir; gövdede Type-C yoktur, her kablosuz şarjda şarj olur; kablolu Type-C sadece 90° B çubuğundadır.",
        40,
        82,
        155,
    )
    o += body
    o.append('<line class="rule" x1="40" y1="98" x2="1360" y2="98"/>')

    # ---- the section, left panel: Q1 and Q2 meeting across the + seam at x = 0
    o.append('<rect class="glass" x="40" y="116" width="820" height="420" rx="6"/>')
    o.append('<rect class="body4" x="80" y="290" width="260" height="40" rx="6"/>')
    o.append('<rect class="body4" x="352" y="290" width="260" height="40" rx="6"/>')
    # 12 µm n=1.585 optical elastomer seam lip at x = 340..352
    o.append('<rect class="gsk" x="340" y="290" width="12" height="40" rx="2"/>')
    # Gold micro-leaf contacts + Titanium micro-dovetail pin across the + seam
    o.append('<rect class="gd" x="330" y="298" width="32" height="7" rx="2"/>')
    o.append('<rect class="gd" x="330" y="310" width="32" height="7" rx="2"/>')
    o.append('<rect class="steel" x="324" y="320" width="44" height="8" rx="2"/>')
    o.append('<rect class="mag" x="296" y="334" width="28" height="10" rx="3"/>')
    o.append('<rect class="mag" x="368" y="334" width="28" height="10" rx="3"/>')
    for (x, y, t) in (
        (80, 176, "SOL VE SAĞ ÇEYREK KARO (40 x 80 x 2.00 mm): biyouyumlu ISO 10993 PC + yanmaz LLZO katı-hal pil"),
        (80, 200, "ORTA (+) OPTİK DUDAK (12 µm, n = 1.585): Fresnel yansıması &lt;%0.0001 · sıfır çizik, sıfır görünür iz"),
        (80, 224, "TİTANYUM ARTl (+) GÖBEK VE MİKRO-KIRLANGIÇ: Z-basamağı &lt;2.5 µm · 64 altın mikro-yaprak kontak"),
        (80, 274, "Q1 KARO (3.0 Wh KATI-HAL PİL + Qİ2)"),
        (366, 274, "Q2 KARO (3.0 Wh KATI-HAL PİL + Qİ2)"),
        (80, 400, "3 ms DEAD-PAD GÜVENLİĞİ: kriptografik el sıkışma tamamlanmadan + kontaklarına akım verilmez"),
        (80, 424, "ALETSİZ 3 SN TAK-ÇIKAR (AB 2023/1542 MD. 11): 3 karo çalışırken 1 karo kesintisiz (hot-swap) değişir"),
        (80, 448, "PORTSUZ VE BUTONSUZ GÖVDE: ekran gövdesinin altında veya kenarında Type-C ya da buton yoktur"),
        (80, 476, "KABLOLU TYPE-C SADECE B MODÜLÜNDE: 40 W PD 3.1 priz B harfinin 90° bükümlü çubuğundadır"),
    ):
        o.append('<text class="lbls" x="%d" y="%d">%s</text>' % (x, y, t))

    # ---- right column
    o.append('<rect class="glass" x="880" y="116" width="480" height="210" rx="6"/>')
    o.append('<text class="t h2" x="900" y="146">4-KARO (+) İÇ PARÇALARI VE GÜVENLİK</text>')
    mods = [
        ("LLZO Katı-Hal Pil", "4x 3.0 Wh = 12.0 Wh · yanmaz, 0 HF"),
        ("Gözlük Kalkanı", "&lt;=36.2 C · ELF &lt;0.08 µT · SAR 0.054"),
        ("n=1.585 Optik Dudak", "&lt;15 µm çiziksiz + birleşim · IP68"),
        ("Ti Artı (+) Göbek", "4-yollu merkez kilit + 64 altın yaprak"),
        ("Qi2.2 + 4x Qi Bobin", "Ø54 mm merkez + 4x Ø22 mm çeyrek"),
        ("90° B Çubuğunda", "Cihazdaki TEK USB-C (40W PD 3.1)"),
    ]
    for (i, (k, v)) in enumerate(mods):
        o.append('<text class="lblb" x="900" y="%d">%s</text>' % (176 + i * 24, k))
        o.append('<text class="s" x="1045" y="%d">%s</text>' % (176 + i * 24, v))
    o.append('<text class="s" x="900" y="322">3 karo çalışırken 1 karo hot-swap değiştirilir.</text>')

    o.append('<rect class="glass" x="880" y="342" width="480" height="194" rx="6"/>')
    o.append('<text class="t h2" x="900" y="372">ŞARJ YOLLARI (Qİ2 KABLOSUZ + B TYPE-C)</text>')
    rows = [
        ("1 · Qi / Qi2.2 ped", "gövde 15-25 W kablosuz şarj alır"),
        ("2 · tekil çeyrek karo", "sökülü karo Ø22 mm bobinle Qi şarj"),
        ("3 · B modülü Type-C", "90° çubuktan 40 W PD 3.1 şarj"),
        ("4 · B modülü veri", "Type-C DP 2.1 + 60GHz mmWave"),
    ]
    for (i, (k, v)) in enumerate(rows):
        o.append('<text class="lblb" x="900" y="%d">%s</text>' % (400 + i * 26, k))
        o.append('<text class="s" x="1040" y="%d">%s</text>' % (400 + i * 26, v))
    o.append('<text class="s" x="900" y="512">Herhangi bir kablosuz şarj pedinde şarj olur;</text>')
    o.append('<text class="s" x="900" y="532">kablolu Type-C sadece B kamera modülündedir.</text>')

    # ---- bottom band
    o.append('<rect class="glass" x="40" y="556" width="1320" height="402" rx="6"/>')
    o.append('<text class="t h2" x="60" y="588">NEDEN GÖVDEDE TYPE-C YOK VE EKRAN 4 PARÇALI (+) TAK-ÇIKAR?</text>')
    reasons = [
        ("1 · sıfır kabalık", "alt batarya çıkıntısı kaldırıldı; pil 2.00 mm polikarbonat karoların içine gömüldü."),
        ("2 · çiziksiz + ekran", "n=1.585 optik elastomer dudak ve kenar-sarımlı elektrotlarla 4 parça tek ekran olur."),
        ("3 · gözlük sağlığı", "yanmaz LLZO katı-hal pil (0 HF gazı, <=36.2 C, SAR 0.054 W/kg, ISO 10993 biyouyumlu)."),
        ("4 · evrensel Qi2 + B", "gövde her kablosuz şarjda şarj olur; Type-C ve aktif beyin sadece 90° B modülündedir."),
    ]
    y = 616
    for (k, v) in reasons:
        o.append('<text class="lblb" x="60" y="%d">%s</text>' % (y, k))
        body, _ = lines(v, 210, y, 145)
        o += body
        y += 26
    o.append('<text class="t h2" x="60" y="740">AB PİL YÖNETMELİĞİ (EU 2023/1542) VE TÜRKİYE UYUMU</text>')
    body, y = lines(
        "AB 2023/1542 Madde 11 (18 Şubat 2027), taşınabilir pillerin kullanıcı tarafından aletsiz, ısısız ve çözücüsüz olarak kolayca "
        "çıkarılıp değiştirilebilmesini zorunlu kılar. Budlum Leaf'in 4 çeyrek ekran-batarya karosu (Q1-Q4) 3 saniyede elle takılıp çıkarılır.",
        60,
        768,
        155,
    )
    o += body
    body, y = lines(
        "Ayrıca 90° bükümlü B kamera modülü kutuda standart gelir ve üzerindeki 40 W USB Type-C PD 3.1 prizi ile 2022/2380 ortak şarj "
        "direktifini tam karşılar; ekran gövdesi ise tamamen portsuz ve sızdırmaz (IP68) kalarak her Qi/Qi2 pedde kablosuz şarj olur.",
        60,
        y + 6,
        155,
    )
    o += body
    body, y = lines(
        "B modülünün sadece anten+Type-C çubuğu 90° dik açıyla yukarıda kalır; yuvarlak kamera ekran üstüne oturur ve öne/arkaya takılır.",
        60,
        y + 6,
        155,
    )
    o += body
    o.append('<text class="lbls" x="60" y="948">Kenetlenme kapıları RL-1 … RL-18 · 90° B modülü kapıları MON-1 … MON-20 · 4-karo (+) ve katı-hal pil kapıları F-01 … F-10</text>')
    o.append("</svg>")
    open(os.path.join(HERE, "E03-PORT-RAY-KESIT.svg"), "w").write("\n".join(o))


if __name__ == "__main__":
    sheet_e01()
    sheet_e02()
    sheet_e03()
    print("wrote E01, E02, E03")
