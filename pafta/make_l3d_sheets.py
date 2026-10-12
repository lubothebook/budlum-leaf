#!/usr/bin/env python3
# BUDLUM LEAF · pafta/make_l3d_sheets.py · revision L.5.0 · 2026-10-12
# Emits P16-PORT-RAYI-PARCA-PARCA.svg:
#   1. The (+) Cross Zero-Scratch Optical & Magnetic Latch (12 um n=1.585 optical lip, central Titanium
#      Cruciform Hub, 8 micro-dovetail pins, 24 N52H magnets, 64 gold micro-leaf contacts, 3 ms Dead-Pad).
#   2. Universal Qi / Qi2.2 Wireless Charging in the Portless Body (O54 mm 4-sector MPP + 4x O22 mm coils).
#   3. The Device's ONLY USB Type-C (40W PD 3.1 + DP 2.1, IP68) inside the 90°-Bent B Stem.
# Gate: pafta/check_sheets.py -> OVER 0, COVERED 0, COLLIDE 0.

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_l3_sheets import head, lines

HERE = os.path.dirname(os.path.abspath(__file__))


def sheet_p16():
    w, h = 1400, 980
    o = [
        head(
            w,
            h,
            "BUDLUM LEAF · (+) ÇİZİKSİZ 4-KARO BARASI, Qİ2 BOBİNLERİ VE 90° B ÇUBUĞUNDA TEK TYPE-C",
            "Ortadaki (+) ciziksiz 4-karo kenetlenme barasi, portsuz govdede Qi2 kablosuz sarj ve 90 derece B cubugundaki tek Type-C",
        )
    ]
    o.append('<text class="t h1" x="40" y="52">(+) ÇİZİKSİZ 4-KARO BARASI, Qİ2 KABLOSUZ ŞARJ VE B ÇUBUĞUNDA TEK TYPE-C</text>')
    body, _ = lines(
        "Ekran gövdesinin altında veya kenarlarında kesinlikle Type-C portu ya da buton yoktur. 4 polikarbonat ekran-batarya karosu ortadaki "
        "artı (+) hattında 12 µm n=1.585 optik dudak, Titanyum Artı göbek, 24 N52H mıknatıs ve 64 altın mikro-yaprak kontakla sıfır çizikle "
        "birleşir. Gövde her Qi/Qi2 pedde kablosuz şarj olur; cihazdaki TEK USB Type-C (40W PD 3.1) 90° bükümlü B çubuğundadır.",
        40,
        80,
        148,
    )
    o += body
    o.append('<line class="rule" x1="40" y1="136" x2="1360" y2="136"/>')

    # ---- A: The section of the (+) Cross Zero-Scratch Optical & Magnetic Seam
    o.append('<rect class="glass" x="40" y="152" width="820" height="380" rx="6"/>')
    o.append('<text class="t h2" x="60" y="180">A · KESİT · (+) ORTA BİRLEŞİM HATTI (n=1.585 OPTİK DUDAK VE Ti ARTl GÖBEK)</text>')
    o.append('<rect class="steel" x="90" y="330" width="700" height="26" rx="4"/>')
    o.append('<text class="lbls" x="96" y="322">Q1 ve Q2 iç + kenarı · Grade-5 Titanyum Artı (+) göbek + 8 mikro-kırlangıç pim</text>')
    for i in range(3):
        o.append('<rect class="gd" x="%d" y="318" width="34" height="8" rx="3"/>' % (330 + i * 60))
    o.append('<text class="lbls" x="330" y="312">64 altın yaprak</text>')
    o.append('<rect class="gd" x="250" y="318" width="16" height="8" rx="3"/>')
    o.append('<text class="lbls" x="140" y="312">3 ms Dead-Pad IC</text>')
    o.append('<rect class="live" x="520" y="318" width="16" height="8" rx="2"/>')
    o.append('<text class="lbls" x="470" y="312">Ti kırlangıç pim</text>')
    o.append('<rect class="steel" x="600" y="318" width="60" height="8" rx="3"/>')
    o.append('<text class="lbls" x="590" y="312">24x N52H mıknatıs</text>')
    o.append('<rect class="gsk" x="270" y="304" width="12" height="14" rx="3"/>')
    o.append('<rect class="gsk" x="690" y="304" width="12" height="14" rx="3"/>')
    o.append('<text class="lbls" x="712" y="316">n=1.585 dudak</text>')
    o.append('<rect class="body4" x="240" y="240" width="500" height="60" rx="8"/>')
    o.append('<text class="lbls" x="250" y="234">4x (40.0 × 80.0 × 2.00 mm) polikarbonat ekran-batarya karosu (LLZO katı-hal pil)</text>')
    o.append('<text class="lbls" x="250" y="268">Corning kenar-sarımlı 0 mm çerçevesiz elektrot</text>')
    o.append('<rect class="mod" x="300" y="286" width="380" height="10" rx="3"/>')
    o.append('<text class="lbls" x="310" y="294">Ø54 mm 4-sektör Qi2.2 MPP bobini + yerel Qi PMIC</text>')
    for i in range(3):
        o.append('<rect class="gd" x="%d" y="296" width="30" height="10" rx="3"/>' % (330 + i * 60))
    o.append('<text class="lbls" x="530" y="264">16 altın yaprak / iç kenar</text>')
    o.append('<rect class="mag" x="600" y="296" width="60" height="10" rx="3"/>')
    o.append('<text class="lbls" x="530" y="282">6x N52H çift-kutuplu / kenar</text>')
    o.append('<line x1="240" y1="304" x2="740" y2="304" stroke="#8a5a12" stroke-width="1.2"/>')
    o.append('<text class="lbls" x="90" y="382">12 µm n=1.585 fenil-florosilikon optik dudak Fresnel yansımasını &lt;%0.0001 düzeyine indirir (0 çizik)</text>')
    o.append('<text class="lbls" x="90" y="402">8 konik Titanyum mikro-kırlangıç pim 4 karoyu &lt;2.5 µm Z-eşdüzlemliliği ile kilitler</text>')
    o.append('<text class="lbls" x="90" y="422">AB 2023/1542 Md. 11: Herhangi bir karo aletsiz &lt;3 saniyede sökülüp takılır (kesintisiz hot-swap)</text>')
    o.append('<text class="lbls" x="90" y="470">3 ms kriptografik el sıkışması (Dead-Pad) tamamlanmadan 64 altın yaprak kontağa akım verilmez.</text>')
    o.append('<text class="lbls" x="90" y="490">Kendi kendini onaran florosilikon optik dudak + hattını IP68 toz ve su geçirmez yapar.</text>')

    # ---- B: Single USB-C in the 90°-Bent B Stem & Universal Qi2 Wireless Charging in the Body
    o.append('<rect class="glass" x="880" y="152" width="480" height="380" rx="6"/>')
    o.append('<text class="t h2" x="900" y="180">B · 90° B ÇUBUĞUNDA TEK TYPE-C VE GÖVDEDE Qİ2</text>')
    o.append('<rect class="steel" x="920" y="214" width="150" height="46" rx="8"/>')
    o.append('<text class="lbls" x="930" y="242">TEK USB-C (B çubukta)</text>')
    o.append('<text class="lbls" x="920" y="284">90° dik bükümlü B çubuğu içinde (4.8 x 8.8 mm)</text>')
    o.append('<text class="lbls" x="920" y="302">40 W USB-PD 3.1 (20 V / 2.0 A) + DP 2.1</text>')
    o.append('<text class="lbls" x="920" y="320">kırmızı IP68 radyal silikon O-ring conta</text>')
    o.append('<rect class="steel" x="920" y="340" width="180" height="46" rx="8"/>')
    o.append('<text class="lbls" x="930" y="368">U_PD + U1..U4 (B halkada)</text>')
    o.append('<text class="lbls" x="920" y="410">4-Karo Ana TCON + UWB/60GHz mmWave SiP</text>')
    o.append('<text class="lbls" x="920" y="428">Ses DSP &amp; Codec + 3 ms Dead-Pad PMIC</text>')
    o.append('<circle class="steel" cx="1250" cy="237" r="24"/>')
    o.append('<circle cx="1250" cy="237" r="12" fill="#ffe9a8" stroke="#8a5a12" stroke-width="2"/>')
    o.append('<text class="lbls" x="1175" y="284">Gövdede Qi / Qi2.2 Şarj</text>')
    o.append('<text class="lbls" x="1175" y="302">Merkez Ø54 mm 4-sektör MPP</text>')
    o.append('<text class="lbls" x="1175" y="320">4x Ø22 mm tekil karo bobini</text>')
    o.append('<text class="lbls" x="1175" y="338">15-25 W evrensel kablosuz</text>')
    o.append('<text class="lbls" x="1175" y="356">Gövdede sıfır port / buton</text>')
    o.append('<text class="lbls" x="900" y="474">Ekran gövdesinde Type-C yoktur; sadece kablosuz şarj alır (Qi / Qi2.2).</text>')
    o.append('<text class="lbls" x="900" y="494">Cihazdaki TEK Type-C portu ve tüm aktif iletişim B kamera modülündedir.</text>')

    # ---- C: (+) Cross Bus & B-Module Surface Pad Allocation
    o.append('<rect class="glass" x="40" y="552" width="660" height="272" rx="6"/>')
    o.append('<text class="t h2" x="60" y="580">C · (+) 64 ALTIN YAPRAK VE B YÜZEY PEDLERİ DAĞILIMI</text>')
    rows = [
        ("Yaprak 1..4 / kenar", "VBAT+ ve GND (3.85 V)", "12 mΩ paralel katı-hal pil"),
        ("Yaprak 5..6 / kenar", "Qi2.2 AC bobin köprüsü", "4 sektörü Ø54 mm halkada birleştirir"),
        ("Yaprak 7..8 / kenar", "Dead-Pad + 1-Wire kripto", "3 ms ECDSA-P256 doğrulama"),
        ("Yaprak 9..14 / kenar", "MIPI DSI-2 diferansiyel", "4-Karo T-OLED sıfır-çizik senkron"),
        ("Yaprak 15..16 / kenar", "PDLC AC + 240 Hz AgNW", "gizlilik kilidi ve dokunma/kalem"),
    ]
    for (i, (k, a, b)) in enumerate(rows):
        yy = 610 + i * 26
        o.append('<text class="lblb" x="60" y="%d">%s</text>' % (yy, k))
        o.append('<text class="lbls" x="235" y="%d">%s</text>' % (yy, a))
        o.append('<text class="lbls" x="430" y="%d">%s</text>' % (yy, b))
    o.append('<text class="lbls" x="60" y="762">4 çeyrek karo birleştiğinde merkezde tam bir Ø54.0 mm Qi2.2 MPP alıcı bobini oluşur.</text>')
    o.append('<text class="lbls" x="60" y="782">Tek bir karo çıkarıldığında kendi Ø22.0 mm bobiniyle herhangi bir Qi pedde şarj olur.</text>')
    o.append('<text class="lbls" x="60" y="802">B modülü ekranın önüne veya arkasına 12 altın yüzey pedi ile kenetlenir.</text>')

    # ---- D: Gates
    o.append('<rect class="glass" x="720" y="552" width="640" height="272" rx="6"/>')
    o.append('<text class="t h2" x="740" y="580">D · KAPILAR RL-1 … RL-18 VE F-01 … F-10 (REV L.5.0)</text>')
    gates = [
        "RL-1 90° B çubuğunda TEK USB-C (10 000 çevrim, IP68)",
        "RL-2 40 W USB-PD 3.1 (B modülü üzerinden şarj/veri)",
        "RL-3 Gövdede sıfır Type-C ve sıfır fiziksel buton",
        "RL-4 Gövdede evrensel Qi / Qi2.2 (15-25 W) kablosuz şarj",
        "RL-5 4-Karo Ana TCON · RL-6 UWB/60GHz mmWave SiP",
        "RL-7 AB 2023/1542 &lt;3 sn Hot-Swap · RL-8 64 altın yaprak",
        "RL-9 12 µm n=1.585 çiziksiz + optik dudak (&lt;%0.0001 yansıma)",
        "RL-10 Merkez Grade-5 Titanyum Artı (+) göbek (&lt;2.5 µm adım)",
        "RL-11..13 24x N52H çift-kutuplu mıknatıs ve 1.5 m düşme",
        "RL-14 3 ms Dead-Pad kripto · RL-15 Göz sıcaklığı &lt;=36.2 C",
        "RL-16..18 ±90° tersinir menteşe ile öne/arkaya ve 4 yöne takım",
        "F-01..10 Yanmaz LLZO katı-hal pil (0 HF gazı, SAR 0.054 W/kg)",
    ]
    for (i, t) in enumerate(gates):
        yy = 610 + i * 18
        o.append('<text class="lbls" x="740" y="%d">%s</text>' % (yy, t))
    o.append('<text class="lbls" x="740" y="830">(+) kenetlenme barası ve 90° B modülü 10 000 tak-çıkar çevrimine dayanır.</text>')

    # ---- E: Ten assembly steps
    o.append('<rect class="glass" x="40" y="844" width="1320" height="112" rx="6"/>')
    o.append('<text class="t h2" x="60" y="872">E · (+) 4-KARO VE 90° B MODÜLÜ KENETLENME MONTAJININ ON ADIMI</text>')
    steps = [
        "1 ISO 10993 PC kabuk",
        "2 LLZO katı-hal pil",
        "3 Qi2.2 + Qi bobinler",
        "4 Mu-metal/grafen",
        "5 T-OLED + kenar sarım",
        "6 n=1.585 optik dudak",
        "7 Ti Artı (+) göbek",
        "8 64 altın yaprak",
        "9 90° B tek Type-C",
        "10 IP68 + Dead-Pad",
    ]
    for (i, t) in enumerate(steps):
        x = 58 + i * 128
        o.append('<text class="lbls" x="%d" y="902">%s</text>' % (x, t))
    o.append('<text class="lbls" x="60" y="932">&lt;15 µm optik derz görünmezliği, 3 ms Dead-Pad kesme süresi ve Qi2.2 verimi her birimde ölçülür.</text>')
    o.append("</svg>")
    open(os.path.join(HERE, "P16-PORT-RAYI-PARCA-PARCA.svg"), "w").write("\n".join(o))


if __name__ == "__main__":
    sheet_p16()
    print("wrote P16")
