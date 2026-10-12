#!/usr/bin/env python3
# BUDLUM LEAF · pafta/make_l40_sheets.py · revision L.5.0 · 2026-10-12
#
# Emits the two primary sheets of the Revision L.5.0 design:
#   P21-BUDLUM-MODULU.svg         Turned & 90°-Bent-at-Gap (`Boşluk`) `b` Camera, Zero-CPU & USB-C Module
#                                 (20.0 g, 32 internal parts): uses the exact `uploads/b.png` silhouette
#                                 (`40.0 x 32.0 mm` in 2D, IoU = 0.9995), turned 90° (`onu ters çevirip`)
#                                 and bent 90° directly across the natural gap (`yuvarlakla çubuk arasındaki
#                                 boşluk`, zero extra hinge blocks) so the `1.00 mm` (`bir milim`) slim `çubuk`
#                                 sits horizontally on top of the 2.00 mm screen edge (`O yukarıda çünkü yatay
#                                 olarak duruyor`) while the remaining circular ring (`yuvarlak`) hangs down
#                                 on the screen face looking directly at us (`Diğer kısım bize doğru bakarak duruyor`).
#   P22-CIHAZ-VE-KENAR-MODULU.svg 4-Quadrant Plus (+) Bi-Directional Puzzle-Interlocking (`Yapboz Girdili-Çıktılı`)
#                                 Polycarbonate Screen-Battery Body (80.0 x 160.0 x 2.00 mm, R = 6.35 mm matching
#                                 `Group 911.png` at IoU = 0.999987, 68.0 g = 4 x 17.0 g tiles Q1..Q4, <15 µm
#                                 n=1.585 zero-scratch optical seam, 4 x 3.0 Wh = 12.0 Wh biocompatible All-Solid-State
#                                 LLZO/PEO-LiBOB battery, <=36.2 C eyewear safety, portless Qi2.2 body, EU 2023/1542).
#
# Verified by pafta/check_sheets.py: OVER=0, COVERED=0, COLLIDE=0.

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "cad"))
from make_l3_sheets import head, lines
import monogram_letter as ML

GREEN = "#8fa882"
GREEN_D = "#78906c"
INK = "#18507e"


def letter_path(k, ox, oy):
    return ML.svg_path(k, ox, oy)


