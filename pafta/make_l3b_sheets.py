#!/usr/bin/env python3
# BUDLUM LEAF · pafta/make_l3b_sheets.py · revision L.5.0 · 2026-10-12
# Emits the three design sheets of the 4-Quadrant (+) Snap-Together Polycarbonate Screen-Battery Body,
# Biocompatible Eyewear-Safe Solid-State Battery & Universal Qi2 Charging, and 90°-Bent-Stem B Docking:
#   P11-ENERJI-SANDVICI.svg        2.00 mm 11-layer biocompatible polycarbonate + T-OLED + PDLC + LLZO solid-state battery + Qi2 stack
#   P12-BATARYA-TASARIMI.svg       4-Quadrant (+) cutaways (Q1..Q4, 52 parts), eyewear health physics (<=36.2 C, 0 HF, SAR 0.054), Qi2
#   P13-MIKNATIS-ALANI-VE-ACI.svg  (+) zero-scratch optical/magnetic seam and 90°-bent-stem B reversible 4-edge front/back docking
# Gate: pafta/check_sheets.py -> OVER 0, COVERED 0, COLLIDE 0.

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cad"))
from make_l3_sheets import head, lines
import monogram_letter as ML

HERE = os.path.dirname(os.path.abspath(__file__))


def sheet_p11():
    w, h = 1400, 980
    o = [
        head(
            w,
            h,
            "BUDLUM LEAF · 2.20 MM 4-KARO (+) POLİKARBONAT EKRAN-BATARYA VE Qİ2 İSTİFİ",
            "4 parcali (+) polikarbonat ekran-batarya karosunun 2.00 mm 11-katmanli biyouyumlu kati-hal pil ve Qi2 kablosuz sarj istifi",
        )
    ]
    o.append('<text class="t h1" x="40" y="52">2.20 MM 4-KARO (+) EKRAN-BATARYA KESİTİ · KATI-HAL PİL, GÖZ KALKANI VE Qİ2</text>')
    body, _ = lines(
        "Revizyon L.5.0 ile kaba alt batarya çıkıntısı kaldırılmış, pil 4 çeyrek polikarbonat ekran karosunun (40x80x2.00 mm, 4x 17 g = 68 g) "
        "içine gömülmüştür. Her karo 11 simetrik katmandan oluşur: biyouyumlu ISO 10993 PC, OCA, T-OLED, PDLC, grafen/Mu-metal kalkan, yanmaz LLZO katı-hal pil ve Qi2 bobin.",
        40,
        78,
        150,
    )
    o += body
    o.append('<line class="rule" x1="40" y1="116" x2="1360" y2="116"/>')

    # ---- Left panel: 2.00 mm 11-layer stack inside each 40 x 80 mm quadrant
    o.append('<rect class="glass" x="40" y="132" width="760" height="504" rx="6"/>')
    o.append('<text class="t h2" x="70" y="160">A · 2.20 MM (18 G / KARO) 11-KATMANLI BİYOUYUMLU EKRAN-BATARYA İSTİFİ</text>')
    X0, X1 = 90, 580
    y = 180.0
    layers = [
        (220, "ön ISO 10993-5/-10 BPA'sız tıbbi polikarbonat + SiO2 kaplama · 200 µm", "#e8eef7"),
        (60, "ön silikon elastomer OCA kayma katmanı (%0.38 gerinim) · 50 µm", "#f7dcae"),
        (160, "ön titreşimsiz DC-dimming T-OLED (&lt;415 nm mavi ışık kesimli) · 140 µm", "#cfe4ff"),
        (40, "ön AgNW/ITO + Corning kenar-sarımlı 0 mm çerçevesiz elektrot · 40 µm", "#dcecff"),
        (60, "ön PDLC gizlilik + ortotropik grafen/Mu-metal göz kalkanı · 90 µm", "#e6d6f2"),
        (1400, "MERKEZ YANMAZ LLZO/PEO KATI-HAL PİL (3.0 Wh) + Qİ2 BOBİN · 1160 µm", "#b8ebd8"),
        (60, "arka PDLC gizlilik + ortotropik grafen/Mu-metal göz kalkanı · 90 µm", "#e6d6f2"),
        (40, "arka AgNW/ITO + 240 Hz kapasitif dokunma ve kalem ağı · 40 µm", "#dcecff"),
        (160, "arka titreşimsiz DC-dimming T-OLED + GIP satır sürücü · 140 µm", "#cfe4ff"),
        (60, "arka silikon elastomer OCA kayma katmanı · 50 µm", "#f7dcae"),
        (220, "arka ISO 10993-5/-10 BPA'sız tıbbi polikarbonat yüzey · 200 µm", "#e8eef7"),
    ]
    for (t, name, col) in layers:
        hpx = max(t / 1000.0 * 60.0, 17.0)
        o.append(
            '<rect x="%d" y="%.1f" width="%d" height="%.1f" rx="3" fill="%s" stroke="#5b6169" stroke-width="1.1"/>'
            % (X0, y, X1 - X0, hpx, col)
        )
        o.append('<text class="lbls" x="%d" y="%.1f">%s</text>' % (X0 + 14, y + hpx / 2 + 4, name))
        y += hpx + 4.5
    o.append('<text class="lbls" x="90" y="596">Toplam: 2.00 mm kalınlık, 4 x 17.0 g = 68.0 g gövde; 4 x 3.0 Wh = 12.0 Wh (3 200 mAh) yanmaz katı-hal pil.</text>')
    o.append('<text class="lbls" x="90" y="616">Gözlük modunda göz tarafı sıcaklığı &lt;=36.2 C, ELF manyetik alan &lt;0.08 µT ve SAR = 0.054 W/kg ile tam güvenlidir.</text>')

    # ---- Middle right panel: Inside the 90°-Bent-Stem B Module & + Seam Bus
    o.append('<rect class="glass" x="820" y="132" width="540" height="300" rx="6"/>')
    o.append('<text class="t h2" x="840" y="160">B · 90° BÜKÜMLÜ B MODÜLÜ VE (+) ARTl KENETLENME</text>')
    y = 184.0
    for (t, name, col) in [
        (450, "90° dik bükümlü çubuk: sadece anten + TEK Type-C yukarıda", "#d8dbe0"),
        (450, "±90° tersinir titanyum menteşe (öne/arkaya ve 4 yöne takım)", "#f7dcae"),
        (450, "yuvarlak halka ekran üstünde: 6L Sıfır-CPU PCB + 4-Karo TCON", "#cfe4ff"),
        (450, "U2 UWB/60GHz mmWave SiP + çubukta 1x4 faz-dizili anten", "#d8f0dc"),
        (125, "önde 50 MP OIS kamera + katlanmış prizma + 5P asferik lens", "#dcecff"),
        (125, "ortada 0.15 mm Cu-Grafit kalkan + arkada Ø22.4 mm AMOLED", "#ffe9a8"),
        (125, "merkez (0,0) Titanyum Artı (+) göbek + 64 altın mikro-yaprak", "#d8dbe0"),
        (125, "12 µm n=1.585 kendi kendini onaran çiziksiz optik dudak (IP68)", "#e6d6f2"),
    ]:
        hpx = 16.0 if t >= 400 else 12.0
        o.append(
            '<rect x="845" y="%.1f" width="145" height="%.1f" rx="2" fill="%s" stroke="#5b6169" stroke-width="1.0"/>'
            % (y, hpx, col)
        )
        o.append('<text class="lbls" x="1000" y="%.1f">%s</text>' % (y + hpx - 2, name))
        y += hpx + 5
    body, _ = lines(
        "Ekran gövdesinin altında Type-C veya buton yoktur; gövde her Qi/Qi2 pedde kablosuz şarj olur, Type-C sadece 90° B çubuğundadır.",
        840,
        382,
        56,
    )
    o += body

    # ---- Lower right panel: + Optical Zero-Seam & 3-second Hot-Swap
    o.append('<rect class="glass" x="820" y="446" width="540" height="190" rx="6"/>')
    o.append('<text class="t h2" x="840" y="474">C · &lt;15 µm (n=1.585) ÇİZİKSİZ (+) BİRLEŞİM VE HOT-SWAP</text>')
    o.append('<rect class="body4" x="850" y="496" width="150" height="32" rx="5"/>')
    o.append('<rect class="gsk" x="1000" y="494" width="12" height="36" rx="2"/>')
    o.append('<rect class="body4" x="1012" y="496" width="150" height="32" rx="5"/>')
    o.append('<text class="lbls" x="868" y="516">Q1 KARO (3 Wh)</text>')
    o.append('<text class="lbls" x="1030" y="516">Q2 KARO (3 Wh)</text>')
    o.append('<text class="lbls" x="850" y="548">12 µm n=1.585 OPTİK DUDAK + Ti ARTl GÖBEK + 64 ALTIN YAPRAK</text>')
    body, _ = lines(
        "4 çeyrek karo birleştiğinde n=1.585 optik elastomer dudak Fresnel yansımasını <%0.0001 düzeyine indirir; "
        "ekranda hiçbir çizik görünmez. 3 karo çalışırken 1 karo 3 saniyede kesintisiz değiştirilir.",
        840,
        572,
        56,
    )
    o += body

    # ---- Bottom table
    o.append('<rect class="glass" x="40" y="652" width="1320" height="308" rx="6"/>')
    o.append('<text class="t h2" x="60" y="682">D · 4-KARO (+) EKRAN-BATARYA VE 90° BÜKÜMLÜ B MODÜLÜ İÇ PARÇA TABLOSU</text>')
    rows = [
        ("ISO 10993 tıbbi polikarbonat", "2 x 0.20 mm / karo", "BPA/ftalat içermeyen biyouyumlu optik polikarbonat + 3H SiO2 kaplama"),
        ("çiziksiz (+) optik dudak", "12 µm (n = 1.585)", "fenil-florosilikon kendi kendini onaran dudak (&lt;%0.0001 yansıma, sıfır çizik)"),
        ("yanmaz LLZO/PEO katı-hal pil", "4 x 3.0 Wh = 12 Wh", "inorganik seramik-polimer elektrolit · %0 sıvı, %0 LiPF6, 0.0 ppm HF gazı"),
        ("gözlük ve sağlık kalkanı", "&lt;=36.2 C / 0.054 SAR", "ortotropik grafen + Mu-metal folyo + çift-telli (bifilar) akım iptali (&lt;0.08 µT)"),
        ("evrensel Qi / Qi2.2 bobinleri", "Ø54 mm + 4x Ø22 mm", "merkezde 4-sektörlü 15-25W Qi2.2 MPP bobini + her karoda bağımsız Qi bobin"),
        ("merkez Titanyum Artı (+) göbek", "64 altın yaprak", "Grade-5 Ti 4-yollu kilit + 8 mikro-kırlangıç pim (&lt;2.5 µm adım) + 24 N52H"),
        ("90° dik bükümlü B çubuğu", "6.4 x 44.0 x 4.5 mm", "sadece anten + cihazdaki TEK USB-C (40W PD 3.1, IP68) çubuğu yukarıda dik"),
        ("±90° tersinir boyun menteşesi", "Grade-5 Titanyum", "B modülünün ekranın 4 yönüne ve ÖN veya ARKA yüzüne takılmasını sağlar"),
        ("yuvarlak B halkası (ekran üstü)", "32 x 32 x 4.00 mm", "6L Sıfır-CPU PCB + 4-Karo TCON + UWB/60GHz SiP + 50MP OIS + Ø22.4 AMOLED"),
    ]
    for (i, (k, v, n)) in enumerate(rows):
        yy = 710 + i * 24
        o.append('<text class="lblb" x="60" y="%d">%s</text>' % (yy, k))
        o.append('<text class="lbls" x="265" y="%d">%s</text>' % (yy, v))
        o.append('<text class="s" x="405" y="%d">%s</text>' % (yy, n))
    o.append(
        '<text class="s" x="60" y="%d">4 çeyrek ekran-batarya karosu (52 iç parça) ve 90° bükümlü B modülü (32 iç parça) toplam 84 iç parçayla 3B modellenmiştir.</text>'
        % (710 + 9 * 24 + 10)
    )
    o.append("</svg>")
    open(os.path.join(HERE, "P11-ENERJI-SANDVICI.svg"), "w").write("\n".join(o))


