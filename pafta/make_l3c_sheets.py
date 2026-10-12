#!/usr/bin/env python3
# BUDLUM LEAF · pafta/make_l3c_sheets.py · revision L.5.0 · 2026-10-12
# Emits the two part-by-part sheets of the Revision L.5.0 90°-Bent-Stem B module:
#   P14-B-MODULU-PARCA-PARCA.svg      all 32 parts exploded (90° stem with LCP antenna + ONLY USB-C port, ±90° Ti hinge, round ring)
#   P15-B-MODULU-OPTIK-VE-PANEL.svg   folded optical path inside 4.00 mm, rear round AMOLED panel, ±90° reversible front/back docking
# Gate: pafta/check_sheets.py -> OVER 0, COVERED 0, COLLIDE 0.

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_l3_sheets import head, lines

HERE = os.path.dirname(os.path.abspath(__file__))

STACK = [
    ("31", "ön safir mercek penceresi · Ø24.0 x 0.35 mm", 52),
    ("30", "ön kamera çerçevesi (mikrofon + hoparlör + flaş yuvalı)", 68),
    ("29", "çift-CCT LED flaş · halka içinde düz", 34),
    ("28", "mikro hoparlör · 9.0 x 3.2 x 2.2 mm (halka içinde)", 56),
    ("27", "çift altın MEMS mikrofon + akustik membran × 2", 48),
    ("26", "5P asferik lens dizisi (5 ayrı optik mercek)", 54),
    ("25", "katlanmış optik prizma · 7.6 x 7.6 mm", 56),
    ("24", "4-eksen OIS bakır ses-bobini aktüatörleri × 4", 58),
    ("23", "50 MP CMOS görüntü sensörü · 12.8 x 9.6 x 0.65 mm", 62),
    ("22", "6-katmanlı Halka Sıfır-CPU Anakart (Ø30.2 / Ø24.4 mm)", 66),
    ("21", "U1 4-Karo Ana TCON + U2 UWB/60GHz mmWave SiP", 60),
    ("20", "U3 Ses DSP &amp; Codec + U4 3 ms Kriptografik Dead-Pad IC", 56),
    ("19", "orta 0.15 mm Bakır-Grafit EM ve termal kalkan (%0 çakışma)", 58),
    ("18", "yuvarlak halka gövde · 32.0 x 32.0 x 4.00 mm (ekran üstünde)", 72),
    ("17", "±90° tersinir Grade-5 Titanyum boyun menteşesi (öne/arkaya)", 64),
    ("16", "90° dik açıyla bükülmüş çubuk gövde · 32.0 x 4.0 x 1.00 mm (r 0.55)", 70),
    ("15", "90° çubuk içi 3-bant LCP anten (Wi-Fi 7, BT 5.4, UWB)", 58),
    ("14", "90° çubuk üstü 1x4 60 GHz mmWave faz-dizili yama antenler", 54),
    ("13", "90° çubuk içi RF eşleme ağı ve esnek LCP koaksiyel köprü", 48),
    ("12", "90° çubuk içi TEK USB Type-C (40W PD 3.1 + DP 2.1) priz", 64),
    ("11", "Type-C kırmızı silikon IP68 sızdırmazlık O-ring contası", 52),
    ("10", "U_PD USB-PD 3.1 EPR şarj denetleyici + 2.2 µH indüktör", 54),
    ("9", "ekran yüzeyine kenetlenen simetrik N52H mıknatıs halkası × 8", 62),
    ("8", "ekran yüzeyine kenetlenen 12 altın pogo/optik yüksek hızlı ped", 58),
    ("7", "su geçirmez FKM elastomer sızdırmazlık contası · IP68", 60),
    ("6", "arka panel ara yalıtım ve EMI kalkanı", 54),
    ("5", "arka yuvarlak AMOLED sürücü ve dokunma katmanı", 60),
    ("4", "arka yuvarlak LTPO AMOLED panel · Ø22.4 mm aktif (1-120 Hz)", 64),
    ("3", "arka optik yapıştırıcı (OCA) · 25 µm", 52),
    ("2", "arka safir/polikarbonat koruyucu kapak · Ø24.0 x 0.35 mm", 62),
    ("1", "arka tersinir kenetlenme sızdırmazlık halkası · Ø24.0 mm (IP68)", 66),
]