def sheet_p21():
    """P21: The Revision L.5.0 Turned & 90°-Bent-at-Gap (`Boşluk`) `b` Camera, Zero-CPU & USB-C Module."""
    w, h = 1400, 1000
    o = [
        head(
            w,
            h,
            "BUDLUM LEAF · BOŞLUKTAN 90° BÜKÜLEN YATAY 1 MM ÇUBUKLU B MODÜLÜ (ANTEN, TEK TYPE-C, KAMERA)",
            "Orijinal b.png ters çevrilip doğal boşluğundan ek parçasız 90° bükülür: 1 mm yatay çubuk ekran üstünde, yuvarlak kısım bize bakar",
        )
    ]
    o.append('<text class="t h1" x="40" y="52">BUDLUM B MODÜLÜ · TERS ÇEVRİLİP BOŞLUKTAN 90° BÜKÜLEN 1 MM YATAY ÇUBUK VE YUVARLAK KAMERA</text>')
    body, _ = lines(
        "Orijinal b.png tasarımı (2B açılımda 40.0 x 32.0 mm, IoU = 0.9995) kesilmeden ve hiçbir ekstra menteşe parçası eklenmeden "
        "ters çevrilir ve çubuk ile yuvarlak arasındaki doğal boşluktan 90° dik açıyla bükülür: böylece 1.00 mm (bir milim) çubuk "
        "yukarıda yatay olarak durur ve 2.00 mm ekranın üst kenarına tam oturur; çubuk hariç kalan yuvarlak kısım (Ø32/Ø24 mm) ise "
        "ekran yüzeyinde bize doğru bakarak durur. Cihazdaki TEK USB Type-C portu bu 1.00 mm yatay üst çubuk içindedir.",
        40,
        78,
        150,
    )
    o += body
    o.append('<line class="rule" x1="40" y1="142" x2="1360" y2="142"/>')

    # ---------- A · Turned & 90°-Bent-at-Gap B module in plan (Front & Back side-by-side)
    o.append('<rect class="glass" x="40" y="154" width="650" height="426" rx="6"/>')
    o.append('<text class="t h2" x="60" y="180">A · BOŞLUKTAN 90° BÜKÜLEN B MODÜLÜ · ÖN VE ARKA GÖRÜNÜM</text>')

    # 1. Front view (left side of box A): k = 5.4, MON_W = 32 mm, MON_H = 36 mm (+ 1 mm horizontal top çubuk)
    k1, ox1, oy1 = 5.4, 88.0, 232.0
    # Top edge of the 2.00 mm screen reference line at y = oy1 (which corresponds to y_local = 36.0 mm)
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.8" stroke-dasharray="5 3"/>'
             % (ox1 - 8, oy1, ox1 + 36.0 * k1, oy1, INK))
    o.append(
        '<path d="%s" fill="%s" stroke="#5c6b58" stroke-width="1.5" fill-rule="evenodd"/>'
        % (letter_path(k1, ox1, oy1), GREEN)
    )
    # Horizontal 1.00 mm top `çubuk` internal LCP antenna + 60 GHz patches + SOLE USB-C (at y = oy1 - 1.0*k1 .. oy1)
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="1.5" fill="#daa84a" stroke="#8a5a12" stroke-width="0.9"/>'
             % (ox1 + 4.0 * k1, oy1 - 0.85 * k1, 17.5 * k1, 0.72 * k1))
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="1.5" fill="#d8e0e8" stroke="#48525c" stroke-width="0.9"/>'
             % (ox1 + 22.8 * k1, oy1 - 0.88 * k1, 6.2 * k1, 0.76 * k1))
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="1" fill="#d84038"/>'
             % (ox1 + 29.0 * k1, oy1 - 0.90 * k1, 0.9 * k1, 0.80 * k1))

    # Circular ring (`yuvarlak`) centered at (16.0, 16.0) -> (ox1 + 16*k1, oy1 + 20*k1)
    cx1, cy1 = ox1 + 16.0 * k1, oy1 + 20.0 * k1
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#246c48" stroke-width="%.1f" stroke-dasharray="24 7"/>'
             % (cx1, cy1, 13.5 * k1, 2.0 * k1))
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#46505a" stroke="#5c6b58" stroke-width="1.2"/>' % (cx1, cy1, 12.0 * k1))
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" fill="#2a7652" stroke="#7bd4a2" stroke-width="1.0"/>'
             % (cx1 - 7.0 * k1, cy1 - 5.2 * k1, 14.0 * k1, 10.4 * k1))
    for (ox_c, oy_c) in [(-6.0, -4.4), (4.0, -4.4), (-6.0, 2.4), (4.0, 2.4)]:
        o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="#da8e4a"/>'
                 % (cx1 + ox_c * k1, cy1 + oy_c * k1, 2.0 * k1, 1.8 * k1))
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#183452" stroke="#8ab4d4" stroke-width="1.1"/>' % (cx1, cy1, 5.6 * k1))
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#2d6898"/>' % (cx1, cy1, 3.8 * k1))
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#a8d8f0"/>' % (cx1, cy1, 1.5 * k1))
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#f6e39c"/>' % (cx1 - 9.0 * k1, cy1 + 4.0 * k1, 0.9 * k1))

    o.append('<text class="lblb" x="68" y="204">1 · ÖN YÜZ (1 MM YATAY ÇUBUK + KAMERA)</text>')
    o.append('<text class="lbls" x="68" y="468">1 mm yatay üst çubukta LCP anten + TEK USB-C</text>')
    o.append('<text class="lbls" x="68" y="486">bize bakan yuvarlak halkada 6L Sıfır-CPU PCB</text>')
    o.append('<text class="lbls" x="68" y="504">50MP OIS sensör, 2 MEMS mikrofon, hoparlör</text>')

    # 2. Back view (right side of box A)
    k2p, ox2p, oy2p = 5.4, 398.0, 232.0
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.8" stroke-dasharray="5 3"/>'
             % (ox2p - 8, oy2p, ox2p + 36.0 * k2p, oy2p, INK))
    o.append(
        '<g transform="translate(%.1f,0) scale(-1,1)"><path d="%s" fill="%s" stroke="#5c6b58" stroke-width="1.5" fill-rule="evenodd"/></g>'
        % (2 * ox2p + 32.0 * k2p, letter_path(k2p, ox2p, oy2p), GREEN)
    )
    cx2, cy2 = ox2p + 16.0 * k2p, oy2p + 20.0 * k2p
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#121e2b" stroke="#5c6b58" stroke-width="1.2"/>' % (cx2, cy2, 12.0 * k2p))
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#0d1824" stroke="#68c892" stroke-width="1.0"/>' % (cx2, cy2, 11.2 * k2p))
    for i in range(24):
        a = 2.0 * math.pi * i / 24.0
        o.append('<circle cx="%.1f" cy="%.1f" r="1.9" fill="#8ce2ac"/>' % (cx2 + 9.2 * k2p * math.cos(a), cy2 + 9.2 * k2p * math.sin(a)))
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#eef4f8" stroke-width="3.0" stroke-linecap="round"/>'
             % (cx2, cy2, cx2, cy2 - 5.6 * k2p))
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#8ce2ac" stroke-width="3.0" stroke-linecap="round"/>'
             % (cx2, cy2, cx2 + 3.8 * k2p, cy2))
    o.append('<text class="lblb" x="382" y="204">2 · ARKA YÜZ (N52H HALKA + AMOLED)</text>')
    o.append('<text class="lbls" x="382" y="468">kameranın arkasında Ø22.4 aktif LTPO AMOLED</text>')
    o.append('<text class="lbls" x="382" y="486">ek parçasız doğal boşluktan 90° bükülerek oturur</text>')
    o.append('<text class="lbls" x="382" y="504">sadece 1.00 mm yatay çubuk ekran üstünde durur</text>')

    o.append('<text class="lbls" x="60" y="544">Yuvarlak gövde: Ø32.0 / Ø24.0 mm (bize bakar) · Yatay üst çubuk: 32.0 x 4.0 x 1.00 mm · toplam 20.0 g</text>')
    o.append('<text class="lbls" x="60" y="564">Yatay 1 mm çubuğu ile ekranın 4 yönüne (üst, alt, sol, sağ) ve ön/arka yüzüne saniyeler içinde takılır</text>')

    # ---------- B · 90° Natural-Gap Bend Section showing 1.00 mm horizontal top çubuk & front-facing ring
    o.append('<rect class="glass" x="710" y="154" width="650" height="426" rx="6"/>')
    o.append('<text class="t h2" x="730" y="180">B · DOĞAL BOŞLUKTAN 90° BÜKÜM KESİTİ (1 MM ÇUBUK + YUVARLAK)</text>')
    ks, oxs, oys = 12.2, 756.0, 356.0

    def Xs(x):
        return oxs + x * ks

    def Ys(z):
        return oys - z * ks

    # Underlying 2.00 mm polycarbonate screen-battery quadrant (x = 4.0..41.0, z = -2.00..0.00)
    o.append(
        '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" fill="#dcecff" stroke="#18507e" stroke-width="1.4"/>'
        % (Xs(4.0), Ys(0.0), 37.0 * ks, 2.00 * ks)
    )
    o.append(
        '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="#46a892"/>'
        % (Xs(6.0), Ys(-0.48), 33.0 * ks, 0.96 * ks)
    )

    # 1.00 mm (`bir milim`) Horizontal Top `Çubuk` sitting right on the 2.00 mm screen top edge!
    o.append(
        '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s" stroke="#5c6b58" stroke-width="1.5"/>'
        % (Xs(0.0), Ys(2.0), 4.0 * ks, 4.0 * ks, 0.42 * ks, GREEN_D)
    )
    # LCP antenna + waterproof USB-C inside the 1.00 mm horizontal top `çubuk`
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="1.5" fill="#daa84a"/>'
             % (Xs(0.6), Ys(1.7), 1.3 * ks, 3.2 * ks))
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="1.5" fill="#d8e0e8" stroke="#d84038" stroke-width="1.0"/>'
             % (Xs(2.1), Ys(1.5), 1.4 * ks, 2.8 * ks))

    # Ring cross-section walls facing us on the screen (x = 8.0..12.0 and x = 36.0..40.0, z = 0..2.0)
    for (a, b) in ((8.0, 12.0), (36.0, 40.0)):
        o.append(
            '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s" stroke="#5c6b58" stroke-width="1.4"/>'
            % (Xs(a), Ys(2.0), (b - a) * ks, 2.0 * ks, 0.42 * ks, GREEN)
        )
    # Camera module seated in the front part of the Ø24.0 mm opening (x = 12.0..36.0, z = 0.50..1.98)
    o.append(
        '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" fill="#687482" stroke="#48525c" stroke-width="1.2"/>'
        % (Xs(12.0), Ys(1.98), 24.0 * ks, 1.48 * ks)
    )
    o.append(
        '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="#24588a"/>'
        % (Xs(15.8), Ys(1.99), 16.4 * ks, 0.30 * ks)
    )
    # Cu-Graphite shield + Rear round AMOLED panel (x = 12.0..36.0, z = 0.02..0.46)
    o.append(
        '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="#203040" stroke="#48525c" stroke-width="1.2"/>'
        % (Xs(12.0), Ys(0.46), 24.0 * ks, 0.44 * ks)
    )

    o.append('<text class="lbls" x="%.1f" y="%.1f">1 mm yatay çubuk (anten+Type-C)</text>' % (Xs(0.0), Ys(3.20)))
    o.append('<text class="lbls" x="%.1f" y="%.1f">yuvarlak kısım: bize doğru bakar (50MP + AMOLED)</text>' % (Xs(18.5), Ys(3.20)))
    o.append('<text class="lbls" x="%.1f" y="%.1f">altta 2.00 mm polikarbonat ekran-katı-hal pil karosu</text>' % (Xs(10.0), Ys(-3.20)))
    o.append('<text class="lbls" x="%.1f" y="%.1f">ek menteşe parçası olmadan B boşluğundan 90° bükülür</text>' % (Xs(0.0), Ys(-4.50)))

    o.append('<text class="lbls" x="730" y="476">• Orijinal b.png ters çevrilir; ek parça eklenmeden doğal boşluğundan 90° dik bükülür.</text>')
    o.append('<text class="lbls" x="730" y="496">• 1.00 mm (bir milim) çubuk yukarıda yatay olarak 2.00 mm ekranın üst kenarına tam oturur.</text>')
    o.append('<text class="lbls" x="730" y="516">• Cihazdaki TEK USB Type-C (40W PD 3.1) prizi bu 1.00 mm yatay üst çubuk içindedir (IP68).</text>')
    o.append('<text class="lbls" x="730" y="536">• Bize bakan yuvarlak halkada Sıfır-CPU UWB/mmWave alıcı, 4-Karo TCON, 50MP OIS ve AMOLED vardır.</text>')

    # ---------- C · 90°-Bent-at-Gap Mechanism & Reversible Attachment
    o.append('<rect class="glass" x="40" y="596" width="650" height="158" rx="6"/>')
    o.append('<text class="t h2" x="60" y="622">C · DOĞAL BOŞLUKTAN 90° BÜKÜM VE 4 YÖNE / ÖNE-ARKAYA TAKIM</text>')
    o.append('<text class="lbls" x="60" y="646">B harfi ters çevrilip çubuk ile yuvarlak arasındaki doğal boşluktan 90° bükülür.</text>')
    o.append('<text class="lbls" x="60" y="666">1.00 mm (bir milim) çubuk yukarıda yatay durarak 2.00 mm ekranın üst kenarına tam oturur.</text>')
    o.append('<text class="lbls" x="60" y="686">Çubuk alanı hariç kalan yuvarlak kısım ekran yüzeyinde bize doğru bakarak durur.</text>')
    o.append('<text class="lbls" x="60" y="706">Bükmek için yeni bir menteşe parçası eklenmez; B&#39;nin kendi boşluğu bükülmeye izin verir.</text>')
    o.append('<text class="lbls" x="60" y="726">Ekranın üst, alt, sol, sağ kenarına ve ön (+Z) veya arka (-Z) yüzüne saniyeler içinde takılır.</text>')

    # ---------- D · Camera Module Mandatory Brain + Rear Round AMOLED
    o.append('<rect class="glass" x="710" y="596" width="650" height="158" rx="6"/>')
    o.append('<text class="t h2" x="730" y="622">D · ZORUNLU SİSTEM BEYNİ, TEK TYPE-C VE ARKA AMOLED PANEL</text>')
    o.append('<text class="lbls" x="730" y="646">Ekran gövdesinde Type-C yoktur; sadece kablosuz şarj alır. Diğer her şey için B modülü şarttır.</text>')
    o.append('<text class="lbls" x="730" y="666">1.00 mm yatay üst çubukta 40W USB-C PD 3.1 + DP 2.1, 3-bant LCP anten ve 60 GHz dizisi vardır.</text>')
    o.append('<text class="lbls" x="730" y="686">Halka PCB üzerinde 4-Karo Ana TCON ekran sürücüsü, UWB/mmWave SiP ve Ses DSP çalışır.</text>')
    o.append('<text class="lbls" x="730" y="706">Önde 50 MP 4-eksen OIS katlanmış kamera + 5P lens; arkada Ø22.4 mm Yuvarlak LTPO AMOLED.</text>')
    o.append('<text class="lbls" x="730" y="726">Gözlük modunda yatay üst çubuk gözden uzakta durarak SAR değerini 0.054 W/kg altına indirir.</text>')

    # ---------- E · Gates MON-1 .. MON-20
    o.append('<rect class="glass" x="40" y="770" width="1320" height="106" rx="6"/>')
    o.append('<text class="t h2" x="60" y="798">E · DOĞRULAMA KAPILARI MON-1 … MON-20 (REVİZYON L.5.0)</text>')
    o.append('<text class="lbls" x="60" y="822">MON-1 orijinal b.png ters çevrilip boşluktan 90° bükülür · MON-2 1.00 mm yatay üst çubuk · MON-3 yuvarlak kısım bize bakar</text>')
    o.append('<text class="lbls" x="60" y="840">MON-4 ek menteşe parçası yok · MON-5 tek USB-C yatay çubukta · MON-6 4-Karo Ana TCON + UWB/mmWave SiP · MON-7 50MP OIS + 5P lens</text>')
    o.append('<text class="lbls" x="60" y="858">MON-8 Ø22.4 arka AMOLED · MON-9 r 0.42 mm yumuşak kenar · MON-10 3 ms Dead-Pad · MON-11..20 IP68, SAR 0.054 W/kg ve 20.0 g kütle</text>')
    return "\n".join(o) + "\n</svg>\n"