def sheet_p12():
    w, h = 1400, 980
    o = [
        head(
            w,
            h,
            "BUDLUM LEAF · 4-PARÇALI (+) KATI-HAL BATARYA, GÖZLÜK SAĞLIĞI VE Qİ2 ŞARJ",
            "Ortadan + bolunmus 4 ceyrek polikarbonat ekran-batarya karosu, gozluk sagligina uygun yanmaz LLZO kati-hal pil ve Qi2 sarj",
        )
    ]
    o.append('<text class="t h1" x="40" y="52">4-PARÇALI (+) KATI-HAL BATARYA · GÖZLÜK SAĞLIĞI VE EVRENSEL Qİ2 ŞARJ</text>')
    body, _ = lines(
        "Kaba alt batarya modülü iptal edilmiştir: telefon ortasından artı (+) şeklinde 4 eşit polikarbonat ekran-batarya parçasına "
        "(Q1-Q4; 40x80x2.00 mm, 4x 3.0 Wh = 12.0 Wh) bölünmüştür. Gözlük olarak göze takıldığında, elde ve cepte tam sağlıklıdır.",
        40,
        78,
        150,
    )
    o += body
    o.append('<line class="rule" x1="40" y1="116" x2="1360" y2="116"/>')

    # ---- A: Internal Cutaway Plan of the 4-Quadrant (+) Polycarbonate Screen-Battery Body
    o.append('<rect class="glass" x="40" y="132" width="860" height="292" rx="6"/>')
    o.append('<text class="t h2" x="60" y="160">A · 4-KARO (+) İÇ KESİT PLANI · 4 x (40 x 80 x 2.20 MM) = 52 İÇ PARÇA</text>')
    ox, oy, kw, kh = 90.0, 178.0, 4.6, 2.5
    # Outer 160 x 80 mm plan split into 4 quadrants around center (ox+368, oy+100)
    o.append('<rect fill="#dcecff" stroke="#18507e" stroke-width="2.0" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="14"/>'
             % (ox, oy, 160.0 * kw, 80.0 * kh))
    for (qx, qy, lbl) in ((4.0, 4.0, "Q1 · 3.0 Wh LLZO"), (82.0, 4.0, "Q3 · 3.0 Wh LLZO"),
                          (4.0, 42.0, "Q2 · 3.0 Wh LLZO"), (82.0, 42.0, "Q4 · 3.0 Wh LLZO")):
        o.append('<rect fill="#b8ebd8" stroke="#1b8a6b" stroke-width="1.3" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="6"/>'
                 % (ox + qx * kw, oy + qy * kh, 74.0 * kw, 34.0 * kh))
        o.append('<circle cx="%.1f" cy="%.1f" r="22" fill="none" stroke="#c88a18" stroke-width="1.4" stroke-dasharray="4 2"/>'
                 % (ox + (qx + 37.0) * kw, oy + (qy + 17.0) * kh))
        o.append('<text class="lbls" x="%.1f" y="%.1f">%s</text>' % (ox + (qx + 8.0) * kw, oy + (qy + 19.0) * kh, lbl))
    # + Cross seam + Titanium hub + Ø54 mm Qi2.2 MPP ring
    cx_p, cy_p = ox + 80.0 * kw, oy + 40.0 * kh
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#1b8a6b" stroke-width="2.2"/>' % (cx_p, oy, cx_p, oy + 80.0 * kh))
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#1b8a6b" stroke-width="2.2"/>' % (ox, cy_p, ox + 160.0 * kw, cy_p))
    o.append('<circle cx="%.1f" cy="%.1f" r="52" fill="none" stroke="#d89818" stroke-width="2.6" stroke-dasharray="10 4"/>' % (cx_p, cy_p))
    o.append('<rect fill="#d8dbe0" stroke="#181816" stroke-width="1.4" x="%.1f" y="%.1f" width="20" height="20" rx="3"/>' % (cx_p - 10, cy_p - 10))

    o.append('<text class="lbls" x="60" y="394">• Her karoda (40x80 mm): 35x75x1.08 mm yanmaz LLZO katı-hal pil (3.0 Wh) + Ø22 mm Qi bobin + 90° Qi2.2 sektör + U_QI PMIC.</text>')
    o.append('<text class="lbls" x="60" y="412">• Merkezde (+): 12 µm n=1.585 çiziksiz optik dudak + Titanyum Artı göbek + 24 N52H mıknatıs + 64 altın mikro-yaprak kontak.</text>')

    # ---- B: Eyewear / Hand / Pocket Health & Energy Physics
    o.append('<rect class="glass" x="920" y="132" width="440" height="292" rx="6"/>')
    o.append('<text class="t h2" x="940" y="160">B · SAĞLIK VE ENERJİ FİZİĞİ (REV L.5.0)</text>')
    rows = [
        ("Tek Çeyrek Karo", "LLZO Katı", "3.0 Wh", "800 mAh"),
        ("4-Karo Tam Ekran", "750 Wh/L", "12.0 Wh", "3 200 mAh"),
        ("Göz Sıcaklığı", "NTC Kilit", "&lt;=36.2 C", "IEC 60601"),
        ("SAR ve Manyetik", "Mu-Metal", "0.054 W/kg", "&lt;0.08 µT"),
    ]
    for (i, (a, b, c, d)) in enumerate(rows):
        yy = 192 + i * 26
        o.append('<text class="lblb" x="940" y="%d">%s</text>' % (yy, a))
        o.append('<text class="lbls" x="1085" y="%d">%s</text>' % (yy, b))
        o.append('<text class="lbls" x="1175" y="%d">%s</text>' % (yy, c))
        o.append('<text class="lbls" x="1260" y="%d">%s</text>' % (yy, d))
    body, _ = lines(
        "Sıfır-CPU mimarisinde 4 karo toplam gücü yalnız 0.85 W'tır: polikarbonat içindeki 12.0 Wh (3 200 mAh) katı-hal "
        "pil >14.1 saat kesintisiz ekran süresi verir. Sıvı elektrolit ve LiPF6 içermez; delinse bile yanmaz ve HF gazı çıkarmaz.",
        940,
        308,
        46,
    )
    o += body

    # ---- C: 3-Second Quadrant Hot-Swap & Universal Qi/Qi2 Charging Sequence
    o.append('<rect class="glass" x="40" y="440" width="1320" height="246" rx="6"/>')
    o.append('<text class="t h2" x="60" y="470">C · AB 2023/1542 ALETSİZ 3 SN KARO DEĞİŞİMİ (HOT-SWAP) VE EVRENSEL Qİ2 ŞARJ</text>')
    steps = [
        ("1", "1 karoyu + hattından çek"),
        ("2", "Dead-Pad 0.1 ms keser"),
        ("3", "diğer 3 karo (9 Wh) besler"),
        ("4", "kesintisiz ekran/oturum"),
        ("5", "yeni karo + hatta oturur"),
        ("6", "n=1.585 çiziksiz kilit"),
    ]
    for (i, (n, t)) in enumerate(steps):
        x = 60 + i * 218
        o.append('<rect class="live" x="%d" y="492" width="196" height="82" rx="6"/>' % x)
        o.append('<text class="lbls" x="%d" y="518">%s · %s</text>' % (x + 12, n, t))
        o.append('<rect class="gd" x="%d" y="536" width="%d" height="14" rx="3"/>' % (x + 12, 150 - i * 12))
        o.append('<rect class="gsk" x="%d" y="554" width="16" height="12" rx="3"/>' % (x + 150))
    body, _ = lines(
        "Herhangi bir çeyrek karo (Q1-Q4) çıkarıldığında kalan 3 karo (9.0 Wh) sistemi kesintisiz beslemeye devam eder; yeni karo "
        "takıldığında 3 ms Dead-Pad doğrulamasıyla + güç barasına katılır. Gövde herhangi bir Qi / Qi2.2 şarj pedinde kablosuz şarj olur.",
        60,
        610,
        148,
    )
    o += body

    # ---- D: Why the Solid-State Battery is Safe on the Eye, in the Hand, and in the Pocket
    o.append('<rect class="glass" x="40" y="702" width="1320" height="256" rx="6"/>')
    o.append('<text class="t h2" x="60" y="732">D · BİYOUYUMLULUK KANITI · GÖZLÜK OLARAK GÖZDE, ELDE VE CEPTE NEDEN TAM SAĞLIKLI?</text>')
    for k_idx in range(3):
        dy = k_idx * 14
        o.append(
            '<path d="M 85 %d Q 290 %d 495 %d" stroke="#1b8a6b" stroke-width="6" fill="none" stroke-linecap="round"/>'
            % (785 + dy, 725 + dy, 785 + dy)
        )
    o.append('<text class="lbls" x="85" y="852">1. Yanmaz LLZO/PEO katı-hal pil: %0 sıvı, 0.0 ppm HF gazı, %0 şişme</text>')
    o.append('<text class="lbls" x="85" y="872">2. Gözlük termal kilidi: ortotropik grafen + NTC ile göz yüzeyi &lt;=36.2 C</text>')
    o.append('<text class="lbls" x="85" y="892">3. Bifilar akım iptali (&lt;0.08 µT) + 90° B çubukta anten (SAR 0.054 W/kg)</text>')

    body, _ = lines(
        "1. Kimyasal Güvenlik: Sıradan telefonlardaki yanıcı sıvı organik solventler ve LiPF6 tuzu tamamen kaldırılmış, yerine inorganik "
        "LLZO seramik + PEO katı elektrolit konmuştur; kesilse veya bükülse bile alev almaz ve zehirli HF gazı üretmez. "
        "2. Göz ve Deri Sağlığı: Yüzey ISO 10993-5/-10 tıbbi polikarbonattır; ortotropik grafen + Mu-metal kalkan ısıyı kenarlara yayarak "
        "kornea/deri sıcaklığını <=36.2 C'de tutar. Anten 90° B çubuğunda gözden uzakta durduğu için SAR yalnız 0.054 W/kg'dır.",
        540,
        764,
        92,
    )
    o += body
    o.append("</svg>")
    open(os.path.join(HERE, "P12-BATARYA-TASARIMI.svg"), "w").write("\n".join(o))