TABLE_A = [
    ("18", "yuvarlak halka çerçeve", "Ø32/Ø24 x 4.0", "4.6 g", "±0.03 mm"),
    ("16", "90° dik bükümlü çubuk", "6.4 x 44.0 x 4.5", "2.6 g", "±0.03 mm"),
    ("17", "±90° titanyum menteşe", "1.5 x 22.0 x 4.0", "1.2 g", "±0.02 mm"),
    ("12", "TEK USB-C 40W + IP68", "4.8 x 8.8 x 3.2", "1.4 g", "±0.02 mm"),
    ("15", "LCP anten + 60GHz dizi", "31.0 x 3.2 x 0.6", "0.7 g", "±0.02 mm"),
    ("22", "6L Sıfır-CPU halka PCB", "Ø30.2/Ø24.4 x 0.6", "1.8 g", "±0.03 mm"),
    ("9", "simetrik N52H + 12 pin", "Ø27.2 halka dizi", "2.4 g", "±0.02 mm"),
    ("28", "mikrofon × 2 + hoparlör", "9.0 x 3.2 x 2.2", "0.9 g", "±0.03 mm"),
]

TABLE_B = [
    ("30", "ön kamera çerçevesi", "Ø24.0 x 2.90", "1.4 g", "±0.02 mm"),
    ("31", "ön safir pencere", "Ø24.0 x 0.35", "0.5 g", "±0.02 mm"),
    ("25", "katlanmış optik prizma", "7.6 x 7.6 x 0.8", "0.6 g", "±5 ark sn"),
    ("26", "5P asferik lens dizisi", "Ø12.0 x 2.0 mm", "1.3 g", "±2 µm"),
    ("23", "50 MP CMOS sensör", "12.8 x 9.6 x 0.65", "0.9 g", "±0.02 mm"),
    ("24", "4-eksen OIS bobinleri", "4 x (2.2 x 1.8)", "0.7 g", "±0.02 mm"),
    ("4", "arka yuvarlak AMOLED", "Ø22.4 aktif (250 ppi)", "0.6 g", "±0.03 mm"),
    ("19", "0.15 mm Cu-Grafit kalkan", "Ø23.2 x 0.15", "0.3 g", "±0.01 mm"),
    ("1", "arka safir + IP68 conta", "Ø24.0 IP68 takım", "0.3 g", "±0.02 mm"),
]

STEPS = [
    "1 90° L-çubuk + halka gövde",
    "2 ±90° titanyum menteşe",
    "3 çubuk içi TEK USB-C priz",
    "4 3-bant LCP + 60GHz anten",
    "5 6L Sıfır-CPU halka PCB",
    "6 4-Karo TCON + UWB SiP",
    "7 50MP sensör + 4 OIS bobin",
    "8 katlanmış prizma + 5P lens",
    "9 0.15 mm Cu-Grafit kalkan",
    "10 Ø22.4 arka LTPO AMOLED",
    "11 simetrik N52H + 12 pin",
    "12 öne/arkaya takılma testi",
]