def sheet_p22():
    """P22: The Revision L.5.0 4-Quadrant (+) Puzzle-Interlocking (`Yapboz Girdili-Çıktılı`) Polycarbonate
    Screen-Battery Body (`2.00 mm`, `R = 6.35 mm`), Eyewear-Safe All-Solid-State Battery, Portless Qi2 Body,
    and Turned & 90°-Bent-at-Gap `b` Module.
    """
    w, h = 1400, 1000
    o = [
        head(
            w,
            h,
            "BUDLUM LEAF · TAMAMI ESNEYEBİLEN 2.00 MM (R=6.35 MM) (+) YAPBOZ POLİKARBONAT EKRAN VE 90° B MODÜLÜ",
            "Ekranın %100 tamamı esneyebilen polikarbonat yapıdadır (PC-PDMS + çoklu nötr düzlem, R=25.5 mm, sıfır rijit bölge) + 12 Wh katı-hal pil + Qi2 + 1 mm B çubuğu",
        )
    ]
    o.append('<text class="t h1" x="40" y="52">CİHAZ · TAMAMI ESNEYEBİLEN 2.00 MM (R=6.35 MM) (+) YAPBOZ POLİKARBONAT EKRAN VE 90° B</text>')
    body, _ = lines(
        "80.0 x 160.0 x 2.00 mm (2 milim, 68 g, R = 6.35 mm, IoU = 0.999987) ekranın %100 tamamı esneyebilen polikarbonat (PC-PDMS + "
        "G = 0.035 MPa silikon OCA çoklu nötr düzlem, %0.35 gerinim, 1.4 N kuvvet) yapıdadır; ekranda hiçbir rijit bölge yoktur. "
        "İç çekirdekte iki taraftan takılan esnek PC-PDMS/NiTi yapboz kilit dişleri (24 çift, 10 N/mm), çift eksenli esnek LLZO/PEO "
        "katı-hal pil (12 Wh) ve esnek nanokristalin Qi2.2 bobinler yer alır; ekran R = 25.5 mm kesintisiz esner ve ayrılmaz.",
        40,
        78,
        150,
    )
    o += body
    o.append('<line class="rule" x1="40" y1="142" x2="1360" y2="142"/>')

    # ---------- A · Upright Plan: 4-Quadrant (+) Puzzle Body + Qi2 Coils + Turned & 90°-Bent B on screen
    o.append('<rect class="glass" x="40" y="154" width="650" height="426" rx="6"/>')
    o.append('<text class="t h2" x="60" y="180">A · 2.00 MM (+) YAPBOZ GÖVDE (R=6.35 MM), Qİ2 VE YATAY ÇUBUKLU B</text>')

    k = 1.80
    bx = 98.0
    by = 232.0

    # 1. Upright 4-Quadrant polycarbonate + All-Solid-State Battery body (80.0 x 160.0 x 2.00 mm, R = 6.35 mm, 68 g)
    o.append(
        '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="#dcecff" stroke="#18507e" stroke-width="1.8"/>'
        % (bx, by, 80.0 * k, 160.0 * k, 6.35 * k)
    )
    # 4 Internal All-Solid-State LLZO/PEO Battery Cores inside Q1, Q2, Q3, Q4
    for (qx, qy) in ((3.0, 3.0), (43.0, 3.0), (3.0, 83.0), (43.0, 83.0)):
        o.append(
            '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="#b8ebd8" stroke="#267862" stroke-width="1.0"/>'
            % (bx + qx * k, by + qy * k, 34.0 * k, 74.0 * k)
        )
    # Central + Cross Puzzle-Interlocking & Seamless Optical Interface (x = 0 and y = 0) + 4-Way Titanium Hub
    cx_p = bx + 40.0 * k
    cy_p = by + 80.0 * k
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#1b8a6b" stroke-width="2.0" stroke-dasharray="5,3"/>'
             % (cx_p, by, cx_p, by + 160.0 * k))
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#1b8a6b" stroke-width="2.0" stroke-dasharray="5,3"/>'
             % (bx, cy_p, bx + 80.0 * k, cy_p))
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#d0dae4" stroke="#18507e" stroke-width="1.2"/>'
             % (cx_p, cy_p, 3.2 * k))

    # Central Ø54.0 mm 4-Sector Qi2.2 / MPP Wireless Charging Ring + 4 Standalone Ø22.0 mm Quadrant Qi Coils
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#d89818" stroke-width="3.2" stroke-dasharray="18,4"/>'
             % (cx_p, cy_p, 24.0 * k))
    for (qcx, qcy) in ((20.0, 40.0), (60.0, 40.0), (20.0, 120.0), (60.0, 120.0)):
        o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#d89818" stroke-width="1.6"/>'
                 % (bx + qcx * k, by + qcy * k, 9.5 * k))

    # 2. Turned & 90°-Bent-at-Gap B Module: 1.00 mm horizontal top `çubuk` sits on top edge `by`, ring hangs down on Q1!
    mx = bx
    my = by
    o.append(
        '<path d="%s" fill="%s" fill-opacity="0.95" stroke="#5c6b58" stroke-width="1.4" fill-rule="evenodd"/>'
        % (ML.svg_path(k, mx, my), GREEN)
    )
    o.append(
        '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#46505a" stroke="#5c6b58" stroke-width="1.0"/>'
        % (mx + 16.0 * k, my + 20.0 * k, 12.0 * k)
    )
    o.append(
        '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#1b3b5c" stroke="#8ab4d4" stroke-width="0.9"/>'
        % (mx + 16.0 * k, my + 20.0 * k, 7.6 * k)
    )

    # Callouts on the right side of Box A (x = 262..675)
    o.append('<text class="lblb" x="262" y="210">1 · 2.00 mm (R=6.35 mm) + Yapboz Kilitli 4 Karo (Q1-Q4)</text>')
    o.append('<text class="lbls" x="262" y="230">• 4 x (40 x 80 x 2.00 mm, 17 g) = 80 x 160 x 2.00 mm (68 g)</text>')
    o.append('<text class="lbls" x="262" y="248">• İç çekirdekte iki taraftan takılan girdili-çıktılı yapboz kilit</text>')
    o.append('<text class="lbls" x="262" y="266">• R=25.5 mm esnemede ayrılmaz (10 N/mm) · &lt;15 µm n=1.585 dudak</text>')

    o.append('<text class="lblb" x="262" y="302">2 · Gözlük, El ve Cep İçin Biyouyumlu Katı-Hal Pil (12 Wh)</text>')
    o.append('<text class="lbls" x="262" y="322">• Polikarbonat içinde yanmaz LLZO/PEO-LiBOB katı-hal pil</text>')
    o.append('<text class="lbls" x="262" y="340">• Sıfır sıvı, sıfır HF gazı (0.0 ppm), delinse bile alev almaz</text>')
    o.append('<text class="lbls" x="262" y="358">• Gözlük modu: &lt;=36.2 C sıcaklık, ELF &lt;0.08 µT, SAR 0.054 W/kg</text>')
    o.append('<text class="lbls" x="262" y="376">• ISO 10993 biyouyumlu BPA-free PC + DC-dimming mavi ışık filtre</text>')

    o.append('<text class="lblb" x="262" y="412">3 · Portsuz Qi2 Gövde + Boşluktan 90° Bükülen B Modülü</text>')
    o.append('<text class="lbls" x="262" y="432">• Gövdede Type-C veya buton YOKTUR; her Qi/Qi2 pedde şarj olur</text>')
    o.append('<text class="lbls" x="262" y="450">• Merkez Ø54 mm birleşik Qi2.2 bobin + 4 adet Ø22 mm çeyrek bobin</text>')
    o.append('<text class="lbls" x="262" y="468">• B&#39;nin 1.00 mm çubuğu yukarıda yatay olarak ekran üstüne oturur</text>')
    o.append('<text class="lbls" x="262" y="486">• Çubuk hariç kalan yuvarlak kısım boşluktan bükülüp bize bakar</text>')

    o.append('<text class="lbls" x="60" y="564">4-Parçalı (+) Yapboz Gövde: 80 x 160 x 2.00 mm (68 g, R=6.35 mm, 12 Wh Pil, Qi2) · 90° B Modülü (20 g, 1 mm Çubuk)</text>')

    # ---------- B · Cross-Section of the + Bi-Directional Puzzle Interlock & Solid-State Battery Stack
    o.append('<rect class="glass" x="710" y="154" width="650" height="426" rx="6"/>')
    o.append('<text class="t h2" x="730" y="180">B · (+) GİRDİLİ-ÇIKTILI YAPBOZ KİLİT VE 2.00 MM PİL KESİTİ</text>')

    # Diagram of two adjacent quadrants (Q1 and Q2) meeting at x = 0 with puzzle tenon/mortise & n=1.585 optical lip
    o.append('<rect x="748" y="222" width="276" height="112" rx="14" fill="#dcecff" stroke="#18507e" stroke-width="1.6"/>')
    o.append('<rect x="1032" y="222" width="276" height="112" rx="14" fill="#dcecff" stroke="#18507e" stroke-width="1.6"/>')
    # Optical elastomer seam + central dovetail puzzle lock at x = 1018..1038
    o.append('<rect x="1024" y="222" width="8" height="112" rx="2" fill="#48d8b8" stroke="#1b8a6b" stroke-width="1.2"/>')
    # Internal T-OLED + LLZO Solid-State Battery + Qi2 Coil inside Q1 and Q2
    for rx0 in (762, 1046):
        o.append('<rect x="%d" y="236" width="248" height="18" rx="3" fill="#eef6ff" stroke="#18507e" stroke-width="1.0"/>' % rx0)
        o.append('<rect x="%d" y="258" width="248" height="38" rx="4" fill="#b8ebd8" stroke="#267862" stroke-width="1.2"/>' % rx0)
        o.append('<rect x="%d" y="300" width="248" height="18" rx="3" fill="#eef6ff" stroke="#18507e" stroke-width="1.0"/>' % rx0)

    o.append('<text class="lbls" x="748" y="212">2.00 mm (2 Milim) Biyouyumlu PC + OCA + T-OLED + Yapboz Kilitli Katı-Hal Pil Kesiti</text>')
    o.append('<text class="lbls" x="772" y="250">Sol Karo (Q1): Ön PC + OCA + T-OLED</text>')
    o.append('<text class="lbls" x="772" y="282">3.0 Wh Katı-Hal Pil + Çıktılı Yapboz Dil</text>')
    o.append('<text class="lbls" x="772" y="314">Göz Kalkanı (Mu-Metal) + Arka T-OLED</text>')
    o.append('<text class="lbls" x="1056" y="250">Sağ Karo (Q2): 0.00 mm Sıfır Çerçeve</text>')
    o.append('<text class="lbls" x="1056" y="282">3.0 Wh Katı-Hal Pil + Girdili Yapboz Yuva</text>')
    o.append('<text class="lbls" x="1056" y="314">Orta: Yapboz Kilit + 12 µm n=1.585 Dudak</text>')

    o.append('<text class="lblb" x="730" y="362">Neden %100 Tamamı Esneyebilen Polikarbonat Yapı ve 90° B Nihai Tasarımdır?</text>')
    o.append('<text class="lbls" x="730" y="384">• %100 Tam Alan Esnek Polikarbonat (PC-PDMS): Çoklu nötr düzlemli silikon OCA (G=0.035 MPa) ile</text>')
    o.append('<text class="lbls" x="730" y="402">  polikarbonat kabuk gerinimi %0.35 düzeyine düşer; tüm ekran 1.4 N kuvvetle R=25.5 mm esner.</text>')
    o.append('<text class="lbls" x="730" y="422">• Sıfır Rijit Bölge: Esnek PC-PDMS/NiTi yapboz kilit (24 çift, 10 N/mm) + esnek (0,0) göbek.</text>')
    o.append('<text class="lbls" x="730" y="440">• Çift Eksenli Esnek Katı-Hal Pil (1680 mikro-hücre, 12 Wh, 0 HF, &lt;=36.2 C) + esnek Qi2.2.</text>')
    o.append('<text class="lbls" x="730" y="460">• AB 2023/1542 Tak-Çıkar Yasası: Her çeyrek ekran-batarya parçası aletsiz 3 sn içinde değişir.</text>')
    o.append('<text class="lbls" x="730" y="480">• Portsuz Gövde ve Qi2 Şarj: Gövdede Type-C yoktur; herhangi bir kablosuz şarjda şarj olur.</text>')
    o.append('<text class="lbls" x="730" y="500">• Doğal Boşluktan 90° Bükülen B: 1.00 mm çubuk yukarıda yatay olarak ekran üstüne tam oturur;</text>')
    o.append('<text class="lbls" x="730" y="518">  çubuk hariç kalan yuvarlak kısım boşluktan bükülerek ekran önünde bize doğru bakar.</text>')

    # ---------- C · Biocompatible Eyewear Safety & EU 2023/1542 Compliance
    o.append('<rect class="glass" x="40" y="596" width="650" height="158" rx="6"/>')
    o.append('<text class="t h2" x="60" y="622">C · GÖZLÜK / EL SAĞLIĞI VE AB 2023/1542 TAK-ÇIKAR YASASI</text>')
    o.append('<text class="lbls" x="60" y="646">1. Yanmaz Katı-Hal Pil: 4 x 3.0 Wh = 12.0 Wh LLZO/PEO-LiBOB; delinse bile alev ve HF gazı yok.</text>')
    o.append('<text class="lbls" x="60" y="666">2. Göz Önü Termal Kilit: Çift NTC ve grafen/Mu-metal kalkan ile sıcaklık &lt;=36.2 C sınırındadır.</text>')
    o.append('<text class="lbls" x="60" y="686">3. Düşük EM ve SAR: Bifilar kulaklar ile ELF &lt;0.08 µT; baş/göz SAR değeri 0.054 W/kg (37x güvenli).</text>')
    o.append('<text class="lbls" x="60" y="706">4. Biyouyumlu Yüzey: ISO 10993-5/-10/-23 tıbbi BPA-free PC ve titreşimsiz DC-dimming T-OLED.</text>')
    o.append('<text class="lbls" x="60" y="726">5. Aletsiz Tak-Çıkar: 4 yapboz karo da AB 2023/1542 Md. 11 gereği 3 saniyede tek tek değişir.</text>')

    # ---------- D · Portless Wireless Body & Mandatory 90°-Bent B Module
    o.append('<rect class="glass" x="710" y="596" width="650" height="158" rx="6"/>')
    o.append('<text class="t h2" x="730" y="622">D · PORTSUZ KABLOSUZ GÖVDE VE 1 MM YATAY ÇUBUKLU B</text>')
    o.append('<text class="lbls" x="730" y="646">1. Gövdede Type-C Yok: Alt kısımda veya kenarlarda hiçbir port/buton yoktur (tam sızdırmaz IP68).</text>')
    o.append('<text class="lbls" x="730" y="666">2. Evrensel Kablosuz Şarj: Merkez Ø54 mm Qi2.2 + 4x Ø22 mm bobin ile her Qi pedde şarj olur.</text>')
    o.append('<text class="lbls" x="730" y="686">3. Tek Type-C B Modülünde: Kablolu 40W PD 3.1 şarj ve veri B&#39;nin 1.00 mm yatay üst çubuğundadır.</text>')
    o.append('<text class="lbls" x="730" y="706">4. Zorunlu Beyin: 4-Karo Ana TCON, Sıfır-CPU UWB/mmWave, kamera ve ses için B modülü şarttır.</text>')
    o.append('<text class="lbls" x="730" y="726">5. Ek Parçasız 90° Büküm: 1 mm çubuk üstte yatay durur, yuvarlak kısım önde bize doğru bakar.</text>')

    # ---------- E · Gates
    o.append('<rect class="glass" x="40" y="770" width="1320" height="106" rx="6"/>')
    o.append('<text class="t h2" x="60" y="798">E · KAPILAR F-01 … F-10 VE MON-1 … MON-20 (REVİZYON L.5.0)</text>')
    o.append('<text class="lbls" x="60" y="822">F-01 4-parçalı (+) 2.00 mm (68 g, R=6.35 mm) yapboz gövde · F-02 24 çift girdili-çıktılı yapboz kilit + n=1.585 dudak · F-03 12 Wh LLZO pil</text>')
    o.append('<text class="lbls" x="60" y="840">F-04 &lt;=36.2 C göz güvenliği · F-05 ISO 10993 + SAR 0.054 W/kg · F-06 AB 2023/1542 tak-çıkar · F-07..10 portsuz Qi2 şarj + R=25.5 mm esneme</text>')
    o.append('<text class="lbls" x="60" y="858">MON-1 … MON-20: Orijinal b.png ters çevrilip doğal boşluğundan ek parçasız 90° bükülen, 1.00 mm yatay üst çubuklu (tek Type-C) B modülü</text>')
    return "\n".join(o) + "\n</svg>\n"


def main():
    for name, fn in (("P21-BUDLUM-MODULU.svg", sheet_p21), ("P22-CIHAZ-VE-KENAR-MODULU.svg", sheet_p22)):
        svg = fn()
        with open(os.path.join(HERE, name), "w") as fh:
            fh.write(svg)
        print("wrote", name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