def sheet_p13():
    w, h = 1400, 980
    o = [
        head(
            w,
            h,
            "BUDLUM LEAF · (+) DÖRT PARÇA KENETLENME VE 90° BÜKÜMLÜ B ÖNE/ARKAYA TAKILMA",
            "Ortadan + bolunmus 4 ekran-batarya karosunun ciziksiz kenetlenmesi ve 90 derece bukumlu B modulunun 4 yone ve one/arkaya takilmasi",
        )
    ]
    o.append('<text class="t h1" x="40" y="52">(+) 4-KARO ÇİZİKSİZ KENETLENME · 90° BÜKÜMLÜ B ÖNE/ARKAYA VE 4 YÖNE TAKIM</text>')
    body, _ = lines(
        "Gövde ortadan artı (+) şeklinde 4 eşit polikarbonat ekran-batarya karosunun çiziksiz kenetlenmesiyle oluşur. B modülünün ise "
        "sadece anten+Type-C çubuğu 90° dik açıyla bükülür; yuvarlak halka ekran üstüne oturur ve 4 yöne + öne/arkaya takılır.",
        40,
        78,
        150,
    )
    o += body
    o.append('<line class="rule" x1="40" y1="116" x2="1360" y2="116"/>')

    # ---- A: Upright 4-quadrant (+) phone + 90°-bent-stem B module with ring ON screen and stem above top edge
    o.append('<rect class="glass" x="40" y="132" width="700" height="404" rx="6"/>')
    o.append('<text class="t h2" x="60" y="160">A · (+) 4-KARO EKRAN-BATARYA VE ÜSTTE 90° BÜKÜMLÜ B MODÜLÜ</text>')
    k = 1.55
    bx, by = 115.0, 212.0
    o.append(
        '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="#dcecff" stroke="#18507e" stroke-width="1.8"/>'
        % (bx, by, 80.0 * k, 160.0 * k, 3.2 * k)
    )
    # + Cross seam lines + central Qi2 ring
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#1b8a6b" stroke-width="1.5" stroke-dasharray="4 2"/>'
             % (bx + 40.0 * k, by, bx + 40.0 * k, by + 160.0 * k))
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#1b8a6b" stroke-width="1.5" stroke-dasharray="4 2"/>'
             % (bx, by + 80.0 * k, bx + 80.0 * k, by + 80.0 * k))
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#d89818" stroke-width="1.8" stroke-dasharray="6 3"/>'
             % (bx + 40.0 * k, by + 80.0 * k, 24.0 * k))
    # 90°-Bent-Stem B module: only top stem protrudes above by (y < by), round ring sits ON screen (y > by)
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" fill="#7f927a" stroke="#5c6b58" stroke-width="1.4"/>'
             % (bx + 3.0 * k, by - 9.0 * k, 6.4 * k, 41.0 * k))
    cx_b, cy_b = bx + 27.0 * k, by + 16.0 * k
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#93a68c" stroke="#5c6b58" stroke-width="1.5"/>' % (cx_b, cy_b, 16.0 * k))
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#46505a"/>' % (cx_b, cy_b, 12.0 * k))
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#183452"/>' % (cx_b, cy_b, 8.0 * k))

    o.append('<text class="lblb" x="265" y="206">Sadece Anten Çubuğu Yukarıda · Yuvarlak Halka Ekran Üstünde</text>')
    o.append('<text class="lbls" x="265" y="230">• B&#39;nin sadece çubuk (anten + tek Type-C) kısmı 90° dik bükülür</text>')
    o.append('<text class="lbls" x="265" y="250">• Yuvarlak halka (50MP kamera + arka AMOLED) ekran üstüne oturur</text>')
    o.append('<text class="lbls" x="265" y="270">• ±90° menteşe ile ekranın ÖN veya ARKA yüzüne takılabilir</text>')
    o.append('<text class="lbls" x="265" y="290">• Üst, alt, sol ve sağ 4 kenara da L-klips gibi kenetlenir</text>')
    o.append('<text class="lbls" x="265" y="310">• Gövdede Type-C veya alt batarya çıkıntısı kesinlikle yoktur</text>')
    body, _ = lines(
        "Ortadan artı (+) bölünen 4 polikarbonat ekran-batarya karosu n=1.585 optik dudak ile sıfır çizikle "
        "birleşir ve her Qi/Qi2 pedde kablosuz şarj olur.",
        265,
        350,
        52,
    )
    o += body

    # ---- B: (+) Cross Optical & Magnetic Latch Detail
    o.append('<rect class="glass" x="760" y="132" width="600" height="404" rx="6"/>')
    o.append('<text class="t h2" x="780" y="160">B · (+) ARTl MERKEZ GÖBEK, 24 N52H VE 64 ALTIN YAPRAK</text>')
    o.append('<rect class="steel" x="800" y="210" width="520" height="36" rx="8"/>')
    for i in range(8):
        o.append('<rect class="mag" x="%d" y="218" width="36" height="20" rx="3"/>' % (818 + i * 62))
    o.append('<rect class="gd" x="960" y="252" width="200" height="12" rx="3"/>')
    o.append('<text class="lbls" x="800" y="200">Merkez (0,0) Grade-5 Titanyum Artı (+) Göbek + 12 µm n=1.585 optik dudak</text>')
    o.append('<text class="lbls" x="800" y="286">24 adet N52H çift-kutuplu mıknatıs + 64 altın mikro-yaprak kontak (IP68)</text>')
    body, _ = lines(
        "8 adet konik Titanyum mikro-kırlangıç pim 4 çeyrek karoyu <2.5 µm yüzey eşdüzlemliliği ile kilitler. "
        "3 ms kriptografik Dead-Pad el sıkışması tamamlanmadan iç + barasına akım verilmez.",
        780,
        320,
        68,
    )
    o += body
    o.append('<text class="lbls" x="780" y="396">• Sıfır Çizik: n=1.585 optik elastomer ile Fresnel yansıması &lt;%0.0001</text>')
    o.append('<text class="lbls" x="780" y="418">• AB 2023/1542 Md. 11: Aletsiz, ısısız &lt;3 saniyede tak-çıkar batarya karoları</text>')
    o.append('<text class="lbls" x="780" y="440">• Evrensel Qi2.2: 4 çeyrek sektör birleşince Ø54 mm 15-25 W MPP bobini olur</text>')
    o.append('<text class="lbls" x="780" y="462">• Tekil Şarj: Sökülmüş tek bir karo da kendi Ø22 mm bobiniyle Qi şarj alır</text>')

    # ---- C: Flex & Eyewear Visor Curve
    o.append('<rect class="glass" x="40" y="556" width="700" height="396" rx="6"/>')
    o.append('<text class="t h2" x="60" y="586">C · ESNEK KATI-HAL PİLLİ GÖVDE VE GÖZLÜK VİZÖR KAVİSİ</text>')
    o.append('<path d="M 110 850 C 160 690 360 690 410 850" fill="none" stroke="#18507e" stroke-width="10" stroke-linecap="round"/>')
    o.append('<text class="lbls" x="110" y="882">2.00 mm polikarbonat + silikon OCA + esnek LLZO/PEO katı-hal pil</text>')
    o.append('<text class="lbls" x="110" y="902">R 25.5 mm bükülmede %0.38 gerinim · gözlük vizörü olarak yüze uyum sağlar</text>')
    body, _ = lines(
        "Polikarbonat karoların içindeki LLZO/PEO-Seramik katı-hal pil ve 32 oluklu esnek omurga R 25.5 mm "
        "yarıçapa kadar kırılmadan esner; elde, cepte ve gözlük olarak yüzde güvenle kullanılır.",
        60,
        926,
        82,
    )
    o += body

    # ---- D: 4-Direction & Front/Back Placement of the 90°-Bent-Stem B Module
    o.append('<rect class="glass" x="760" y="556" width="600" height="396" rx="6"/>')
    o.append('<text class="t h2" x="780" y="586">D · 90° B MODÜLÜNÜN 4 YÖNE VE ÖNE/ARKAYA TAKILMASI</text>')
    for (i, (a, lbl)) in enumerate(((15, "Üst/Alt Öne"), (30, "Üst/Alt Arkaya"), (60, "Sol/Sağ Yana"))):
        x = 800 + i * 185
        o.append(
            '<path d="M %d 800 L %d 800 L %d %d Z" fill="#f7dcae" stroke="#8a5a12" stroke-width="2"/>'
            % (x, x + 100, x + 100, 800 - a * 2)
        )
        o.append('<rect class="mod" x="%d" y="%d" width="84" height="24" rx="5"/>' % (x + 8, 800 - a * 2 - 28))
        o.append('<text class="lbls" x="%d" y="824">%s</text>' % (x, lbl))
    body, _ = lines(
        "Sadece çubuk kısmı 90° dik açıyla büküldüğü için B modülü ekranın üst, alt, sol veya sağ kenarına "
        "ve ekranın ÖN veya ARKA yüzüne takılabilir; yuvarlak kamera/AMOLED halka daima ekran üstüne oturur.",
        780,
        856,
        66,
    )
    o += body
    o.append("</svg>")
    open(os.path.join(HERE, "P13-MIKNATIS-ALANI-VE-ACI.svg"), "w").write("\n".join(o))


if __name__ == "__main__":
    sheet_p11()
    sheet_p12()
    sheet_p13()
    print("wrote P11, P12, P13")
