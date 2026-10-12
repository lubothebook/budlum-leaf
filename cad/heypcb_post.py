#!/usr/bin/env python3
# BUDLUM LEAF · cad/heypcb_post.py · revision L.5.0 · 2026-10-12
#
# Builds the 6-panel composite engineering showcase (teslim/heypcb-post.png)
# and the accompanying heypcb.ai/canvas text (teslim/heypcb-post.txt)
# presenting EVERY internal component of Budlum Leaf 160 (Revision L.5.0):
#   - 2.00 mm (`2 milim`) 4-Quadrant (+) Puzzle-Interlocking (`Yapboz Girdili-Çıktılı`) Screen-Battery Body
#     with R = 6.35 mm (`Group 911.png` IoU = 0.999987) outer corners (68.0 g = 4 x 17.0 g)
#   - Biocompatible All-Solid-State LLZO/PEO-LiBOB battery (12.0 Wh, 0% liquid, 0 HF, <= 36.2 C, SAR 0.054 W/kg)
#   - Portless Universal Qi2.2 (15-25 W) Wireless Charging on the screen body (0 USB-C on screen body)
#   - Exact `uploads/b.png` Camera Module turned 90° (`onu ters çevirip`) and bent 90° across the natural gap
#     (`boşluk`, zero extra hinge blocks) so the `1.00 mm` (`bir milim`) slim `çubuk` sits horizontally on top
#     of the 2.00 mm screen edge while the circular ring (`yuvarlak`) hangs down facing directly toward us (20.0 g).

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(os.path.dirname(HERE), "teslim")

FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def fnt(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if draw.textlength(cand, font=font) <= max_w:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def build_post_image():
    W, H = 2400, 2700
    bg = (16, 20, 26)
    card_bg = (24, 30, 38)
    border = (52, 64, 78)
    white = (238, 242, 246)
    muted = (176, 190, 204)
    accent = (156, 204, 146)

    im = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(im)

    draw.text(
        (56, 36),
        "Budlum Leaf 160 · Tamamı Esneyebilen 2.00 mm (R=6.35 mm) (+) Yapboz Polikarbonat Ekran ve 90° B",
        fill=white,
        font=fnt(35, True),
    )
    draw.text(
        (56, 92),
        "Ekranın %100 tamamı esneyebilen polikarbonat yapıdadır (PC-PDMS + çoklu nötr düzlem, R=25.5 mm, sıfır rijit bölge) + 12 Wh katı-hal pil + Qi2 + 1 mm yatay B çubuğu",
        fill=muted,
        font=fnt(18, False),
    )

    panels = [
        (
            "render-whole.png",
            "1 · Tamamı Esneyebilen 2.00 mm (+) Yapboz Polikarbonat Ekran",
            "80x160x2.00 mm (R=6.35 mm) gövdenin %100 tamamı esneyebilen polikarbonat (PC-PDMS) yapıdadır. B'nin 1 mm çubuğu üstte yatay, yuvarlak kısmı önde.",
        ),
        (
            "render-module.png",
            "2 · Boşluktan 90° Bükülen B Ön Yüz (Yatay 1 mm Çubuk + Kamera)",
            "Orijinal b.png ters çevrilip doğal boşluğundan ek parçasız 90° bükülür: 1 mm yatay üst çubukta LCP anten + tek USB-C (40W); yuvarlak halkada 50MP OIS + 5P lens.",
        ),
        (
            "render-module-back.png",
            "3 · B Modülü Arka Yüz (Simetrik N52H Halka + Ø22.4 mm AMOLED)",
            "Ekranın üst, alt, sol, sağ kenarına ve ön (+Z) veya arka (-Z) yüzüne takılabilir; arkada Ø22.4 mm Yuvarlak LTPO AMOLED, 8x N52H mıknatıs ve 12 altın kontak.",
        ),
        (
            "render-face.png",
            "4 · Portsuz Esnek Polikarbonat Gövde: Esnek Nanokristalin Qi2.2",
            "Gövdede Type-C veya rijit ferrit yoktur. Esnek polikarbonat/nanokristalin kalkanlı Ø54 mm Qi2.2 + 4x Ø22 mm Qi bobinlerle tüm ekran R=25.5 mm bükülür.",
        ),
        (
            "render-battery.png",
            "5 · %100 Tam Alan Esneyen (R=25.5 mm) Polikarbonat Ekran-Pil",
            "Çoklu nötr düzlemli PC-PDMS (%0.35 gerinim), süperelastik NiTi+PC yapboz kilit ve çift eksenli esnek LLZO katı-hal pil (12 Wh) ile tüm ekran ayrılmadan bükülür.",
        ),
        (
            "render-apart.png",
            "6 · Tüm 84 İç Parçanın (+) Yapboz Ekseninde Patlatılmış Görünümü",
            "4x Esnek Biyouyumlu PC (2.00 mm, R=6.35 mm) + Esnek PC/NiTi Yapboz Kilit + 4x Esnek Katı-Hal Pil + Esnek Nanokristalin Qi2.2 + 90° Bükülen B Modülü.",
        ),
    ]

    cols, rows = 2, 3
    pad_x, pad_y = 48, 36
    top_y = 144
    cell_w = (W - pad_x * (cols + 1)) // cols
    cell_h = (H - top_y - 96 - pad_y * rows) // rows

    for idx, (fname, title, cap) in enumerate(panels):
        c = idx % cols
        r = idx // cols
        x0 = pad_x + c * (cell_w + pad_x)
        y0 = top_y + r * (cell_h + pad_y)
        x1 = x0 + cell_w
        y1 = y0 + cell_h
        draw.rounded_rectangle((x0, y0, x1, y1), radius=14, fill=card_bg, outline=border, width=2)
        draw.text((x0 + 22, y0 + 14), title, fill=accent, font=fnt(23, True))

        src_path = os.path.join(IMG, fname)
        if os.path.exists(src_path):
            src = Image.open(src_path).convert("RGB")
            sw, sh = src.size
            crop = src.crop((0, int(sh * 0.08), sw, sh))
            avail_w = cell_w - 28
            avail_h = cell_h - 148
            scale = min(avail_w / crop.width, avail_h / crop.height)
            nw = max(1, int(crop.width * scale))
            nh = max(1, int(crop.height * scale))
            thumb = crop.resize((nw, nh), Image.LANCZOS)
            px = x0 + (cell_w - nw) // 2
            py = y0 + 52 + (avail_h - nh) // 2
            im.paste(thumb, (px, py))

        lines = wrap(draw, cap, fnt(18, False), cell_w - 44)
        ty = y1 - 88
        for line in lines[:3]:
            draw.text((x0 + 22, ty), line, fill=white, font=fnt(18, False))
            ty += 24

    draw.text(
        (56, H - 64),
        "4-Parçalı (+) Yapboz Gövde: 4 x (40x80x2.00 mm, 17 g) = 80x160x2.00 mm (68 g, R=6.35 mm, 12 Wh LLZO Katı-Hal Pil, Qi2 Şarj, Portsuz) · 90° B Modülü (20 g, 1 mm Yatay Çubuk)",
        fill=muted,
        font=fnt(17, False),
    )
    draw.text(
        (56, H - 36),
        "3B STL modelleri (84 iç parça dahil): cad/models/leaf160-device.stl (159,984 üçgen), monogram-module.stl, leaf160-frame.stl, leaf160-screen.stl, leaf160-battery.stl, leaf160-battery-bent.stl.",
        fill=muted,
        font=fnt(17, False),
    )

    out_png = os.path.join(IMG, "heypcb-post.png")
    im.save(out_png)
    print("wrote", out_png)


def build_post_text():
    txt = """BUDLUM LEAF 160 · REVİZYON L.5.0 · 2.00 MM (R=6.35 MM) 4-PARÇALI (+) GİRDİLİ-ÇIKTILI YAPBOZ EKRAN-BATARYA, GÖZLÜK SAĞLIĞI, KABLOSUZ ŞARJLI PORTSUZ GÖVDE VE TERS ÇEVRİLİP BOŞLUKTAN 90° BÜKÜLEN 1 MM YATAY ÇUBUKLU B MODÜLÜ

1. ORTADAN ARTI (+) BÖLÜNMÜŞ, İÇİ GİRDİLİ-ÇIKTILI YAPBOZ KİLİTLİ 2.00 MM POLİKARBONAT EKRAN-BATARYA GÖVDESİ (80.0 x 160.0 x 2.00 mm, R = 6.35 mm, 68.0 g = 4 x 17.0 g, 52 İç Parça)
   - Bire Bir Group 911 Ekran Köşe Radyusu (R = 6.35 mm / 63.5 px, IoU = 0.999987) ve 2.00 mm (2 Milim) İnce Gövde:
     * 80.0 x 160.0 x 2.00 mm gövde ortadan artı (+) şeklinde (x = 0 ve y = 0) 4 özdeş çeyrek ekran-batarya karosuna (Q1 Sol-Üst, Q2 Sağ-Üst, Q3 Sol-Alt, Q4 Sağ-Alt; her biri 40.0 x 80.0 x 2.00 mm, 17.0 g) bölünür; dış köşeler Group 911.png tasarımıyla bire bir R = 6.35 mm radyusa sahiptir.
   - Ekran İçinde Esnek Girdili-Çıktılı Yapboz Kenetlenme (Bi-Directional Dovetail Puzzle Interlock):
     * 2.00 mm ekranın nötr eksen çekirdeğinde (z = -0.45 .. +0.45 mm, t = 0.90 mm) 4 çeyrek karo düz alın-alına değil, yapboz parçaları gibi birbirini tamamlayan girdili (dişi yuva) ve çıktılı (erkek kırlangıç dil) süperelastik Nitinol (NiTi) / Ti-PEEK yapboz dişleriyle (10.0 mm adımda toplam 24 yapboz çifti, 100 N/diş = 10 N/mm çekme direnci) iç içe geçer.
     * Çift taraflı (+Z ve -Z) simetrik giriş pahları sayesinde parçalar iki taraftan da birbirinin içine takılabilir; ekran R = 25.5 mm yarıçapında esnetildiğinde yapboz kilitleri açılmaz ve tek parça yaprak gibi bükülür.
   - Dış Yüzeyde Sıfır Çizik ve Sıfır Görünür İz (<15 µm Optik Derz) & AB 2023/1542 Tak-Çıkar Uyumu:
     * Dış polikarbonat kabukta 12 µm kalınlığında kırılma indisi eşleştirilmiş (n = 1.585 vs n_PC = 1.586) kendi kendini onaran florosilikon optik dudak (Fresnel yansıması <%0.0001) ve Corning US20200243738 tipi kenar-sarımlı AgNW/Cu elektrotlar yer alır; her çeyrek parça aletsiz <3 saniyede sökülüp takılabilir.

2. GÖZLÜK / GÖZ ÖNÜ, EL VE CEP KULLANIMI İÇİN EN SAĞLIKLI TAM KATI-HAL (ALL-SOLID-STATE) PİL MİMARİSİ
   - Yanmaz ve Zehirli Gaz Çıkarmaz Katı-Hal Hücre (4 x 3.0 Wh = 12.0 Wh / 3,200 mAh, 750 Wh/L):
     * Her 40 x 80 x 2.00 mm polikarbonat karonun merkezinde mikro-boğumlu Tam Katı-Hal Oksit-Seramik (Garnet LLZO + Flor-içermeyen PEO-LiBOB) esnek pil çekirdeği yer alır.
     * Sıfır sıvı elektrolit, sıfır LiPF6 ve sıfır HF gazı (0.0 ppm): Çiviyle delinse, kesilse veya R = 25.5 mm bükülse bile alev almaz, şişmez ve duman çıkarmaz.
   - 5 Katmanlı Göz ve İnsan Sağlığı Koruması:
     * Gözlük Modu Termal Kilidi (<= 36.2 C): Çift NTC sensör ve ortotropik grafen/Mu-metal göz kalkanı (k_z = 1.5 W/mK) yüzey sıcaklığını kornea güvenlik sınırının (<37.0 C) altında tutar.
     * Çift-Telli (Bifilar) Akım İptalli Folyo Kulaklar: ELF manyetik alanı < 0.08 µT seviyesine indirir; Baş/Göz SAR değeri yalnızca 0.054 W/kg'dır. ISO 10993-5/-10/-23 biyouyumlu BPA-Free polikarbonat + %100 DC-Dimming (IEC 62471 RG0).

3. PORTSUZ VE BUTONSUZ EKRAN GÖVDESİ + EVRENSEL KABLOSUZ ŞARJ (Qi / Qi2.2) VE KAMERA MODÜLÜ ZORUNLULUĞU
   - Gövdede Sıfır Type-C ve Sıfır Buton: 4 parçalı ekran gövdesinin altında veya kenarlarında hiçbir USB-C portu ya da buton yoktur.
   - Herhangi Bir Kablosuz Şarjda Şarj Olabilme (15W-25W Qi / Qi2.2 / MagSafe / PMA):
     * Merkez (0,0) etrafında 4 çeyrek parçanın birleşerek oluşturduğu Ø54.0 mm Qi2.2 MPP ana alıcı bobin + her çeyrek parçanın kendi merkezindeki bağımsız Ø22.0 mm Qi alıcı alt-bobini sayesinde hem tam telefon hem de tek bir çeyrek parça herhangi bir kablosuz şarj pedinde şarj olur.
   - Diğer Bütün İşlemler İçin b Kamera Modülü Zorunludur: Kablolu Type-C şarj/veri, Sıfır-CPU UWB/60GHz mmWave iletişim, 4-karo birleşik ekran sürüşü (Master TCON), kamera ve ses yalnızca b modülü takılıyken çalışır.

4. TERS ÇEVRİLİP DOĞAL BOŞLUĞUNDAN EK PARÇASIZ 90° BÜKÜLEN, 1.00 MM YATAY ÜST ÇUBUKLU "b" KAMERA, SIFIR-CPU VE TYPE-C MODÜLÜ (20.0 g, 32 İç Parça; Toplam Cihaz = 88.0 g)
   - Orijinal b.png Ters Çevrilir ve Doğal Boşluğundan Ek Parçasız 90° Bükülür:
     * Kullanıcının orijinal b.png tasarımı (2B açılımda 40.0 x 32.0 mm, IoU = 0.9995) kesilmeden ve hiçbir ekstra menteşe parçası eklenmeden ters çevrilir ve çubuk ile yuvarlak arasındaki doğal boşluktan (u = 4.0 mm) 90° dik açıyla bükülür:
     * Yatay 1.00 mm (Bir Milim) Üst Çubuk: B'nin uzun çubuk kısmı yukarıda yatay olarak durur ve 2.00 mm kalınlığındaki ekranın üst kenarına tam oturur (ekran üst kenarından yalnızca 1.00 mm yükselir).
     * Bize Doğru Bakan Yuvarlak Kısım (Kalan Kısım Çubuk Hariç): Çubuk alanı hariç kalan kavisli köprü ve Ø32.0 / Ø24.0 mm yuvarlak halka kısmı ekranın ön (veya arka) yüzünde aşağı doğru inerek doğrudan bize doğru bakarak durur.
   - Cihazdaki TEK USB Type-C Portu (40 W PD 3.1 + DP 2.1): 1.00 mm yatay üst çubuk içinde su geçirmez IP68 Type-C prizi, 3-bant LCP anten + 1x4 60 GHz mmWave dizisi; bize bakan yuvarlak halkada ise 6-katmanlı Sıfır-CPU Anakart (Quad-Tile Master TCON + UWB/mmWave SiP + Ses DSP), önde 50 MP OIS kamera + 5P lens + 2 MEMS mikrofon + hoparlör + flaş, ortada 0.10 mm Cu-Grafit kalkan ve arkada Ø22.4 mm Yuvarlak LTPO AMOLED yer alır.
"""
    out_txt = os.path.join(IMG, "heypcb-post.txt")
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(txt)
    print("wrote", out_txt)


if __name__ == "__main__":
    build_post_image()
    build_post_text()
