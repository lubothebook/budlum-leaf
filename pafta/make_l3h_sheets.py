#!/usr/bin/env python3
# BUDLUM LEAF · pafta/make_l3h_sheets.py · revision L.5.0 · 2026-10-12
# Emits P20-RADYO-VE-ANTENLER.svg:
#   1. Inside the 90°-Bent Stem of the `b` module: 3-Band LCP Antenna Strip (Wi-Fi 7, BT 5.4, UWB)
#      + 1x4 60 GHz mmWave Phased-Array Patch Antennas + Coaxial Feedline + Single USB-C port.
#   2. Inside the Round Ring of the `b` module (on screen): U2 UWB/60GHz mmWave Zero-CPU SiP + U1 Master TCON.
#   3. Inside the 4-Quadrant (+) Portless Body: Universal Qi2.2 (O54 mm) & 4x Qi (O22 mm) Wireless Coils
#      + Mu-metal/Graphene Ocular Shield (Head/Eye SAR = 0.054 W/kg, ELF < 0.08 uT).
# Gate: pafta/check_sheets.py -> OVER 0, COVERED 0, COLLIDE 0.

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cad"))
from make_l3_sheets import head, lines
import monogram_letter as ML

HERE = os.path.dirname(os.path.abspath(__file__))


def sheet_p20():
    w, h = 1400, 1000
    o = [
        head(
            w,
            h,
            "BUDLUM LEAF · 90° B ÇUBUĞU ANTENLERİ (LCP + 60 GHz), GÖZLÜK SAR GÜVENLİĞİ VE Qİ2 BOBİNLERİ",
            "90 derece bukumlu B cubugunda 3-bant LCP anten ve 1x4 60 GHz mmWave dizi, gozluk modunda 0.054 W/kg SAR ve govdede Qi2 sarj",
        )
    ]
    o.append('<text class="t h1" x="40" y="52">ANTEN VE Qİ2 · 90° B ÇUBUĞUNDA LCP + 60 GHz DİZİ VE GÖVDEDE Qİ2.2 BOBİNLERİ</text>')
    body, _ = lines(
        "Revizyon L.5.0'da tüm RF vericileri B modülünün 90° dik açıyla bükülmüş çubuğu içindedir (3-bant LCP Wi-Fi 7 / BT 5.4 / UWB "
        "anten + 1x4 60 GHz mmWave yama dizi). Böylece gözlük modunda anten gözden uzakta kalır ve SAR değeri 0.054 W/kg olur. Portsuz "
        "4-karo ekran gövdesinde ise Ø54 mm Qi2.2 MPP ve 4x Ø22 mm Qi kablosuz şarj bobinleri yer alır.",
        40,
        78,
        150,
    )
    o += body
    o.append('<line class="rule" x1="40" y1="136" x2="1360" y2="136"/>')

    # ---------- A: 4-Quadrant (+) body + 90°-Bent-Stem B module antenna & Qi2 map
    o.append('<rect class="glass" x="40" y="152" width="820" height="330" rx="6"/>')
    o.append('<text class="t h2" x="60" y="180">A · HARİTA · 90° B ÇUBUĞUNDA LCP + 60 GHz ANTEN VE GÖVDEDE Qİ2 BOBİNLERİ</text>')
    k = 1.35
    bx, by = 135.0, 224.0
    # Upright 80 x 160 4-quadrant (+) polycarbonate body
    o.append(
        '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="#dcecff" stroke="#18507e" stroke-width="1.8"/>'
        % (bx, by, 80.0 * k, 160.0 * k, 3.2 * k)
    )
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#1b8a6b" stroke-width="1.5" stroke-dasharray="4 2"/>'
             % (bx + 40.0 * k, by, bx + 40.0 * k, by + 160.0 * k))
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#1b8a6b" stroke-width="1.5" stroke-dasharray="4 2"/>'
             % (bx, by + 80.0 * k, bx + 80.0 * k, by + 80.0 * k))
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#d89818" stroke-width="2.0" stroke-dasharray="6 3"/>'
             % (bx + 40.0 * k, by + 80.0 * k, 24.0 * k))
    # 90°-Bent-Stem B module: stem protruding above top edge (with LCP + 60GHz patches), ring ON screen
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" fill="#7f927a" stroke="#5c6b58" stroke-width="1.4"/>'
             % (bx + 3.0 * k, by - 9.0 * k, 6.4 * k, 41.0 * k))
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="#daa84a" stroke="#8a5a12" stroke-width="1.0"/>'
             % (bx + 4.2 * k, by - 7.5 * k, 3.2 * k, 26.0 * k))
    cx_b, cy_b = bx + 27.0 * k, by + 16.0 * k
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#93a68c" stroke="#5c6b58" stroke-width="1.5"/>' % (cx_b, cy_b, 16.0 * k))
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#46505a"/>' % (cx_b, cy_b, 12.0 * k))

    o.append('<text class="lblb" x="275" y="212">1 · 90° Dik Bükümlü B Çubuğunda LCP + 1x4 60 GHz Anten</text>')
    o.append('<text class="lbls" x="275" y="234">• Sadece çubuk kısmı 90° dik bükülerek ekran kenarında yukarıda kalır</text>')
    o.append('<text class="lbls" x="275" y="254">• A1/A2/A3 3-bant LCP anten: Wi-Fi 7 (2.4/5/6 GHz), BT 5.4 ve UWB</text>')
    o.append('<text class="lbls" x="275" y="274">• ANT1..ANT4: çubuk sırtında 1x4 faz-dizili 60 GHz altın yama antenler</text>')
    o.append('<text class="lbls" x="275" y="294">• Gözlük modunda anten şakak dışında kalarak SAR&#39;ı 0.054 W/kg yapar</text>')
    o.append('<text class="lbls" x="275" y="314">• Cihazdaki TEK USB Type-C (40W PD 3.1) prizi de bu 90° çubuktadır</text>')

    o.append('<text class="lblb" x="275" y="352">2 · Yuvarlak B Halkasında U2 SiP ve Gövdede Evrensel Qi2.2 Şarj</text>')
    o.append('<text class="lbls" x="275" y="374">• Ekran üstüne oturan 6L halka PCB&#39;de U2 UWB/60GHz mmWave SiP</text>')
    o.append('<text class="lbls" x="275" y="394">• 4 karo merkezde birleşince Ø54.0 mm Qi2.2 MPP (15-25 W) bobin olur</text>')
    o.append('<text class="lbls" x="275" y="414">• Her karoda ayrıca bağımsız Ø22.0 mm Qi bobin + nanokristal EM zırh</text>')
    o.append('<text class="lbls" x="275" y="434">• B modülü 4 yöne ve ekranın önüne/arkasına takılarak hüzmeyi korur</text>')

    # ---------- B: The radiators & coils
    o.append('<rect class="glass" x="880" y="152" width="480" height="330" rx="6"/>')
    o.append('<text class="t h2" x="900" y="180">B · ANTENLER, Qİ2 BOBİNLERİ VE EM KALKAN</text>')
    rad = [
        ("90° çubuk A1 (2.4 GHz)", "25.0 mm LCP monopol · +2.4 dBi"),
        ("90° çubuk A2 (Wi-Fi 7)", "12.8 mm 5-7 GHz kol · +3.4 dBi"),
        ("90° çubuk A3 (UWB)", "9.6 mm yarık · 6.5-8.5 GHz · +2.6 dBi"),
        ("90° çubuk ANT1..4", "1x4 60 GHz altın yama · +8.2 dBi"),
        ("B halka U2 SiP", "UWB + 60 GHz mmWave 0-gecikmeli SiP"),
        ("Merkez Qi2.2 bobin", "4x 90° sektör = Ø54 mm MPP (15-25 W)"),
        ("Çeyrek Qi bobinleri", "4x Ø22 mm tekil karo şarj bobini"),
        ("Göz EM kalkanı", "Mu-metal + bifilar kulak (&lt;0.08 µT)"),
    ]
    for i, (a, b) in enumerate(rad):
        yy = 208 + i * 22
        o.append('<text class="lbls" x="900" y="%d">%s</text>' % (yy, a))
        o.append('<text class="lbls" x="1085" y="%d">%s</text>' % (yy, b))
    o.append('<text class="lbls" x="900" y="408">90° dik bükümlü B çubuğu 4 kenara ve öne/arkaya takılabildiği için</text>')
    o.append('<text class="lbls" x="900" y="428">kullanıcı tutuşuna göre en açık RF görüş açısına yerleştirilebilir.</text>')
    o.append('<text class="lbls" x="900" y="448">Baş/Göz SAR değeri 0.054 W/kg ile ICNIRP sınırının 37 kat altındadır.</text>')

    # ---------- C: Zero-CPU video link & +/-90° Hinge Coaxial Bridge
    o.append('<rect class="glass" x="40" y="496" width="820" height="192" rx="6"/>')
    o.append('<text class="t h2" x="60" y="524">C · SIFIR-CPU 60 GHz / UWB GÖRÜNTÜ AKIŞI VE ±90° KOAKSİYEL KÖPRÜ</text>')
    g1 = (
        "90° dik açıyla bükülmüş çubuk içindeki 3-bant LCP anten ve 1x4 60 GHz mmWave yama dizisi, ±90° tersinir titanyum "
        "menteşeden geçen 50 Ohm esnek LCP mikro-koaksiyel köprü ile yuvarlak halkadaki U2 alıcı-verici SiP çipine bağlanır."
    )
    body, _ = lines(g1, 60, 550, 92)
    o += body
    g2 = (
        "U2 SiP çipi aldığı sıkıştırılmamış kareleri doğrudan yanındaki U1 4-Karo Ana TCON çipine iletir; U1 ise 12 altın yüzey "
        "pedi ve + barası üzerinden 4 polikarbonat karoyu sıfır çizik ve sıfır gecikmeyle sürer."
    )
    body, _ = lines(g2, 60, 616, 92)
    o += body

    # ---------- D: Why bending and eyewear mode stay rock-stable
    o.append('<rect class="glass" x="880" y="496" width="480" height="192" rx="6"/>')
    o.append('<text class="t h2" x="900" y="524">D · GÖZLÜK MODUNDA EM VE ANTEN GÜVENLİĞİ</text>')
    d_txt = (
        "Cihaz gözlük/vizör olarak göze takıldığında, karoların içindeki çift-telli (bifilar) pil kulakları ve Mu-metal folyo "
        "manyetik alanı <0.08 µT düzeyine indirir. RF antenler ise ekran içinde değil, kenardaki 90° B çubuğunda göz küresinden "
        "42-68 mm uzakta durur; böylece göz dokusunda ısınma veya yüksek SAR oluşmaz."
    )
    body, _ = lines(d_txt, 900, 552, 52)
    o += body

    # ---------- E: B module & 4-Quadrant body radio/coil split
    o.append('<rect class="glass" x="40" y="704" width="820" height="150" rx="6"/>')
    o.append('<text class="t h2" x="60" y="732">E · 90° BÜKÜMLÜ B MODÜLÜ VE 4-KARO (+) GÖVDE PAYLAŞIMI</text>')
    cam = [
        ("90° B çubuğu (anten)", "Wi-Fi 7 (2.4/5/6 GHz), BT 5.4, UWB + 1x4 60 GHz mmWave faz-dizili yama anten"),
        ("90° B çubuğu (Type-C)", "Cihazdaki TEK USB Type-C (40W PD 3.1 + DP 2.1, IP68) + U_PD kontrolcü"),
        ("Yuvarlak B halkası", "6L Sıfır-CPU PCB: U1 4-Karo Ana TCON + U2 UWB/mmWave SiP + U3 Ses DSP"),
        ("B halka içi kamera/ses", "50 MP OIS kamera + Ø22.4 mm arka AMOLED + 2x MEMS mikrofon + hoparlör"),
        ("4-Karo (+) merkez Qi2", "4x 90° sektör birleşimiyle Ø54.0 mm Qi2.2 MPP (15-25 W) kablosuz şarj"),
        ("4-Karo (+) tekil Qi", "Her karoda bağımsız Ø22.0 mm Qi bobin + U_QI PMIC (her şarj pediyle uyumlu)"),
    ]
    for i, (a, b_txt) in enumerate(cam):
        o.append('<text class="lbls" x="60" y="%d">%s</text>' % (760 + i * 15, a))
        o.append('<text class="lbls" x="235" y="%d">%s</text>' % (760 + i * 15, b_txt))

    # ---------- F: Gates
    o.append('<rect class="glass" x="880" y="704" width="480" height="150" rx="6"/>')
    o.append('<text class="t h2" x="900" y="732">F · KAPILAR RF-9 … RF-20 VE MON-11 (REV L.5.0)</text>')
    g = [
        "MON-11: Sadece 90° B çubuğunda LCP + 60 GHz anten dizisi",
        "RF-9: A1/A2/A3 + ANT1..ANT4 VSWR (1.5:1 altı) doğrulaması",
        "RF-10: ±90° tersinir menteşede 50 Ohm LCP koaksiyel köprü",
        "RF-11: 4 yöne ve öne/arkaya takımda 360° hüzme kilidi",
        "RF-12: Gözlük modunda Baş/Göz SAR = 0.054 W/kg (&lt;2.0 W/kg)",
        "RF-16: Portsuz gövdede Qi / Qi2.2 (15-25 W) evrensel şarj",
    ]
    for i, t in enumerate(g):
        o.append('<text class="lbls" x="900" y="%d">%s</text>' % (760 + i * 16, t))

    # ---------- G: Part list
    o.append('<rect class="glass" x="40" y="868" width="1320" height="108" rx="6"/>')
    o.append('<text class="t h2" x="60" y="896">G · 21 RADYO, ANTEN, Qİ2 KABLOSUZ ŞARJ VE YÜKSEK HIZLI İLETİM PARÇASI</text>')
    p1 = "1 90° B çubuk gövdesi (r 0.55) · 2 A1 2.4 GHz LCP kol · 3 A2 5-7 GHz Wi-Fi 7 kol · 4 A3 UWB yarığı · 5 pi-eşleme ağı"
    p2 = "6 ±90° menteşe LCP koaksiyel köprü · 7-10 ANT1..ANT4 4x 60 GHz altın yama anten · 11 B halka U2 UWB/60GHz mmWave SiP"
    p3 = "12 U1 4-Karo Ana TCON · 13-16 4x 90° Qi2.2 MPP bobin sektörü (Ø54 mm) · 17-20 4x Ø22 mm Qi bobin · 21 Mu-metal/grafen EM kalkan"
    o.append('<text class="lbls" x="60" y="924">%s</text>' % p1)
    o.append('<text class="lbls" x="60" y="942">%s</text>' % p2)
    o.append('<text class="lbls" x="60" y="960">%s</text>' % p3)
    return "\n".join(o) + "\n</svg>\n"


def main():
    for name, fn in (("P20-RADYO-VE-ANTENLER.svg", sheet_p20),):
        svg = fn()
        with open(os.path.join(HERE, name), "w") as fh:
            fh.write(svg)
        print("wrote", name.split("-")[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