def sheet_p14():
    w, h = 1400, 980
    o = [
        head(
            w,
            h,
            "BUDLUM LEAF · 90° BÜKÜMLÜ B MODÜLÜ PARÇA PARÇA (31 GRUP, 22.0 G)",
            "Sadece çubuğu 90° dik bükülen, yuvarlağı ekran üstüne oturan, tek Type-C portlu B modülünün tüm iç parçaları",
        )
    ]
    o.append('<text class="t h1" x="40" y="52">B MODÜLÜ (REV L.5.0) · 90° BÜKÜMLÜ ÇUBUK, TEK TYPE-C VE KAMERA PARÇALARI</text>')
    body, _ = lines(
        "Revizyon L.5.0 B modülünde sadece soldaki çubuk (anten) kısmı ±90° tersinir titanyum menteşe ile 90° dik açıyla "
        "bükülür ve ekran kenarında/yukarısında dik kalır; kalan yuvarlak halka (32 x 32 x 4.00 mm) doğrudan ekranın "
        "üzerine oturur. Cihazdaki TEK USB Type-C portu 90° çubuk içindedir; modül ekranın önüne/arkasına ve 4 yönüne takılır.",
        40,
        78,
        155,
    )
    o += body
    o.append('<line class="rule" x1="40" y1="136" x2="1360" y2="136"/>')

    # ---- A: Exploded stack
    o.append('<rect class="glass" x="40" y="152" width="640" height="676" rx="6"/>')
    o.append('<text class="t h2" x="60" y="180">A · SIRALI PATLATMA · ÖN KAMERADAN 90° ÇUBUĞA VE ARKA PANELE</text>')
    y0, pitch, cx = 208, 19.0, 195
    for (i, (num, name, bw)) in enumerate(STACK):
        yy = y0 + i * pitch
        cls = "steel" if num in ("18", "16", "17", "12", "9") else "body4"
        if num in ("15", "14", "8", "29"):
            cls = "gd"
        if num in ("22", "21", "4", "5"):
            cls = "mod"
        o.append('<rect class="%s" x="%.1f" y="%.1f" width="%d" height="9" rx="2"/>' % (cls, cx - bw / 2.0, yy - 7, bw))
        o.append('<text class="lbls" x="64" y="%.1f">%s</text>' % (yy, num))
        o.append('<text class="lbls" x="242" y="%.1f">%s</text>' % (yy, name))
    o.append('<line x1="60" y1="%d" x2="660" y2="%d" stroke="#d5d5cf" stroke-width="1.2"/>' % (y0 + len(STACK) * pitch + 4, y0 + len(STACK) * pitch + 4))
    o.append('<text class="lbls" x="60" y="%d">Yuvarlak halka ekran üstünde (4.00 mm) · Sadece 90° anten+Type-C çubuğu yukarıda dik</text>' % (y0 + len(STACK) * pitch + 18))

    # ---- B: 90° Bent Stem, Hinge, Single USB-C & Zero-CPU Ring PCB
    o.append('<rect class="glass" x="700" y="152" width="660" height="330" rx="6"/>')
    o.append('<text class="t h2" x="720" y="180">B · 90° BÜKÜMLÜ ÇUBUK, TEK TYPE-C VE SIFIR-CPU HALKA · 15.6 g</text>')
    for (i, (num, name, size, mass, tol)) in enumerate(TABLE_A):
        yy = 206 + i * 30
        o.append('<text class="lbls" x="720" y="%d">%s</text>' % (yy, num))
        o.append('<text class="lbls" x="752" y="%d">%s</text>' % (yy, name))
        o.append('<text class="lbls" x="960" y="%d">%s</text>' % (yy, size))
        o.append('<text class="lbls" x="1140" y="%d">%s</text>' % (yy, mass))
        o.append('<text class="lbls" x="1230" y="%d">%s</text>' % (yy, tol))
    o.append('<text class="lbls" x="720" y="466">±90° tersinir titanyum menteşe ile B modülü ekranın önüne/arkasına ve 4 yönüne takılır.</text>')

    # ---- C: Front camera, Cu-Graphite shield & rear round AMOLED panel parts
    o.append('<rect class="glass" x="700" y="498" width="660" height="330" rx="6"/>')
    o.append('<text class="t h2" x="720" y="526">C · ÖN 50MP OIS KAMERA, KALKAN VE ARKA AMOLED · 6.4 g</text>')
    for (i, (num, name, size, mass, tol)) in enumerate(TABLE_B):
        yy = 552 + i * 28
        o.append('<text class="lbls" x="720" y="%d">%s</text>' % (yy, num))
        o.append('<text class="lbls" x="752" y="%d">%s</text>' % (yy, name))
        o.append('<text class="lbls" x="960" y="%d">%s</text>' % (yy, size))
        o.append('<text class="lbls" x="1140" y="%d">%s</text>' % (yy, mass))
        o.append('<text class="lbls" x="1230" y="%d">%s</text>' % (yy, tol))
    o.append('<line x1="720" y1="802" x2="1340" y2="802" stroke="#d5d5cf" stroke-width="1.2"/>')
    o.append('<text class="lbls" x="720" y="820">Toplam kütle: 15.6 g + 6.4 g = 20.0 g · Cihazdaki tek Type-C ve tüm aktif beyin buradadır.</text>')

    # ---- D: Assembly steps
    o.append('<rect class="glass" x="40" y="844" width="1320" height="112" rx="6"/>')
    o.append('<text class="t h2" x="60" y="872">D · MONTAJ SIRASI · 12 ADIM VE DOĞRULAMA</text>')
    for (i, t) in enumerate(STEPS):
        x = 60 + (i % 6) * 218
        yy = 896 + (i // 6) * 24
        o.append('<text class="lbls" x="%d" y="%d">%s</text>' % (x, yy, t))
    o.append('<text class="lbls" x="60" y="946">Kritik muayene: 90° L-çubuk menteşe kilidi, tek USB-C IP68 sızdırmazlığı ve %0 Z-çakışması.</text>')
    o.append("</svg>")
    open(os.path.join(HERE, "P14-B-MODULU-PARCA-PARCA.svg"), "w").write("\n".join(o))


def sheet_p15():
    w, h = 1400, 980
    o = [
        head(
            w,
            h,
            "BUDLUM LEAF · 90° BÜKÜMLÜ B MODÜLÜ OPTİK YOL, ARKA PANEL VE ÖNE/ARKAYA TAKILMA",
            "Yuvarlak kısım ekran üstünde (50MP OIS + Ø22.4 mm AMOLED), sadece 90° bükümlü çubuk (anten + tek Type-C) yukarıda",
        )
    ]
    o.append('<text class="t h1" x="40" y="52">B MODÜLÜ · EKRAN ÜSTÜNDE YUVARLAK KAMERA/PANEL VE 90° BÜKÜMLÜ ÇUBUK</text>')
    body, _ = lines(
        "B modülünün yuvarlak halkası (Ø32.0 mm dış, Ø24.0 mm iç açıklık) doğrudan ekranın üzerine oturur; sadece soldaki "
        "anten + Type-C çubuğu 90° dik açıyla bükülerek ekran kenarında/yukarısında dik kalır. Böylece modül ekranın 4 "
        "yönüne ve ÖN veya ARKA yüzüne takılabilir.",
        40,
        78,
        152,
    )
    o += body
    o.append('<line class="rule" x1="40" y1="136" x2="1360" y2="136"/>')

    # ---- A: Rear round AMOLED panel & 90° Bent Stem
    o.append('<rect class="glass" x="40" y="152" width="660" height="430" rx="6"/>')
    o.append('<text class="t h2" x="60" y="180">A · ARKA YUVARLAK AMOLED VE 90° DİK BÜKÜMLÜ ÇUBUK</text>')
    cx, cy = 220.0, 345.0
    o.append('<circle cx="%.1f" cy="%.1f" r="128" fill="#93a68c" stroke="#5c6b58" stroke-width="1.6"/>' % (cx, cy))
    o.append('<circle cx="%.1f" cy="%.1f" r="96" fill="#121e2b" stroke="#5c6b58" stroke-width="1.4"/>' % (cx, cy))
    o.append('<circle cx="%.1f" cy="%.1f" r="89" fill="#0d1824" stroke="#68c892" stroke-width="1.2"/>' % (cx, cy))
    for i in range(24):
        a = 2.0 * math.pi * i / 24.0
        o.append('<circle cx="%.1f" cy="%.1f" r="2.5" fill="#8ce2ac"/>' % (cx + 74.0 * math.cos(a), cy + 74.0 * math.sin(a)))
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#eef4f8" stroke-width="3.6" stroke-linecap="round"/>' % (cx, cy, cx, cy - 46.0))
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#8ce2ac" stroke-width="3.6" stroke-linecap="round"/>' % (cx, cy, cx + 32.0, cy))
    o.append('<text class="lblb" x="372" y="220">Yuvarlak AMOLED Panel (Ø22.4 mm)</text>')
    o.append('<text class="lbls" x="372" y="244">• Ekran yüzeyinin üstüne paralel oturur</text>')
    o.append('<text class="lbls" x="372" y="264">• 1-120 Hz LTPO · 220 x 220 px · 600 nit</text>')
    o.append('<text class="lbls" x="372" y="284">• Saat, kronometre, bildirim ve vizör</text>')
    o.append('<text class="lbls" x="372" y="304">• Önde 50MP OIS ile Cu-Grafit kalkanla ayrılır</text>')
    o.append('<text class="lbls" x="372" y="324">• Simetrik N52H halka ile öne/arkaya takılır</text>')
    o.append('<text class="lblb" x="372" y="364">90° Dik Bükümlü Çubuk (Anten + Type-C)</text>')
    o.append('<text class="lbls" x="372" y="388">• Sadece çubuk kısmı 90° dik açıyla bükülür</text>')
    o.append('<text class="lbls" x="372" y="408">• 3-bant LCP anten + 60 GHz mmWave dizisi</text>')
    o.append('<text class="lbls" x="372" y="428">• Cihazdaki TEK USB Type-C (40W PD 3.1) priz</text>')
    o.append('<text class="lbls" x="372" y="448">• ±90° menteşe ile 4 yöne ve öne/arkaya takılır</text>')
    o.append('<text class="lbls" x="60" y="516">Ekran gövdesinde Type-C yoktur; kablolu şarj ve tüm aktif iletişim B modülündedir.</text>')
    o.append('<text class="lbls" x="60" y="538">Gözlük modunda 90° anten çubuğu gözden uzakta kalarak SAR değerini 0.054 W/kg yapar.</text>')

    # ---- B: Folded optical path inside 4.00 mm
    o.append('<rect class="glass" x="720" y="152" width="640" height="430" rx="6"/>')
    o.append('<text class="t h2" x="740" y="180">B · 4.00 MM İÇİNDE KATLANMIŞ OPTİK YOL VE Z-İSTİFİ</text>')
    o.append('<text class="lbls" x="740" y="212">ön safir pencere (z = 4.00 mm) · 84° görüş açısı</text>')
    o.append('<line x1="800" y1="228" x2="800" y2="300" stroke="#18507e" stroke-width="2.4"/>')
    o.append('<rect class="mod" x="782" y="300" width="36" height="26" rx="4"/>')
    o.append('<text class="lbls" x="826" y="318">G1 · asferik giriş mercekleri</text>')
    o.append('<text class="lbls" x="740" y="264">3.40 mm dikey</text>')
    o.append('<path d="M 800 326 L 800 372 L 700 372 L 700 470" fill="none" stroke="#18507e" stroke-width="2.4"/>')
    o.append('<path d="M 786 372 L 814 372 L 800 348 Z" class="steel"/>')
    o.append('<text class="lbls" x="820" y="356">45° katlama prizması</text>')
    o.append('<text class="lbls" x="806" y="410">14.0 mm yatay yol (halka içinde)</text>')
    o.append('<rect class="mod" x="682" y="412" width="36" height="24" rx="4"/>')
    o.append('<text class="lbls" x="740" y="430">5P asferik lens grubu</text>')
    o.append('<rect class="mod" x="682" y="440" width="36" height="20" rx="4"/>')
    o.append('<text class="lbls" x="740" y="456">4-eksen OIS bakır bobin aktüatörleri</text>')
    o.append('<rect class="steel" x="680" y="466" width="40" height="14" rx="3"/>')
    o.append('<text class="lbls" x="740" y="478">0.15 mm Cu-Grafit EM/termal kalkan</text>')
    o.append('<rect class="dead" x="676" y="486" width="48" height="18" rx="3"/>')
    o.append('<text class="lbls" x="740" y="500">50 MP CMOS sensör (12.8 x 9.6 mm) + 6L PCB</text>')
    o.append('<text class="lbls" x="740" y="530">Yuvarlak halka ekranın üstüne oturur; sadece 90° çubuk yukarıda kalır.</text>')
    o.append('<text class="lbls" x="740" y="550">Arka yarıda (z = 0.00..0.85 mm) Ø22.4 mm Yuvarlak LTPO AMOLED çalışır.</text>')

    # ---- C: Timing, light and power
    o.append('<rect class="glass" x="40" y="600" width="660" height="272" rx="6"/>')
    o.append('<text class="t h2" x="60" y="628">C · 90° ÇUBUK, KAMERA VE SİSTEM BEYNİ ÖZETİ</text>')
    rows = [
        ("90° dik çubuk", "Sadece anten + TEK Type-C (40W) yukarıda/kenarda dik"),
        ("yuvarlak halka", "32x32x4 mm · doğrudan ekranın üzerine paralel oturur"),
        ("öne/arkaya takım", "±90° titanyum menteşe ile ön/arka ve 4 yöne takılır"),
        ("sistem beyni", "4-Karo Ana TCON + Sıfır-CPU UWB/60GHz mmWave SiP"),
        ("halka içi ses", "2 x MEMS mikrofon + 9.0 x 3.2 mm hoparlör + flaş"),
        ("toplam kütle", "20.0 g · r 0.55 mm yumuşak kenar · IP68 su geçirmez"),
    ]
    for (i, (k, v)) in enumerate(rows):
        yy = 656 + i * 26
        o.append('<text class="lblb" x="60" y="%d">%s</text>' % (yy, k))
        o.append('<text class="lbls" x="230" y="%d">%s</text>' % (yy, v))
    body, _ = lines(
        "B modülü olmadan ekran sadece kablosuz şarj alır; diğer her şey için B şarttır.",
        60,
        826,
        74,
    )
    o += body

    # ---- D: Gates MON-1 .. MON-20
    o.append('<rect class="glass" x="720" y="600" width="640" height="272" rx="6"/>')
    o.append('<text class="t h2" x="740" y="628">D · KAPILAR MON-1 … MON-20 (REV L.5.0)</text>')
    gates = [
        ("MON-1..2", "Sadece çubuğu 90° dik bükülen, yuvarlağı ekran üstünde B"),
        ("MON-3..4", "Önde 50MP OIS kamera, arkada Ø22.4 mm AMOLED panel"),
        ("MON-5", "±90° menteşe ile ekranın önüne/arkasına ve 4 yönüne takım"),
        ("MON-6..8", "Cihazdaki TEK USB-C (40W) 90° bükümlü çubuk içinde"),
        ("MON-9", "B'nin tüm 90° kenarları r 0.55 mm yumuşatılmış"),
        ("MON-10..12", "4-Karo Ana TCON, UWB/mmWave SiP, 3 ms Dead-Pad, IP68"),
        ("MON-13..20", "Gözlük modunda SAR 0.054 W/kg ve 50.000 çevrim menteşe"),
    ]
    for (i, (k, v)) in enumerate(gates):
        yy = 656 + i * 26
        o.append('<text class="lblb" x="740" y="%d">%s</text>' % (yy, k))
        o.append('<text class="lbls" x="860" y="%d">%s</text>' % (yy, v))
    o.append('<text class="lbls" x="740" y="850">Kamera dönmez; modülün kendisi ±90° menteşeyle öne veya arkaya takılır.</text>')
    o.append("</svg>")
    open(os.path.join(HERE, "P15-B-MODULU-OPTIK-VE-PANEL.svg"), "w").write("\n".join(o))


if __name__ == "__main__":
    sheet_p14()
    sheet_p15()
    print("wrote P14, P15")
