# BUDLUM LEAF · CANLI ARENA API SÜREKLİ TAM SİSTEM DENETİMİ, YORUMLAMASI VE KULLANIM HATASI BULMA RAPORU (14:21 – 15:21)

**Çalışma Aralığı:** `2026-10-12 14:24 – 15:21:08 Europe/Istanbul (+03)`
**Yönetici Modu:** Sadece Orkestrasyon (Bu rapordaki tüm inceleme, yorumlama ve kullanım hatası tespitleri doğrudan Arena API üzerindeki **`claude-opus-5-5`**, **`gpt-6-sol`** ve **`claude-sonnet-5-5`** modelleri tarafından üretilmiştir).
**Toplam Üretilen Denetim Hacmi:** `14` uzman ajan raporu, toplam **`376,464` karakter** (`~62,744` kelime).

## ÇALIŞTIRILAN AJANLAR ÖZET TABLOSU

| Dalga | Ajan ID | Model | Router | Başlangıç (TSİ) | Bitiş (TSİ) | Süre (sn) | Karakter |
|---|---|---|---|---|---|---:|---:|
| `WAVE_01` | `W1_A2_OPUS_CAD_LEAF_V2_ASSEMBLY` | **`claude-opus-5-5`** | `coding-router-preview` | `2026-10-12 14:26:27 +03` | `2026-10-12 14:31:50 +03` | `323.28` | `25,270` |
| `WAVE_01` | `W1_A1_OPUS_CAD_MONOGRAM_AND_GEOM` | **`claude-opus-5-5`** | `claude-coding-router-preview` | `2026-10-12 14:26:25 +03` | `2026-10-12 14:36:01 +03` | `576.29` | `23,634` |
| `WAVE_02` | `W2_A3_GPT6_OPTICAL_SEAM_AND_TOUCH_AUDIT` | **`gpt-6-sol`** | `coding-router-preview` | `2026-10-12 14:36:06 +03` | `2026-10-12 14:41:38 +03` | `332.42` | `1,382` |
| `WAVE_02` | `W2_A1_OPUS_POLYCARBONATE_MECHANICS_AUDIT` | **`claude-opus-5-5`** | `exo` | `2026-10-12 14:36:01 +03` | `2026-10-12 14:42:29 +03` | `387.81` | `28,556` |
| `WAVE_02` | `W2_A2_OPUS_PUZZLE_SEAM_USAGE_FAILURES` | **`claude-opus-5-5`** | `claude-coding-router-preview` | `2026-10-12 14:36:03 +03` | `2026-10-12 14:44:18 +03` | `494.63` | `31,542` |
| `WAVE_03` | `W3_A1_OPUS_SOLID_STATE_BATTERY_AUDIT` | **`claude-opus-5-5`** | `claude-coding-router-preview` | `2026-10-12 14:44:18 +03` | `2026-10-12 14:49:55 +03` | `336.69` | `28,597` |
| `WAVE_03` | `W3_A2_OPUS_QI22_AND_EDDY_CURRENT_AUDIT` | **`claude-opus-5-5`** | `coding-router-preview` | `2026-10-12 14:44:21 +03` | `2026-10-12 14:54:51 +03` | `629.88` | `28,027` |
| `WAVE_04` | `W4_A3_SONNET_DOCK_AND_MODELS_AUDIT` | **`claude-sonnet-5-5`** | `coding-router-preview` | `2026-10-12 14:56:49 +03` | `2026-10-12 15:04:04 +03` | `434.9` | `25,935` |
| `WAVE_04` | `W4_A1_OPUS_B_MODULE_PACKAGING_AND_USBC` | **`claude-opus-5-5`** | `claude-coding-router-preview` | `2026-10-12 14:56:44 +03` | `2026-10-12 15:04:12 +03` | `448.21` | `23,177` |
| `WAVE_04` | `W4_A2_OPUS_CAMERA_OPTICS_AND_THERMAL_AUDIT` | **`claude-opus-5-5`** | `coding-router-preview` | `2026-10-12 14:56:47 +03` | `2026-10-12 15:04:12 +03` | `445.71` | `23,555` |
| `WAVE_05` | `W5_A3_SONNET_PAFTA_AND_MASTER_AUDIT` | **`claude-sonnet-5-5`** | `coding-router-preview` | `2026-10-12 15:04:17 +03` | `2026-10-12 15:10:50 +03` | `392.32` | `25,785` |
| `WAVE_05` | `W5_A1_OPUS_ZERO_CPU_NETWORK_AND_LATENCY_AUDIT` | **`claude-opus-5-5`** | `exo` | `2026-10-12 15:04:12 +03` | `2026-10-12 15:11:09 +03` | `416.54` | `37,239` |
| `WAVE_05` | `W5_A2_OPUS_FINAL_DIRECTIVE_CONSISTENCY_AUDIT` | **`claude-opus-5-5`** | `claude-coding-router-preview` | `2026-10-12 15:04:15 +03` | `2026-10-12 15:11:16 +03` | `420.92` | `28,474` |
| `WAVE_06` | `W6_A1_OPUS_CHIEF_RED_TEAM_SYNTHESIS` | **`claude-opus-5-5`** | `claude-coding-router-preview` | `2026-10-12 15:11:16 +03` | `2026-10-12 15:21:08 +03` | `591.99` | `45,291` |

---

## DALGA 1 · 3B CAD VE GEOMETRİ KODU DENETİMİ (`cad/monogram_letter.py`, `cad/leaf_geom.py`, `cad/leaf_v2.py`, `cad/render3d.py`)

### W1_A2_OPUS_CAD_LEAF_V2_ASSEMBLY · Model: `claude-opus-5-5` (Router: `coding-router-preview`, Başlangıç: `2026-10-12 14:26:27 +03`, Bitiş: `2026-10-12 14:31:50 +03`, Süre: `323.28 sn`, Uzunluk: `25,270` karakter)

# BUDLUM LEAF L.5.0: 3B Montaj, Tolerans ve Çarpışma Denetimi

**Hedef dosyalar:** `cad/leaf_v2.py` (L.5.0) ve `cad/render3d.py` (L.4.1)

---

## 0. Kapsam sınırı

Önce şunu bilmeniz gerekiyor: gönderdiğiniz iki dosyanın da orta kısmı kesilmiş. Şunlar elimde yok:

- `monogram_parts`, `quad_plus_body_parts`, `bent_quad_plus_parts` ve `place_parts` fonksiyonlarının gövdeleri,
- `mod_dx / mod_dy / mod_dz` değerleri,
- `leaf_geom.py` ve `monogram_letter.py` (`MON_W`, `MON_H`, `STEM_*`, `RING_*` sabitleri ve çizgi fonksiyonları).

Bu yüzden **52 iç parçayı tek tek kontrol edemiyorum.** Koordinatlar elimde değil, uydurursam denetim geçersiz olur. Yapabildiklerim şunlar:

1. Sizin verdiğiniz sayısal aralıkları (Z bantları, USB-C kutusu) tam olarak doğruluyorum.
2. Görünen kodda ve docstring'de ölçüyle kanıtlanabilen hataları gösteriyorum.
3. Kesik kısımdaki 52 parça için çalıştırabileceğiniz bir çarpışma testi veriyorum (§6).

Bulguları üç sınıfta işaretledim: **[KESİN]** sayıyla kanıtlı, **[KOŞULLU]** gizli koda bağlı, **[DOĞRULANMALI]**.

---

## 1. USB Type-C: `box_part(26.4, 36.48, 6.2, 0.62, 0.20, -1.65, 0.38)`

### 1.1 Parametreler

`box_part(cx, cy, w, h, r, z0, z1)` imzasına göre kutu şöyle:

| Eksen | Model | Gerçek USB-C dişi (receptacle) | Oran |
|---|---|---|---|
| X (genişlik `w`) | **6.20 mm** | Fiş girişi iç ölçüsü ≈ 8.34 mm, dış kabuk ≈ 8.9 mm | %74 (2.1 mm eksik) |
| Y (`h`) | **0.62 mm** | İç yükseklik ≈ 2.56 mm, dış kabuk ≈ 3.1–3.3 mm | %24 |
| Z (`z1 − z0`) | **2.03 mm** | Takma derinliği ≈ 6.2–7.4 mm | %27–33 |
| Hacim | 6.2 × 0.62 × 2.03 ≈ **7.8 mm³** | ≈ 8.9 × 3.2 × 7.0 ≈ **200 mm³** | yaklaşık 1/25 |

Fonksiyonun ara değerleri: `r_c = max(0.04, min(0.20, 0.62×0.45 = 0.279)) = 0.20`, `b_c = min(0.08, 2.03×0.42, 0.20×0.8) = 0.08`. Geometri hatasız üretiliyor ama ölçüler yanlış.

**Muhtemel eksen karışıklığı [KOŞULLU]:** 6.2 mm, USB-C'nin tipik takma derinliğine çok yakın. 0.62 mm de dil (tongue) kalınlığına (≈0.70 mm) yakın. Büyük olasılıkla modellenen şey konnektörün kendisi değil, **içindeki dil**, ve derinlik ile genişlik eksenleri karışmış. Dış kabuk, tutma yayları, SMT/THT bacakları ve fişin girdiği boşluk hiç modellenmemiş.

### 1.2 1.00 mm çubuğa sığıyor mu? Hayır, iki yönde de sığmıyor [KESİN]

Docstring'e göre çubuk ekranın 2.00 mm'lik kenarının üstünde, y = +80.0 … +81.0 mm aralığında duruyor. Yani çubuğun kesiti en fazla **1.00 mm (Y) × ~2.00 mm (Z)**. Bu kesitle iki yönelim mümkün:

- **Priz yukarı (+Y) bakıyorsa:** üst yüzde 8.34 × 2.56 mm'lik bir ağız gerekir. Z'de 2.56 > 2.00, yani ağız gövde kalınlığından geniş. Ayrıca fiş 6.2–6.65 mm içeri girer. Çubuk 1.00 mm olduğuna göre fiş **5.2–5.7 mm kadar ekran gövdesine (y < 80) dalar.** O bölgede Q1/Q2 karosunun pili, yapboz çekirdeği ve TOLED'i var. Bu doğrudan hacimsel çakışma.
- **Priz yana (±X) bakıyorsa:** ağız 8.34 × 2.56 mm, çubuk kesiti 1.00 × 2.00 mm. Kesit alanı yaklaşık 21.3 mm²'ye karşı 2.0 mm², yani **10 kat küçük.**

Daha temel bir sınır da var: **erkek fişin kendi kalınlığı 2.40 mm.** Kalınlığı 2.40 mm'den az olan bir cihaza USB-C fiş fiziksel olarak takılamaz. Bugün USB-C kullanan en ince cihazlar bile priz bölgesinde 3.5 mm civarının altına inemiyor. 2.00 mm gövde ve 1.00 mm çubuk için USB-C **mümkün değil.** Bu bir tolerans sorunu değil, standardın kendisiyle çelişki.

### 1.3 Kutu çubuk kabuğundan taşıyor mu? [KESİN]

Kutunun Z yüksekliği 2.03 mm. Çubuk Z'de 1.00 mm kalınlıktaysa kutu **en az 1.03 mm dışarı taşar.** Bu, çubuğun hangi Z aralığında olduğundan bağımsız, basit bir çıkarma işlemi.

Ölçeği görmek için örnek: çubuk [−0.62, +0.38] aralığındaysa (z1 = 0.38 ve `EDGE_R = 0.62` bu aralığı akla getiriyor), kutu alttan 1.03 mm sarkar.

Çubuğun 1.00 mm'si Y yönündeyse (docstring'deki y = 80…81), Y'de 0.62 mm kâğıt üstünde sığar. Ama bu durumda da Z'deki 2.03 mm, ekranın 2.00 mm kenarını **0.03 mm aşar.** Yani priz kabuğu gövde kenarından dışarı çıkar.

### 1.4 XY konumu [DOĞRULANMALI, büyük olasılıkla HATALI]

Docstring siluetin 40.0 × 32.0 mm olduğunu söylüyor.

- `MON_H = 32` ise `cy = 36.48` siluetin **4.48 mm dışında** kalır.
- Dik "b" 32 × 40 ölçüsündeyse, (26.4, 36.48) noktası harfin sağ üst köşesine düşer. Tipografik bir "b"de sap (ascender) solda olduğundan **sağ üst bölge boştur.** Kutu malzemenin içinde değil havada kalır.

Kontrolü `point_in_polygon((26.4, 36.48), b_outer_outline())` ile yapın. Kutunun dört köşesi de çubuk poligonunun içinde, en az 0.3 mm duvar payıyla kalmalı.

### 1.5 USB-C ile ilgili diğer elektrik, ısı ve mekanik sorunlar

| # | Bulgu | Fizik ve sayılar |
|---|---|---|
| a | **"Ekran gövdesinde sıfır USB-C" ile 40 W şarjın çelişkisi** | 40 W, çubuktaki prizden geliyor ama piller ekran karolarında. Gücün modülden karolara geçmesi gerekiyor: 20 V × 2 A ya da düşük voltajda 8–10 A. Bunun için kenar kontakları lazım ve 1.00 mm'lik çubuk ile karo kenarı arasında böyle bir arayüz modellenmemiş. Ekran "portsuz" değil, sadece portu modüle taşınmış. |
| b | **Çubuk yalnızca Q1 ve Q2'ye değiyor** | Çubuk üst kenarda (y = +80). Q3/Q4'e güç ve sinyal ancak x = 0 ve y = 0 dikişlerindeki yapboz kilitleri üzerinden geçebilir. Bükülen, tak-çıkar mekanik bir kilit üzerinden düşük dirençli ve tekrarlanabilir kontak tanımlanmamış. |
| c | **DP 2.1 ile "Zero-CPU" çelişkisi** | DP 2.1 Alt-Mode, UHBR10/20 hızında görüntü kaynağı ister: GPU veya ekran denetleyicisi, retimer/re-driver, 85–90 Ω kontrollü empedanslı diferansiyel çiftler. Bu çiftlerin "eksiz" 90° bükümden geçmesi gerekiyor. 20 Gbps hızda bükümdeki empedans süreksizliği göz diyagramını kapatır. |
| d | **PD 3.1 etiketi** | 40 W (20 V / 2 A) SPR sınıfında; EPR (28/36/48 V) gerekmiyor. "PD 3.1" yazmak yanlış değil ama gereksiz. Asıl sorun aşağıdaki şarj hızı. |
| e | **40 W şarj ile pil kimyasının çelişkisi** | 12 Wh pakete 40 W yaklaşık **3.3C** demek. PEO bazlı polimer elektrolitin 25 °C'deki iletkenliği 10⁻⁶–10⁻⁵ S/cm. PEO hücreler pratikte 60–80 °C'de çalışır. Hem "≤ 36.2 °C" hem 3.3C (Qi2 25 W için bile 2.1C) aynı anda sağlanamaz. Düşük sıcaklıkta yüksek akım Li-metal anotta dendrit ve kısa devre riski demek. |
| f | **Mekanik yük** | USB-C takma/çekme kuvveti tipik olarak 5–20 N. Bu kuvvet 1.00 mm × ~40 mm'lik çubuğa ve 20 g'lık modülün oturma yüzeyine biniyor. Tutma mekanizması (mıknatıs, tırnak) yok. Çekerken oluşan moment modülü sökecek kadar büyük. |
| g | **Anten ile priz kabuğu yan yana** | 3 bantlı LCP anten ve 1×4 60 GHz dizisi, metal priz kabuğuyla aynı 1 mm'lik çubukta. 60 GHz'de λ = 5.0 mm, λ/2 aralıklı 4 eleman yaklaşık 10 mm yer kaplar. Priz kabuğu ve 0–1 mm altındaki pil akım toplayıcıları (Cu/Al folyo) toprak düzlemi gibi davranır. Normalde gereken 1–3 mm'lik antenden uzak tutma bölgesi sıfır. Rezonans kayar, verim çöker. |

---

## 2. Gövde Z yığını: verilen bantların tek tek kontrolü

### 2.1 Bant tablosu (karo yerel koordinatı, z = 0 … 2.00)

| Z aralığı (mm) | Katman | Kalınlık |
|---|---|---|
| 0.00 – 0.48 | Arka yığın (`back_toled`, `eye_shield`, alt yarı bindirme) | 0.48 |
| **0.48 – 1.44** | **Katı-hal pil** | 0.96 |
| **0.55 – 1.45** | **Yapboz çerçevesi / çekirdek** | 0.90 |
| 1.44 – 1.46 | Boşluk (pil ile bobin arası) | **0.02** |
| **1.46 – 1.62** | **Qi2 bobinleri** | 0.16 |
| 1.62 – 2.00 | Ön yığın (`front_toled`, kapak) | 0.38 |

Toplam kontrolü: 0.48 + 0.96 + 0.02 + 0.16 + 0.38 = **2.00 mm**, tutarlı.

Patlatılmış görünümdeki ofsetler (`front_toled` +9.5, bobinler +3.5, pil −3.0, `back_toled` −9.0) bu sıralamayı doğruluyor: **bobinler pil ile ön ekran arasında.**

### 2.2 İkili çakışma analizi

| Çift | Z kesişimi | Sonuç |
|---|---|---|
| Pil ↔ yapboz çerçevesi | [0.55, 1.44] = **0.89 mm**, pil kalınlığının **%93'ü** | **Z'de kesin çakışma [KESİN].** Çakışmamaları için XY izdüşümlerinin kesinlikle ayrık olması gerekir. |
| Pil ↔ Qi2 bobini | Yok (1.44 < 1.46) | Kâğıt üstünde temiz, aradaki boşluk **20 µm** |
| Çerçeve ↔ Qi2 bobini | Yok (1.45 < 1.46) | Kâğıt üstünde temiz, aradaki boşluk **10 µm** |
| Pil ↔ arka yığın | 0.48'de yüz yüze, sıfır boşluk | Temas var, tolerans payı yok |
| Bobin ↔ ön yığın | 1.62'de yüz yüze, sıfır boşluk | Temas var, tolerans payı yok |

### 2.3 Pil ile çerçeve gerçekten çakışıyor mu? [KOŞULLU, YÜKSEK RİSK]

Z'deki çakışma kesin. Sonuç, çerçevenin nasıl modellendiğine bağlı:

- **Çerçeve dolu bir plakaysa:** `quadrant_puzzle_outline` tek bir dış çizgiden ekstrüde edilmişse (docstring "mid-plane core" diyor, yani çekirdek), pil XY'de %100 onun içinde kalır. Sonuç: **0.89 mm × pil alanı kadar hacim, iki katı cisimde aynı anda.** Pil alanı yaklaşık 28 cm² ise bu **≈ 2.5 cm³ iç içe geçme** demek.
- **Çerçeve gerçekten bir halkaysa:** `mesh_from_rings` içindeki `inner` dalı ile iç kesik açılmışsa, pilin XY izdüşümü iç kesiğin içinde kalmalı. Bu durumda aşağıdaki boşluk payları gerekir.

**Gereken XY boşluğu (ısıl genleşmeden):** PC'nin CTE değeri yaklaşık 65–70 ppm/K, LLZO seramiğinki yaklaşık 15 ppm/K. 80 mm boyunda ΔT = 30 K için:

ΔL = 80 × (68 − 15)·10⁻⁶ × 30 ≈ **0.13 mm**

Çerçeve ile pil arasında her kenarda en az ~0.15 mm boşluk yoksa, ısınmada çerçeve pili sıkıştırır (soğuyunca da boşluk açılıp tıkırdar).

**Docstring'le çelişki:** Yapboz kilitleri x = 0 ve y = 0 dikişlerinde. Yani çerçeve en azından karonun iç kenarlarında var olmak zorunda. Pil bu kenarlara kadar uzanıyorsa (40 × 80 alanı kapasite için sonuna kadar kullanılmışsa) kilit dişleri pilin içine girer.

### 2.4 10–20 µm'lik boşluklar üretilemez [KESİN]

- İnce cidarlı PC enjeksiyon toleransı tipik olarak ±0.05 mm, yani **±50 µm.**
- Beş katmanın her biri ±10–30 µm toleranslı olsa bile karekök toplamı (RSS) yaklaşık ±40 µm, en kötü durum toplamı ±100 µm.
- Bu dağılımda 10 µm'lik nominal boşluk, üretilen parçaların büyük kısmında **negatif** çıkar, yani parçalar sıkışır.

**Pilin nefes alması bunu daha da kötüleştiriyor.** LLZO hücrelerde Li-metal anot tipiktir. Li'nin hacimsel kapasitesi 3860 mAh/g × 0.534 g/cm³ ≈ 2061 mAh/cm³, yani **1 mAh/cm² için yaklaşık 4.85 µm** Li kalınlık değişimi.

800 mAh, yaklaşık 28 cm²'ye dağılınca bütün katmanlar toplamında ≈ 28.6 mAh/cm² eder. Bu da şarj-deşarjda **≈ 139 µm Li kaplama/sökme salınımı** demek. Grafit anot olsaydı anotta ~%10 genleşme olurdu, o da onlarca µm.

Her iki durumda da **20 µm'lik boşluk ilk şarjda kapanır.** Pil bobini ve ön ekranı iter. Bunun sonucu OLED'de Mura (basınç izi) ve TFE kapsülleme katmanında çatlaktır.

### 2.5 Qi2 yığını fiziksel olarak eksik [KESİN]

- **Ferrit kalkanı yok.** Bobin pilden yalnızca 20 µm uzakta. Ferrit olmadan alternatif manyetik alan (128–360 kHz) pilin Cu/Al akım toplayıcılarında girdap akımı oluşturur. Sonuç: pil içinden ısınma, düşük kuplaj, düşük verim.
- **Qi2 MPP mıknatıs halkası yok.** Qi2 hizalama için mıknatıs dizisi şart. Telefonlarda bu dizi yaklaşık 0.5–1.0 mm kalınlıkta. 0.16 mm'lik bantta bobin, ferrit ve mıknatıs birlikte yer alamaz.
- **Bobin ön TOLED'in arkasında.** OLED'in metal katodu (Ag/Mg-Ag ya da Al) ve TFT arka yüzeyi tüm alanı kaplayan iletken bir levha. Bunlar ek girdap akımı kaybı ve kuplaj düşüşü getirir.
- **Merkezdeki Ø54 mm "4 sektörlü" bobin dört ayrı karoya bölünmüş.** Yarıçap 27 mm, merkez (0,0); x = 0 ve y = 0 dikişlerini kesiyor. Sökülebilen dört parça üzerinde kapalı bir sargı ilmeği ancak dikişlerde **birkaç amper AC taşıyan dört konnektörle** kurulabilir. Tanımlanmamış. Docstring "ZERO USB-C" derken bu kontaklardan da söz etmiyor. Patlatılmış görünümde `q` öneki olmayan parçalar (0,0) ofsetinde kalıyor, yani merkez bobin karolardan ayrı havada asılı çiziliyor. Görsel bile sorunu ele veriyor.
- **Çeyrek bobinlerin yerleşimi [KOŞULLU]:** Bobin (±20, ±40) merkezli ve Ø22 ise, merkez bobinle mesafe √(20² + 40²) = 44.7 mm. Bu, yarıçaplar toplamı 27 + 11 = 38 mm'den büyük, yani XY'de çakışma yok. Merkez farklıysa tekrar kontrol edilmeli.

### 2.6 Isıl bütçe: "≤ 36.2 °C" iddiası [KESİN, iyimser]

25 W Qi2'de, ferritsiz ve bobin-pil arası 20 µm iken uçtan uca verim en iyi ihtimalle %75–85. Bu, gövdede **4–6 W** kayıp demek.

- Yüzey alanı: 2 × 0.08 × 0.16 = 0.0256 m²
- Doğal taşınım + ışınım katsayısı: h ≈ 15 W/m²K
- Ortalama sıcaklık artışı: ΔT ≈ 5 / (15 × 0.0256) ≈ **13 K**

25 °C ortamda ortalama ~38 °C olur, bobin üstünde sıcak noktalar daha yüksek. Ekranı şarj pedine yüzüstü koymak bir yüzü tamamen kapatır, durum daha da kötüleşir. Ayrıca PEO elektrolit zaten bu sıcaklıkta yeterince iletken değil (§1.5e). Yani hücre ya serin kalır ama şarj olmaz, ya da şarj olur ama 36.2 °C sınırını aşar.

### 2.7 Enerji yoğunluğu [KESİN, fiziksel olarak sınırda]

Bir karodaki pil hacminin üst sınırı: 40 × 80 × 0.96 = 3.07 cm³. Bu, çerçeve ve kenar payları düşülmemiş hali.

3.0 Wh / 3.07 cm³ ≈ **980 Wh/L.** Bu değer ticari en iyi Li-iyon hücrelerin (~750–800 Wh/L) üstünde. Çerçeve payı düşülünce gerçek değer **1100 Wh/L'yi aşar.** İnce LLZO/PEO hücreler ambalaj payı yüzünden hücre seviyesinde çok daha düşük kalır. 800 mAh ve 3.0 Wh bu hacimde gerçekçi değil.

---

## 3. Bükülme (R = 25.5 mm): `bent_quad_plus_parts`

### 3.1 Gerinim [KESİN]

Tek nötr eksenli 2.00 mm'lik bir plakada yüzey gerinimi ε = t / (2R) = 2.00 / 51 = **%3.92**. Render altyazısındaki "%0.35" ancak katmanlar birbirinden tamamen ayrılıp kayarsa mümkün. O durumda da yapboz kilitleri ve bindirme dikişleri yükü taşımaz.

Katman bazında (orta düzlem z = 1.00 kabulüyle):

| Katman | Orta düzleme uzaklık | Gerinim | Malzeme sınırı |
|---|---|---|---|
| LLZO pil yüzeyleri (0.48 / 1.44) | 0.52 / 0.44 mm | **%2.0 / %1.7** | LLZO seramik kırılma gerinimi ~%0.1–0.2. **Çatlar.** |
| Qi2 bakır bobin (1.46–1.62) | 0.46–0.62 mm | **%1.8–2.4** | Cu elastik sınırı ~%0.2–0.3. Kalıcı deformasyon ve yorulma. |
| Ön TOLED (1.62–2.00) | 0.62–1.00 mm | **%2.4–3.9** | ITO ~%1, TFE inorganik katmanlar ~%0.5–1. Çatlar. |

### 3.2 Geometrik açılar ve kendi kendine çarpışma [KESİN veya KOŞULLU]

- **80 mm genişlik R = 25.5 boyunca bükülürse:** 80 / 25.5 = 3.14 rad, yani **180°.** Gövde yarım silindir olur, X genişliği yaklaşık 2R = 51 mm'ye iner. Render-battery sahnesinde -48 ve +46 ofsetleriyle iki cisim çakışmaz (−73.5…−22.5 ve +6…+86).
- **160 mm uzunluk R = 25.5 boyunca bükülürse:** 160 / 25.5 = 6.27 rad ≈ **359.5°.** 2π × 25.5 = 160.2 mm. Gövde kapalı bir halkaya döner. Ancak R orta düzleme göre alınmışsa iç yüzeyin yarıçapı 24.5 mm ve çevresi 153.9 mm. Bu durumda iç yüzey **6.1 mm üst üste biner**, yani gövde kendi içine girer. Üst kenardaki B modülü de alt kenarla (y = −80) çarpışır. Bükme ekseni kodda görünmüyor, kontrol edilmeli.
- **Mesh yoğunluğu ve kiriş hatası [KOŞULLU, KRİTİK]:** `rounded_rect` köşelere n = 8 nokta koyuyor ama düz kenarlarda sadece 2 köşe noktası var. Bükme vertex bazında yapılıyorsa 40 mm'lik bir kenar yay değil kiriş olarak kalır. Kiriş sapması:

  s = R − √(R² − (c/2)²) = 25.5 − √(650.25 − 400) ≈ **9.7 mm**

  Bu, 2.00 mm'lik gövdenin yaklaşık 5 katı. Farklı Z'deki katmanlar farklı vertex dağılımına sahipse bükülmüş render'da **dev sahte çakışmalar** oluşur. Bükmeden önce kenarlar ≤ 0.5 mm aralıkla alt bölümlere ayrılmalı.

### 3.3 Yapboz kilitleri ve bükülme kinematiği [KESİN]

- Kırlangıç kuyrukları Z'de sadece 0.55–1.45 aralığında, yani 0.90 mm yüksekliğinde. XY'de çekmeye direnirler ama **Z yönünde kayarak ayrılırlar.** Bükülme ise dikişte tam olarak Z yönünde kesme ve soyulma yükü üretir. Kilit, kendisini açan yükle yükleniyor.
- **Hem yarım bindirme dikişi hem Z'den sökülme hem "< 3 s değişim":** Bir karonun Z'den çıkabilmesi için hem x = 0 hem y = 0 dikişinde üstteki taraf olması gerekir. Dört karo bir merkezde döngüsel olarak buluştuğundan en az bir karo kilitli kalır. Q4'ü 3 saniyede değiştirmek, diğer karoların bindirme yönlerine bağlı.
- **"10 N/mm" kabaca kontrol [KOŞULLU varsayımla]:** Diş boynu 1 mm genişlik ve 0.9 mm yükseklikte varsayılırsa, PC'nin ~60 MPa çekme dayanımıyla diş başına ≈ 54 N. 24 diş × 54 N ≈ 1300 N. Toplam dikiş uzunluğu 80 + 160 = 240 mm olduğundan ortalama **≈ 5.4 N/mm**, iddia edilen değerin yarısı. Nitinol ekleme yapılırsa artar, ama Nitinol ile PC arasında yük aktarımının nasıl sağlandığı tanımlanmamış.

---

## 4. Optik, ekran ve gerçek kullanım

| # | Bulgu | Fizik ve sayılar |
|---|---|---|
| a | **Dikişlerde görünür siyah artı** | Her karo ayrı bir OLED. Her OLED'in kenarında TFE kapsülleme ve nem engeli için tipik olarak 0.3–1 mm ölü bant ile GOA/fan-out alanı gerekir. 800 × 1600 px / 80 × 160 mm = 254 ppi, piksel aralığı 100 µm. 15 µm'lik optik dikiş pikselden küçük ama **bitişik iki ölü bant 0.6–2 mm genişliğinde siyah bir artı** çizer. n = 1.585 kırınım indisi eşlemesi ölü pikselleri gizlemez. |
| b | **"Sıfır çizik polikarbonat"** | PC'nin kurşun kalem sertliği yaklaşık 2B–HB, Mohs ölçeğinde ~2–3. Kum (kuvars, Mohs 7) çizer. "Sıfır çizik" fiziksel olarak mümkün değil. Sert kaplama ekleniyorsa onun da kalınlığı ve %3.9'luk gerinim sınırı var. |
| c | **Ön yığın 0.38 mm** | PI tabanlı OLED (~0.10–0.15) + TFE + dokunmatik + OCA (0.05–0.10 × 2) + kapak (≥ 0.2). Toplam en az ~0.45–0.6 mm, yani sığmıyor. Polarizör eklenirse 0.1 mm daha. |
| d | **Ön halka ekranı kapatıyor** | Ø32 mm halka y = 44…80 bandında ön yüzde duruyor. Kabaca 32 × 36 mm, yani ön ekranın yaklaşık %9'u kapanıyor. Halka 2.00 mm öne çıkıyor. |
| e | **Halka Qi2 pedinde cihazı eğiyor** | Cihaz şarj için ön yüzü aşağıda konunca (bobin ön tarafta) halka cihazı kaldırır. Dönme noktası y = −80'de, halka y ≈ +62'de: eğim ≈ 2/142. Merkez bobinde (y = 0) ek boşluk ≈ 2 × 80/142 ≈ **1.1 mm.** Kuplaj düşer, MPP mıknatıs hizalaması bozulur. |
| f | **Çubuk ile kenar yarıçapının uyumsuzluğu** | Gövde üst kenarında `EDGE_R = 0.62` mm yuvarlatma var. Modülün iç köşe yarıçapı 0.62'den küçükse boşluk kalır ve modül tıkırdar. Büyükse çubuk kenara düz oturmaz. "Eksiz 90° büküm" yapan bir malzemede (LCP veya PCB) minimum bükme yarıçapı kalınlığın 6–10 katı, yani 1 mm için birkaç mm. Bükümün kendisi ekranın ön üst köşesiyle çakışır. |
| g | **2.00 mm halkada 50 MP OIS kamera** | 50 MP sensörlü (~1/2.76", die yaklaşık 5.1 × 3.8 mm) bir OIS modülü tipik olarak 4–6 mm yükseklik ister: optik iz uzunluğu, aktüatör, sensör ve alt tabaka. 2.00 mm derinlik yetmez. Ayrıca OIS ve ISP ile "Zero-CPU" iddiası çelişiyor. |
| h | **Halka içindeki arka AMOLED** | Ø22.4 mm ekran Ø24 mm deliğin içindeyse radyal boşluk sadece 0.8 mm. 6 katmanlı PCB (0.6–0.8 mm kalınlık), kamera ve anten 4 mm genişliğindeki halka şeridine sıkıştırılmış. |
| i | **İnanılmaz hassasiyet iddiaları** | IoU = 0.999987 ve 0.9995 değerleri, 10 px/mm rasterizasyonda kenar pikseli hatasından daha küçük. Doğrulanamaz. ELF, SAR ve ISO 10993 değerleri ölçüm verisi olmadan yazılmış. |

---

## 5. `render3d.py` ve kod seviyesindeki bulgular

| # | Konum | Bulgu |
|---|---|---|
| 1 | Başlık: "zero Z-fighting" | Ressam algoritması (üçgen merkezine göre `-zc` sıralaması) z-buffer kullanmaz. Bu yüzden klasik Z-fighting olmaz ama **iç içe geçen ya da 10–20 µm aralıklı katmanlarda sıralama hatası** yapar. Daha önemlisi bu renderer **çarpışmayı hiçbir şekilde tespit etmez.** Yarı saydam ve iç içe geçmiş katmanlar render'da kusursuz görünebilir. Render'lar "çakışma yok" kanıtı olarak kullanılamaz. |
| 2 | Merkezden üçgen yelpazesiyle kapak | Görünen kodda alt ve üst kapaklar merkez noktadan yelpaze (`c_bot`, `c_top`) ile kapatılıyor. Bu yalnızca **yıldız biçimli (star-convex)** çizgilerde doğru çalışır. "b" silueti ve yapboz dişli `quadrant_puzzle_outline` belirgin şekilde içbükey. Yelpaze üçgenleri diş yuvalarının **dışına taşar**, komşu karonun dişine sahte bir kapak çizer. Görsel çakışma oluşur ve STL çıktısı manifold olmaz. Başlıktaki "zero concave fan artifacts" iddiası bu yöntemle doğru değil. Ear-clipping ya da kısıtlı Delaunay kullanılmalı. |
| 3 | `render_scene`: `item[4]` | 5. eleman `order` için `float()` ile okunuyor. `qbody_parts` öğeleri `(name, v, f, col, a)` biçiminde. `place_parts` adı başa koyup ya da sona ekleyip aynen döndürürse `float(name)` hata verir veya `item[0]` string olur. `place_parts` görünmüyor, kontrol edilmeli. |
| 4 | `a255 = max(12, …)` | Alfa = 0 (gizli) parçalar bile %5 opaklıkla çiziliyor. Gizlenmesi gereken yardımcı geometri sahnede kalır. |
| 5 | `box_part`: `r_c = max(0.04, …)` | min(w, h) < 0.089 mm olduğunda r_c > h/2 olur ve çizgi kendi üstüne biner. z1 ≤ z0 durumunda `b_c` 0.01'e kırpılıyor ama yüzey normalleri ters dönüyor. Girdi doğrulaması yok. |
| 6 | Sahne Z referansları tutarsız | `whole_scene` ve `bat_scene` gövdeyi −T/2 kaydırıyor (−1…+1), `apart_scene` kaydırmıyor (0…2). Modül ofsetleri (`mod_dz`) her iki sahnede aynı. Patlatılmış görünümde modül-gövde ilişkisi 1 mm kayık. |
| 7 | Patlatma sınıflandırması | `"bifilar"` adı pil grubuna (−3.0) düşüyor. Bifilar genelde bir sargı tipi, yani bobin olması muhtemel. `if/elif` sırası yüzünden yanlış katmanda gösterilebilir. `q` öneki olmayan merkez MPP bobini (0,0) ofsetinde kalıyor. |
| 8 | Revizyon tutarsızlığı | `leaf_v2` L.5.0 (2026-10-12), `render3d` L.4.1 (2026-10-07). Ufak bir nokta, ama başlıktaki "84 subparts = 52 + 32" sayısı ancak gizli kodda sayılarak doğrulanabilir. |
| 9 | `annular_arc` | Sargı yönleri kontrol edildi: alt yüz −z, üst yüz +z, uç kapaklar zıt yönlü. **Doğru.** |

---

## 6. 52 parça için çakışma testi (gizli kod için)

Koordinatlar elimde olmadığı için bu testi siz çalıştırmalısınız. AABB ön elemesi ve ardından gerçek mesh kesişimi yapar:

```python
# cad/check_collisions.py
import itertools, numpy as np, trimesh
from leaf_v2 import quad_plus_body_parts, monogram_parts   # gerçek isimlerle

TOL = 0.05  # mm: üretim toleransı; bunun altındaki boşluk da "fail"

def aabb(v):
    v = np.asarray(v); return v.min(0), v.max(0)

def check(parts, label):
    meshes = [(n, trimesh.Trimesh(np.asarray(v), np.asarray(f), process=True))
              for (n, v, f, c, a) in parts]
    for (n1, m1), (n2, m2) in itertools.combinations(meshes, 2):
        (a0, a1), (b0, b1) = m1.bounds, m2.bounds
        gap = np.maximum(b0 - a1, a0 - b1)          # eksen bazlı boşluk
        if (gap < TOL).all():                        # AABB'ler TOL içinde
            if not (m1.is_watertight and m2.is_watertight):
                print(f"[{label}] NON-MANIFOLD: {n1} / {n2}")
                continue
            inter = m1.intersection(m2)              # manifold3d backend
            vol = inter.volume if inter and not inter.is_empty else 0.0
            if vol > 1e-6:
                print(f"[{label}] ÇAKIŞMA {vol:8.4f} mm³ : {n1} ↔ {n2}")
            elif gap.max() < TOL:
                print(f"[{label}] TOLERANS<{TOL} ({gap.max()*1e3:.0f} µm): {n1} ↔ {n2}")

check(quad_plus_body_parts(), "BODY")
check(monogram_parts(), "B-MOD")
# USB-C kutusunun çubuk içinde kalıp kalmadığı:
#   (usb.difference(bar)).volume > 0  ->  kabuk dışına taşma
```

Testte özellikle bakılması gerekenler:

1. Pil ↔ çerçeve çiftinde kesişim hacmi sıfırdan büyük mü?
2. Çerçeve ↔ bobin (10 µm) ve pil ↔ bobin (20 µm) çiftleri `TOLERANS` uyarısı veriyor mu? Vermeleri gerekir.
3. USB-C ↔ çubuk için `difference` sonucu sıfır değil.
4. Bükülmüş sürümde testi kenarları alt bölümlere ayırdıktan sonra tekrarlayın (§3.2).
5. Merkezden yelpazeyle kapatılan içbükey çizgiler non-manifold çıkacaktır; önce düzeltin (§5-2).

---

## 7. Özet ve önem sırası

| Önem | Bulgu | Tür |
|---|---|---|
| **KRİTİK** | USB-C 1.00 mm çubuğa ve 2.00 mm gövdeye fiziksel olarak sığmaz (fiş kalınlığı 2.40 mm, priz yaklaşık 3.2 × 8.9 mm). Kutu ölçüleri gerçeğin yaklaşık 1/25'i, Z'de en az 1.03 mm taşıyor. | KESİN |
| **KRİTİK** | Pil ile yapboz çerçevesi Z'de 0.89 mm (%93) üst üste biniyor. Çerçeve dolu plakaysa ≈ 2.5 cm³ iç içe geçme var. | KESİN (Z) / KOŞULLU (XY) |
| **KRİTİK** | %3.9 yüzey gerinimi LLZO (sınır ~%0.1–0.2), bakır bobin ve OLED/TFE için yıkıcı. | KESİN |
| **KRİTİK** | 10–20 µm boşluklar ±50 µm kalıp toleransının ve yaklaşık 139 µm'lik Li-metal nefes almasının çok altında. | KESİN |
| YÜKSEK | Qi2 yığınında ferrit ve MPP mıknatısı yok; Ø54 bobin dört sökülebilir karoya bölünmüş. | KESİN |
| YÜKSEK | PEO pil kimyası ile "≤ 36.2 °C" ve 2–3.3C şarj aynı anda sağlanamaz; 25 W Qi2'de ΔT yaklaşık 13 K. | KESİN |
| YÜKSEK | Yaklaşık 980–1100 Wh/L enerji yoğunluğu ticari sınırın üstünde. | KESİN |
| YÜKSEK | Uzun eksende bükülürse gövde kendi içine yaklaşık 6 mm giriyor; kaba mesh ile kiriş sapması yaklaşık 9.7 mm. | KOŞULLU |
| YÜKSEK | "Portsuz ekran" iddiasına rağmen güç ve sinyal modülden karolara, ayrıca dikişler üzerinden Q3/Q4'e nasıl geçecek, tanımlanmamış. | KESİN |
| ORTA | Dikişlerde görünür siyah artı, ön yığının 0.38 mm'ye sığmaması, 2 mm'lik halkada OIS kamera. | KESİN |
| ORTA | Renderer çarpışma göstermez; merkezden yelpaze kapak içbükey çizgileri bozuyor; olası `float(name)` hatası. | KESİN / KOŞULLU |
| DÜŞÜK | Sahne Z referansları tutarsız, `bifilar` sınıflandırması, alfa tabanı, revizyon tarihleri. | KESİN |

**Genel sonuç:** Verdiğiniz sayılar tek başına iki kritik çakışmayı kanıtlamaya yetiyor: USB-C ile çubuk arasındaki taşma ve pil ile çerçevenin Z'deki çakışması. Bunlara 10–20 µm'lik üretilemez boşluklar ve bükülme gerinimi ekleniyor. Mevcut haliyle tasarım hem geometri hem fizik açısından **montajlanamaz durumda.** 52 parçanın koordinat bazında kesin doğrulaması için kesilen fonksiyon gövdeleri ile `leaf_geom.py` ve `monogram_letter.py` dosyalarını gönderin ya da §6'daki testi çalıştırıp çıktısını paylaşın.

### W1_A1_OPUS_CAD_MONOGRAM_AND_GEOM · Model: `claude-opus-5-5` (Router: `claude-coding-router-preview`, Başlangıç: `2026-10-12 14:26:25 +03`, Bitiş: `2026-10-12 14:36:01 +03`, Süre: `576.29 sn`, Uzunluk: `23,634` karakter)

# Budlum Leaf L.5.0: `monogram_letter.py` ve `leaf_geom.py` CAD denetim raporu

## 0. Kapsam ve kanıtlanabilirlik sınırı

İki sorunun cevabını en çok etkileyen fonksiyonların gövdeleri gönderilen metinde yok (`... [ORTA KISIM KISALTILDI] ...`):

| Görünmeyen öğe | Etkilediği soru |
|---|---|
| `_fold_uv_to_3d` (tamamı) | Soru 1: büküm yarıçapı, 3B çakışma |
| `_puzzle_lobe_1d` döngü gövdesi (`steps` sonrası) ve `quadrant_puzzle_pair` (tamamı) | Soru 2: faz/işaret |
| `_build_structured_strip_3d`, `b_outer_outline`, `bore_outline`, `stack`, `mesh_from_rings` | Mesh bütünlüğü |

Bu yüzden iki tür bulgu var:
- **[KESİN]**: Görünen sayılardan ve formüllerden doğrudan hesaplanan ya da çelişkisi kanıtlanan bulgular.
- **[KOŞULLU]**: Kesik kodun en olası yazımı varsayılarak çıkarılan bulgular. Varsayım her seferinde açıkça yazılı.

Görmediğim kodu "doğru" ya da "yanlış" ilan etmiyorum. Onun yerine eşleşme koşulunu denklemle veriyorum, kod sahibi kendi koduna uygulayarak tek satırda doğrulayabilir.

---

## 1. Temel çelişki: üç ayrı Z ekseni tanımı [KESİN, KRİTİK]

İki soru da "ekran nerede?" sorusuna bağlı. Dosyalar bunu üç farklı şekilde cevaplıyor:

| Kaynak | Ekranın Z aralığı |
|---|---|
| `leaf_geom.main` → `stack(..., 0.0, th, ...)` | **z = 0 … +2.00** (STL gövdesi) |
| `leaf_geom` başlığı: "core z = −0.45 … +0.45 inside the 2.00 mm screen" | **z = −1.00 … +1.00** (merkezli) |
| `monogram_letter` başlığı: çubuk "z = −2.00 … +0.80 across the 2.00 mm screen top edge" | Üçüncü bir referans, iki tanıma da uymuyor |

Sonuçlar:
- STL gövdesi z = 0…2 ise yapboz çekirdeği (−0.45…+0.45) **yarı yarıya gövdenin dışında** kalıyor: 0.45 mm'lik dilim boşlukta.
- `b` çubuğunun z aralığı hangi tanım seçilirse seçilsin ekranla tutarlı değil (bkz. §2.4).

**Düzeltme:** Tek bir Z ekseni seçilmeli (öneri: z = −1…+1, ön yüz +Z) ve iki dosyada da aynı sabit kullanılmalı.

---

## 2. Soru 1: `b` modülünün u = 4.0 mm'den 90° bükülmesi

### 2.1 2B geometri: formüller doğru, başlıktaki tarif yanlış

**Kesişim formülü doğru [KESİN].** Vadi çemberi C_V = (16,16), r_val. Halka dış çemberi C_D = (24,16), r_out. İki denklem çıkarılınca:

(u−16)² − (u−24)² = r_val² − r_out²  →  16u − 320 = r_val² − r_out²  →  **u = (320 + r_val² − r_out²)/16**

d = 0 için: u = (320 + 144 − 256)/16 = **13.000**, v = 16 − √(144 − 9) = **4.381**. Koddaki `u_int` / `v_int` doğru.

**Başlıktaki tarif yanlış [KESİN, ORTA].** Başlık "doğal boşluk u = 4.0…8.0 mm, v > 4.381" ve "boğaz v = 0…4.381" diyor. Gerçek geometri başka:

- Boşluk = vadi diskinin içi ∩ halka diskinin dışı. Genişliği sabit 4 mm değil:

| v (mm) | Sol sınır (çubuk / vadi yayı) | Sağ sınır (halka dış yayı) | Boşluk genişliği |
|---|---|---|---|
| 4.381 | 13.00 | 13.00 | **0 (sivri uç)** |
| 10 | 5.61 (vadi yayı) | 9.17 | 3.56 |
| 16 | 4.00 | 8.00 | **4.00 (tek minimum)** |
| 30 | 4.00 | 16.25 | 12.25 |

- Boğaz sadece v ≤ 4.381 değil. Vadi yayının altındaki bütün bölge malzeme: u = 5'te malzeme v = 11.2'ye, u = 4'te v = 16'ya kadar çıkıyor.

**Boşluğun ucunda 29°'lik keskin çentik var [KESİN, YÜKSEK].** P = (13, 4.381) noktasında iki yayın teğetleri arasındaki iç açı:

cos α = ((P−C_V)·(P−C_D))/(12·16) = (33 + 135)/192 = 0.875  →  **α = 28.96°**

`b_2d_outer_uv` bu noktada yuvarlatma yapmıyor, kök yarıçapı 0. Yani 29°'lik, çatlak benzeri bir V-çentik var. Teorik gerilme yoğunlaşması (Kt) sınırsız.

Daha kötüsü: Halka + kamera kütlesi çubuğa **yalnızca bu çentiğin altındaki bağ ile** bağlı. Vadi yayı ile halka arasında P'ye kadar boşluk uzanıyor; ayırıcı en kısa kesit P → (13, 0), yani **4.381 mm × t**. t = 1 mm ise taşıyıcı kesit 4.38 mm².

**Kaba düşme kontrolü [KOŞULLU].** Varsayımlar: modül alanı ≈ 550 mm², alüminyum (≈ 1.5 g), düşmede ≈ 3000 g ivme.
- Kuvvet: 1.5 g × 3000 g ≈ 44 N
- Nominal gerilme: ≈ 10 MPa
- Kt = 3…5 ile: 30–50 MPa

PC'nin akma dayanımı ≈ 62 MPa, yani PC sürümünde pay çok dar. Çentik ucuna en az R 0.5–1.0 mm yuvarlatma şart.

**Kod düzeyinde küçük kusurlar [KESİN, DÜŞÜK].**
- `r_stem = max(0.4, CAP_R − d)`, merkez (2, 30) sabit kalırken d > 1.6 olunca kapak yayı u = 1.6…2.4'te kalıyor, sol kenar ise u = d > 1.6. İçe kaydırılmış kontur kendini kesiyor. `r_bot` için de aynısı.
- `RING_C = VALLEY_C = (16,16)`: halka merkezi büküm sonrası (X,Y) çerçevesinde, vadi merkezi 2B (u,v) çerçevesinde. Vadi merkezi büküm sonrası çerçevede (16, 24) olmalı. Bu sabit 3B'de kullanılırsa vadi halkayla eş merkezli çıkar.

### 2.2 Büküm hattının fiilen ne kadarı malzemeden geçiyor? [KESİN, YÜKSEK]

Büküm hattı u = 4, v = 0…32 boyunca (büküm sonrası X = 0…32).

| v aralığı | u = 4 hattında durum |
|---|---|
| 0 … 16 | Malzeme var (boğaz) |
| 16 … 30 | u = 4 çubuğun serbest iç kenarı, hattın ötesinde malzeme yok |

Docstring'deki büküm bölgesi u = 3.6…4.8. Bu bölgenin tamamen dolu olduğu aralık vadi yayından hesaplanıyor: 16 − √(144 − 11.2²) = 11.69. Yani **v ∈ [0, 11.69]**.

Sonuçlar:
1. 32 mm'lik çubuğun yalnızca **11.7–16 mm'si** menteşeye bağlı, hepsi X = 0 ucunda. Kalan **16–20 mm** konsol olarak boşta.
2. v = 11.7…16 arasında vadi yayı büküm hattına **teğet** yaklaşıyor (yay (4,16)'da u = 4'e teğet). Kenarı büküm hattına teğet ya da eğik giren bir sac bükülünce kenar yırtılır ve şişer. Standart çözüm büküm boşaltma kesiği (bend relief: genişlik ≥ t, derinlik ≥ t + r_i). Geometride yok.
3. v = 16…32 aralığında u = 3.6…4.0 şeridi tek taraflı bükülüyor. Çubuğun sağ yarısında 0.4 mm'lik aşağı kıvrık bir dudak oluşuyor.

### 2.3 Büküm yarıçapı: üç kaynak üç farklı r_i veriyor [KESİN, KRİTİK]

Plaka kalınlığı t = 1.00 mm (yatay çubuk yüksekliği = levha kalınlığı). Büküm payı formülü:

BA = (π/2)·(r_i + K·t),  dış lif gerinimi ε ≈ t/(2r_i + t)

| Kaynak | Çıkan r_i | ε (dış lif) |
|---|---|---|
| "Sıfır menteşe, u = 4.0'dan dik açı" | 0 | **%100** (fiziksel olarak imkânsız) |
| Docstring "u = 3.6…4.8" (BA = 1.2 mm, K = 0.33…0.5) | 0.43 … 0.26 | %54 … %66 |
| z = +0.80 düz bitiş, ekran −1…+1 (dikey bacak iç yüzü z = +1) | **0.20** | **%71** |
| z = +0.80 düz bitiş, ekran 0…2 (STL) | 1.20 | %29 |
| Ekran kenar yuvarlatmasına (0.62) oturan büküm | 0.62 | %45 |

**Açınım uzunluğu da tutmuyor:** `STEM_W = 4.0` ve büküm u = 3.6'da başlıyorsa düz çubuk 3.6 mm olmalı. Başlıktaki z aralığı ise 2.8 mm. **0.8 mm'lik fark** hangi Z tanımı seçilirse seçilsin kapanmıyor.

**Malzeme açısından:**
- **PC:** Akma gerinimi ≈ %6. Elastik kalmak için r_i ≥ t(1/0.06 − 1)/2 ≈ **7.8 mm** gerekir. %30–70 gerinimle soğuk bükülen PC beyazlaşır, mikro çatlar (crazing) ve kalıcı iç gerilme taşır; solvent/yağ temasında gerilme çatlaması kaçınılmaz olur. Docstring'deki "ön veya arka" ifadesi modülün tekrar tekrar katlanabileceğini ima ediyor. PC canlı menteşe malzemesi değil (o iş için PP kullanılır), birkaç düzine çevrimde kırılır.
- **Metal:** 6061-T6 için r_min ≈ 1.5–2.5t, 5052-H32 ≈ 1t, Ti Gr2 ≈ 2–2.5t. r_i = 0.2–0.43 mm hiçbirine uymuyor.
- **Kamera/USB sinyal hattı:** Esnek devre menteşeden geçmek zorunda. IPC-2223'e göre statik bükümde r ≥ 6t (tek katman) ile 24t (çok katman); 0.1 mm FPC için 0.6–2.4 mm. 0.2–0.43 mm'de bakır çatlar ve MIPI'nin 100 Ω diferansiyel empedansı bozulur.

### 2.4 Çubuk ile 2.00 mm ekran kenarı arasındaki ilişki [KESİN, KRİTİK]

**a) Genişlik uyuşmuyor.** Çubuk u = 0…4 → Z derinliği **4.0 mm**. Başlıktaki aralık −2.0…+0.8 = **2.8 mm**. Ekran 2.0 mm. Üç sayı birbirini tutmuyor.

**b) Z senaryoları:**

| Senaryo | Çubuğun ekran kenarındaki temas aralığı | Arkadan taşma | Ön tarafta |
|---|---|---|---|
| Ekran −1…+1 | −1.0…+0.8 (1.8 mm) | **1.0 mm** boşta | 0.2 mm açık; büküm r_i = 0.2 olmak zorunda (ε = %71) |
| Ekran 0…2 (STL) | 0…+0.8 (0.8 mm) | **2.0 mm** boşta | Ön yüz z = +2'ye **1.2 mm** kısa; dikey bacağa ancak r_i = 1.2 bükümle bağlanabilir |

**c) Temas yüzeyi aslında 0.76 mm.** `edge_fillet(2.0) = min(0.68, 0.62) = 0.62 mm`. 2.00 mm'lik kenarın düz kısmı 2.00 − 2×0.62 = **0.76 mm**. 4 mm'lik çubuk 0.76 mm'lik düz şeritte sallanır. Yapıştırma alanı 0.76 × 32 = 24.3 mm²; menteşe tarafında efektif ≈ 9–12 mm².

**d) Sıfır boşluk.** Çubuk alt yüzü y = 36.0 ile ekran üst kenarı (y_phone = 80.0) tam üst üste; dikey bacak iç yüzü ile ekran ön yüzü de öyle. Yapıştırıcı için pay yok (PSA bant 0.05–0.15 mm). Üretim toleransıyla ya boşluk ya **girişim** olur.

**e) İç köşe:** Büküm r_i (0.2–0.43) < ekran yuvarlatması (0.62), dolayısıyla teorik bir çarpışma yok. Köşegende (0.62 − r_i)(√2 − 1) ≈ 0.08–0.17 mm hava boşluğu kalıyor; modül köşeye oturmuyor.

**f) Mesh'te kirişin ekrana girmesi [KOŞULLU].** Varsayım: `_fold_uv_to_3d` büküm bölgesini sınırlı sayıda düz üçgenle kesiyor.

- `stem_pairs` her satırda yalnızca **iki sütun** üretiyor (u_left, u_right). `_build_structured_strip_3d` alt bölme yapmıyorsa, u = 4.0 sütunu büküm yayında 30°'de (≈ (4.0 − 3.6)/1.2 × 90°) yer alıyor.
- u = 0 (düz) ile u = 4 arasındaki üçgen, düz düzlemin altına iner. u = 3.6'da ≈ r(1 − cos 30°)·0.9 ≈ **0.09 mm** ekran üst yüzeyine girer.
- Kaba kesim örneği: bükümün iki yanında 0.4 mm ve 0.8 mm'lik bacaklar tek kirişle bağlanırsa, kiriş ekranın R 0.62 kenar yuvarlatmasına **0.147 mm** girer. Kirişin yuvarlatma merkezine uzaklığı 0.473 mm; 0.62 − 0.473 = 0.147.

### 2.5 `bridge_pairs`: yanlış sabit kodlanmış eşik, basamak hatası [KESİN, YÜKSEK]

```python
if u <= 12.5:   # vadi yayı
else:           # halka dış yayı
```

Gerçek kesişim d = 0'da **u = 13.0**. d > 0'da daha da sağa kayıyor: d = 0.5'te r_val = 12.3, r_o = 15.7 ve u = 14.05.

| d | u = 12.5'te vadi v_top | u = 12.5'te halka v_top | Üst yüzeyde basamak |
|---|---|---|---|
| 0 | 4.522 | 4.876 | **0.354 mm** |
| 0.5 | 4.208 | 5.312 | **1.10 mm** |

u = 12.5 … u_int aralığında mesh, 2B konturun gerçek boşluğunu dolduruyor; boşluğun sivri ucu mesh'te yok. Ayrıca 0.35–1.1 mm'lik dik bir duvar oluşuyor. 2B SVG ile 3B STL arasında bu bölgede birebir eşleşme yok.

**Düzeltme:** Eşik u_int(d) = (320 + r_val² − r_o²)/16 ile dinamik hesaplanmalı ya da v_top = max(vadi, halka) değil, gerçek kontur kullanılmalı.

### 2.6 Diğer mesh kusurları [KESİN]

1. **Şeritler örtüşüyor, birleştirilmiyor.** Çubuk u ≤ 4.0, boğaz u ≥ 3.6 → v = 0…16 boyunca 0.4 × 16 = **6.4 mm²** eş düzlemli üst üste üçgen (u = 3.6'da `du` sınırlandığı için v_top = 16). Boğaz u = 23.5 civarında `v_top = max(v_bot + 0.4, …)` ile halkanın içine giriyor. Üç kabuk Boolean birleşim yapılmadan ardı ardına ekleniyor: su geçirmez değil, kendini kesen yüzeyler var, hacim/kütle iki kez sayılıyor.
2. **İçe kaydırma katsayıları tutarsız.** Halka 0.7d, boğaz 0.6d, çubuk 0.6d (0.32 ile sınırlı), `b_2d_outer_uv` 1.0d. Kaydırılmış yüzeyler birleşim yerlerinde basamaklı.
3. **Halka dikişi:** `ring_pairs` N+1 nokta üretiyor, ilk ve son nokta aynı. Builder kaynak yapmıyorsa dikişte açık kenar kalır [KOŞULLU].
4. **SVG dolgu kuralı:** `b_2d_outer_uv` saat yönünde (alt kenar sola → sol kenar yukarı). Delik `reversed(bore_outline)`. bore_outline CCW ise ters çevrilince o da CW olur; SVG'nin varsayılan `nonzero` kuralında **delik dolu çizilir** [KOŞULLU]. `plan_svg`'deki ayrı daire bu hatayı görsel olarak maskeliyor.
5. **`svg_path` docstring'i:** "boşluk ve boğaz oy … oy + 4k" diyor (y = 36…32). Gerçekte boğaz u = 13'e kadar (y = 27), boşluk y = 23.75'e kadar uzanıyor.

### 2.7 Cihaz düzeyinde kullanım hataları

**Bükülebilir ekranla rijit modül [KESİN, KRİTİK].** İddia: R = 25.5 mm bükülme. Rijit kiriş ile yay arasındaki sehim s = R − √(R² − (c/2)²):
- c = 32 mm (modül genişliği): **5.64 mm**
- c = 36 mm (modül yüksekliği): **7.44 mm**

Modül ya ayrılır ya da ekran o bölgede bükülemez.

Ek bir not: 160 mm / 25.5 mm = 6.27 rad ≈ 2π. Telefon uzun ekseninde bu yarıçapa bükülünce Ø51 mm'lik **tam bir tüpe** dönüşür. Kısa eksende 80 / 25.5 = π, yani yarım silindir.

**Masada sallanma [KESİN, ORTA].**
- Ön yüzden 1 mm çıkıntılı halka: ekran aşağı konunca telefon halkanın ve alt kenarın üzerinde durur; 140 mm kolda ≈ 0.41° eğim, halka ve ekran çizilir.
- Arkadan 1–2 mm taşan çubuk: ekran yukarı konunca 160 mm kolda ≈ 0.36–0.72° eğim.

**Ekranı kapatma [KESİN, ORTA].** Halka dış diski π·16² = 804 mm² ve 12 800 mm² ekranın üstünde (ön yüzde, aktif alanda). Delik şeffaf değilse ≈ %6.3, şeffafsa ≈ %2.75 artı boğaz ve çubuk. Metal halka kapasitif dokunmayı bozar (sahte dokunma, topraklama).

**USB-C ve kamera fiziksel olarak sığmıyor [KESİN, KRİTİK].**
- USB-C dişi soket ağzı **8.34 × 2.56 mm**. Modül 1 mm kalın, halka et kalınlığı 4 mm, çubuk 4 × 1 mm.
- Ayrıca çapraz-dosya çelişkisi: başlık "Zero-CPU & USB-C Module", plan satırı "Gövdede Type-C yok". 15–25 W USB-PD bir PD denetleyicisi gerektirir, "Zero-CPU" ile çelişir.
- Telefon sınıfı kamera modülü yüksekliği 3–6 mm. 1 mm'ye ancak ~1 mm'lik endoskop sensörleri sığar (ör. OVM6948 sınıfı).

**Isıl darboğaz [KOŞULLU].** PC modül varsayımıyla (k ≈ 0.2 W/m·K):
- 1 mm et, 24.3 mm² temas üzerinden iletim: R = 1e-3 / (0.2 × 24.3e-6) ≈ **206 K/W**
- Konveksiyon (≈ 1100 mm², h = 10): ≈ 91 K/W
- Paralel toplam ≈ 63 K/W → 0.25 W kamera ≈ **+16 K**

---

## 3. Soru 2: `_puzzle_lobe_1d` / `quadrant_puzzle_pair` eşleşmesi

### 3.1 Profil fonksiyonunun analizi [KESİN]

ω(θ) = sin θ + 0.28 sin 3θ

Ekstremumlar: ω' = cos θ + 0.84 cos 3θ = 0. cos 3θ = 4c³ − 3c yazılınca:

c·(3.36c² − 1.52) = 0  →  c² = 0.45238  →  θ = 47.73° ve 132.27°;  c = 0 → θ = 90°

| θ | ω | amp = 1.95 | amp = 2.2 (varsayılan) |
|---|---|---|---|
| 47.73° (tepe) | **0.9077** | 1.770 mm | 1.997 mm |
| 90° (ortadaki çukur) | **0.72** | 1.404 mm | 1.584 mm |
| Lob ile yuva arası tepe-tepe | 1.8155 | **3.540 mm** | 3.994 mm |

Bulgular:
1. **Genlik çelişkisi:** Fonksiyon varsayılanı `amp = 2.2`, siz `amp = 1.95` diyorsunuz. `quadrant_puzzle_pair` hangisini geçiriyor, görünmüyor. İki değer arasında tepe farkı 0.227 mm.
2. **Gerçek tepe ≠ amp:** Etkin tepe amp değil, **0.9077·amp**.
3. **Lob "M" biçimli:** Her lobun tepesinde 0.366 mm'lik (amp = 1.95) bir çukur var; iki tepeli bir dalga. "Boyundan başa genişleyen dovetail" değil.

**Simetriler (ispat için gerekli):**
- ω(−θ) = −ω(θ) (tek fonksiyon)
- ω(θ + π) = −ω(θ) → erkek ve dişi yarım dalga birebir eş şekil
- ω(π − θ) = sin θ + 0.28 sin(3π − 3θ) = ω(θ) → her lob kendi ekseni etrafında simetrik, eğimi yok

### 3.2 Eşleşme koşulu: denklemle ispat

**Varsayım (görünen koddan):** `pts.append((s0, 0.0))`, `pts.append((s_start, 0.0))` satırları (s, n) çiftleri üretildiğini gösteriyor. Sınır n(s) = σ·A·ω(θ(s)) biçiminde. θ doğrusal:

θ(s) = 2πN·(s − s_start)/(s_end − s_start),  L = s_end − s_start

Uç payları simetrik (her uçta 4.5 mm), bu yüzden L iki yönde de aynı.

Küresel dikiş X = 0 (qx = −1 | qx = +1) ya da Y = 0 (qy = −1 | qy = +1). Sol karo X < f_L(s), sağ karo X > f_R(s) bölgesini kaplıyor.

**Boşluksuz ve girişimsiz eşleşme ⟺ f_L(s) ≡ f_R(s) her s için.**

**Tarama yönü ters olduğunda.** CCW çevre taramasında sol karo dikişi aşağıdan yukarı, sağ karo yukarıdan aşağı gezer. Kod `s1 < s0` durumunu işaretli payla zaten ele alıyor; bu durumda:

θ_R(s) = 2πN − θ_L(s)  ⇒  ω(θ_R) = ω(−θ_L) = **−ω(θ_L)**

Yani yönün ters çevrilmesi tek başına işareti çeviriyor.

**Doğruluk tablosu.** Ofset küresel X'e uygulanıyorsa:

| Tarama yönleri | sign_dir (σ_L, σ_R) | Sonuç |
|---|---|---|
| Aynı | Aynı | ✅ Birebir eş: f_L = f_R |
| Aynı | Zıt | ❌ f_R = −f_L |
| Zıt | Aynı | ❌ f_R = −f_L |
| Zıt | Zıt | ✅ Birebir eş |

Ofset her karonun **kendi dış normaline** uygulanıyorsa (sol karo +X, sağ karo −X), bir işaret daha döner ve tablonun son sütunu tersine çevrilir. CCW tarama + dış normal kombinasyonunda **iki karoya aynı sign_dir geçilmeli**. Sık yapılan "`sign_dir = qx`" ataması bu durumda hatalı olur.

**Hatalı durumda (f_R = −f_L) büyüklük.** Lob alanı = A·∫₀^π ω dθ·(L/2πN). ∫₀^π ω dθ = 2 + 0.28·(2/3) = 2.1867.

| Dikiş | L | N | Pay başına girişim alanı | Toplam girişim | Toplam boşluk | 0.9 mm çekirdekte hacim |
|---|---|---|---|---|---|---|
| Dikey (80 mm kenar) | 71 mm | 4 | 24.1 mm² | **96.4 mm²** | 96.4 mm² | ≈ 87 mm³ |
| Yatay (40 mm kenar) | 31 mm | 2 | 21.0 mm² | **42.1 mm²** | 42.1 mm² | ≈ 38 mm³ |

Hatalı durumda tepe girişimi **2·0.9077·A = 3.54 mm** (amp = 1.95). Montaj fiziksel olarak imkânsız olur.

**Tek satırlık doğrulama testi:** Her dikiş için iki karonun noktalarını küresel koordinata çevirip ortak s ızgarasında max|f_L − f_R| < 1 µm olduğunu assert edin.

**Faz kayması riski [KOŞULLU].** Bir karo kenarı r_inner köşeleri hariç (±(hh − 0.18)), diğeri tam ±hh ile parametrelenirse L farkı 0.36 mm olur. Dikey dikişte uçta faz kayması 2π·4·0.36/71 ≈ 0.127 rad, yani ≈ 0.23 mm ofset hatası. Karolar aynı s0/s1 değerlerini kullanmalı.

**Örnekleme toleransı [KESİN].** İki karo farklı düğüm noktalarıyla örneklenirse poligonlar en fazla sehim kadar birbirinden sapar. Sehim δ ≈ Δs²/(8R_min). En küçük eğrilik yarıçapı R_min = 1/(A·|ω''|·k²):

| Dikiş | k = 2πN/L | Tepe R | Çukur R | δ ≤ 15 µm için Δs | Kenar başına gereken örnek |
|---|---|---|---|---|---|
| Dikey | 0.354 /mm | 1.82 mm | 2.69 mm | ≤ 0.467 mm | **≥ 152** |
| Yatay | 0.405 /mm | 1.39 mm | 2.05 mm | ≤ 0.408 mm | **≥ 76** |

Kesik koddaki `steps` değeri bu sayıların altındaysa veya iki karo ofsetli düğümler kullanıyorsa, "< 15 µm" iddiası tutmaz.

### 3.3 "Hem çekmede hem kesmede kilit" iddiası matematiksel olarak yanlış [KESİN, KRİTİK]

**Teorem.** Sınır tek değerli bir fonksiyonun grafiği ise (X = f(s), (s, n) biçimi), dikişe dik yöndeki öteleme bloke edilemez.

**İspat.** Sağ karo R = {X > f(s)}, sol karo L = {X < f(s)}. Sağ karo +δ kadar X'e ötelenirse R' = {X > f(s) + δ} olur. L ∩ R' = ∅ her δ > 0 için geçerli. Ayrılmaya geometrik bir engel yok. ∎

- `sin 3θ` harmoniği sadece normal yöndeki şekli değiştiriyor, alt-kesim (undercut) oluşturamıyor.
- Gerçek dovetail için profilin s'ye göre çok değerli olması gerekir; teğet yönde de bir terim lazım: s' = s + B·g(θ).

**Kesme altında kama etkisi.** Sıfır geçişlerindeki yanak eğimi dn/ds = A·1.84·k:
- Dikey dikiş: 1.270 → **51.8°**
- Yatay dikiş: 1.454 → **55.5°**

Kesme yükü F'nin dikişe dik ayırıcı bileşeni F_n = F·(tan α − μ)/(1 + μ tan α). μ = 0.4 ile F_n ≈ **0.58·F**. Kesme yükünün yarıdan fazlası karoları ayırmaya çalışıyor ve buna yalnızca yapıştırıcı direniyor. "Ayrılmadan birlikte bükülme" iddiası desteklenmiyor.

### 3.4 "±Z'den takılabilir" iddiası ile iç çekirdek kilidi çelişiyor [KESİN, KRİTİK]

Kilit yalnızca çekirdekte (z = −0.45…+0.45), dış PC yüzeyler ise düz alın dikişiyle buluşuyor. A karosunun lobu B'nin bölgesine 1.77 mm giriyor. Orada B'nin üstte (z = 0.45…1) ve altta (z = −1…−0.45) kendi kabukları var. Lob yuvası B içinde kapalı bir cep.

| Takma yönü | Sonuç |
|---|---|
| ±Z | ❌ B'nin kabukları engeller |
| Düzlem içi, dikişe dik | ✅ Mümkün (grafik profil sayesinde), ama aynı yönde ayrılır (§3.3) |

İddia edilen iki özellik (±Z'den takma ve çekmede kilit) aynı anda sağlanamaz; şu anki tasarım ikisini de sağlamıyor.

### 3.5 Pürüzsüzlük ve köşe kusurları [KESİN, ORTA]

**Uç paylarında C¹ süreksizliği.** s_start noktasında düz pay biter. ω'(0) = 1 + 0.84 = 1.84 olduğu için profil düz bölgeden aniden 51.8° (dikey) ve 55.5° (yatay) eğimle kalkıyor. amp = 2.2'de 55.1° / 58.6°. Bu bir köşe; "smooth" iddiasına aykırı ve gerilme yoğunlaşması yaratır. Düzeltme: θ'ya sin²-rampa ile pencere uygulanmalı.

**Merkezde iğne deliği.** + kesişiminde dört karonun r_inner = 0.18 mm'lik köşeleri bir boşluk bırakıyor:
- Alan: (4 − π)·r² = **0.0278 mm²**
- Köşegen boyutu: 2r(√2 − 1) = **149 µm**

"< 15 µm dikiş" iddiasının **~10 katı**.

**Dış kenarda çentik.** Dikişin dış kenara çıktığı her noktada iki r_inner yayı **0.36 mm genişlik × 0.18 mm derinlik** bir çentik açıyor. Toplam 4 nokta, elle hissedilir.

**`quadrant_outline` köşe kaydırması.** r_c = r − 0.6d kullanılıyor; doğru içe kaydırma için r − d olmalı. Köşegende kaydırma d + 0.166d, yani köşelerde **%17 fazla** içe kayma.

### 3.6 "< 15 µm" toleransının fiziksel bütçesi [KESİN, YÜKSEK]

| Etken | Büyüklük |
|---|---|
| PC kalıp çekmesi değişkenliği (±%0.05 × 80 mm) | **±40 µm** |
| Karolar arası 10 K sıcaklık farkı (68 ppm/K × 80 mm) | **54 µm** |
| R = 25.5 mm bükümde dış kabuk alın dikişinin açılması (z/R × 2–5 mm kayma uzunluğu) | **≈ 80–200 µm** |
| Merkezdeki r_inner boşluğu | **149 µm** |

**Optik:** Florosilikonların kırılma indisi tipik olarak ≈ 1.38–1.40. PC ile n = 1.585'te eşleşen ticari bir florosilikon yok (fenil silikonlar bile ~1.53–1.55'te kalıyor).
- Arayüz yansıması ((1.585 − 1.39)/2.975)² ≈ **%0.43**, iki arayüzde ≈ %0.86. Koyu ekranda görünür bir çizgi.
- 61.3°'nin üstündeki açılarda tam iç yansıma oluşur; dikiş parlar.
- Çapraz-dosya çelişkisi: `leaf_geom` başlığı "zero-scratch" diyor; çıplak PC'nin kalem sertliği ≈ HB.

---

## 4. Diğer çapraz-dosya çelişkileri

| # | Çelişki | Sayısal karşılık |
|---|---|---|
| 1 | STL gövdesi tek parça `rounded_rect`: 4 karo, yapboz ve `b` modülü üretim verisinde yok | Üretilen STL iddia edilen ürünü temsil etmiyor |
| 2 | `leaf80` "tekil karo" dört köşesi R 6.35; `quadrant_outline` karosunda yalnızca **bir** köşe 6.35 | İki geometri farklı |
| 3 | Plan satırı "4x (w/2 × h/2)" | leaf80 → "4x(20×40)" ✗; leaf480 → "4x(160×240)" ✗ (40×80 karo ise 48 karo gerekir) |
| 4 | leaf480 gövde köşesi R = 14 ≠ karo varsayılanı r_outer = 6.35 [KOŞULLU] | Köşede (14 − 6.35)(√2 − 1) = **3.17 mm** gövde dışına taşma |
| 5 | `quadrant_outline` yalnızca tek dış köşeli 4 karo için; iç ve kenar karoları tanımsız | "ÇOKLU (+)" ölçeklenemez |
| 6 | 68 g / 4 karo, 6.4 cm³ PC karo = 7.68 g | Ortalama yoğunluk **2.66 g/cm³** |
| 7 | 12 Wh / 25.6 cm³ toplam hacim | Tüm yığın için 469 Wh/L; pil hacmi %50 ise **≈ 940 Wh/L**, ticari teknolojinin ötesinde |
| 8 | PEO elektrolit, "≤ 36.2 °C" | PEO oda sıcaklığında ≈ 10⁻⁶–10⁻⁷ S/cm, 60–80 °C ister. 15–25 W şarj ile çelişiyor |
| 9 | 25 W Qi2, %70–75 verim → 6–8 W kayıp | h ≈ 16 W/m²K, 0.0256 m² → ΔT ≈ 17 K → 25 °C ortamda ≈ 42 °C > 36.2 °C |
| 10 | Merkez Qi bobini (plan çizimi rq = 26.4 mm, Ø52.8) | **Dört dikişin hepsini kesiyor**; ayrılabilir karolarda sürekli sargı imkânsız |

---

## 5. Öncelikli düzeltme listesi

1. **Tek Z ekseni:** Ekran −1…+1, `b` dikey bacağı z = +1…+2, çubuk y = 36…37. Çubuk Z aralığını açınımdan türetin: z_back = +1 − r_i − (STEM_W − BA_stem).
2. **Büküm yarıçapını açık parametre yapın:** r_i ≥ 1t (metal) veya ≥ 6t (FPC). BA = (π/2)(r_i + Kt) açınım hesabını `_fold_uv_to_3d` içine koyun. u = 4'te sıfır yarıçaplı kat (crease) kullanmayın.
3. **Büküm boşaltma kesiği** v ≈ 11.7–16 bölgesine, **R ≥ 0.5 mm yuvarlatma** P = (13, 4.381) sivri ucuna.
4. **`bridge_pairs`:** Sabit `12.5` yerine u_int(d) kullanın. Üç şeridi Boolean birleşimle tek, su geçirmez kabuğa çevirin. İçe kaydırma katsayılarını tek bir d'ye bağlayın.
5. **Yapboz:**
   - (a) Ortak s ızgarasında f_L ≡ f_R assert'i ekleyin.
   - (b) Tarama yönü ve normal kuralına göre sign_dir'i tablodaki doğru satıra göre atayın.
   - (c) Gerçek kilit için teğet bileşen ekleyin; profil çok değerli (undercut) olmalı.
   - (d) Uç paylarında C¹ pencere uygulayın.
   - (e) amp değerini tek bir yerde tanımlayın (1.95 mi 2.2 mi).
6. **"< 15 µm", "n = 1.585 florosilikon", "1 mm'de USB-C/kamera", "R = 25.5 mm bükülen rijit modül"** iddialarını spesifikasyondan çıkarın ya da gerçek bütçeyle değiştirin.

## 6. Kesin hüküm için gereken kod

`_fold_uv_to_3d`, `_puzzle_lobe_1d`'nin `steps` sonrası gövdesi, `quadrant_puzzle_pair` ve `_build_structured_strip_3d` gönderilirse:
- §2.4-f'deki mesh girişimini kesin değerle ölçerim.
- §3.2'deki doğruluk tablosunda kodun hangi satıra düştüğünü belirleyip "eşleşiyor / X mm girişim var" diye kesin hüküm veririm.

Şu anki kesin sonuçlar:
- Profil, nasıl parametrelenirse parametrelensin, **çekme kilidi sağlayamaz**.
- `b` modülünün mevcut sayıları **birbiriyle ve ekranla tutarlı bir 3B geometri tanımlamıyor**.


---

## DALGA 2 · TAMAMI ESNEYEBİLEN POLİKARBONAT (`PC-PDMS`) MEKANİĞİ VE YAPBOZ KİLİT KULLANIM HATALARI (`BUDLUM-LEAF-ARGE-PLAN.md`, `HARDWARE/06, 08, 12, 16, 17`)

### W2_A3_GPT6_OPTICAL_SEAM_AND_TOUCH_AUDIT · Model: `gpt-6-sol` (Router: `coding-router-preview`, Başlangıç: `2026-10-12 14:36:06 +03`, Bitiş: `2026-10-12 14:41:38 +03`, Süre: `332.42 sn`, Uzunluk: `1,382` karakter)

## Denetim sonucu

Bu tasarımın en zayıf iddiası, **indisleri eşleştirilmiş 12 µm’lik bir dudağın dört ayrı ekranı hem optik olarak kesintisiz hem de dokunmatik olarak sürekli kılacağı** varsayımıdır. Verilen Fresnel hesabı, yalnızca temiz, kusursuz temas eden iki malzemenin **tek bir düz arayüzünde, dik gelişteki** yansımayı hesaplar. Aşınma, araya giren hava veya sıvı, OLED’lerin etkin alan sınırları ve ayrı dokunmatik matrislerin birleşimi bu hesabın dışındadır.

`HARDWARE/06` ve `HARDWARE/17` içerikleri verilmemiştir; dolayısıyla bunlardaki elektrot çizimi, tarama zamanlaması veya kalibrasyon hakkında doğrulanmış bir özellik varsayamam. Aşağıdaki bulgular verilen `HARDWARE/16` ve `HARDWARE/10` metinleri ile belirtilen fiziksel parametrelere dayanır.

### 1. Sıcaklık, aşınma ve kirlenmenin `+` çizgisine etkisi

**Temiz dikişte bile belirtilen yansıma yalnızca bir sınırın değeridir.** Verilen indislerle:

\[
R=\left(\frac{n_{\rm PC}-n_{\rm dudak}}{n_{\rm PC}+n_{\rm dudak}}\right)^2
=\left(\frac{0{,}001}{3{,}171}\right)^2
\approx9{,}95\times10^{-8}
\]

Bu, kesir olarak yansıma; yüzde olarak yaklaşık **%0,00000995**’tir. Dosyadaki `<%0,0001` sınırını karşılar, fakat toplam ekran yansıması, dikiş kontrastı veya «görünmezlik» ölçüsü değildir. İkinci sınır, kaplama, eğik ışık, yüzey pürüzlülüğü ve yansıyan ışığın yönü hesaba katılmamıştır.

Referans indislerin **

### W2_A1_OPUS_POLYCARBONATE_MECHANICS_AUDIT · Model: `claude-opus-5-5` (Router: `exo`, Başlangıç: `2026-10-12 14:36:01 +03`, Bitiş: `2026-10-12 14:42:29 +03`, Süre: `387.81 sn`, Uzunluk: `28,556` karakter)

# BUDLUM LEAF: Polimer, çoklu nötr düzlem ve esnek ekran mekaniği denetimi

**İncelenen dosyalar:** `BUDLUM-LEAF-ARGE-PLAN.md` (v2.0 / L.5.0), `HARDWARE/12-THE-BEND-LAW.md`, `HARDWARE/16-THE-SCREEN-PART-BY-PART.md`
**Yöntem:** Dosyalardaki her sayıyı yeniden hesapladım: kinematik gerinim, shear-lag (kayma gecikmesi), viskoelastik davranış, difüzyon ve geçirgenlik, kütle ve kalınlık toplamları, optik. Malzeme değerlerinde tipik literatür aralıklarını kullandım. Varsayım yaptığım yerleri ayrıca belirttim. Sonuçlar mertebe kestirimidir. Kesin değerler gerçek malzeme verisi ve fiziksel testle doğrulanmalıdır.

---

## 0 · Yönetici özeti: kritik bulgular

| # | Bulgu | Ciddiyet | Kısaca |
|---|---|---|---|
| K1 | OCA kayma miktarı en az 3 kat, kinematik olarak 15 kat düşük hesaplanmış | **Kritik** | `0.18 mm` değil. Gerçek uç kayması `0.5–2.7 mm` aralığında. `γ ≈ 12–68`, yani `%1200–6800` |
| K2 | `0.35%` kabuk gerinimi ile `G = 0.035 MPa` ayrıştırma birlikte sağlanamaz | **Kritik** | Shear-lag boyu yaklaşık `14–18 mm`. Panelin ortası bağlı kalır, kabukta gerinim `~%3+` olur |
| K3 | Çekirdek gerinimi 10 kat hatalı | **Kritik** | `0.21%` yazılmış. Doğrusu `0.53/25.5 = 2.08%` |
| K4 | T-OLED, AgNW ve PDLC için yazılan "kendi nötr ekseni" gerinimleri fiziksel değil | **Kritik** | Bu katmanların arasında kayma katmanı yok. Gerçek değerler `%2.1–3.1` |
| K5 | Polikarbonat altlık üzerine LTPO TFT üretilemez | **Kritik** | PC'nin Tg'si `~145 °C`. LTPS/oksit TFT süreci `300–450 °C` ister |
| K6 | Yığında hiçbir nem/oksijen bariyeri (TFE, bariyer film) yok | **Kritik** | PC'nin WVTR'si OLED ihtiyacından yaklaşık `10^7` kat yüksek. İlk kara noktalar saatler içinde çıkar |
| K7 | "Sıfır çerçeve" (bezel) şartı TFE kenar sızdırmazlığıyla çelişir | **Kritik** | TFE için `0.5–1.5 mm` dam/örtüşme payı gerekir |
| K8 | Dosya 16'nın kütle toplamı `72.0 g`, `68.0 g` değil | Yüksek | Aritmetik hata |
| K9 | Dosya 16'nın katman toplamı `2.13–2.15 mm`, `2.00 mm` değil | Yüksek | Geometri sığmıyor |
| K10 | "Sıfır rijit bölge" iddiası Ti hub, N52H mıknatıs, LLZO seramik, Mu-metal ve nanokristal şeritle çelişir | Yüksek | Dosyalar arası çelişki |
| K11 | "Fenil-floro-silikon `n = 1.585`" kimyasal olarak tutarsız | Yüksek | Flor kırılma indisini düşürür |
| K12 | Çift taraflı Mu-metal ve grafit kalkan Qi kuplajını keser | Yüksek | Deri kalınlığı (skin depth) yaklaşık `8 µm`, kalkan `50 µm` |
| K13 | PC, `0.35–0.38%` gerinimde çevresel gerilme çatlağına (ESC) açık | Yüksek | Güneş kremi, el kremi ve alkol bu eşiğin altında bile çatlatabilir |
| K14 | Batarya enerji yoğunluğu ve PEO çalışma penceresi fiziksel sınırların dışında | Yüksek | Hücre düzeyinde `~1060 Wh/L` isteniyor. PEO `>3.8 V`'ta oksitlenir ve oda sıcaklığında iletkenliği zayıftır |

---

## 1 · Temel kinematiğin yeniden hesabı

### 1.1 Dosyaların kendi sayıları

- Monolitik `2.00 mm` levhada dış lif: `ε = (t/2)/R = 1.00/25.5 = %3.92` ✔. "3.92%" buradan geliyor.
- Kendi ekseni etrafında bükülen `0.18 mm` kabuk: `0.09/25.5 = %0.353` ✔
- Dosya 16'daki `0.20 mm` kabuk: `0.10/25.5 = %0.39`. Dosya 16 `%0.38` diyor, yaklaşık doğru. Ancak bu, dosya 12'deki `0.18 mm` değeriyle çelişiyor.
- `R = 15 mm`'de `0.09/15 = %0.60`. Dosya `%0.58` yazmış, küçük bir hata.

### 1.2 Tablodaki her katman için "kendi nötr ekseni" varsayımı

Dosya 12'nin gerinim tablosu her katmanın kendi ekseni etrafında büküldüğünü varsayıyor:

| Katman | Dosyanın kullandığı mesafe | Sorun |
|---|---|---|
| T-OLED `130 µm` | `65 µm` → `0.255%` | Ancak iki yanında da kayma katmanı varsa geçerli. T-OLED'in altında AgNW'ye doğrudan bağ var. |
| AgNW `40 µm` | **`50 µm`** → `0.20%` | 40 µm'lik bir katmanın yarı kalınlığı 20 µm'dir. 50 µm geometrik olarak imkânsız. |
| PDLC `80 µm` | `45 µm` → `0.18%` | Yarı kalınlık 40 µm olmalı. Ayrıca bu katman da ayrışmış değil. |
| Çekirdek `1060 µm` | "nötr düzlem" → **`0.21%`** | Çekirdeğin yüzeyi z = ±0.53 mm'de. `0.53/25.5 = %2.08`. Hata 10 kat. |

11 katmanın içinde yalnızca 2 kayma katmanı (OCA) var. Dolayısıyla mekanik olarak yalnızca **üç kiriş** oluşur: üst kabuk, iç blok (`1.56 mm`) ve alt kabuk. İç blok (T-OLED, AgNW, PDLC, çekirdek, PDLC, AgNW, T-OLED) tek bir kiriş gibi davranır ve nötr ekseni z = 0'dadır. Gerçek gerinimler şöyledir:

| Katman | z aralığı (mm) | Gerçek gerinim (R = 25.5 mm) | Dosyadaki sınır | Durum |
|---|---|---|---|---|
| Çekirdek (LLZO/PEO) | 0 – 0.53 | **%2.08** | %1.5 | **Aşıyor.** LLZO seramiğinin kırılma gerinimi `~%0.1–0.2` |
| PDLC | 0.53 – 0.61 | **%2.39** | %2.5 | Sınırda, yorulmada çöker |
| AgNW/IZO (dosya 16'da ITO) | 0.61 – 0.65 | **%2.55** | %2.0 | **Aşıyor.** ITO'da çatlama `~%1` |
| T-OLED + (olması gereken) TFE | 0.65 – 0.78 | **%3.06** | %1.2 | **2.5 kat aşıyor.** Piksel kaybı |

**Sonuç:** "Çoklu nötr düzlem" yalnızca iki kabuğu kurtarır, o da hayalî bir OCA sayesinde (bkz. §2). Ekranın kendisi, yani TFT, OLED, TFE ve iletken katmanlar ile batarya çekirdeği **ayrışmamıştır** ve gerinim sınırlarının 1.7–20 katı üzerindedir.

### 1.3 Bükme kuvveti: "48 kat azalma, 1.4 N"

Eğilme rijitliği kalınlığın küpüyle ölçeklenir:

- Tam bağlı yığın: `t³ = 2.00³ = 8.00`
- İki kabuk ayrışmış, iç blok bağlı: `2·0.18³ + 1.56³ = 0.0117 + 3.796 = 3.81`
- **Azalma oranı: ~2.1 kat, 48 kat değil.** 48 kat elde etmek için onlarca kayma katmanı gerekir.

Kuvvetin büyüklüğü (b = 80 mm, iç blok için ortalama E ≈ 1 GPa varsayımıyla; LLZO bunu artırır):

- `EI_iç = 1e9 × 0.08 × (1.56e-3)³ / 12 ≈ 2.5e-2 N·m²`
- `M = EI/R = 2.5e-2 / 0.0255 ≈ 0.99 N·m`
- 50 mm kol ile parmak kuvveti `≈ 20 N`.

1.4 N'luk kuvvet, eşdeğer olarak yalnızca `~0.57 mm` kalınlığında monolitik bir PC levhayı `R = 25.5 mm`'ye büker. **İddia yaklaşık 15 kat iyimser.** Kabukların ayrışması zaten sorun değildi. Rijitliği belirleyen, 1.56 mm'lik ayrışmamış iç bloktur.

---

## 2 · Soru 1: OCA kayma gerinimi, sürünme, delaminasyon ve optik bulanıklık

### 2.1 Kullanıcının hesabı doğru, ama gerçek durum daha kötü

Sizin hesabınız `γ = 0.18/0.04 = 4.5` (%450) aritmetik olarak doğru. Fakat dosyadaki `0.18 mm` kayma değerinin kendisi yanlış. Bu sayı muhtemelen kabuk kalınlığının (`0.18 mm`) yanlışlıkla kayma sütununa yazılmasından geliyor.

**Kinematik (tam ayrışma) durumu.** Kabuk alt yüzeyi ile iç blok üst yüzeyi arasındaki gerinim farkı:

```
Δε = κ · (0.78 + 0.09) mm = 0.87 / 25.5 = 3.41 %
```

Kayma, bükülme merkezinden uca doğru doğrusal olarak birikir: `δ(x) = Δε · x`

| Bükme yönü | Yarı uzunluk | Uç kayması δ | γ = δ / 0.04 mm |
|---|---|---|---|
| 160 mm boyunca (dosyanın "full wrap" senaryosu; 160/25.5 = 6.27 rad ≈ 359°) | 80 mm | **2.73 mm** | **68 (%6800)** |
| 80 mm boyunca | 40 mm | **1.36 mm** | **34 (%3400)** |

Dosyanın kendi `0.18 mm` değeri, ancak bükülen bölgenin yalnızca `0.18/0.0341 ≈ 5.3 mm` uzunluğunda olması hâlinde geçerlidir. Bu, "%100 tam alan bükülme" iddiasıyla doğrudan çelişir.

### 2.2 Kayma gerinimini uzama sınırıyla karşılaştırma

Dosya OCA için "%400 uzama" sınırı veriyor. Bu bir çekme sınırıdır. Basit kaymada asıl germe oranı şöyle hesaplanır:

```
λ₁ = γ/2 + √(1 + γ²/4)
```

| γ | λ₁ | Mühendislik uzaması | %400 sınırına göre |
|---|---|---|---|
| 4.5 (sizin hesabınız) | 4.71 | **%371** | Tek bükmede sınırın %93'ü. 200 000 çevrimde yorulma kesin |
| 12–16 (shear-lag, aşağıda) | 12–16 | %1100–1500 | 3–4 kat aşım |
| 68 (kinematik) | ~68 | ~%6700 | 17 kat aşım, kohezif yırtılma |

Yani dosyanın kendi `0.18 mm` değeriyle bile OCA ilk bükmede kopma sınırının %93'üne çıkıyor.

### 2.3 Shear-lag analizi: ayrışma ile kabuk gerinimi aynı anda sağlanamaz

OCA'nın kabuğu gerçekten ayrıştırıp ayrıştırmadığını shear-lag parametresi belirler (birim genişlik başına, bükme terimi dahil):

```
λ² = (G/tₐ) · [ 1/(E₁t₁) + 1/(E₂t₂) + d²/(E₁I₁ + E₂I₂) ]

G/tₐ   = 0.035e6 / 0.04e-3                = 8.75e8 Pa/m
E₁t₁   = 2.3e9 × 0.18e-3                  = 4.14e5 N/m   (PC)
E₂t₂   ≈ 1e9 × 1.56e-3                    = 1.56e6 N/m   (iç blok, varsayım)
d      = 0.91 mm (kabuk ağırlık merkezi ile z = 0 arası)
ΣEI    ≈ 0.317 N·m
→ λ²   ≈ 8.75e8 × 5.67e-6 ≈ 4.96e3  →  1/λ ≈ 14 mm   (varsayımlara göre 14–18 mm)
```

- 160 mm yönünde `λL/2 ≈ 5.6`, 80 mm yönünde `≈ 2.8`.
- **Sonuç:** Kabuk yalnızca uçlardaki `~14–28 mm` bölgede ayrışır. Panelin ortasında OCA yükü aktarır ve kabuk yeniden iç bloğa bağlanır. Ortadaki kabuk dış lif gerinimi `%0.35` değil, tam bağlı değere (`%3.5–3.9`) yaklaşır.
- Uçtaki maksimum kayma gerilmesi: `τ_max ≈ (G/tₐ)·Δε/λ ≈ 8.75e8 × 0.0341 / 70 ≈ 0.42–0.55 MPa`. Buna karşılık gelen `γ_max ≈ 12–16` ve uç kayması `≈ 0.5–0.6 mm`.

**Temel ikilem:**

- OCA yeterince yumuşaksa kabuğu ayrıştırır. O zaman milimetre mertebesinde kayma ve `γ > 30` oluşur, OCA yırtılır.
- OCA yırtılmayacak kadar sertse kabuk bağlı kalır. O zaman kabuk gerinimi `%3–4` olur, `%0.35` değil.

`G = 0.035 MPa` ve `40 µm` ile iki hedef aynı anda sağlanamaz.

### 2.4 Uzun süre bükülü kalma (cep, kılıf, saatlerce bekleme)

**a) Statik tutma gerilmesi.** Standart PSA "holding power" testi (PSTC-107: 25×25 mm alanda 1 kg) yaklaşık `τ ≈ 15.7 kPa` uygular. Leaf'teki OCA'nın kenar gerilmesi:

- Dosyanın kendi γ = 4.5 değeriyle: `τ = 0.035 × 4.5 = 158 kPa`, testin 10 katı.
- Shear-lag tahminiyle: `0.42–0.55 MPa`, testin 27–35 katı.

Silikon PSA'lar 1 kg testinde saatler ile günler arasında dayanır. 10–35 kat gerilmede **dakikalar ile saatler içinde kohezif akma ve sürünme beklenir.**

**b) Sürünme ve gerilme gevşemesi.** Silikon OCA viskoelastiktir (1 Hz'de tipik tanδ ≈ 0.2–0.5; tam çapraz bağlı olmayan sol fazı uzun sürede akar). 10³–10⁵ s ölçeğinde G(t) başlangıç değerinin `%30–70`'ine düşebilir. Vücut sıcaklığında (32–37 °C) bu süreç hızlanır. Bunun sonucu:

- Saatlerce bükülü kalan cihazda OCA kaymayı **"kabul eder"**, iç gerilme gevşer.
- Cihaz düzleştirildiğinde kabuk ile çekirdek arasında **ters yönde artık kayma** kalır. Dosyanın kendi γ = 4.5 değeriyle ve yalnızca %30 kalıcı akma varsayımıyla uç ofseti `~54 µm` olur. Gerçekçi 0.5–2.7 mm kaymada bu `150–800 µm` mertebesine çıkar.
- Asimetrik artık kayma, cihazı bimetal gibi **kalıcı olarak kıvırır**. B-3'teki "`160 mm` üzerinde `0.05 mm` düzlük" şartı ve B-2'deki "kalıcı deformasyon > `0.05 mm` yok" şartı fiziksel olarak sağlanamaz.
- PEO çekirdek oda sıcaklığında Tg'nin (`~-60 °C`) çok üstündedir ve kendisi de sürünür. Çekirdek kalıcı şekil aldığında OCA bunu kabuğa aktarır. Kıvrılma iki kaynaktan birden gelir.

**c) Kenar delaminasyonu.** Shear-lag çözümünde kayma gerilmesi **serbest kenarda maksimumdur**. Kenarda buna bir de soyma (peel, σ_zz) gerilmesi eklenir. Sonuçlar:

- Çekme tarafında kenar soyma çatlağı başlar, basma tarafında ise kabuk kenarda "tünel" açar (buckle-delamination).
- Kenar kayması 0.5–2.7 mm iken `R = 0.65 mm` yuvarlatılmış kenar, IP68 contası ve yan duvardan geçen kenar iletkenleri **her bükmede milimetre mertebesinde ileri geri sürtünür**. B-8'deki IP68 şartı birkaç bin çevrimden sonra tutmaz.
- **Isıl kayma bunlara eklenir.** PC'nin CTE'si `~65–70 ppm/K`, iç bloğunki tahminen `~20–40 ppm/K`. `ΔT = 40 K` için (−10 ile +45 °C arası, B-7) uç kayması `30e-6 × 40 × 80 mm ≈ 0.1 mm` ve `γ ≈ 2.4`. Yani cihaz bükülmeden, yalnızca sıcaklık değişiminden OCA'da %240 kayma oluşur.

**d) Optik bulanıklık (haze) ve mura.**

- Yüksek kayma ve kenardaki hidrostatik çekme, PSA'da **kavitasyon ve fibrilasyon** başlatır. Mikro boşluklar ışığı saçar ve kenarlarda beyazlaşma bandı oluşur. Faz 1'deki `haze < %0.6` hedefi ilk statik bekletme testinde aşılır.
- Silikon su buharına son derece geçirgendir (§3.4). Nem, mikro boşluklarda yoğuşur ve sıcak-nemli ortamda OCA bulanıklaşır.
- **İndis iddiası:** Saf PDMS'in kırılma indisi `n ≈ 1.41`, yüksek fenilli siloksanlarınki pratikte `≈ 1.53–1.55`. `n = 1.585` ve `G = 0.035 MPa` birlikte çelişkilidir, çünkü fenil oranı yükseldikçe Tg ve modül de yükselir. Gerçekçi `n = 1.41–1.50` ile PC arayüzünde normal gelişte `R = ((1.586−1.41)/(1.586+1.41))² ≈ %0.35` yansıma olur. Kayma kaynaklı mikro-dalgalanma bu arayüzde **Newton halkaları ve mura** olarak görünür.

**e) Ek-yeri (seam) dudağına etkisi.** Karolar ayrı modüller olduğundan (ve "< 3 s swap" iddiasına göre değiştirilebildiğinden) her karonun kabuğu kendi merkezine göre kayar. Ek yerinde komşu iki karonun kabuk uçları ters yönde `~1.4 mm` (shear-lag tahminiyle `~0.5 mm`) hareket eder. **`12 µm`'lik dudak milimetre mertebesindeki bu harekete dayanamaz.** Ya yırtılır ya da ek yerinde görünür bir aralık açılır. "`<2.5 µm` Z-adımı" ve "Fresnel R < %0.0001" iddiaları bu kinematikle bağdaşmıyor.

**f) PC kabuğun kendisi.** OCA kabuğu ayrıştıramadığı için orta bölgede kabuk gerinimi `%3–4` olur. Bu da `σ ≈ 50–60 MPa` demektir ve PC'nin akma gerilmesine (`~60–65 MPa`) çok yakındır. PC'nin 2×10⁵ çevrimdeki yorulma dayanımı tipik olarak `~20–25 MPa` mertebesindedir, yani B-1 sağlanamaz. Saatlerce bükülü kalmada bu gerilme düzeyinde **sürünme ve kırazlanma (crazing)** başlar. Dosya PC-PDMS için "`> %30` elastik uzama" diyor, oysa gerçek akma gerinimi `~%6–7`'dir ve uzun süreli tersinir sınır `~%1–2`'dir. Dosya 12'nin kendi tablosu da "`6.0–30.0%`" yazarak bu iddiayla çelişiyor.

### 2.5 Soru 1'in yanıtı

**Evet, üçü de olur, hatta dosyanın kendi sayılarıyla bile.**

- **Sürünme:** Statik bekletmede OCA kenar gerilmesi holding-power testinin 10–35 katı. Dakikalar ile saatler içinde akma, ardından kalıcı kıvrılma.
- **Delaminasyon:** Kenarda kayma ve soyma gerilmelerinin toplamı silikon PSA'nın kohezif ve adhezif dayanımına (`~0.3–1 MPa`) ulaşıyor. Termal çevrim ve 200 000 bükme ile ilerleyen kenar ayrılması bekleniyor.
- **Optik bulanıklık:** Kavitasyon, nem yoğuşması ve indis uyumsuzluğundan kaynaklanan mura.

Tasarımın asıl kusuru bunlardan da derin: Ayrışma, ekranı (OLED/TFE/TFT) ve bataryayı hiç korumuyor. Yalnızca dış PC kabuğu koruyor, o da shear-lag nedeniyle yalnızca uç bölgelerde.

---

## 3 · Soru 2: PC geçirgenliği, kara nokta (dark spot) süresi ve TFE

### 3.1 Bariyer ihtiyacı ile PC arasındaki fark

| Büyüklük | PC (tipik, 38 °C / %90 RH) | 0.18 mm PC | OLED gereksinimi | Fark |
|---|---|---|---|---|
| WVTR | `~3–5 g·mm/(m²·gün)` | **`~17–28 g/m²·gün`** (25 °C / %50 RH'de `~3–5`) | **`≤ 10⁻⁶ g/m²·gün`** | **~10⁷ kat** |
| OTR | `~50–110 cm³·mm/(m²·gün·atm)` | `~300–600 cm³/m²·gün·atm` | `≤ 10⁻⁵ cm³/m²·gün·atm` | ~10⁷–10⁸ kat |

Dosya 12'nin 11 katmanında ve dosya 16'nın 10 parça grubunda **TFE, bariyer film, ince cam (UTG) veya Al₂O₃/SiNx katmanı hiç yok.** T-OLED "PC film üzerinde" ve üstü de OCA ile PC'ye bakıyor, yani OLED'in iki yüzü de PC ile çevrili.

### 3.2 Katot tüketimi: kaç saat, kaç gün?

T-OLED'de yarı geçirgen katot olarak tipik `~10–15 nm` Mg:Ag kullanılır. Bu, en hassas katot türüdür.

```
Mg kütlesi (10 nm, 1 m²) = 10e-9 m × 1.74e6 g/m³        = 0.0174 g/m²   → 7.2e-4 mol
Mg + 2H₂O → Mg(OH)₂ + H₂ → gereken su = 1.43e-3 mol × 18 = 0.026 g/m²
```

| Senaryo | Su akısı | Katot eşdeğeri suyun gelme süresi |
|---|---|---|
| 25 °C / %50 RH, 0.18 mm PC | `~4 g/m²·gün` | `0.026/4 gün ≈ 9 dk` (+ difüzyon gecikmesi) |
| 38 °C / %90 RH (cep, ter) | `~22 g/m²·gün` | `≈ 1.7 dk` (+ gecikme) |

**Difüzyon gecikmesi (lag time):** Sudaki PC difüzyon katsayısı `D ≈ 5–8×10⁻¹² m²/s`.

```
t_lag = L²/(6D) = (0.18e-3)² / (6 × 6e-12) ≈ 900 s ≈ 15 dk
Kararlı akıya ulaşma ≈ L²/D ≈ 1.5 saat
```

**PC'nin içindeki su deposu, en kritik nokta:** PC, %50 RH'de denge durumunda `~%0.15` (doygunlukta `~%0.35`) ağırlıkça su tutar.

```
0.18 mm PC kabuk : 1.2e6 g/m³ × 1.8e-4 m × 0.0015 ≈ 0.32 g/m²
0.13 mm PC altlık (OLED'in hemen altında) ≈ 0.23 g/m²
```

Bu, katodu tümüyle oksitlemeye yetecek suyun **10–20 katı** demektir ve montaj anında zaten içeridedir. Dış dünyayla bağlantı kesilse bile OLED'in doğrudan altındaki PC altlık suyunu katoda verir. Vakum buharlaştırma sırasında PC'den gelen gaz çıkışı, üretim hattında kara nokta tohumları da oluşturur.

**Zaman çizelgesi (mertebe kestirimi, kapsüllenmemiş ve PET/PC ile korunmuş OLED literatürüyle uyumlu):**

| Durum | İlk kara noktalar | Belirgin parlaklık / alan kaybı | Kullanılamaz |
|---|---|---|---|
| Dosyada yazıldığı gibi (TFE yok, PC/OCA ile çevrili) | **dakikalar – birkaç saat** | **~1 gün** | **~1–3 gün** (38 °C / %90 RH'de saatler) |
| TFE var ama bükmeyle çatlamış (§3.5) | ilk bükme günleri | çatlak hatları boyunca karanlık çizgiler, haftalar | haftalar – birkaç ay |
| TFE sağlam ama kenarı açıkta ("0 bezel") | kenarlarda günler | kenardan içeri ilerleyen ölü bant, haftalar | aylar |

### 3.3 Diğer neme duyarlı katmanlar

- **AgNW:** Nem ve kükürtle (H₂S, insan teri) sülfürleşir, telin kesiti incelir ve ΔR hızla artar. "`<%0.8` ΔR" şartı birkaç hafta içinde kaybedilir.
- **PEO-LiBOB:** Elektrolit çok higroskopiktir. LiBOB hidrolize olur ve iletkenlik düşer.
- **LLZO:** Nem ve CO₂ ile Li⁺/H⁺ değişimi ve Li₂CO₃ yüzey tabakası oluşur, arayüz direnci büyür. Li metal anot kullanılıyorsa su ile reaksiyon H₂ üretir. Bu durumda B-9'daki "`0.0 ppm` gaz çıkışı ve `0.0%` şişme" iddiası tutmaz.
- **PDLC:** Sıvı kristal ve polimer arayüzü nemle bozulur. Sürme gerilimi ve haze kayar.

### 3.4 Yanal sızma kanalı olarak silikon OCA

PDMS'in su buharı geçirgenliği PC'den yaklaşık 10 kat (`~10⁴ Barrer` mertebesi), difüzyon katsayısı ise `D ≈ 1–2×10⁻⁹ m²/s`'dir.

```
1 mm yanal ilerleme  : L²/D ≈ 1e-6 / 1e-9   ≈ 17 dk
20 mm (karo yarı eni): (0.02)² / 1e-9       ≈ 4.6 gün
```

Yani **40 µm'lik OCA düzlemi birkaç gün içinde ortam nemine doyar** ve nemi T-OLED'in tüm yüzeyine yanal olarak dağıtır. IP68 sıvı suyu engeller, su buharını engellemez. B-8 su buharını hiç test etmiyor.

### 3.5 TFE eklense bile R = 25.5 mm'de çatlar mı?

Kısa yanıt: **mevcut yığın yerleşimiyle evet.**

- TFE, OLED'in üstünde, yani iç bloğun dış yüzeyinde (`z ≈ 0.78 mm`) yer alır. Altında kayma katmanı yoktur. Gerçek gerinim `0.78/25.5 = %3.06`.
- Kırılma başlangıç gerinimi (tipik literatür aralığı): PECVD SiNx (`~0.5–1 µm`) için `%0.3–1.0`, ALD Al₂O₃ (`20–50 nm`) için `%0.5–1.0` (çok ince filmde `~%1.5`'e kadar). 2×10⁵ çevrimde yorulma bu değerleri `~%60–70`'e indirir.
- **Güvenlik payı negatif, yaklaşık 3–6 kat aşım.** Çekme tarafında bükme eksenine dik **kanal çatlakları** oluşur ve tüm alan bükülebildiği için çatlaklar panelin tamamına yayılır. Basma tarafında `%1–2`'den itibaren TFE kabarıp ayrılır (buckle-delamination).
- Dosyanın kendi `%0.25` değeri bile (yalnızca T-OLED iki yandan ayrışmış olsaydı geçerli olurdu) SiNx için sınırın yarısına denk gelir. Al₂O₃ ise sıcak ve nemli ortamda suda çözünür (hidratasyon/korozyon). Bu yüzden saf Al₂O₃ yerine Al₂O₃/ZrO₂ veya Al₂O₃/TiO₂ nanolaminat ya da SiNx/organik/SiNx yığını gerekir.
- **Sıfır çerçeve çelişkisi:** TFE'nin kenarında organik katmanı durduran bir dam ve inorganik katmanların örtüşmesi gerekir. Bu kenar payı tipik olarak `0.5–1.5 mm`'dir. Dosya 16 ise ek yeri çerçevesini `0.00 mm` olarak tanımlıyor (karo başına panel `39.8` mm, karo `40.0` mm, yani kenar başına `0.1 mm`). **Bu iki şart birlikte sağlanamaz.** TFE eklenirse ya ek yerinde `1–3 mm`'lik ölü bant oluşur ya da TFE kenarı açık kalır ve §3.2'deki "kenardan ilerleyen ölü bant" senaryosu başlar.

### 3.6 Daha temel sorun: TFT polikarbonat üzerinde üretilemez

- LTPS sürecinde dehidrojenasyon `~450 °C`, oksit TFT tavlaması `~300–350 °C` ister. LTPO ikisini birden içerir.
- PC'nin Tg'si `~145–150 °C`, PC-PDMS'inki biraz daha düşüktür. Endüstri bu yüzden poliimid kullanır (Tg `> 350 °C`, CTE `~3–10 ppm/K`).
- CTE uyumsuzluğu: PC'nin `~70 ppm/K` CTE'si, `ΔT = 20 K` işlem dalgalanmasında 80 mm üzerinde `0.11 mm`'lik genleşme verir. Bu, 508 ppi'de (piksel adımı 50 µm) **~2 piksellik hizalama hatası** demektir ve fotolitografi katman hizalaması tutmaz.
- **"%100 polikarbonat" ve "LTPO T-OLED on PC film" ifadeleri aynı cihazda bir arada olamaz.**

### 3.7 Soru 2'nin yanıtı

- Dosyada yazıldığı hâliyle (bariyer yok) ilk kara noktalar **saatler içinde** çıkar, cihaz **~1–3 günde** kullanılamaz hâle gelir. Sıcak ve nemli ortamda bu süre saatlere iner.
- PC'nin kendi içindeki su, dış bariyer olsa bile katodu öldürmeye yeter.
- TFE eklense bile mevcut yerleşimde `%3`'lük gerinimle çatlar ve sıfır çerçeve şartı TFE'nin kenar sızdırmazlığını imkânsız kılar.

---

## 4 · Dosyalar arası çelişkiler ve diğer fiziksel hatalar

### 4.1 Aynı parça için farklı sayılar

| Parametre | ARGE / Dosya 12 | Dosya 16 |
|---|---|---|
| Dış kabuk | `0.18 mm` PC-PDMS | `0.20 mm` BPA'sız PC (+`8 µm` sert kaplama) |
| OCA | `0.04 mm`, `G = 0.035 MPa` | `0.05 mm`, `G = 0.08 MPa` |
| T-OLED | `0.13 mm` | `0.14 mm` |
| Şeffaf iletken | AgNW/**IZO** | AgNW/**ITO** (ITO `~%1`'de çatlar) |
| PDLC | 2 adet × `0.08 mm` | 1 adet × `0.09 mm` |
| Çekirdek | `1.06 mm` | `1.08 mm` |
| Kabuk gerinimi | `%0.35` | `%0.38` |
| Çevrim ömrü | `200 000` | `10 000+` (20 kat fark) |
| (0,0) hub | PC-PDMS + `80 µm` NiTi | Grade-5 Ti + 8 Ti pim + 24 adet N52H mıknatıs |
| Kalkan | listede yok | grafen + Mu-metal (`0.05 mm` × 2) |

### 4.2 Toplam kalınlık (dosya 16)

```
2×0.20 + 2×0.05 + 2×0.14 + 2×0.04 + 1×0.09 + 2×0.05 + 1.08
= 0.40 + 0.10 + 0.28 + 0.08 + 0.09 + 0.10 + 1.08 = 2.13 mm  (+0.016 sert kaplama = 2.146 mm)
```

**Sonuç `2.00 mm`'ye sığmıyor.** Ayrıca hiçbir listede TFT backplane, TFE, polarizör veya katmanlar arası yapıştırıcılar ayrı kalem olarak yok. Bunlar eklenirse fark büyür.

### 4.3 Toplam kütle (dosya 16)

```
12.8 + 1.6 + 6.8 + 1.6 + 1.9 + 3.4 + 0.2 + 2.9 + 6.4 + 34.4 = 72.0 g   (≠ 68.0 g)
```

- **Kabuk kütlesi:** `8 × 40 × 80 × 0.20 mm³ = 5.12 cm³`. PC yoğunluğu 1.20 olduğundan kütle `≈ 6.1 g` olmalı. 12.8 g için yoğunluğun `2.5 g/cm³` olması gerekir, bu da camın yoğunluğudur.
- **Batarya:** `4 × 35 × 75 × 1.08 = 11.34 cm³` hacimde 12 Wh, yani **`~1060 Wh/L`** ve `349 Wh/kg`. Lazerle kesilen ızgara aralıkları (örneğin 0.3 mm kerf) aktif alanı `~%77`'ye düşürür ve aktif hacimdeki yoğunluk `~1370 Wh/L` olur. Bu değer bugünkü ticari hücrelerin (`~750–800 Wh/L`) ve laboratuvar katı hal hücrelerinin üzerindedir. Buna 1680 mikro hücrenin her birinin akım toplayıcısı, bağlantıları ve kapsülasyonu da eklenecek.
- **PEO penceresi:** PEO `~3.8–4.0 V` üzerinde oksitlenir. 12 Wh / 3200 mAh oranı `3.75 V` nominal gerilim demektir ve bu NMC katot gerektirir. PEO ise pratikte LFP (`~3.2–3.4 V`) ile sınırlıdır. Ayrıca PEO'nun iyonik iletkenliği `~10⁻⁶–10⁻⁵ S/cm` (oda sıcaklığı) olduğu için `60–80 °C` çalışma sıcaklığı ister. Bu da cihazın "`≤ 36.2 °C`" şartıyla doğrudan çelişir.

### 4.4 "Sıfır rijit bölge" iddiasıyla çelişen bileşenler

| Bileşen | Neden sorunlu |
|---|---|
| LLZO | Garnet tipi bir seramiktir, kırılma gerinimi `~%0.1–0.2`. Çekirdekte gerçek gerinim `%2.08`, yani 10–20 kat aşım |
| Grade-5 Ti hub ve pimler | E = 114 GPa. EI_seam/EI_tile = 1.00 iddiası Ti ile sağlanamaz |
| 24 adet N52H | Sinterlenmiş NdFeB gevrek ve rijittir |
| Mu-metal | Plastik gerinimde manyetik geçirgenliğini kaybeder (hidrojen tavı gerektirir). N52H'nin (Br ≈ 1.4 T) yakınında doyuma gider (`~0.75 T`) ve kalkan işlevi biter |
| FeSiBCuNb nanokristal (60 µm) | Tavlandıktan sonra çok gevrektir. Esnek hâle getirmek için kırıklı (flake) işlem uygulanırsa µr `12 000`'den `~1 000–3 000`'e düşer. Çekirdekte `%2`'lik gerinimde kırılır |

### 4.5 Optik çelişkiler

- **Floro-silikon ile `n = 1.585`:** Flor indisi düşürür (floro-silikon `n ≈ 1.38–1.40`). Fenil ve flor zıt yönde etki eder. Fresnel aritmetiği (`9.9e-8`) doğru, ancak girdisi gerçekçi değil.
- **Termo-optik sapma:** PC'de `dn/dT ≈ −1.1×10⁻⁴ /K`, silikonda `≈ −(3.5–4.5)×10⁻⁴ /K`. 20 ile 45 °C arasında `Δn ≈ 7×10⁻³`. B-6'daki "indis kayması > 0.001 yok" şartını malzemenin kendi fiziği ihlal ediyor. Dağılım farkı da var (PC Abbe sayısı `~30`, fenil silikon `~35–45`), mavide uyumsuzluk büyür. Sonuç olarak ek yeri belirli açılardan görünür.
- **Ek yeri piksel boşluğu:** Komşu panellerin aktif alanları arasında yaklaşık `0.2 mm` boşluk kalır. Bu 50 µm adımda ~4 piksel eder. 30 cm'de 1 yay dakikası `≈ 87 µm` olduğundan `200 µm`'lik koyu çizgi gözle görülür. Ayrıca `79.6 × 159.6 = 12 704 mm²`, dosyada yazan `12 696` değil.
- **Çift kırılma:** PC'nin gerilme-optik katsayısı `C ≈ 70–80×10⁻¹² Pa⁻¹`. Saf bükmede kabuğun içindeki çekme ve basma büyük ölçüde birbirini götürür. Ancak shear-lag'den gelen membran gerilmesi ve ekstrüzyon artık gerilmesi net gecikme oluşturur. `σ = 8 MPa` ve 0.18 mm için yaklaşık `115 nm` gecikme hesaplanır, bu da çeyrek dalgaya yakın bir değerdir. Polarize güneş gözlüğüyle bakıldığında gökkuşağı benzeri mura görülür.
- **`0.65 mm` kenar yarıçapı ve aktif alan:** Aktif alanın genişliği `79.6 mm`, yani yuvarlatılmış kenarın içine taşıyor. Bu bölgede görüntü bozulur. Ayrıca `R = 6.35 mm`'lik köşeler dikdörtgen bir aktif alanla bağdaşmaz.

### 4.6 Elektromanyetik ve ısıl hatalar

- **Qi'nin bloke olması:** Mu-metal ve grafit kalkanlar bobinlerin iki yanında yer alıyor. Mu-metal için deri kalınlığı `δ ≈ 1.41 mm / √(µr·σ_rel) ≈ 8 µm` (128 kHz, µr ≈ 2×10⁴). `50 µm` kalınlık ~6 deri kalınlığına denk gelir ve **akıyı keser**. Grafit (`σ ~ 10⁶ S/m`, `δ ≈ 1.4 mm`) ise girdap akımı kaybı ve ısınma üretir.
- **Isıl bütçe:** 15–25 W şarjda %75–80 verimle `~4–7 W` ısı çıkar. Yüzey alanı `2 × 0.0128 m²`, `h ≈ 10–12 W/m²K` ile `ΔT ≈ 5/(12 × 0.0256) ≈ 16 K`. 25 °C ortamda yüzey `~41 °C` olur, `≤ 36.2 °C` şartı sağlanamaz. Pedin üzerinde tek yüz kapalı olduğunda durum daha kötüdür. PC'nin ısıl iletkenliği `0.2 W/mK` olduğundan sıcak noktalar oluşur.
- **Gösterim çakışması:** "R" sembolü aynı belgede köşe yarıçapı (`6.35 mm`), bükme yarıçapı (`25.5 mm`) ve Fresnel yansıması için kullanılıyor. Bu, ASD-STE100'ün "bir terim, tek anlam" kuralına aykırı.

### 4.7 Gerçek kullanıma özgü riskler

- **Çevresel gerilme çatlağı (ESC):** PC'nin güneş kremi (avobenzon, oktokrilen), oleik asit, IPA ve bazı el kremleri için kritik gerinimi tipik olarak `~%0.2–0.6`. Dosyanın kendi `%0.35–0.38` değeri bu aralığın tam içinde. Tekrarlı bükme ve cilt yağlarıyla temas kırazlanma ve çatlak üretir. PC-PDMS bu duyarlılığı azaltır ama ortadan kaldırmaz.
- **Çizilme:** 3H sert kaplamayı kuvars kumu (Mohs 7) çizer. "Sıfır çizik" iddiası gerçekçi değil.
- **UV ve hidroliz:** PC UV altında sararır. 85 °C / %85 RH ortamında hidroliz molekül ağırlığını düşürür ve malzeme gevrekleşir. B-6 nemsiz yalnızca 45 °C'de test ediyor, nem testi hiç yok.
- **NiTi'nin "süperelastik" etkisi kullanılmıyor:** Süperelastik dönüşüm `~%1–8` gerinimde başlar. `%0.21`'de NiTi yalnızca E ≈ 70–80 GPa olan rijit bir östenit gibi davranır.

---

## 5 · Önerilen düzeltmeler

1. **Yığını yeniden tasarlayın.** TFT, OLED ve TFE'yi nötr düzleme (z ≈ 0) yerleştirin, bataryayı ekran bölgesinden ayırın. Bu mümkün değilse kalınlığı ve bükme yarıçapını birbirine bağlayan şartı açıkça yazın: kritik katmanda `ε ≤ %0.3–0.5` için `z/R ≤ 0.004`.
2. **Altlığı PI yapın** ve üzerine TFE uygulayın (SiNx/organik/SiNx veya Al₂O₃ nanolaminat, hedef WVTR ≤ 10⁻⁶). Dış kabukta bariyerli PC/PET film ya da ince cam (UTG, 30–50 µm) kullanın. PC'yi yalnızca dış kozmetik ve darbe katmanı olarak tutun.
3. **Sıfır çerçeve iddiasından vazgeçin** ya da ek yerinde TFE dam payını (≥ 0.5 mm) kabul edip ek yeri tasarımını buna göre yapın.
4. **OCA'yı kenar gerilmesine göre boyutlandırın.** Shear-lag analizini (FEA ile) yapın. Statik bekletmede `γ ≤ ~3` ve kenar `τ ≤ holding-power sınırı × güvenlik katsayısı` hedefleyin. Tam alan bükme ile ayrışmayı aynı anda istemek yerine bükme bölgesini sınırlandırın.
5. **Kütle ve kalınlık toplamlarını** tek bir BOM tablosunda birleştirin. 68 g / 72 g ve 2.00 mm / 2.13 mm çelişkilerini giderin.
6. **Bataryayı yeniden belirleyin.** Wh/L hedefini mevcut teknolojiye göre `~600–750 Wh/L`'ye çekin. Ya PEO ile LFP katot ya da başka bir elektrolit ile NMC seçin. Isıl hedefi buna göre güncelleyin.

**Eklenmesi gereken testler:**

| Test | Amaç |
|---|---|
| ASTM F1249 / Ca testi (WVTR), 60 °C/%90 ve 85 °C/%85 | Bariyer doğrulaması |
| R = 25.5 mm'de 24–168 saat statik sarım, 37 ve 60 °C'de, ardından düzlük ve haze ölçümü | OCA sürünmesi ve kalıcı kıvrılma |
| OCA lap-shear sürünme ve gevşeme testi, γ = 3–15 | Malzeme sınırı |
| ESC: güneş kremi, oleik asit ve IPA ile gerinimli PC | Gerçek kullanım |
| Bükülü durumda TFE çatlak görüntüleme ve kara nokta büyüme hızı ölçümü | Bariyerin bükmede dayanıklılığı |
| Mu-metal ve grafit kalkanlı yapıda Qi kuplaj verimi | EM uyumu |

**Sonuç:** Mevcut hâliyle Leaf ekranı ne mekanik olarak bükülmeye (OCA kopar, çekirdek ve OLED gerinim sınırını 2–20 kat aşar) ne de kimyasal olarak yaşamaya (bariyer yok, ilk kara noktalar saatler içinde çıkar) uygun. Belgedeki sayıların büyük kısmı, ayrışmanın her katmana uygulandığı varsayımından ve birkaç aritmetik hatadan geliyor.

### W2_A2_OPUS_PUZZLE_SEAM_USAGE_FAILURES · Model: `claude-opus-5-5` (Router: `claude-coding-router-preview`, Başlangıç: `2026-10-12 14:36:03 +03`, Bitiş: `2026-10-12 14:44:18 +03`, Süre: `494.63 sn`, Uzunluk: `31,542` karakter)

# Budlum Leaf L.5.0 · Mekanik Kilit, Aşınma, Sızdırmazlık ve Tolerans Denetimi

**Kapsam:** `06-FORM-LANGUAGE-AND-EDGES.md`, `08-CONNECTION-SPEC.md`, `17-BODY-AND-SANDWICH-PART-BY-PART.md`
**Hüküm:** **REDDEDİLDİ.** Bu tasarım üretime, prototipe ya da "gate geçti" etiketine uygun değil. Üç sorunun da cevabı olumsuz. Ayrıca belgelerde, sorulan konuların dışında kalan ve sistemi başka yönlerden de işlemez kılan fiziksel hatalar var.

---

## 0 · İzlenebilirlik: soruda kullanılan bazı değerler belgelerde yok

Önce şunu belirtmem gerekiyor: soruda geçen **"0.90 mm kalınlıkta 24 kırlangıç kuyruğu (yapboz dişi)"**, **"100 N/diş"** ve **"800 N/kol"** değerlerinin üç dosyada da karşılığı yok. Belgelerde tanımlı olan mekanik kilit elemanları şunlar:

| Belgedeki eleman | Adet | Değer |
|---|---|---|
| Konik Grade-5 Ti pim (`Ø0.70 x 2.40 mm`) | 8 (her iç kenarda 2) | Z-adımı `<2.5 µm` |
| `N52H` mıknatıs | 24 (her yarım eksende 6) | `11.2 N` çekme, `18.5 N` kesme (her yarım eksen için) |
| Altın mikro-yaprak kontak | 64 (her yarım eksende 16) | `18 mΩ` |
| `(0,0)` haç biçimli Ti göbek | 1 | geometrisi tanımsız |
| `12 µm` fenil-floro-silikon dudak | sürekli | `n = 1.585` |

Bunun anlamı:
1. **Tasarımda form kilidi geometrisi (diş profili, açı, boşluk, yön) tanımlanmamış.** "micro-dovetail pins" (`08 §1.2`) ifadesi kendi içinde çelişkili. Pim ve kırlangıç kuyruğu farklı kinematiğe sahip iki ayrı eleman. Hangisinin kastedildiği belli değil.
2. **Sorudaki sayılar da kendi içinde tutarsız.** `8 diş/kol × 4 yarım eksen = 32` diş eder, 24 değil. 24 diş için kol başına 6 diş, yani `600 N/kol` olmalı. Ya da sistem 3 kollu olmalı, ama haçın 4 kolu var.

Aşağıda iki durumu ayrı ayrı değerlendiriyorum: (a) belgelerde yazanlar, (b) sorudaki 24 diş / 100 N senaryosu, varsayım olarak.

---

## 1 · Dosyalar arası sayısal çelişkiler

| # | İddia | Nerede | Hesap / karşı kanıt | Sonuç |
|---|---|---|---|---|
| C1 | Gövde kalınlığı `2.00 mm` | 06 metin, 08, 17 metin | Katman tablosu: `0.20+0.05+0.14+0.04+0.09+1.16+0.52 = 2.20 mm`. Z-aralığı `-1.10..+1.10` da 2.20 mm. 06 ve 17 başlıkları da "2.20 mm" diyor. | **Gerçek kalınlık 2.20 mm.** "2.00 mm" eski bir değer. |
| C2 | Gövde kütlesi `68.0 g` | 06, 08, 17 | 17'deki Grup 1–10 toplamı: `12.8+1.6+6.8+1.6+1.9+3.4+34.4+2.4+3.2+3.9 = 72.0 g`. Başlık da "72 G" diyor. | **+4.0 g hata.** Karo başına 18.0 g, 17.0 değil. |
| C3 | B modülü `20.0 g` | 08, 17 metin | Grup 11–14 toplamı: `7.6+9.8+3.8+0.8 = 22.0 g`. Başlık da "22 G". | **+2.0 g hata** |
| C4 | Cihaz toplamı `88.0 g` | 17 | `72.0 + 22.0 = 94.0 g` | **+6.0 g (%6.8)** |
| C5 | Dış köşe `R = 6.35 mm` | 06 tablo, 17 Grup 1 | 06'daki formül: `R = 3.20 × (80/80)^0.25 = 3.20 mm`. Aile tablosu da 3.20 diyor. 6.35 mm, 1/4 inçe denk geliyor; büyük olasılıkla eski bir değer. | **İki kat fark.** Kalıp çizimi hangisine göre yapılacak? |
| C6 | Leaf 2800 köşe `6.40 mm` | 06 §2 | `3.20 × (1800/80)^0.25 = 3.20 × 2.178 = 6.97 mm` | **Formülle uyuşmuyor.** Diğer sınıflar (2.69 / 3.81 / 4.53 / 5.86) doğru çıkıyor. |
| C7 | Leaf 160² `144 g` | 06 §2 | `8 × 17 = 136 g` (ya da 8 × 18 = 144 g, C2'deki 72 g'ın 18 g/karo değeriyle) | Hangi karo kütlesinin geçerli olduğu belirsiz |
| C8 | "2.20–2.40 mm solid-state tile law" | 06 §2 | Aynı tabloda Leaf 160 = `2.00 mm` | Kural ile örnek birbirini tutmuyor |
| C9 | "12 edges r = 0.65 mm" | 17 Grup 1 | 06'da tüm gövde için 8 yatay kenar var. Bir karoda dış çevreye denk gelen kenar her yüzde 2, iki yüzde toplam 4. | 12 sayısı ne gövdeye ne karoya uyuyor |
| C10 | PC kabuk kütlesi `12.8 g` | 17 Grup 1 | `8 × (40 × 80 × 0.20 mm) = 5.12 cm³`. PC yoğunluğu 1.20 g/cm³ ile **6.1 g**. 12.8 g için 2.5 g/cm³ gerekir, bu da cam yoğunluğu. | Malzeme ya da kütle yanlış |
| C11 | Kesme tutuşu `18.5 N` > çekme `11.2 N` | 08 | Mıknatısın kesme tutuşu sürtünmeden gelir: `≈ μ·F_çekme = 0.2–0.3 × 11.2 = 2.2–3.4 N`. 18.5 N ancak mekanik form kilidiyle mümkün, o da tanımlı değil. | **Fiziksel olarak tutarsız** |
| C12 | Aktif alan `79.6 × 159.6 mm`, dış kenarda 0.2 mm | 06, 17 | Kenarda `r = 0.65 mm` yuvarlatma var. Bu yuvarlatma Z'de `1.10 − 0.65 = 0.45 mm`'ye kadar iner ve 1–5 numaralı katmanların hepsini keser. OLED dış kenardan en az 0.65 mm içeride bitmek zorunda, buna bir de sızdırmazlık payı eklenir. | En fazla `≈ 78.7 × 158.7 mm`, gerçekçi değer bunun da altı. **Bu iddia geometrik olarak imkânsız.** |

**C1 ve C2'nin pratik sonucu:** Gövde kütlesi, kalınlık ve tolerans zinciri, kısacası her şey yanlış taban değerle hesaplanmış. Aşağıda gerçek değerleri, yani 2.20 mm ve 18 g/karo kullanıyorum.

---

## 2 · SORU 1: Toz, kum, tüy ya da yağ varken `<15 µm` (nominal 12 µm) derz kapanır mı?

### 2.1 Ölçek karşılaştırması

| Kirletici | Tipik boyut | 12 µm boşluğa oranı | Sıkıştırılabilir mi? |
|---|---|---|---|
| Kuvars kum tanesi | 50–100 µm | **4–8 kat** | Hayır. Mohs 7, yaklaşık 1100 HV |
| Manyetit (siyah plaj kumu) | 50–200 µm | **4–17 kat** | Hayır, üstelik ferromanyetik |
| Pamuk lifi (cep tüyü) | 12–20 µm çap, mm'ler uzunluk | **1–1.7 kat** | Kısmen. Selüloz lif sıkıştırılınca yaklaşık 8–10 µm'nin altına inmez. |
| Polyester lif | 10–25 µm | 1–2 kat | Az |
| İnsan saçı | 50–100 µm | 4–8 kat | Hayır |
| Deri pulu (korneosit) | 30–40 µm × 0.5–1 µm kalınlık | kalınlık olarak 0.1 kat | Evet, ama nemle şişer |
| Sebum filmi (parmak yağı) | 1–5 µm | 0.1–0.4 kat | Sıvı. Kılcallıkla boşluğa yayılır. |

**Sonuç:** Tek bir kum tanesi ya da tek bir saç teli derzi **50–100 µm açık tutar**. Bu, 15 µm hedefinin 3–7 katı.

### 2.2 Mıknatıs kum tanesini ezebilir mi?

Kuvarsı ezmek mümkün değil. Daha kötü bir şey olur: tane PC'ye gömülür.

- Bir yarım eksendeki toplam mıknatıs kuvveti, en kötü durumda tek bir taneye biner: `F = 11.2 N`.
- PC akma dayanımı `σ_y ≈ 65 MPa`, plastik akma basıncı `p ≈ 3σ_y ≈ 195 MPa`.
- 11.2 N'u taşımak için gereken temas alanı `A = 11.2 / 195e6 = 5.7e-8 m² = 0.057 mm²`. Bu, temas yarıçapı `a ≈ 135 µm` demek.
- 75 µm çaplı bir tanenin yarıçapı 37.5 µm. Bu temas alanına **tane PC'ye tamamen gömülmeden ulaşılamaz.**

Sonuç olarak tane ya PC duvarına (ya da 12 µm dudağa) gömülür ve **kalıcı bir çukur ile birkaç µm'lik kabarma** bırakır, ya da derz açık kalır. İlk durumda derz bir sonraki takışta da düzgün oturmaz, Z-adımı `<2.5 µm` hedefi kalıcı olarak kaybolur. 8 µm'lik 3H sert kaplama kuvarsa karşı koruma sağlamaz, kumla çizilir. Dolayısıyla belgelerdeki **"zero-scratch" iddiası bu malzemeyle tutmuyor.**

### 2.3 Mıknatıslar kirliliği kendi içine çekiyor (en kritik bulgu)

24 adet N52H mıknatıs derz yüzeyinin hemen arkasında duruyor. Ayrıca 4 dış kenarda 8'er tane daha var (`06 §3`). Yüzey alanı birkaç yüz mT'ye ulaşır.

- Plaj ve sokak kumunda %1–10 oranında manyetit ya da ilmenit bulunur.
- Ceplerde anahtarlardan ve bozuk paralardan gelen demir tozu olur.
- Karolar cepte **ayrı ayrı** taşındığında derz yüzeyleri açıkta kalır ve **ferromanyetik tozu aktif olarak toplar.** Mıknatıs yüzeyine yapışmış manyetit tanesi tırnak ya da bezle kolayca çıkmaz.

Yani tasarım, yalnızca kirlenmeye açık değil. Kirliliği kendi içine çeken bir yapıda.

### 2.4 Cep tüyü: kılcal fitil etkisi ve IP68 kaybı

Tek bir pamuk lifi (yaklaşık 15 µm) bile:
1. Derzi lif çapı kadar açık tutar.
2. Selüloz hidrofilik olduğu için **fitil gibi davranır** ve suyu dudak contasının üzerinden kılcallıkla içeri taşır.
3. "Self-healing" elastomerler genelde yumuşak ve yapışkandır. Yapışkan yüzey tüyü daha kolay tutar.

### 2.5 Su girişi: IP68 iddiası

Paralel levha arasında kılcal giriş basıncı `Δp = γ(cosθ₁ + cosθ₂)/h` ile hesaplanır.

| Durum | γ (N/m) | θ | h | Δp (su girişine direnç) |
|---|---|---|---|---|
| Her iki yüz floro-silikon, saf su | 0.072 | yaklaşık 110° (cos = −0.342) | 15 µm | **≈ 3.3 kPa** (yaklaşık 33 cm su) |
| Bir yüz PC (θ ≈ 80°), bir yüz silikon | 0.072 | 80° / 110° | 15 µm | `0.072 × (0.174 − 0.342)/15e-6 ≈ 0.8 kPa` |
| Sabunlu su, ter ya da sebumlu yüzey | ≈ 0.030 | < 90° | 15 µm | **Negatif. Su kendiliğinden içeri çekilir.** |

IP68 tipik olarak 1.5 m derinlik (yaklaşık 14.7 kPa) ile tanımlanır, daha yüksek sınıflarda 6 m (yaklaşık 59 kPa). Tablodaki **en iyi durum bile hedefin 4.5–18 katı altında.** Ter ya da sabunla kirlenmiş derz ise suyu kendisi emer.

Kontak conta olarak düşünülürse de sorun var. 12 µm'lik dudakta %20–30 sıkıştırma, yani 2.4–3.6 µm. Enjeksiyonla kalıplanmış ve lamine edilmiş PC kenarında dalgalanma bunun çok üstündedir (5–20 µm). **Bu sızdırmazlık profilometre seviyesinde bile kapatılamaz.**

IP6X toz testi IEC 60529'a göre ≤75 µm talk tozuyla yapılır. Tozun ince fraksiyonu 15 µm'den küçük olduğu için açıklıktan doğrudan geçer.

### 2.6 Parmak yağı: optik ve kimyasal etkiler

**Fresnel iddiasının kontrolü:**
- Belgedeki değer: `R = ((1.586 − 1.585)/(1.586 + 1.585))² = (0.001/3.171)² = 9.94e-8`. Aritmetik doğru.
- Ancak bu değer, arayüzde **hiç hava bulunmadığı ve tam optik temas olduğu** varsayımına dayanıyor. 100 nm'lik bir hava filmi bile varsa `R(PC/hava) = ((1.586 − 1)/2.586)² = %5.1`. Bu da iddianın **yaklaşık 500 000 katı.** Kuru elastomer ile PC arasında optik temas için yüzey pürüzlülüğü yaklaşık 50 nm'nin altında olmalı ve yüzey kusursuz temiz olmalı. Bu, sahada sağlanabilecek bir koşul değil.
- Boşluğa sebum dolarsa (n ≈ 1.47): `R = ((1.586 − 1.47)/3.056)² = 1.44e-3 = %0.14`. Bu **iddianın 14 500 katı.** İnce film girişimi nedeniyle gökkuşağı renkli bir çizgi de oluşur.

**Malzeme iddiası:** "Fenil-floro-silikon, n = 1.585" kimyasal olarak gerçekçi değil. Fenil grubu kırınım indisini yükseltir (fenil silikonlar ≈ 1.53–1.55). Florlama ise düşürür (floro-silikonlar ≈ 1.38–1.40). Bu ikisinin kombinasyonuyla 1.585'e ulaşmak inandırıcı değil.

**Daha önemli nokta:** Çizginin görünür olup olmamasını kırınım indisi belirlemez. Asıl belirleyici, **derzde piksel olmaması.**
- OLED panellerin ince film kapsülleme (TFE) bariyeri, kenarda tipik olarak ≥0.3–1.0 mm boşluk ister.
- Her karoda iki derz kenarı var. İki komşu karo yan yana gelince derzde **en az 0.6–2 mm genişliğinde karanlık bir haç** oluşur.
- 508 ppi'de piksel aralığı 50 µm. Yani bu karanlık bant **12–40 piksel** genişliğinde olur.
- İndis eşleştirmesinin bu sorunla ilgisi yok.

**Kimyasal etki (çevresel gerilme çatlaması, ESC):** PC, ESC'ye en duyarlı mühendislik plastiklerinden biri. Sebumdaki oleik asit, güneş kremlerindeki oktokrilen ve avobenzon, dezenfektanlardaki izopropil alkol bilinen ESC ajanları. Gerilim altındaki keskin kenarlara temas ettiklerinde sorun başlar:
- Bunlar kırlangıç diş dipleri, pim delikleri ve 90° derz köşeleri.
- Kalıcı gerinim yaklaşık %0.5'i aşarsa **çatlaklanma (crazing) birkaç hafta içinde** görülür.
- Mıknatıs ön yükü bu kalıcı gerilimi sürekli sağlar.

### 2.7 Kirlilik olmasa bile 12 µm ısı ve nem altında tutulamaz

**Isıl genleşme:** PC için `α ≈ 65–70e-6/K`. Laminatın etkin değeri yaklaşık 30–70e-6/K.

| Senaryo | Hesap | Sonuç |
|---|---|---|
| Bir karo başparmak altında ya da şarj bobini üstünde, karolar arası ΔT = 5 K | `70e-6 × 40 mm × 5 = 14 µm` | **Tüm derz bütçesi bu tek etkiyle tükeniyor** |
| Ön ve arka yüz arasında ΔT = 2 K (güneş ya da yüz teması) | Eğrilik `κ = αΔT/t = 70e-6 × 2/2.2 = 6.4e-5 /mm`, sehim `= κL²/8 = 6.4e-5 × 80²/8` | **≈ 51 µm sehim.** Z-adımı `<2.5 µm` hedefinin 20 katı. |
| Nem: PC yaklaşık %0.15–0.35 su emer, doğrusal şişme yaklaşık %0.03–0.06 | `40 mm × 0.0005` | **≈ 20 µm** |

**Silikon dudak:** Kalıcı sıkışma (compression set) tipik olarak %10–30. Dudak yaklaşık 1000 takma-çıkarma döngüsünden sonra 12 µm'lik ön yükünü kaybeder.

### 2.8 Aşınma: Archard tahmini

`V = k·F·s/H` formülüyle:
- k: üç cisimli abrazyon (kumlu ortam) için yaklaşık 1e-3 ile 1e-2 arası
- F = 11.2 N (yan yüzeylere bastıran mıknatıs ön yükü)
- s = 2.2 mm (Z yönünde takma mesafesi)
- H_PC ≈ 150 MPa

Bir döngüde bir yarım eksendeki aşınma hacmi `V ≈ 1.6e-4 – 1.6e-3 mm³`. Bu hacim yaklaşık 88 mm²'lik diş yan yüzeyine dağılınca:
- Bir döngüde 0.002–0.02 µm
- **1000 döngüde (günde bir değişimle yaklaşık 3 yıl) 2–20 µm**

Kumlu kullanımda aşınma, 12 µm bütçesini **ürün ömrü içinde tamamen tüketir.** Altın kontaklar için de durum benzer: 0.76 µm'lik sert altın kaplama kum varlığında birkaç yüz döngüde nikel tabakaya kadar aşınır. Ardından mikro titreşim korozyonu (fretting) ve kontak direncinde artış gelir.

### 2.9 Temizlik

0.9 mm'lik diş dipleri, Ø0.70 mm pim delikleri ve 12 µm'lik oluklar parmakla temizlenemez. Temizlemek için fırça, basınçlı hava ya da alkol gerekir. Alkol de PC için ESC riski taşır (2.6).

> **Soru 1'in cevabı:** Kapanamaz. Tek bir kum tanesi ya da saç teli derzi 50–100 µm açık bırakır. Mıknatıslar manyetit tozunu aktif olarak çeker. Pamuk lifi suyu içeri taşır. Kirlilik hiç olmasa bile 5 K'lik sıcaklık farkı ya da nem değişimi 12 µm bütçesini tek başına tüketir. Derz, kırınım indisinden bağımsız olarak, piksel boşluğu nedeniyle 0.6 mm'den geniş görünür.

---

## 3 · SORU 2: `(0,0)` merkezinde kinematik aşırı belirlilik ve 4. karonun takılması

### 3.1 Serbestlik derecesi sayımı

Her karonun 6 serbestlik derecesi var: x, y, z, θx, θy, θz. Q4'ü düşünelim. Q1 ve Q3 ile iki derz paylaşıyor.

- Her konik pim, ekseninin dik olduğu 2 yönü kısıtlar. Q4'ün iki derzinde 4 pim var, bu 8 kısıt eder.
- Her yarım eksende 6 yapboz dişi daha olduğunu varsayarsak, her diş en az 1 düzlem içi kısıt ekler: toplam 12.
- Buna dudak teması (12 µm boşluğu da belirlemeye çalışan bir referans) ve Ti göbek eklenir.
- **6 serbestlik derecesine karşı 20'den fazla kısıt var.** Bu, belirgin bir aşırı belirlilik.

Ayrıca 4 karo merkezin etrafında **kapalı bir halka** oluşturuyor. Kapalı halkada imalat hataları yok olmaz, son kapanan derzde birikir.

### 3.2 Halka kapanma toleransı

Q2|Q1 üst sırada, Q3|Q4 alt sırada olsun.
- Sol ve sağ dış kenarların hizalı olması için `W₂ + W₁ + g_üst = W₃ + W₄ + g_alt` olmalı.
- Dikey derz (x = 0) üst ve alt yarıda aynı çizgide olmalı. Bunun için `W₂ = W₃` ve `W₁ = W₄` gerekiyor. Aksi halde y = 0'da bir kademe oluşur.
- Her karo için genişlik toleransı ±t ise en kötü durumda uyumsuzluk 4t olur. Derzin `12 ± 3 µm` kalması için **t ≤ ±0.75 µm** gerekir.
- **Diklik:** 80 mm kenarda 12 µm sapma, yaklaşık 0.15 mrad (31 açısaniye) diklik demek. Lamine bir pil-ekran sandviçinde bu değere ulaşılamaz.

ISO 20457 / DIN 16742'ye göre 40 mm'lik PC kalıp parçasının hassas toleransı yaklaşık ±0.03–0.05 mm, yani **±30–50 µm.** Lazerle kesilmiş lamine kenarda ise ısıdan etkilenen bölge ve koniklik yüzünden ±20–50 µm. Gereken değer ile ulaşılabilen değer arasında **40–60 kat** fark var. Pil içeren bir laminatın kenarı da taşlanarak düzeltilemez.

### 3.3 Diş geometrisine göre üç olasılık

Belgelerde diş geometrisi yok. Her olasılığı ayrı ayrı ele aldım:

**(A) Profil XY düzleminde, Z boyunca kalıp gibi uzatılmış (klasik yapboz):**
- Takma yönü sadece Z. Dördüncü karo teorik olarak iki derze aynı anda Z'den girebilir, çünkü yapboz parçası birden fazla komşuya Z yönünden takılabilir.
- **Ama Z yönünde hiçbir şekil kilidi olmaz.** Karoyu Z'de yalnızca mıknatıs sürtünmesi tutar (yaklaşık 2–3 N, C11). Bu durumda "100 N/diş" yalnızca düzlem içinde geçerli. Karo, Z'deki herhangi bir darbeyle çıkar (bkz. 4.3).
- Takma sırasında komşu derzlerdeki mıknatıslar karoyu yana çeker ve diş yan yüzeylerini birbirine bastırır. Sürtünme kuvveti `μ × (11.2 + 11.2) ≈ 0.4 × 22.4 ≈ 9 N` olur. Diş boşluğu birkaç µm olduğu için yapışıp kayma (stick-slip) ve sıkışma kaçınılmaz.
- **Çekmece sıkışması:** Kaba yaklaşımla, itme noktası sürtünme merkezinden `e > L/(2μ)` kadar uzaktaysa çekmece sıkışır. Burada L = 2.2 mm temas boyu, μ = 0.4, yani **e > 2.75 mm** olunca sıkışma başlar. 40 × 80 mm'lik bir karoyu baş parmakla iterken itme noktası merkezden 10–30 mm uzaktadır. **Karo eğilir ve sıkışır.**

**(B) Kırlangıç profili derz kesitinde (XZ ya da YZ düzleminde), ray derz boyunca uzanıyor:**
- y = 0 derzindeki raylar X boyunca kaymayı, x = 0 derzindeki raylar Y boyunca kaymayı gerektirir.
- Dördüncü karonun iki derze aynı anda girmesi için **aynı anda hem X hem Y yönünde kayması** gerekir. Bu mümkün değil: X rayına girmiş bir karo Y yönünde hareket edemez, tersi de geçerli.
- Montaj ancak sıralı yapılabilir: önce Q1+Q2 çifti Y'de kaydırılır, sonra Q3+Q4 çifti, en son iki çift X'te birleştirilir.
- **"Herhangi bir karo tek başına <3 s'de değişir" iddiası bu geometride geçersiz.** Q1'i çıkarmak için Y'de kaydırmak gerekir ama Q4'e bağlı X rayı buna izin vermez. Q1 ancak önce yarı gövde sökülerek çıkarılabilir.

**(C) Bindirme (half-lap), 2.2 mm kalınlıkta 0.90 mm diş:**
- x derzinde Q1 alttaysa Q4 üsttedir. y derzinde ise sıra döngüsel olarak değişir.
- (0,0)'da dört köşenin bindirme bölgeleri üst üste gelir: `4 × 0.90 = 3.6 mm > 2.2 mm`. **Merkez noktada fiziksel çakışma var.**
- Fırıldak (pinwheel) dizilimde son karonun bir komşunun altına, diğerinin üstüne aynı anda girmesi gerekir. **Saf öteleme hareketiyle bu yapılamaz.** Ancak eğip kaydırarak yapılabilir, o da diğer kilitleri zorlar.

**Konik Ti pimler hangi seçenekte olursa olsun ayrıca kilitleniyor:** Pim derz kenarında Ø0.70 mm ve 2.4 mm boyunda (her tarafta 1.2 mm) ve derze dik yatıyor.
- x = 0 derzindeki pimler X ekseninde. Takılmak için X yönünde 1.2 mm hareket gerekir.
- y = 0 derzindeki pimler Y ekseninde. Takılmak için Y yönünde 1.2 mm hareket gerekir.
- Dördüncü karo 45° çaprazdan sokulursa, X pimi deliğe girerken aynı anda Y yönünde de 1.2 mm kayması gerekir. Pim, deliğinin duvarını keserdi.
- **Sonuç: düzlem içi pimler ile çift eksenli derz birlikte kinematik olarak kilitleniyor.** Bu ancak delikleri yarık yaparak çözülebilir, o zaman da `<2.5 µm` konumlandırma kaybolur.

### 3.4 Merkez düğüm noktası

- **Köşe yarıçapı boşluğu:** Kalıplanan bir parçada keskin 90° köşe yapılamaz, en küçük köşe yarıçapı tipik olarak 0.1–0.2 mm. Dört köşe yuvarlatıldığında merkezde `4 × (1 − π/4) r² = 0.858 r²` alanında bir boşluk kalır. r = 0.2 mm için bu yaklaşık 0.034 mm², köşegeni yaklaşık 0.17 mm. **Bu, görünür bir karanlık nokta ve bir sızıntı kanalı.**
- **Dört yönlü conta birleşimi:** Contalarda T ve + birleşimleri bilinen sızıntı noktalarıdır. Burada dört ayrı dudak bir noktada uç uca geliyor. Kalıpla tek parça üretilmiş sürekli bir conta olmadan IP68 sağlanamaz.
- **Ti göbeğin sahibi tanımsız:** Göbek bir karoya bağlıysa, o karo çıkınca diğer üçü merkez referansını kaybeder. Ayrı bir parçaysa, kaybolmaya müsait ve dördüncü bir aşırı kısıt kaynağı.

### 3.5 Karo kimliği, simetri ve hata önleme (poka-yoke)

Katman yığını ön-arka simetrik. Buna göre Q2, Q1'in Y ekseni etrafında 180° çevrilmişi, Q4 de X ekseni etrafında çevrilmişi.

- Q1'in alt kenarı Q4'ün üst kenarıyla eşleşiyor. Q4, Q1'in X etrafında çevrilmiş hali ise iki kenar aynı fiziksel kenardır ve diş dizilimi x'e göre aynı sıradadır. **Diş dişin karşısına gelir ve çarpışır.**
- Dolayısıyla en az **iki farklı parça tipi** gerekir: {Q1, Q3} ve {Q2, Q4}, birbirine Z etrafında 180° dönmüş çiftler. Bipolar mıknatıs kutuplarının da buna uyması gerekir.
- Kullanıcı cebinden rastgele bir karo çektiğinde yanlış tip ya da yanlış yön ihtimali yüksek. **"<3 s" hedefi bu yüzden de tutmaz.** Bipolar mıknatıslar yanlış hizada iteceği için kullanıcı tutarsız bir "çekip itme" hissi yaşar.

### 3.6 Mıknatısın aniden çekmesi (snap)

Son 0.5 mm'de 22.4 N'luk mıknatıs kuvveti karoyu hızlandırır. 12 µm'lik dudak ve keskin PC derz kenarları bu çarpmayı karşılar. Derz kenarları keskin olmak zorunda, çünkü 0.65 mm'lik yuvarlatma derzde V oluk açardı. Sonuç: **kenar ufalanması.** 3H kaplama gevrek bir tabaka olduğu için kenarda pul pul kalkar.

> **Soru 2'in cevabı:** Dişler Z'den takılan yapboz profiliyse dördüncü karo teorik olarak girebilir. Ama düzlem içi pimler, iki eksenli mıknatıs çekişi ve 2.2 mm'lik temas boyu yüzünden karo sürtünür ve sıkışır. Ayrıca Z yönünde kilit olmaz. Dişler kırlangıç rayıysa ya da bindirmeyse **geometrik kilitlenme kesin:** tek karo çıkarılamaz, merkezde 3.6 mm > 2.2 mm çakışması var. Her iki durumda da halka kapanması ±0.75 µm/karo tolerans gerektiriyor. Bu, ulaşılabilir değerin 40–60 katı daha sıkı.

---

## 4 · SORU 3: Sökme kuvveti paradoksu

### 4.1 Elle sökülebilir mi?

Gövdede **hiç buton yok, serbest bırakma mandalı yok, tırnak çentiği yok** (`08 §2`). Derz 12 µm, yani tırnak girecek yer yok. Karoyu kavramanın tek yolu 2.2 mm'lik dış kenarı iki parmakla sıkıştırmak (pinch). Kenar 0.65 mm yuvarlatılmış ve leke tutmaz floro kaplamalı.

Gereken sıkıştırma kuvveti `F_pinch = F_söküm / (2μ)`. Deri ile floro kaplamalı PC arasında μ yaklaşık 0.15–0.25, yağlı parmakta daha düşük. Hesapta μ = 0.2 kullandım.

| Tutma senaryosu | Sökme kuvveti | Gereken sıkıştırma kuvveti | İnsan kapasitesi (anahtar tutuşu*) |
|---|---|---|---|
| Belge: düzlem içi, 2 derz × 11.2 N | 22.4 N | **56 N** | Kadın 50–70 N, erkek 80–110 N, yaşlı 30–50 N |
| Belge: Z yönü, 2 × 18.5 N (form kilidi varsa) | 37 N | **93 N** | Çoğu kullanıcının üstünde |
| Soru senaryosu: 2 kol × 800 N | 1600 N | **4000 N** | **İmkânsız** |
| Soru: tek kol 800 N | 800 N | **2000 N** | **İmkânsız** |

*Anahtar tutuşu (lateral pinch) değerleri tipik literatür aralıkları.

Ayrıca kuvvet 2.2 mm genişliğinde bir temas şeridine biniyor. Parmak yastığında yaklaşık 1 MPa üzerinde basınç ağrıya yol açar, dolayısıyla belgedeki değerlerle bile söküm acı verir.

### 4.2 Karo çekilince hangi derz açılır?

Kullanıcı Q1'i çekerken, öbür eliyle diğer üç karoyu tutmak zorunda. Ama o üç karo da birbirine sadece 11.2 N ile bağlı. Bu, eşit güçte halkalardan oluşan bir zincir. **Hangi derzin açılacağı belirsiz.** Büyük olasılıkla Q1'den önce Q2/Q3 ya da Q3/Q4 derzi açılır ve gövde elde dağılır. Bu sırada açılan derzlerde ekran kesilir, bağlantı kopar, Dead-Pad el sıkışması baştan başlar.

### 4.3 Paradoksun öbür yüzü: tutma kuvveti düşme ve eğilmeye yetmiyor

**Düşme (1 m, sert zemin):**
- Çarpma hızı `v = √(2gh) = 4.43 m/s`
- PC köşesinde duruş mesafesi yaklaşık 0.5 mm alınırsa ivme `a = v²/(2d) ≈ 19 600 m/s²`, yani yaklaşık 2000 g
- 18 g'lık karoya etkiyen atalet kuvveti `F = 0.018 × 19 600 ≈ 350 N`
- Tutma kuvveti 11.2–18.5 N. **Arada 19–31 kat fark var. Karolar düşmede kesin dağılır** ve açıkta kalan kontaklarıyla yere saçılır.

**Eğilme (menteşe etkisi):** Mıknatıslar yaklaşık z = 0'da, dönme ekseni yüzey kenarında, kaldıraç kolu yaklaşık 1.1 mm.
- y = 0 derzi (2 yarım eksen): `M_kapasite ≈ 22.4 N × 1.1 mm ≈ 24.6 N·mm`
- Telefonu alt yarısından yatay tutunca, üst yarının kendi ağırlığından gelen moment: `0.036 kg × 9.81 × 40 mm ≈ 14.1 N·mm`. Güvenlik katsayısı yalnızca 1.7.
- Seam'den 70 mm uzakta 1 N'luk bir dokunuş eklenirse: `14.1 + 70 = 84 N·mm`, kapasitenin 3.4 katı. **Kullanıcı ekrana dokunduğu anda gövde derzden katlanır.**
- Konik pimlerin eksenel tutuşu yok, bu yüzden derzin dönerek açılmasına direnç göstermezler.
- Arka cepte oturulduğunda ise derz tamamen bir menteşe gibi çalışır.

**Paradoksun özeti:**
- Elle sökülebilmek için tutma kuvveti yaklaşık 20–40 N'u geçmemeli.
- Düşmeye dayanmak için tutma kuvveti yaklaşık 350 N'un üstünde olmalı.
- Arada **yaklaşık 10 katlık bir boşluk var ve hiçbir sabit tutma kuvveti iki şartı birden karşılamaz.** Bu ancak mekanik kazançlı, iki konumlu bir mekanizmayla çözülebilir: kam, sürgülü mandal, bayonet ya da yaylı itici ile kilitli konumda yüksek tutuş, serbest konumda sıfıra yakın tutuş. Belgelerde böyle bir mekanizma yok.

### 4.4 EU 2023/1542 Madde 11'e yapılan atıf yanlış

- Madde 11, portatif pillerin son kullanıcı tarafından "kolayca sökülebilir ve değiştirilebilir" olmasını istiyor (18 Şubat 2027'den itibaren). **Piyasada bulunan genel aletlerle sökmeye izin veriyor.** Isı ya da çözücü gerektirmemesi ve özel alet gerekiyorsa ücretsiz verilmesi gibi şartlar var.
- Yönetmelikte **"<3 s" diye bir süre ya da "aletsiz" şartı yok.** "<3 s" tasarımın kendi koyduğu bir hedef; yönetmeliğe uygunluk gerekçesi olarak gösterilemez.
- Bu tasarımda pil, ekranla tek parça olan bir karonun içinde. Pil değişimi, iki OLED paneli ve PDLC filmi de dahil komple modül değişimi anlamına geliyor. Bunun "pil değişimi" sayılıp sayılmayacağı, maliyet ve atık açısından ayrıca hukuki değerlendirme gerektirir.
- 4 ayrı pil = 4 ayrı ürün. Madde 13'teki etiket ve QR kodu, CE işareti ve taşıma testleri (UN 38.3) her karo için ayrı ayrı yapılmalı.

> **Soru 3'ün cevabı:** 800 N/kol tutuşu olan bir karoyu elle sökmek mümkün değil, 2000–4000 N sıkıştırma kuvveti gerekir. Belgedeki 11.2 N bile, leke tutmaz kaplamalı 2.2 mm'lik kenarda 56–93 N sıkıştırma ister ve gövdenin elde dağılmasına yol açar. Öte yandan bu 11.2 N, düşmeye (yaklaşık 350 N) ve dokunma momentine dayanmaya yetmiyor. **Hiçbir sabit tutma kuvveti bu iki şartı aynı anda karşılamıyor.**

---

## 5 · Sistemin geri kalanındaki fiziksel imkânsızlıklar

| # | Bulgu | Fizik ve sayılar |
|---|---|---|
| P1 | **Mu-metal kablosuz şarjı engelliyor** | Mu-metal için μr ≈ 30 000, σ ≈ 1.6e6 S/m. Qi2'nin yaklaşık 360 kHz çalışma frekansında deri derinliği `δ = √(2/(ωμσ)) ≈ 3.8 µm`. Katman 5 ve 7'deki yaklaşık 20 µm'lik Mu-metal ≥5δ kalınlıkta. **Bobin iki Mu-metal levhanın arasında kaldığı için şarj alanı bloklanır,** Mu-metal girdap akımıyla ısınır ve yabancı cisim algılama (FOD) şarjı keser. İletken grafen levha da ek kayıp yaratır. |
| P2 | **Ø54 mm Qi2.2 bobin dört karoya bölünmüş** | Bobinin her sarımı 4 derzi keser. 10 sarımlı bir bobin için 40 kontak geçişi gerekir: `40 × 18 mΩ = 0.72 Ω` ek direnç. 1.5 A rms akımda `P = 1.5² × 0.72 ≈ 1.6 W` ısı, derz boyunca yoğunlaşmış halde. Üstelik 64 kontağın 40'ı yalnızca bobine gider; VSYS ve MIPI'ye yer kalmaz. |
| P3 | **Şarj ısısı 36.2 °C sınırına sığmıyor** | Şarj pedi üzerindeyken sadece bir yüz soğur: `h ≈ 10 W/m²K × 0.0128 m² × (36.2 − 25) K ≈ 1.4 W`. 25 W şarjda %75 verimle yaklaşık 6 W ısı çıkar. **Şarj 5 W'ın altına düşmek zorunda.** 35 °C ortam sıcaklığında ise ΔT 1.2 K kaldığı için şarj pratikte imkânsız. |
| P4 | **PEO elektrolit 36.2 °C altında çalışmaz** | PEO'nun iyonik iletkenliği 25 °C'de yaklaşık 1e-6–1e-5 S/cm. Pratik akım için 60–80 °C gerekir. Hücre "≤36.2 °C" sınırıyla güç veremez. |
| P5 | **Hacimsel enerji yoğunluğu** | `3.0 Wh / (35 × 75 × 1.08 mm = 2.835 cm³) = 1058 Wh/L` ve `349 Wh/kg`. Bugünkü en iyi telefon hücreleri yaklaşık 750–800 Wh/L. 1.08 mm'lik ince hücrelerde paketleme payı büyük olduğu için gerçekçi değer 400–550 Wh/L. **Yaklaşık 2 kat abartılı.** |
| P6 | **LLZO seramik eğilmeye dayanmaz** | Belgede R = 25.5 mm eğilme var. 1.08 mm'lik LLZO'da gerinim `0.54/25.5 = %2.1`. Seramiğin kırılma gerinimi yaklaşık %0.1. **Belgenin kendi eğilme senaryosunda pil çatlar.** Cep basıncı ve düşmede de risk aynı. |
| P7 | **Derzde "0.00 mm bezel"** | OLED ince film kapsülleme payı ≥0.3 mm. Kenar sarma (edge-wrap) için gereken PI bükümünün yarıçapı en az yaklaşık 0.3 mm ve bu büküm derz yüzüne denk gelir. O bölgede mıknatıs, pim ve kontak yaprakları var. **Çakışma.** |
| P8 | **Karonun yan duvarları malzeme listesinde yok** | PC kabuklar sadece ön ve arka düz levhalar (40 × 80 × 0.20 mm). Derz yüzünde OCA, OLED ve AgNW katmanlarının kesik kenarları açıkta kalır. **Karo cihazdan ayrıyken nem OLED'e saatler içinde ulaşır.** Pim deliği ve mıknatıs yuvasının açılacağı bir çerçeve malzemesi de tanımlı değil. |
| P9 | **Mıknatıs kuvveti yerleşime sığmıyor** | Mıknatıs yüksekliği en fazla yaklaşık 1–1.6 mm olabilir. Aradaki boşluk iki PC duvarı + dudak, yaklaşık 0.4 mm. Bu boşlukta 1 × 1 × 3 mm'lik bir N52H çifti mıknatıs başına yaklaşık 0.3–0.5 N verir. 6 mıknatısla **yaklaşık 2–3 N, iddia edilen 11.2 N'un 4–5 katı altında.** Gerçekçi 0.1–0.3 N/mm² yüz basıncıyla 11.2 N için 37–112 mm² yüz alanı gerekir. 1 mm yükseklikte bu, 40 mm'lik yarım eksenin tamamından daha uzun bir mıknatıs demek. |
| P10 | **Kontak yaprakları derzi iter** | Güvenilir altın temas için kontak başına yaklaşık 0.3 N gerekir: `16 × 0.3 = 4.8 N`. Net tutuş `11.2 − 4.8 = 6.4 N` kalır. Dudak sıkıştırma kuvveti de çıkarılınca daha azı. |
| P11 | **MIPI sinyali yaylı kontak üzerinden** | 100 Ω diferansiyel empedans gerekir. Yaprak kontaklarda empedans süreksizliği olur ve titreşimde bağlantı anlık kopar. Sonuç: titreşimde ekranda bozulma. |
| P12 | **Cepte ayrı taşınan karolar** | Açık kenardaki mıknatıslar anahtar ve bozuk parayı çeker. Karolar birbirine rastgele yönlerde yapışır. Altın kontaklar metal cisimlerle kısa devre riski taşır; Dead-Pad'in 0 V kesmesi hücre içi anahtara bağlı ama bu anahtar tanımlı değil. |

---

## 6 · Yeniden tasarım önerileri

1. **Karodan karoya kilitlemeyi bırakın.** Her karo, rijit bir merkez şaseye (Mg ya da Ti, + biçimli kiriş) Maxwell tipi üç oluklu kinematik bağlantıyla ayrı ayrı oturmalı: 3 küre ve 3 V-oluk, tam 6 kısıt. Kapalı halka ortadan kalkar ve tolerans her karoda şaseye göre bağımsız tutulur. Böylece ±0.75 µm yerine ±20 µm'lik toleranslar kabul edilebilir hale gelir.
2. **İki konumlu kilit mekanizması koyun.** Örneğin şasede gizli bir kam ya da sürgü: kilitli konumda ≥300 N tutuş, serbest konumda ≤5 N. Kamın mekanik kazancı 10:1'den büyük olmalı ve bir bozuk parayla ya da tırnakla çevrilebilmeli. Bu, Madde 11'in "genel alet" şartına uyar.
3. **12 µm optik derz hedefinden vazgeçin.** Dürüst bir 0.4–0.8 mm'lik dekoratif conta bandı ya da kasıtlı bir V-kanal tasarlayın. Bu bant OLED kapsülleme payını görünür bir tasarım öğesine dönüştürür.
4. **Sızdırmazlığı kontak tipi bir dudağa bırakmayın.** Her karoyu kendi içinde hermetik kapatın (lazer kaynaklı çerçeve ya da kalıpla tek parça TPE). Derzler arasında su ve toz sızdırmazlığı gerekmesin. Kontaklar için tek tek contalı pogo pimler kullanılsın.
5. **Kir için kaçış yolları açın.** Diş yan yüzeylerinde 0.2 mm derinlikte kir cepleri ve kendini temizleyen sürtünme dudakları olsun. Mıknatısları yüzeyden en az 0.5 mm geri çekin ve paslanmaz ferritik akı yönlendiriciyle derz yüzeyindeki alanı düşürün.
6. **Malzemeleri değiştirin.** ESC'ye dayanıklı kopolyester ya da PA12 kullanın, veya PC kalacaksa diş dibindeki kalıcı gerinimi %0.3'ün altında tutun. 3H yerine kumaya karşı en az 9H'lik bir cam ya da safir yüz düşünün.
7. **Qi2 ve Mu-metal sorununu çözün.** Bobinin üstünde Mu-metal olmamalı. Ferrit levhayı bobinin arkasına koyun. Ø54 mm bobini derzlere bölmeyin; bunun yerine karo başına tek bir bobin kullanın.
8. **Belgelerdeki temel değerleri tek bir kaynakta düzeltin.** Kalınlık 2.20 mm, karo 18 g, gövde 72 g, cihaz 94 g, R = 3.20 mm. Tüm "gate" sonuçları bu değerlerle yeniden hesaplanmalı.

---

## 7 · Prototip doğrulama test planı

| Test | Yöntem | Kabul kriteri |
|---|---|---|
| Kir toleransı | ISO 12103-1 A2 ince toz + %5 manyetit ve pamuk tüyü, 500 takma-çıkarma döngüsü | Derz ≤ hedef, Z-adımı ≤ hedef, kontak direncinde artış ≤ 10 mΩ |
| Sızdırmazlık | IEC 60529 IP6X (talk, 2 kPa vakum, 8 saat) ve IPX8 (1.5 m, 30 dk), yeni ve 1000 döngü sonrası | İçeride toz ya da su yok |
| Düşme | 1.5 m, 26 yön, betonda (MIL-STD-810H 516.8) | Hiçbir karo ayrılmamalı |
| Eğilme ve dokunma | Telefon tek yarısından tutulurken 3 N noktasal yük | Derz açılmamalı |
| Söküm ergonomisi | 5. ve 95. persentil kullanıcılarla, yağlı parmak koşulunda | %95 kullanıcı ≤ 30 N ile ve ≤ 10 s'de sökebilmeli |
| ESC | Oleik asit ve güneş kremi teması, %0.5 gerinim, 72 saat (ISO 22088-3) | Çatlaklanma yok |
| Isıl çevrim | −20 °C ile +60 °C arası, 500 döngü | Derz ve Z-adımı spesifikasyon içinde |

**Kapanış:** "<15 µm sıfır çizgi derz", "<3 s aletsiz değişim" ve "IP68" iddiaları aynı mekanizmada birbiriyle çelişiyor. Biri sağlandığında diğerleri bozuluyor. Mevcut belgeler bu çelişkiyi çözmüyor, üstelik birbirleriyle de tutarsız (C1–C12). Tasarımın yukarıdaki kinematik şase ve iki konumlu kilit mimarisiyle yeniden ele alınmasını öneririm.


---

## DALGA 3 · KATI-HAL (`LLZO/PEO-LiBOB`) BATARYA, GÖZLÜK GÜVENLİĞİ VE PORTSUZ `Qi2.2` KABLOSUZ ŞARJ HATALARI (`HARDWARE/02, 04, 11, 14, 15`)

### W3_A1_OPUS_SOLID_STATE_BATTERY_AUDIT · Model: `claude-opus-5-5` (Router: `claude-coding-router-preview`, Başlangıç: `2026-10-12 14:44:18 +03`, Bitiş: `2026-10-12 14:49:55 +03`, Süre: `336.69 sn`, Uzunluk: `28,597` karakter)

# BUDLUM LEAF L.5.0 Enerji Sistemi Denetimi (`11-THE-ENERGY-SHEET.md` + `15-…-PART-BY-PART.md`)

**Denetim türü:** Elektrokimya, katı-hal batarya güvenliği, termal, mekanik ve dosyalar arası tutarlılık
**Yöntem:** Hiçbir araç çalıştırmadım. Bütün hesaplar elle yapıldı ve sadece iki dosyadaki verilere dayanıyor. Literatürden aldığım değerler (iletkenlik, ASR, CCD, şişme) tipik aralık olarak verildi. Bunların ölçümle doğrulanması gerekir.

---

## 0 · Kısa sonuç

İki dosyadaki tasarım **bu haliyle fiziksel olarak gerçekleştirilemez.** Ana sorunlar şunlar:

| # | Bulgu | Önem |
|---|---|---|
| K-1 | `3.0 Wh / 2.835 mL = 1 058 Wh/L` çıkıyor. Dosyadaki `750 Wh/L` iddiasıyla çelişiyor. `750 Wh/L` doğruysa hücre `2.13 Wh`, toplam `8.5 Wh` olur. | Kritik |
| K-2 | Oda sıcaklığında PEO bazlı katı hücrede `<28 mΩ` iç direnç olanaksız. Gerçekçi değer `0.3–2.5 Ω`, `0 °C`'de `×8–35` daha kötü. | Kritik |
| K-3 | Ya iç direnç gerçekten `28 mΩ`'dur ve Q4 takılınca **`~14.5 A`** dengeleme akımı akar, ya da direnç gerçekçidir ve `25 W` şarj olanaksızdır. İki iddia birlikte doğru olamaz. | Kritik |
| K-4 | BOM'da akım sınırlama elemanı yok (endüktör, DC-DC, sigorta, PTC). "Aktif dengeleme" iddiası donanımla karşılanmıyor. | Kritik |
| K-5 | `1 058 Wh/L` sadece Li-metal anotla mümkün. Li-metal anot SoC'ye göre `~100–160 µm` şişer. Bu, `<2.5 µm` Z-basamak ve "`0%` swelling" iddialarını çürütür. Ayrıca MPa mertebesinde yığın basıncı gerekir; `0.20 mm` PC kabuk bunu taşıyamaz. | Kritik |
| K-6 | Karo Z yığını `≥2.40–2.58 mm` tutuyor, karo kalınlığı ise `2.00 mm`. | Kritik |
| K-7 | PEO `4.2 V` NMC katodunda oksitlenir. "`LiFePO4/NMC`" ifadesi kimyayı belirsiz bırakıyor ve `800 mAh = 3.0 Wh` eşitliği LFP ile tutmuyor. | Yüksek |
| K-8 | `25 W` Qi şarjında `3–7 W` kayıp oluşur. Bu kayıpla `36.2 °C` kesme sınırının altında kalmak termal olarak olanaksız. | Yüksek |
| K-9 | Kütle çelişkisi: `68.0 g` (4×17) ile `72.00 g` (4×18) aynı tabloda bile çelişiyor. | Orta |
| K-10 | `180 mF` "ince-film seramik" kapasitör `14 mm³` hacme sığmaz (yaklaşık `~1000×` fazla). Sığsaydı bile `3 s` değil `~0.5 s` köprü sağlardı. | Yüksek |

---

## 1 · Sorudaki sayıların kontrolü

Hesaba geçmeden önce sorudaki bazı sayıları dosyalarla karşılaştırdım:

| Sorudaki değer | Dosyadaki değer | Not |
|---|---|---|
| `LLZO/PEO-LiBOB` | `LLZO/PEO` + "`LiFePO4/NMC`" | **LiBOB dosyalarda hiç geçmiyor.** Tuz belirtilmemiş. Bu da bir eksiklik (bkz. §4). |
| `1.06 mm` kalınlık | `1.08 mm` | Dosyalarda `1.06` geçmiyor. |
| `33.2 × 73.2 × 0.96 mm = 2.33 cm³` | `35.0 × 75.0 × 1.08 mm` (`2.83 mL`) | Sorudaki ölçüler dosyalarda yok. Aktif alan gibi düşünülmüş olabilir. |
| `%20 SoC = 3.40 V` | Dosyada yok | NMC'de `%20 SoC` dinlenme OCV'si tipik olarak `~3.55–3.65 V`. `3.40 V` daha çok `%5–10 SoC`'ye karşılık gelir. LFP'de `%100` ≈ `3.40–3.45 V` olur. Yine de en kötü durumu görmek için `ΔV = 0.80 V` ile hesapladım. |

**Sorudaki aritmetik doğru:** `33.2 × 73.2 × 0.96 = 2 333 mm³`, `3.0 / 0.002333 = 1 286 Wh/L`. Ama bu ölçüler dosyadan gelmiyor. Dosyanın kendi ölçüleriyle de çelişki var (§2).

---

## 2 · Hacimsel ve gravimetrik enerji tutarlılığı (Madde 1)

### 2.1 Dosyanın kendi sayılarıyla hesap

```
Hücre hacmi  = 35.0 × 75.0 × 1.08 = 2 835 mm³ = 2.835 mL   (dosya "2.83 mL" diyor, doğru)
Enerji       = 3.0 Wh
Yoğunluk     = 3.0 / 0.002835 L = 1 058 Wh/L                (dosya "750 Wh/L" diyor, YANLIŞ)
```

İki iddia birbirini dışlıyor:

| Hangisi doğruysa | Hücre başı | Toplam (4 karo) | `0.85 W`'ta çalışma süresi |
|---|---|---|---|
| `3.0 Wh` doğru | — | `12.0 Wh` | `14.1 h` (yoğunluk `1 058 Wh/L`) |
| `750 Wh/L` doğru | `750 × 0.002835 = 2.13 Wh` | `8.5 Wh` | **`10.0 h`** (`9.0 h`, %90 dönüşüm verimiyle) |
| 3 karo (swap sırasında) | — | `6.4 Wh` | `7.5 h` |

**Kese dahil edilince:** Kese (BOM #5) `35.4 × 75.4 × 0.09 mm` olarak hücreye eklenirse dış hacim `35.4 × 75.4 × 1.17 = 3 123 mm³` olur. Bu `960 Wh/L` demek ve hâlâ `750`'nin çok üstünde. Üstelik kesenin `0.2 mm`'lik kenar payı gerçekçi değil (§7.3). Gerçek bir ısıl yapışma flanşı (`2–3 mm`) eklenince ya hücre küçülür ya da kese karoya sığmaz.

### 2.2 Bu yoğunluk nereden geliyor?

- `1 058 Wh/L` paketleme dahil, `1.08 mm` kalınlıkta küçük bir hücre için gösterilmiş bir değer değil. Büyük format, anotsuz ya da Li-metal anotlu katı hücreler için bile duyurulan en iyi değerler `~900–1 000 Wh/L` mertebesinde.
- `1 mm` kalınlıktaki hücrelerde kese, akım toplayıcılar ve tab payı ölü hacmin büyük kısmını oluşturur. İnce ticari hücreler tipik olarak `200–500 Wh/L` aralığında kalır.
- Grafit anotla `1 058 Wh/L` mümkün değil. **Bu değer Li-metal anot gerektirir.** Bunun sonuçları §4.3 ve §4.4'te.

### 2.3 Gravimetrik kontrol

- Hücre kütlesi `8.60 g` (BOM #1–4, satır başına): `3.0 / 0.0086 = 349 Wh/kg`.
- Yoğunluk: `8.60 / 2.835 = 3.03 g/cm³`. LLZO (`~5.1 g/cm³`) ağırlıklı bir yapı için makul.
- `349 Wh/kg` laboratuvar sınırında bir değer. Kalın seramik ayırıcı ve `1 mm` kalınlıkta seri üretimde gerçekçi değil.

### 2.4 mAh ve kimya tutarsızlığı

`800 mAh × V_nom = 3.0 Wh` eşitliği `V_nom = 3.75 V` demek. Bu NMC/NCM'ye işaret eder. Dosya ise "`LiFePO4/NMC`" diyor:
- LFP ile: `800 mAh × 3.2 V = 2.56 Wh`. Bu `3.0 Wh` değil.
- NMC ile: PEO elektrolit uyumsuz (§4.1).

`3 200 mAh = 4 × 800 mAh` olduğuna göre **4 karo paralel bağlı.** Bu da Madde 2'deki dengeleme akımı sorununu doğrudan doğuruyor.

---

## 3 · İyonik iletkenlik, ASR ve `<28 mΩ` iddiası

### 3.1 Tipik iletkenlik değerleri

| Malzeme | `σ` (25 °C) |
|---|---|
| Sıvı LiPF6/karbonat | `~1×10⁻²` S/cm |
| Ta/Al katkılı LLZO (bulk) | `~3×10⁻⁴ – 1×10⁻³` S/cm (tane sınırları düşürür) |
| PEO-LiTFSI veya PEO-LiBOB (yarı kristal) | `~10⁻⁶ – 10⁻⁵` S/cm |
| LLZO dolgulu PEO kompozit | `~10⁻⁵ – 10⁻⁴` S/cm |

PEO'nun kristal fazı yaklaşık `~60 °C`'de erir. Ticari PEO bataryaları (örneğin Bolloré LMP) bu yüzden **`60–80 °C`'de** çalıştırılır. Bu tasarım ise bataryayı `36.2 °C`'de kesiyor. Yani **PEO, hiçbir zaman verimli çalıştığı sıcaklık penceresine giremiyor.**

### 3.2 `<28 mΩ` iddiasının ASR ile kontrolü

```
800 mAh / ~4 mAh·cm⁻² (gerçekçi alan yükü) ≈ 200 cm² toplam elektrot alanı
35 × 75 mm = 26.25 cm² katman başı  →  ~7.6 bi-hücre katmanı
1.08 mm / 8 ≈ 135 µm tekrar birimi (katot ~60 + ayırıcı ~20 + Li ~20 + toplayıcılar)  → sınırda mümkün
```

Yalnızca ayırıcının katkısı (`L = 20 µm`, `σ = 1×10⁻⁴`):
```
ASR_ayırıcı = L/σ = 2×10⁻³ cm / 1×10⁻⁴ S/cm = 20 Ω·cm²
R_ayırıcı   = 20 / 200 = 0.10 Ω = 100 mΩ
```

Bu tek başına hedefin `3.6` katı. Gerçek hücrede buna şunlar eklenir:
- Kompozit katot içindeki iyonik yol (PEO kataliti): `20–100 Ω·cm²`
- Li/LLZO arayüzü (yüzey işlemi yoksa): `10–1000 Ω·cm²`
- Katot/LLZO arayüzü (uzay yükü, ara faz): `10–100 Ω·cm²`

**Gerçekçi toplam ASR (25 °C) `60–500 Ω·cm²` aralığında, yani `R_hücre ≈ 0.3–2.5 Ω`.**
`<28 mΩ` için toplam ASR'nin `≤5.6 Ω·cm²` olması gerekir. Bu sıvı elektrolitli güç hücresi seviyesi. Karşılaştırma için: `800 mAh` ticari sıvı LiPo hücreler bile `1 kHz` AC'de tipik olarak `50–100 mΩ` ölçülür. **ENR-11'deki `<28 mΩ` kapısı bu kimyayla geçilemez.**

### 3.3 Soğuk hava (`0–10 °C`, kışın dışarıda gözlük olarak kullanım)

PEO ve tane sınırı iletimi için Arrhenius yaklaşımı (`Ea = 0.6–1.0 eV`, PEO'nun erime noktası altında gerçekçi aralık):

| T | `Ea = 0.6 eV` | `Ea = 1.0 eV` |
|---|---|---|
| 25 °C | 1× | 1× |
| 10 °C | `~3.0×` daha dirençli | `~6.2×` |
| 5 °C | `~5.4×` | `~16.5×` |
| 0 °C | `~8.5×` | `~35×` |

(`k/Ea` ile hesaplandı, örnek: `exp(6963 K × (1/278 − 1/298)) = e^1.68 = 5.4`.)

**Sonuçları:**
- `25 °C`'de `1 Ω` olan bir hücre `0 °C`'de `8.5–35 Ω` olur.
- Swap sırasında (3 karo, `0.85/3 = 0.283 W` → `~77 mA` karo başına) gerilim düşümü `0.65–2.7 V` olur. **Sistem kararmaya (brown-out) gider.** "Zero reboot" iddiası soğukta geçersiz.
- Kullanılabilir kapasite de düşer, çünkü düşük sıcaklıkta polarizasyon kesme gerilimine daha erken ulaşır.
- **Kendini ısıtma çözüm değil:** Bir karonun ısı kapasitesi yaklaşık `17 g × ~1.2 J/g·K ≈ 20 J/K`. `5 → 30 °C` ısıtmak karo başına `500 J` (`0.14 Wh`) gerektirir. Asıl sorun sürekli kayıp: 4 karonun iki yüzü `0.0256 m²`, `h = 10–25 W/m²K` (rüzgâr) ve `ΔT = 25 K` ile **`6.4–16 W` sürekli ısı kaybı** oluşur. Bu, `0.85 W`'lık bütçenin `7–19` katı.

### 3.4 Soğukta şarj ve Li-metal dendrit riski

LLZO/Li için kritik akım yoğunluğu (CCD) oda sıcaklığında tipik olarak `~0.3–1 mA/cm²`. Sıcaklık düştükçe CCD de düşer.

| Senaryo | Akım (karo başı) | Akım yoğunluğu (200 cm²) | C-oranı |
|---|---|---|---|
| `25 W` Qi2.2, 4 karo, `~3.8 V` | `6.25 W / 3.8 V ≈ 1.64 A` | `8.2 mA/cm²` | `~2C` |
| `10 W` yerel Qi, tek karo | `≈ 2.6 A` | `13 mA/cm²` | `~3.3C` |

Her iki durumda da akım yoğunluğu CCD'nin **`10–40` katı.** Sonuç: dendritler tane sınırları boyunca ilerler ve **iç kısa devreye** yol açar. "Yanmaz" iddiası bu senaryoda anlamını yitirir (§4.5).

---

## 4 · Kimya ve malzeme uyumsuzlukları

### 4.1 PEO ve 4.2 V NMC
PEO'nun oksidatif kararlılık sınırı yaklaşık `~3.8–4.0 V vs Li/Li⁺`. `4.20 V`'luk NMC katotta PEO oksitlenir. Sonuç empedans artışı ve hızlı kapasite kaybı. LiBOB tuzu sınırı biraz yükseltse de `4.2 V`'ta uzun ömür sağlamaz. Klasik PEO çifti LFP'dir (`~3.45 V`), ama LFP ile `3.0 Wh` tutmaz (§2.4). **Kimya seçimi tutarsız.**

### 4.2 LLZO'nun nem ve CO₂ duyarlılığı
LLZO havada H⁺/Li⁺ değişimi yapar ve yüzeyinde `Li₂CO₃` ile `LiOH` oluşur. Bu katman arayüz direncini büyük ölçüde artırır. Hermetiklik bu yüzden kritik, ama kesenin kenar payı (`0.2 mm`) bunu sağlayamaz (§7.3).

### 4.3 "`0%` swelling" iddiası yanlış, ve bu optik dikiş toleransını bozar
Li-metal anot, alan kapasitesi başına yaklaşık `~4.85 µm` kalınlık değiştirir:
```
4 mAh/cm² × 4.85 µm = ~19.4 µm / katman
× ~8 katman = ~155 µm tam döngü "nefes alma"  (hücre kalınlığının %14'ü)
```
`%100` ile `%20` SoC arasındaki fark yaklaşık `~0.8 × 155 ≈ 124 µm`. Bu durumda:
- Tam dolu Q4 ile `%20` SoC'deki komşu karolar arasında **`~120 µm` Z-basamağı** oluşur. Dosyadaki hedef `<2.5 µm` (`~50×` ihlal). `<15 µm` optik dudak da bunu kapatamaz.
- "`0.0%` swelling" ve "`0%` swelling" ifadeleri fiziksel olarak yanlış.

### 4.4 Yığın basıncı
Li-metal katı hücreler arayüz temasını korumak için tipik olarak `~1–10 MPa` yığın basıncı ister.
```
1 MPa × 26.25 cm² = 2 625 N  (≈ 268 kgf) / karo
```
`0.20 mm` PC kabuk, `0.05 mm` silikon OCA (`G = 0.08 MPa`) ve `11.2 N` mıknatıs tutuşu bu kuvvetin yanında önemsiz kalır. Basınç olmayınca boşluklar oluşur, arayüz direnci artar ve akım yoğunluğu yerel olarak yükselir. Bu da dendrit riskini büyütür.

### 4.5 "Yanmaz" ve "nail test'te 0 yangın" iddiaları
- LLZO yanmaz, ama **PEO organik bir polimerdir ve yanar.**
- Li-metal `180 °C`'de erir ve nem ya da hava ile şiddetli tepkimeye girer.
- NMC katot `~200 °C` üzerinde O₂ salar. Li-metal ile birleşince termal kaçak mümkündür ve katı hücrelerde gösterilmiştir.
- "`0.0 ppm` HF" iddiası LiPF6 olmadığı için mantıklı, ama ölçülemez bir sıfır değer. ENR-15 kapısının sıfır yerine bir algılama limitiyle tanımlanması gerekir.

### 4.6 Mekanik bükülme ve LLZO kırılganlığı
BOM #22 şöyle diyor: "`0.38%` strain at `R 25.5 mm`". Bu, karonun `25.5 mm` yarıçapa kadar büküldüğünü ima ediyor. Bükülmede yüzey gerinimi:
```
ε = y / R ;  y ≈ 0.5 mm (nötr eksenden uzaklık) → ε = 0.5/25.5 = %2.0
```
LLZO'nun kırılma gerinimi `σ_f/E ≈ 150 MPa / 150 GPa ≈ %0.1`. Gerinim bunun **`~20` katı.** LLZO çatlar ve çatlaklar dendritlerin doğrudan ilerleyeceği yollar haline gelir. Bükülme kastedilmiyorsa bile gözlük düşmesi ya da cepte sıkışma aynı riski taşır.

---

## 5 · Madde 2: Q4 (`%100`, `4.20 V`) mevcut üç karoya (`%20`, `3.40 V`) takıldığında dengeleme akımı

### 5.1 Topoloji
- 4 karo paralel bağlı (`3 200 mAh = 4 × 800`).
- Akım yolu: Q4 hücresi, tablar, Dead-Pad anahtarı (BOM #13, `2 × 2 × 0.32 mm`), `+` dikiş kontakları (BOM #18, `18 mΩ` adet başı) ve üç karonun paralel eşdeğeri.
- Kontak dağılımı: Toplam 64 kontak, yarım eksen başına 16. Q4 iki yarım eksene dokunuyor (32 kontak). Bu 16 kontak VSYS, GND, QI2 ve MIPI arasında paylaşılıyor. Varsayımım her yarım eksende 4 VSYS ve 4 GND kontağı. Buna göre dikiş başına döngü direnci `4.5 + 4.5 = 9 mΩ`, iki dikiş paralel olunca **`~4.5–9 mΩ`**.
- MOSFET yolu (çift yönlü bloke için sırt sırta iki FET, `2 × ~5 mΩ`): yaklaşık **`~10 mΩ`**.

### 5.2 Senaryo A: Dosyanın kendi değeri (`R_hücre = 28 mΩ`)

```
R_döngü = R_Q4 + R_üçlü + R_kontak + R_FET + R_iz
        = 28 + 28/3 + ~7 + ~10 + ~1 ≈ 55 mΩ
I_ilk   = ΔV / R_döngü = 0.80 V / 0.055 Ω ≈ 14.5 A
```

| Büyüklük | Değer | Yorum |
|---|---|---|
| Q4 deşarj oranı | `14.5 A / 0.8 Ah ≈ 18C` | Li-metal katı hücre için yıkıcı |
| Diğer üç karonun şarj akımı | `~4.8 A` her biri `≈ 6C` | `≈ 24 mA/cm²`. CCD'nin `25–80` katı, **dendrit ve kısa devre** |
| Döngüdeki ilk güç | `ΔV²/R = 0.64/0.055 ≈ 11.6 W` | 68 g'lık cihaz için çok yüksek |
| Q4 içindeki ilk güç | `14.5² × 0.028 ≈ 5.9 W` | 17 g'lık karo, `~20 J/K` |
| Q4 ilk ısınma hızı | `5.9 / 20 ≈ 0.29 K/s` | `25 → 36.2 °C` yaklaşık **`40–60 s`**'de |
| VSYS kontağı başına akım (8 kontak) | `~1.8 A` | Altın kaplı BeCu yaprak kontaklar tipik olarak `0.5–2 A` için tasarlanır |
| Kontak başına I²R | `1.8² × 0.018 ≈ 58 mW` | `1.4 × 0.9 mm`'lik bir kontak için ciddi |

### 5.3 İlk temas anı (contact bounce)
Mıknatıslı bir hızlı geçmede (`11.2 N`) kontaklar aynı anda değmez. İlk değen tek bir VSYS kontağı ve tek bir GND kontağı olur:
```
R_döngü' ≈ 55 − 7 + 2 × 18 ≈ 84–90 mΩ  →  I ≈ 9 A, tek kontak üzerinden
V_kontak = 9 × 0.018 ≈ 0.16 V
```
Altında **yumuşama gerilimi `~0.08–0.12 V`, erime gerilimi `~0.43 V`.** `0.16 V`'ta a-spot yumuşar ve mikro kaynak oluşur. Sıçrama sırasında gerilim kısa süreli olarak `0.43 V`'a yaklaşırsa altın kaplama yerel olarak erir. Sonuç: kaplamanın aşınması, alttaki Ni/BeCu'nun açığa çıkması ve fretting korozyonu. Birkaç yüz swap sonra `18 mΩ`'luk kontak `50–200 mΩ`'a çıkar. `0.8 V` kalıcı ark için yetersiz (minimum ark gerilimi `~12 V`), ama **yumuşama ve kaynak için fazlasıyla yeterli.**

### 5.4 Toplam enerji kaybı ve zaman sabiti
OCV eğimini kapasitör gibi modelleyelim: `%80 SoC ≈ 0.64 Ah`, `0.80 V` aralığında.
```
C_hücre ≈ 0.64 Ah × 3600 / 0.80 V ≈ 2 880 F (eşdeğer)
C_eş    = (2880 × 8640) / (2880 + 8640) = 2 160 F
E_kayıp = ½ × C_eş × ΔV² = ½ × 2160 × 0.64 ≈ 691 J ≈ 0.19 Wh   (R'den bağımsız)
τ       = R × C_eş = 0.055 × 2160 ≈ 119 s
Son SoC = (100 + 3×20)/4 = %40 ; Q4 480 mAh verir, diğerleri 160'ar mAh alır
```

Isının dağılımı:
- Q4 içinde: `691 × 28/55 ≈ 352 J`. Adyabatik varsayımla `ΔT ≈ 17 K`.
- Karonun termal zaman sabiti `~20 J/K ÷ (10 W/m²K × 0.0064 m²) ≈ 310 s`. Bu, `τ = 119 s` ile aynı mertebede, yani ısının çoğu karoda birikir. Q4 tahminen **`~35–40 °C`'ye çıkar ve `36.2 °C` NTC kesmesi tetiklenir.**
- Kontaklarda: `691 × 7/55 ≈ 88 J`. Bu ısı birkaç mm³'lük kontak bölgesine yoğunlaşır.

### 5.5 Ters senaryo daha da tehlikeli
Kullanıcı `%20`'lik bir karoyu üç tam dolu karonun arasına takarsa, toplam akım yine `~14.5 A` olur ama **tamamı tek bir hücreye şarj olarak girer.** Bu `~18C` şarj, `~72 mA/cm²` demek, yani CCD'nin `70–240` katı. **Tek seferde dendrit ve iç kısa devre beklenir.** Bu, çok olası bir kullanıcı senaryosu.

### 5.6 Senaryo B: Gerçekçi iç direnç (`0.3–2.5 Ω`)
`R_hücre = 1 Ω` için `R_döngü ≈ 1 + 0.33 + 0.02 ≈ 1.35 Ω`, `I ≈ 0.59 A` (`~0.74C`). Termal olarak sorun yok. **Ancak bu durumda:**
- ENR-11'deki `<28 mΩ` kapısı geçilemez.
- `25 W` şarj ve `10 W` tek karo şarjı olanaksız (gerilim düşümü `1.6–2.6 V`, ayrıca CCD aşılır).
- Ters senaryoda (§5.5) bile tek hücreye `~0.6 A`, yani `3 mA/cm²` girer. Bu oda sıcaklığında CCD'nin üstünde ve soğukta çok daha kötü.

**Çıkmaz şu:** Dosyadaki performans iddiaları (`28 mΩ`, `25 W`) doğruysa hot-swap tehlikeli. Hot-swap güvenliyse performans iddiaları yanlış. **Her iki durumda da doğrudan paralel bağlama yanlış bir mimari.**

### 5.7 Koruma donanımı BOM'da yok
- **"Aktif dengeleme" için gereken eleman yok:** Paralel hücreler aynı gerilimi paylaşır. Paralelde "dengeleme" ancak her karonun akımı kontrollü bir dönüştürücüyle ayarlanırsa mümkün. Bunun için endüktör ya da anahtarlamalı kapasitör gerekir. BOM'da (#11 `3.2 × 2.8 × 0.38 mm` ASIC) **hiçbir endüktör yok.**
- Dead-Pad anahtarı (#13, `2 × 2 mm`): WLCSP yük anahtarları bu boyutta tipik olarak `~4–6 A` taşır. `14.5 A`'lik bir ani akım SOA sınırını aşar.
- **Sigorta, PTC veya akım ölçüm şöntü yok.**
- NTC'ler hücre sıcaklığını ölçer. Kontaklardaki a-spot ısınmasını **algılayamaz**, çünkü ısıl kütle çok küçük ve tepki süresi saniyeler mertebesinde.
- Akış şöyle: 3 ms'lik kimlik doğrulama bitiyor, FET kapanıyor ve kontrolsüz bir paralel bağlantı oluşuyor. "Balances the new tile" ifadesinin arkasında donanım karşılığı yok.

### 5.8 Önerilen düzeltme
1. **Karo başına çift yönlü buck-boost dönüştürücü ile ortak VSYS barası:** Her karo akımı ayrı ayrı programlanır (örneğin `≤0.3C`). Şarj ve deşarj sıcaklık ve SoC'ye göre sınırlanır. Bunun için yaklaşık `2 × 2 × 1 mm` boyutunda bir endüktör ve yer gerekir. Mevcut Z bütçesiyle bu sığmaz (§7).
2. **Alternatif olarak ideal diyot-OR deşarj ve yalnızca şarj cihazından şarj:** Karolar birbirini şarj edemez, yük en yüksek gerilimdeki karodan çekilir.
3. **Yumuşak başlatma (soft-start):** FET kapısını rampa ile kontrol et (`dV/dt` sınırı) ve `|ΔV| > 50 mV` olduğunda paralel bağlamayı reddet.
4. **Önce değen uzun GND ve sense kontakları, sonra güç kontakları** (make-first-break-last). Böylece ilk temas akımı önlenir.
5. **Kontak sınıfı:** VSYS kontağı başına `≥3 A` sürekli akım için tasarla ve sertleştirilmiş altın kaplama kullan (`≥0.76 µm`, Co veya Ni katkılı).

---

## 6 · Termal bütçe: Qi2.2 25 W ve 36.2 °C kesme sınırı

### 6.1 Isı atma kapasitesi
```
Toplam yüzey (iki yüz) A = 0.08 × 0.16 × 2 = 0.0256 m²
h (doğal konveksiyon + ışınım) ≈ 10 W/m²K
25 °C ortamda 36.2 °C sınırı: ΔT = 11.2 K → Q_max ≈ 10 × 0.0256 × 11.2 ≈ 2.9 W
```
Şarj sırasında cihazın bir yüzü şarj pedinin üzerinde durur. Ped hem bu yüzden ısı atımını engeller hem de kendisi ısınır. Bu yüzden gerçek değer `Q_max ≈ 1.5–2 W` civarında.

### 6.2 Şarj kaybı
- `0.18 mm` kalınlıkta Litz bobin, 4 ayrı `90°` sektör ve 4 ayrı doğrultucu ile uçtan uca verim gerçekçi olarak `%70–80`. `25 W`'ta bu **`5–7.5 W` kayıp** demek.
- Bunun üzerine hücrenin I²R kaybı eklenir: `4 × 1.64² × R`. `R = 28 mΩ` ile `0.3 W`, `R = 1 Ω` ile **`10.8 W`**.
- Sonuç: kayıp, ısı atma kapasitesinin **`3–8` katı.** NTC birkaç dakika içinde akımı keser. Ulaşılabilir sürekli şarj gücü gerçekte yaklaşık **`~4–8 W`** (ENR-12'deki `15–25 W` geçilemez).

### 6.3 `35.8 °C` kararlı durum ile `36.2 °C` kesme arasındaki marj
- Marj yalnızca **`0.4 K`.** Hassas NTC'lerin toleransı `±0.5 K`, komparatör histerezisi ve ofseti de buna eklenir. Sonuç: sık sık gereksiz kesme.
- Yazın ortam `35–38 °C` olur, gözlük alında `~34 °C` cilde yakın durur, cep vücut ısısındadır. Bu koşullarda cihaz **sürekli kesmede kalır.** IEC 62368-1'in uzun süreli temas sınırları (`~43–48 °C`) çok daha geniş. `36.2 °C` tercihi aşırı korumacı ve PEO'nun ihtiyacının (`≥60 °C`) tam tersi.

### 6.4 "`k_z = 1.5 W/m·K` aerojel yalıtkan" çelişkisi
Aerojelin ısıl iletkenliği `~0.015–0.02 W/m·K`. `1.5 W/m·K` cam (`~1`) ya da seramik seviyesi. Bu bir yalıtkan değil. Ya değer yanlış ya da malzeme. Ayrıca `0.05 mm` kalınlıktaki pirolitik grafit (`k_xy = 1100`) ısıyı düzlem içinde yayar ama dışarı atmaz. Darboğaz yüzeyden havaya geçiş (`h`) ve yayıcı bunu değiştirmez.

### 6.5 Manyetik ekranlama
- **Mu-metal** `µ_r > 25 000` değerine yalnızca DC ve düşük frekansta ulaşır. Qi frekansında (`~100–360 kHz`) girdap akımı kayıpları yüzünden etkisiz kalır ve ısınır. Doyma noktası `~0.75 T`. N52H mıknatısların (`Br ≈ 1.4 T`) yakınında **yerel olarak doyar.**
- `0.09 mm` FeSiB nanokristal ferrit, Qi2 mıknatıs halkasının (#20) DC alanında kısmen doyar. Bu, Qi2 tasarımlarında bilinen bir sorun. Bobin endüktansı kayar ve verim düşer.
- Bobinlerin hemen altında Al kese ve Cu akım toplayıcılar var. Ferrit doyarsa bunlarda girdap akımı ısınması oluşur, yani §6.2'deki kayıp daha da artar.
- Qi2 MPP sertifikası tek parça bir dairesel Rx bobini ve kesintisiz bir mıknatıs halkası varsayar. **4 ayrı karoya bölünmüş sektörler ve doğrultucular Qi2.2 uyumluluğu açısından belirsiz.** Bir karo çıkarıldığında MPP halkası da kırılmış olur.

---

## 7 · Geometri ve tolerans

### 7.1 Z yığını karo kalınlığını aşıyor

| Katman (karo başı) | Kalınlık (mm) |
|---|---|
| PC kabuk ×2 (#21) | 0.40 |
| Silikon OCA ×2 (#22) | 0.10 |
| T-OLED ×2 (#23) | 0.28 |
| AgNW/ITO ×2 (#24) | 0.08 |
| PDLC ×1 (#25) | 0.09 |
| Katı hücre (#1–4) | 1.08 |
| Kese (#5) | 0.09 |
| Ferrit + Mu-metal ×2 (#9) | 0.18 |
| Grafit yayıcı ×2 (#10) | 0.10 |
| Qi bobini (#7/#8, en kalın) | 0.18 |
| **Toplam** | **2.58** |

- **Karo kalınlığı `2.00 mm`. Aşım `+0.58 mm` (%29).** Bobinler bir boşluğa gömülse bile `2.40 mm`, kese hücreye dahil sayılsa bile `2.31 mm` çıkıyor.
- Yapıştırıcı katmanları, tolerans yığılması ve Li şişmesi (`~124–155 µm`, §4.3) bu hesaba dahil değil.
- Ti göbek (#15) `1.40 mm`, mıknatıslar (#17) `1.0 mm`, kontaklar (#18) `0.35 mm` kalınlıkta. Bunlar ancak kenar marjına yerleşebilir. O marjın sorunları §7.2'de.

### 7.2 Kenar marjı
- Karo `40 × 80 mm`, kese `35.4 × 75.4 mm`. Her kenarda **`2.3 mm`** kalıyor.
- Bu `2.3 mm`'ye sığması gerekenler: PC yan duvarı, 1.4 mm derinlikte mıknatıslar, 1.4 mm derinlikte kontaklar, Ø0.7 mm Ti pimler (#16), yan duvar elektrotları (#24) ve optik dudak. Bunlar iç içe yerleştirilmezse sığmaz, yerleştirilirse de tolerans payı kalmaz.
- **Ti göbek çakışması:** `6 × 6 mm`'lik göbek her karonun köşesine `3 × 3 mm` giriyor. Kese köşesi ise kenardan `2.3 mm` içeride başlıyor. Yani köşede **`0.7 × 0.7 mm`'lik bir çakışma** var. Kese köşesi `≥1 mm` yarıçapla yuvarlatılmazsa ve göbek bölgesinde yer açılmazsa parçalar çarpışır.
- **Tab:** `12.0 × 2.4 mm`'lik tab (#6) kısa kenardan çıkarsa `2.3 mm` marja sığmaz. Ya katlanması (ek kalınlık) ya da uzun kenar boyunca yerleştirilmesi gerekir. Uzun kenarda da mıknatıslarla çakışır.

### 7.3 Kese sızdırmazlığı
Kese ile hücre arasındaki fark `(35.4 − 35.0)/2 = 0.2 mm`. Al-laminat ısıl yapışma flanşı gerçek bir nem bariyeri için tipik olarak **`2–4 mm`** genişlik ister. `0.2 mm` flanş ile su buharı kenarlardan girer ve LLZO bozulur (§4.2). "Zero-outgassing" ve "hermetic" iddiaları bu geometriyle karşılanamaz.

### 7.4 Gözlük olarak kullanımda saydamlık
- Hücre alanı `35 × 75 = 2 625 mm²`, karo alanı `40 × 80 = 3 200 mm²`. **Karonun `%82`'si opak.** Bu alanda Al kese, Cu ve Li katmanları, ferrit, Mu-metal ve bobinler var.
- Saydam T-OLED ve "`0 V` clear glass" PDLC iddialarıyla birlikte düşünülünce bu karodan bakarak **görmek olanaksız.** Gözlük kullanım senaryosu mimariyle çelişiyor.
- Kütle de sorunlu: göz önünde `68–72 g`. Tipik gözlükler `20–35 g`, akıllı gözlükler `~50 g` civarında.

---

## 8 · Hot-swap mantığı ve köprü kapasitörü

### 8.1 Zaman çelişkisi
- §3.1'de: "`<0.8 ms` içinde `0 V`".
- §3.4, ENR-12 ve BOM #13'te: "`3 ms` handshake".
İki değer aynı işlem için mi kullanılıyor, ayrı işlemler mi, tanımlı değil. `3 ms`'lik kimlik doğrulama, kontak sıçramasının (`~1–10 ms`) bitmesini beklemiyor. FET sıçrama sürerken kapanırsa §5.3'teki hasar kaçınılmaz.

### 8.2 `180 mF` "ince-film seramik/polimer" kapasitör (#14)
```
Hacim = 14 × 4 × 0.25 = 14 mm³  →  180 mF / 14 mm³ ≈ 12.9 mF/mm³
En yoğun MLCC'ler: ~10–15 µF/mm³ (ör. 100 µF / 1206 ≈ 8 mm³)
→ İddia, MLCC sınırının ~1 000 katı. Ancak bir EDLC süperkapasitör bu seviyeye yaklaşır, o da seramik değildir.
```

Kapasitör sığsaydı bile köprü süresi yetmezdi:
```
E = ½ × 0.18 × (3.7² − 3.0²) ≈ 0.42 J  →  0.85 W'ta ≈ 0.5 s   (iddia: 3 s)
3 s için gereken: C = 2 × 2.55 J / 4.69 V² ≈ 1.09 F
```
Kaldı ki diğer 3 karo zaten yükü taşıyor, bu kapasitörün amacı da belirsiz.

---

## 9 · Dosyalar arası ve dosya içi çelişkiler

| # | Çelişki | Kaynak |
|---|---|---|
| Ç-1 | `68.0 g` (4×17) ile `72.00 g` (4×18). BOM satırlarının toplamı `72.00 g`, toplam satırı ise "`72.00 g (4 × 17 g)`" diyor ve `4 × 17 = 68`. | 11 §1/§2, 15 başlık ve toplam satırı |
| Ç-2 | `750 Wh/L` ile `3.0 Wh / 2.83 mL = 1 058 Wh/L` | 11 §2 |
| Ç-3 | "`LiFePO4/NMC`" ile `800 mAh × 3.75 V = 3.0 Wh` (LFP ile tutmaz) | 11 §2 |
| Ç-4 | `<0.8 ms` Dead-Pad ile `3 ms` handshake | 11 §3.1 ve §3.4 |
| Ç-5 | "Active cell balancing" var ama BOM'da endüktör veya dönüştürücü yok | 15 #11 |
| Ç-6 | "Aerogel insulator" ile `k_z = 1.5 W/m·K` | 11 §2, 15 #10 |
| Ç-7 | `0%` swelling ve `<2.5 µm` Z-basamak ile Li-metal şişmesi (`~120 µm`) | 11 §1/§3, 15 #16 |
| Ç-8 | `2.00 mm` karo ile `≥2.40–2.58 mm` yığın | 15 tamamı |
| Ç-9 | "Non-flammable" ile PEO'nun organik ve yanıcı olması | 11 §1, 15 #1–4 |
| Ç-10 | Saydam gözlük kullanımı ile `%82` opak hücre alanı | 11 §1, 15 #23/#25 |
| Ç-11 | `36.2 °C` kesme ile PEO'nun `≥60 °C` çalışma ihtiyacı | 11 §2 |
| Ç-12 | `25 W` şarj ile `~2.9 W` ısı atma kapasitesi ve CCD | 11 §2, ENR-12 |
| Ç-13 | `180 mF` / `14 mm³` / "<3 s glitch-free" | 15 #14 |
| Ç-14 | `SAR = 0.054 W/kg`: hesap doğru (`2.0/0.054 = 37×`), ama RF vericisi BOM'da tanımlı değil. Değer neye göre ölçüldü belirsiz. | 11 §2 |
| Ç-15 | "`25 part groups (52 physical body subparts)`": BOM'daki adetlerden 52 sayısı türetilemiyor (kontaklar, mıknatıslar ve pimler sayılınca 100'ün üzerinde çıkıyor). | 15 toplam satırı |

Doğru çıkan hesaplar: `12.0/0.85 = 14.1 h` ✓, `3 × 3.0 = 9.0 Wh` ✓, `64 / 4 yarım eksen = 16`, `2 × 16 = 32` kontak/karo ✓, `35 × 75 × 1.08 = 2.83 mL` ✓. Çalışma süresi hesabı ise dönüşüm verimini (`~%85–90`) ve düşük sıcaklıkta kullanılabilir kapasiteyi hesaba katmıyor. Gerçekçi değer `~12 h` (25 °C), soğukta çok daha az.

---

## 10 · Tasarım için öneriler

1. **Enerji iddialarını düzelt:** Paketlenmiş hücre için `≤600 Wh/L` hedefle (`~1.7 Wh/karo`, `~6.8 Wh` toplam). Ya da kalınlık bütçesini artır.
2. **Kimyayı netleştir:** Oda sıcaklığı ve soğuk çalışma şartsa PEO uygun değil. Sülfür (LPSCl, `~10⁻³ S/cm`) veya halojenür (Li₃InCl₆ gibi) katı elektrolitler düşünülebilir, ama ikisinin de nem ve yığın basıncı sorunları var. Daha gerçekçi bir yol yarı katı ya da jel polimer ve LFP/grafit kombinasyonu. "Sıfır sıvı" iddiasından vazgeçilerek güvenlik paketleme ve BMS üzerinden sağlanabilir.
3. **Paralel mimariyi değiştir:** Karo başına çift yönlü DC-DC dönüştürücü kullan, `ΔV > 50 mV` ise paralel bağlamayı reddet, soft-start uygula, önce GND/sense sonra güç kontağı değsin, sigorta veya eFuse ekle.
4. **Şarjı sınırla:** `T < 10 °C` ise şarj etme. `10–25 °C` arasında `≤0.2C`, oda sıcaklığında `≤0.5C` uygula. Qi gücünü termal modelle sınırla (`~5 W` sürekli).
5. **Termal pencere:** Kesme sınırını IEC 62368-1 temas sınırlarına göre yeniden belirle (örneğin `43 °C` dış yüzey) ve hücre sıcaklığını ayrı izle. `0.4 K` marjı en az `3 K`'e çıkar.
6. **Geometriyi yeniden düzenle:** Z bütçesini `2.6–3.0 mm`'ye çıkar ya da katmanları azalt (örneğin tek yüzlü OLED, PDLC'yi kaldırmak). Kese için `≥2 mm` flanş, Ti göbek için köşe boşluğu ve tab yerleşimi gerekli.
7. **Gözlük kullanımında** batarya saydam görüş alanının dışına (sap veya köprü bölgesine) taşınmalı. Görüş alanında %82 opaklık kabul edilemez.

---

## 11 · Yeni veya güncellenmiş doğrulama kapıları

| Kapı | Koşul |
|---|---|
| ENR-11r | `0 °C`, `10 °C`, `25 °C`'de EIS ve DCIR. `0.85 W` yükte `0 °C`'de VSYS düşümü `<200 mV`. |
| ENR-22 (yeni) | `4.20 V` ile `3.40 V` arası en kötü durum hot-swap: tepe akım `≤1 A`, kontak sıcaklığı artışı `≤10 K`, kontak direnci 10 000 swap sonrası `≤25 mΩ`. |
| ENR-23 (yeni) | Ters swap (`%20` karo üç tam dolu karoya): karoya giren akım `≤0.3C`, CCD testinde kısa devre yok. |
| ENR-24 (yeni) | `%0` ile `%100` SoC arası karo kalınlık değişimi `≤10 µm` (ölçüm: lazer profilometre). |
| ENR-12r | Ortam `25 °C`, ped üzerinde sürekli şarj. Tüm yüzeyler kesme sınırının altında kalırken ulaşılan güç kaydedilir. |
| ENR-15r | Çivi ve ezme testi GB/T 31485 veya UL 1642 uyarınca, `%100 SoC` ve `60 °C` ön koşullu. HF yerine "algılama limiti altında" kriteri. |

---

**Özet:** Bu enerji sistemi kağıt üzerinde tutarlı görünen ama fiziksel olarak birbiriyle çelişen hedefleri birleştiriyor: oda sıcaklığında PEO, `28 mΩ`, `1 058 Wh/L`, `0%` şişme, `2 mm` karo, `25 W` şarj, `36.2 °C` kesme ve doğrudan paralel hot-swap. Madde 2'deki senaryoda, dosyanın kendi değerleri kabul edilirse ilk anda `~14.5 A` / `~18C` akım, `~11.6 W` döngü gücü ve `~690 J` kayıp oluşur. Kontaklarda yumuşama ve kaynak, Q4'te `~40–60 s` içinde NTC kesmesi ve alıcı hücrelerde dendrit kaynaklı kısa devre riski beklenir. Bu, sadece dosyadaki sayılarla yapılmış bir hesap. Gerçek davranış ölçümle doğrulanmalı, ama mimari bu haliyle onaylanamaz.

### W3_A2_OPUS_QI22_AND_EDDY_CURRENT_AUDIT · Model: `claude-opus-5-5` (Router: `coding-router-preview`, Başlangıç: `2026-10-12 14:44:21 +03`, Bitiş: `2026-10-12 14:54:51 +03`, Süre: `629.88 sn`, Uzunluk: `28,027` karakter)

# Budlum Leaf Rev. L.5.0 — Qi2.2 kablosuz güç, manyetik alan ve eddy akımı denetimi

**İncelenen dosyalar:** `02-ELECTRONICS-AND-BUSES.md`, `04-PORT-RAIL.md`, `14-PORT-RAIL-PART-BY-PART.md`
**Yöntem:** Bu bir analitik masa başı denetimidir. FEM simülasyonu ya da ölçüm yapılmadı. Tüm sayılar kapalı form fizik formülleriyle ve açıkça yazılmış varsayımlarla hesaplandı. Dosyalarda olmayan değerler (sarım sayısı, mıknatıs boyutu, kontak konumu) için aralık verdim.

---

## 0. Özet

| # | Bulgu | Önem |
|---|---|---|
| 1 | 4 sektörlü Ø54 bobin, dosyadaki kontak sayısıyla **sürekli bir spiral olarak kurulamaz**. Kurulabilen tek yapı "D-sektör" halkalardır. Bu yapıda radyal akım bacakları tam olarak `+` derzinin üzerine düşer ve bobin içindeki Ø32 mm iç bölgenin akısı **hiç toplanmaz**. Tahminen k 2–3 kat düşer. %86 verim iddiası tutmaz, gerçekçi değer yaklaşık %65–72. | **Kritik** |
| 2 | Derz bir **gömülü yabancı cisim** gibi davranır. İyi senaryoda derzdeki eddy kaybı yaklaşık 0.1–0.3 W ve yerel ısınma +1…+7 K. D-sektör topolojisinde (derzde 10–15 mT alan) kayıp yaklaşık 2–4 W ve derz yaklaşık **60–105 °C** olur. Tek tek mıknatıslarda yerel olarak N52H'nin 120 °C sınırı aşılabilir. | **Kritik** |
| 3 | Derzi dört kez geçen **GND/VSYS halkası** ve birbirine değebilecek **N52H Qi2 halka yayları**, bobin akısını çevreleyen **kısa devre sargı** oluşturur. Bu yollarda 1–2 W ek kayıp ve kuplaj çöküşü beklenir. | **Kritik** |
| 4 | Rezonans kondansatörleri (8 × 0201 C0G) ne gereken kapasiteyi (360 kHz'de yaklaşık 22 nF, 127.7 kHz'de yaklaşık 170 nF) ne de gerilimi (yaklaşık 70 V tepe) sağlayabilir. | **Kritik** |
| 5 | Soru 2: 5 W ısı, 36.2 °C sınırını **her senaryoda** aşar. En iyi ideal durumda yüzey yaklaşık 41 °C, pedin üstünde yaklaşık 58 °C, bobin üstündeki yerel sıcak bölgede 60 °C üstü olur. 36.2 °C altında kalarak sürekli taşınabilecek ısı yaklaşık **0.6–1.8 W**, bu da yaklaşık **3–6 W** gerçek şarj gücüne karşılık gelir. | **Kritik** |
| 6 | LLZO/PEO hücre 25 W'ta yaklaşık **2.1 C** ile şarj edilmek isteniyor. PEO bazlı elektrolit iyi iletkenlik için 50–80 °C ister. Bu, 36.2 °C sınırıyla fiziksel olarak çelişir. | **Kritik** |
| 7 | Dosyalarda birbiriyle çelişen çok sayıda değer var: "<8 mW" seam kaybı (gerçekte 100 mW'tan fazla), 0.38 % gerinim (gerçekte 3.9 %), 8 ile 16 AC kontağı, 3 A VSYS ile 6.25 A ihtiyacı, 0.08 µT iddiası, "nanokristalin FeSiB", 27 W Qi2.2 gibi. | Yüksek |

---

## 1. Soruların öncülleri dosyalarla tutuyor mu?

| Sorudaki öncül | Dosyalarda olan | Sonuç |
|---|---|---|
| "`+` derzinde 24 adet N52H" | Üç dosyada da **yok**. Dosyalarda yalnızca B-stem'de 8 × N52H (Part 32, 3.2×1.6×1.1 mm), kenar tutucu şeritleri (Part 10) ve **Ø56 mm Qi2 hizalama halkası (4 yay, Part 4)** var. | Derz mıknatısları büyük olasılıkla başka bir dosyadan (03/05?) geliyor. Burada **varsayım** olarak hesapladım. Boyut için Part 32'yi vekil aldım. |
| "80 µm Nitinol yapboz telleri" | Üç dosyada da **yok**. | Varsayım olarak hesapladım. |
| "64 altın yaprak alanın içinden geçiyor" | 64 kontak (4 × 16) **derzin tamamına** dağılmış: x=0 boyunca 160 mm, y=0 boyunca 80 mm. Bobin yalnızca R ≤ 27 mm içinde. | Eşit aralık varsayımıyla 64 kontağın yaklaşık 30–32'si R ≤ 27 mm bölgesine düşer: ±X yarı eksenlerinde 2.5 mm aralıkla yaklaşık 10–11'er, ±Y yarı eksenlerinde 5 mm aralıkla yaklaşık 5–6'şar. Bobin akımını gerçekten taşıyanlar yalnızca `QI2_AC_RING` kontaklarıdır: 02'ye göre 8 adet, 14'e göre 16 adet ("8 pairs"). Bu da bir çelişki. |
| "%80 verim, 5 W ısı" | 04 dosyası **%86** diyor. | 25 W **çıkış** gücüyse %80'de kayıp 6.25 W olur, 5 W değil. Kaybın da hepsi cihazda değildir, bir kısmı vericide kalır. Ayrıntısı §5.1'de. |
| "Isı doğrudan PC ekranın merkezinde" | Isı bobinde, doğrultucu IC'de, buck dönüştürücüde, bataryada ve derzde oluşur. PC bir **ısı yalıtkanıdır** (k ≈ 0.2 W/m·K). | Isının dağılımı farklı, ama sonuç daha da kötü (§5). |

---

## 2. Taban fizik parametreleri (f = 360 kHz, ω = 2.262·10⁶ rad/s)

Deri kalınlığı: δ = √(2ρ / (ω·µ₀·µr))

| Malzeme | ρ (Ω·m) | µr | δ @360 kHz | Ne anlama geliyor |
|---|---|---|---|---|
| Bakır (Litz) | 1.72e-8 | 1 | **110 µm** | 0.18 mm tel (r = 90 µm) sınırda. Yakınlık etkisi büyük. 360 kHz'de normalde 40–80 µm tel kullanılır. |
| BeCu C17200 (yaprak) | ~7.7e-8 | 1 | **233 µm** | Yaprak 350 µm kalın, yani δ'dan büyük. Eddy kaybı kayda değer. |
| NdFeB (N52H) | ~1.5e-6 | ~1.05 | **~1.0 mm** | mm boyutlu mıknatısın tüm hacmi kayıp üretir. |
| NdFeB üzerindeki Ni-Cu-Ni kaplama (Ni) | 7e-8 | ~100 (doymamış) | **~22 µm** | Kaplama ferromanyetik: hem histerezis hem eddy kaybı. Cu ara katı direnci düşürür. |
| NiTi (Nitinol) | ~8.2e-7 | ~1 | **~760 µm** | 80 µm tel tamamen düşük frekans rejiminde. |
| Mu-metal | ~5.5e-7 | 25 000 (DC) | **~4 µm** (360 kHz'de µr birkaç bine düşerse yaklaşık 10–20 µm) | 360 kHz'de "kalkan" değil, **kayıplı bir iletken levha**. |

**Alan büyüklükleri (varsayım):**
- **Verici–alıcı arasındaki eksenel alan:** MPP verici bobini yaklaşık 10 sarım, yaklaşık 4 A_rms, R ≈ 20 mm alırsak B = µ₀NI/(2R) ≈ 1.8 mT tepe. Ferritle birlikte **≈ 2–3.5 mT**.
- **Alıcı akımı:** 25 W ve V_rect ≈ 12 V için I_dc ≈ 2.1 A. Bobin akımı ≈ 1.11 × 2.1 ≈ **2.3–2.8 A_rms** (yaklaşık 3.5 A tepe).
- **Alıcı bobin endüktansı:** R = 16–27 mm, N ≈ 10 için Wheeler formülü yaklaşık 6.2 µH verir. Ferritle **≈ 8–9 µH**.
- **Bobin üzerindeki reaktif gerilim:** V_L = ωLI ≈ 2.262e6 × 9e-6 × 3.5 ≈ **70 V tepe**.
- **Sarım başına indüklenen gerilim:** ≈ 1–1.5 V_rms.

---

## 3. Temel hata: 4 sektörlü bobin bu kontaklarla kurulamıyor

### 3.1 Spirali dörde bölmek
Sürekli bir spiral bobini x=0 ve y=0 hatlarından kesersek, **her sarım her derz geçişinde bir kontak** ister. N = 10 için 10 × 4 = **40 kontak** gerekir. Dosyada AC halkasına ayrılan kontak sayısı **8** (02: her yarı eksende 7–8) ya da **16** (14: "x 8 pairs"). Yani sürekli spiral **mümkün değil**.

### 3.2 Geriye kalan tek yapı: D-sektör (pasta dilimi) halkalar ve sonuçları
Her çeyrek kendi içinde kapalı bir sektör sargısıdır. Dört sektör seri bağlanır ve 8 kontak buna yeter. Ama bunun bedeli var:

1. **Radyal bacaklar derzin üzerinde.** Her sektörün 0° ve 90° kenarlarındaki N sarımlık bacaklar tam olarak ±X ve ±Y derzlerine paralel uzanır. Komşu sektörlerin bacaklarında akım **ters yönlüdür**. Uzak alanda birbirlerini götürürler, ama **aralarındaki boşlukta alan toplanır**. Bacaklar arası d = 2 mm için:
   B_orta = 2µ₀(NI)/(πd) = 2 × 1.2566e-6 × 35 / (π × 0.002) ≈ **14 mT tepe**.
   Bu, normal verici–alıcı alanının yaklaşık 5–7 katıdır. Ve tam olarak altın yaprakların, mıknatısların ve Nitinol tellerinin bulunduğu yere düşer.
2. **İç bölgenin akısı toplanmıyor.** Sektörler R = 16..27 mm arasında. Klasik bir spiralde her sarım içteki Ø32 mm diski (yaklaşık 804 mm², vericinin en güçlü olduğu bölge) çevreler. D-sektörde bu alanı **hiçbir sarım çevrelemez**. Sarım başına etkin alan yaklaşık 1452 mm² yerine yaklaşık 743 mm²'dir. Merkezde B daha yüksek olduğu için alanla ağırlıklandırınca **M ≈ %35–50'ye** düşer.
3. **Verime etkisi.** η_max = k²Q₁Q₂ / (1+√(1+k²Q₁Q₂))²
   - Klasik spiral: k = 0.5, Q₁ = Q₂ = 50 → yalnızca bobinden bobine η ≈ %92.5
   - D-sektör: k ≈ 0.2, Q₂ ≈ 30 (bacaklar ve kontaklar yüzünden) → η ≈ %77
   - İnvertör (≈ 0.95) ve doğrultucu (≈ 0.93) ile çarpınca uçtan uca **≈ %68**.
   **04'teki "%86 verim" ve Part 3'teki "86% eff." bu topolojiyle tutarsız.**
4. Kuplaj düştüğü için verici aynı gücü vermek için daha fazla akım sürer. Bu da derzdeki B'yi ve dolayısıyla eddy kaybını (B² ile) artırır. Ayrıca sabit tasarımlı MPP vericileri bu gerilim/akım sınırında **25 W'a hiç ulaşamayabilir**.

### 3.3 Bakır kütlesi ve direnç
Part 1: 4 sektörün toplam kütlesi 1.40 g. Toplamın gerçekten 4.80 g ettiği tablodan doğrulanıyor, yani 1.40 g dört sektörün toplamı. Bu yaklaşık 156 mm³ bakır demek.
- Klasik spiral, N = 10: toplam tel boyu ≈ 1.35 m, kesit ≈ 0.116 mm² → R_dc ≈ 0.20 Ω.
- D-sektör, sarım başına 88 mm radyal bacak eklenince: toplam boy ≈ 2.23 m, kesit ≈ 0.07 mm² → R_dc ≈ 0.55 Ω. 0.18 mm telde yakınlık etkisiyle R_ac ≈ 0.7 Ω.
- Seri 4 kontak × 18 mΩ eklenince R ≈ 0.3–0.8 Ω. **Bobin kaybı 2.5² × R ≈ 1.9–4.9 W.** Yalnızca bu kalem, soru 2'deki 5 W'ın tamamını tek başına doldurabilir.
- "0.18 mm Litz" ifadesi belirsiz. Bu demet çapıysa bakır kesiti yaklaşık 0.025 mm² olur ve direnç birkaç Ω'a çıkar, 25 W imkânsızlaşır.

### 3.4 Rezonans kondansatörleri (Part 7) karşılanamıyor
- 360 kHz, L = 9 µH için C = 1/(ω²L) ≈ **21.7 nF**. 127.7 kHz için ≈ **173 nF**.
- Gerilim: V_C = I/(ωC) ≈ 3.5 / (2.262e6 × 21.7e-9) ≈ **71 V tepe**.
- 0201 boyutunda (0.6 × 0.3 mm) C0G kondansatörler pratikte nF mertebesinde ve 25–50 V sınıfında kalır. Karo başına 8 adet yaklaşık 8–17 nF eder. Sektör başına dağıtılmış seri kondansatör kullanılsa bile her sektör yaklaşık 87 nF / 18 V ister. **Hem kapasite hem gerilim tutmuyor.** İki frekansı (127.7 ve 360 kHz) karşılamak ayrıca anahtarlamalı kondansatör bankası ve FET ister. BOM'da bunlar yok.
- **Ø22 mm yerel bobinin rezonans kondansatörü (Cs, gerekirse Cd) BOM'da hiç yok.** Part 7 yalnızca merkezi bobin için tanımlanmış.

### 3.5 Hangi doğrultucu? (Part 5 / QB bloğu)
- Her karoda bir tane, yani **4 × U_QI (her biri 25 W)** var. Seri bir AC halkasının ise yalnızca **2 ucu** olur. Halka 4 doğrultucuya birden bağlanırsa doğrultucular arasında çekişme ve dolaşan akım oluşur. Tek doğrultucuya bağlanırsa diğer üç tanesi gereksiz kalır.
- Tek doğrultucu senaryosunda 25 W'ın 4 bataryaya derz üzerinden dağıtılması gerekir. 25 W / 4 V = **6.25 A**, ama VSYS "up to **3.0 A**". 3 A × 4 V = 12 W. **25 W dağıtılamaz.**
- 3.2 × 2.8 mm'lik paketin 25 W'ta yaklaşık %92–94 verimle 1.5–2 W harcaması, ısı yayıcı (grafit ya da buhar odası) olmayan 2 mm PC karoda yerel olarak +60…+120 K demektir.
- **Pil boşken kilitlenme:** Dead-Pad kuralına göre kontaklar 3 ms kimlik doğrulama bitene kadar 0 V'ta kalıyor. Bobin halkası kapanmadan doğrultucu enerji alamaz. Kimlik doğrulama içinse enerji gerekir. Dört pil de tamamen boşsa merkezi Qi2.2 **hiç devreye giremez**. Kurtarma yalnızca Ø22 yerel bobinlerle mümkün.
- **"0 V" iddiası `QI2_AC_RING` için fiziksel olarak yanlış.** Bobin alan içindeyken indüklenen gerilim FET'ten bağımsızdır. Ping sırasında bile birkaç V, güç aktarımında yaklaşık 70 V tepe reaktif gerilim kontaklarda görünebilir. Seri FET koyarsanız 4 × Rds_on kaybı eklenir.

---

## 4. Soru 1: Derzdeki eddy (Foucault) kayıpları ve sıcaklık

### 4.1 Kullanılan formüller (düşük frekans yaklaşımı, zaman ortalaması)
- Normal alandaki ince disk: P = σω²B₀²·π·a⁴·t / 16
- Normal alanda, en dar kenarı w olan levha: P/V ≈ σω²B₀²·w² / 24 (dikdörtgende yaklaşık 0.5 düzeltme çarpanı)
- Enine alandaki tel, birim boy başına: P' ≈ π·σω²B₀²·r⁴ / 16 (mertebe)
- Kapalı halka: EMF = ω·Φ, P = EMF²·R / (R² + X²)
- Isı: derzi iki yana açılan çizgisel kaynak gibi düşündüm (iki taraflı kanatçık modeli). ΔT = q' / (2·√(2h·k·t)), h ≈ 12 W/m²K.
  - Saf PC: k·t = 0.2 × 0.002 = 4e-4 W/K → ΔT ≈ 5.1·q'
  - Bakır ve batarya folyosu katkısıyla k·t ≈ 0.03 W/K → ΔT ≈ 0.6·q'

### 4.2 Altın yapraklar (BeCu, 1.4 × 0.9 × 0.35 mm, Au/Ni)
| Mekanizma | Hesap | Sonuç |
|---|---|---|
| Eddy, yaprak düz yatıyorsa, B = 2 mT | a_eş = 0.63 mm, t = 0.35 mm. a·t/δ² ≈ 4 olduğundan reaksiyon alanı kaybı biraz düşürür. | **≈ 1.5–3 mW/yaprak**. 30 yaprakla ≈ 45–90 mW |
| Eddy, yaprak derz duvarında dikse, D-bacakları arasında 14 mT | B, 1.4 × 0.35 mm kesiti görür. w = 0.35 mm, V = 0.44 mm³. P ≈ 150·B² W | **≈ 15–30 mW/yaprak**. 20–30 yaprakla ≈ 0.4–0.9 W |
| **Halka akımından omik kayıp (asıl kalem)** | I = 2.5 A_rms, R ≈ 18 mΩ, AC'de yaklaşık 20–22 mΩ | **≈ 0.11–0.14 W/yaprak**. 4–8 yaprakla **≈ 0.45–1.1 W** |
| Ni alt kaplama | Ferromanyetik ve yaklaşık 1–3 µm. Histerezis kaybı küçük ama manyetik alanı odaklar. | İkincil |

Ek riskler:
- Kontak direnci yaprak başına yaklaşık 0.3–0.5 N yay kuvvetine bağlıdır. 64 yaprak tolerans yığılmasında yaklaşık **19 N açıcı kuvvet** üretir. Derz kilidi bunu tutamazsa direnç artar, Q düşer ve FOD tetiklenir.
- Mikro kayma (fretting) ve Ni gözeneklerinde oksitlenme 18 mΩ'u zamanla 50–100 mΩ'a çıkarır. Bu da ısınmayı ve kaybı artırır, döngü kendini besler.
- Karo 2.5 A taşırken ayrılırsa ("<3 s" söküm) ½LI² ≈ 55 µJ'lük ark oluşur. Altın her ayrılmada aşınır.
- Islak derzde yaklaşık 70 V tepe ve 360 kHz AC potansiyel, Ni katmanında elektrolitik korozyon başlatır. IP68 bunu engellemez, yalnızca suyun girmesini sınırlar.

### 4.3 Derzdeki N52H mıknatıslar (varsayım: 24 adet, 3.2 × 1.6 × 1.1 mm, derz boyunca 10 mm aralık → yaklaşık 10 tanesi R ≤ 27 mm)
- P ≈ 0.5 × σω²B²w²/24 × V. σ = 6.7e5, w = 1.6 mm, V = 5.6 mm³ → **P ≈ 1000·B² W/mıknatıs**
  - B = 2 mT: **≈ 4 mW**. 10 mıknatısla ≈ 40 mW
  - B = 3.5 mT (merkez): ≈ 12 mW
  - B = 14 mT (D-bacak boşluğu): **≈ 0.2 W/mıknatıs**. 10 mıknatısla **≈ 2 W**
- **Yerel sıcak nokta:** PC içine gömülü mıknatıs için yayılma direnci R ≈ 1/(4·k·a) = 1/(4 × 0.2 × 1.2e-3) ≈ 1000 K/W. 0.2 W'ta kaba sınır **≈ +100…200 K**. N52H'nin en yüksek çalışma sıcaklığı yaklaşık **120 °C**. Bu aşılırsa mıknatıs **kalıcı olarak mıknatıslığını kaybeder** ve derz kilidi zayıflar. PC'nin Tg değeri (yaklaşık 145–150 °C) bile tehlikeye girer.
- Ni-Cu-Ni kaplamadaki **Cu ara katı** (yaklaşık 5–10 µm) yüzey direncini düşürür ve kaybı artırır.
- **DC kutuplama sorunu:** Mıknatıslar ferritin yanında yerel doyma yaratır. %10 endüktans düşüşü rezonansı yaklaşık %5 kaydırır (360 → yaklaşık 378 kHz). Sabit 360 kHz'te çalışan MPP vericisinde bu doğrudan verim kaybıdır. Karo konum toleransı her montajda L değerini değiştirir.

### 4.4 80 µm Nitinol teller
- Açık (halka oluşturmayan) tel, r = 40 µm: P' ≈ 3·B² W/m. 14 mT'da bile yaklaşık **0.6 mW/m**. **İhmal edilebilir.**
- **Kapalı halka oluşursa durum tamamen değişir.** Teller derz boyunca birleşip bobin akısını çevreleyen bir halka oluşturursa:
  - Halka çapı Ø54, B = 1 mT → EMF = ωBA = 2.262e6 × 1e-3 × 2.29e-3 ≈ **5.2 V tepe**
  - Tel direnci (yaklaşık 170 mm): R = ρL/A ≈ 28 Ω → P ≈ 5.2² / (2 × 28) ≈ **0.5 W**, 80 µm'lik bir telin içinde
  - Bu tel saniyeler içinde ısınır ve Nitinol'ün **Af dönüşüm sıcaklığını** (tipik olarak 30–90 °C) geçer. Faz dönüşümü yapboz kilidinin şeklini ve rijitliğini değiştirir: kilit kendiliğinden açılabilir ya da sıkışabilir. Bu bir **elektromekanik güvenlik riski**.
- Küçük yapboz sekmeleri (yaklaşık 2 × 2 mm halka) yalnızca yaklaşık 0.1 mW üretir. Zararsız.

### 4.5 Ø56 mm Qi2 hizalama halkası (Part 4, 0.52 g, 4 yay)
- Kesit = 0.52 g / 7.5 g/cm³ / 176 mm ≈ **0.39 mm²**. Gövde direnci ≈ 0.67 Ω, Cu ara kat paralelde ≈ 0.11 Ω.
- Yaylar derzde birbirine değerse (mıknatıslar derzin iki yakasında birbirini çeker, Ni kaplama iletkendir) **tüm bobin akısını çevreleyen kısa devre sargı** oluşur.
  - EMF ≈ 1.2 V_rms. X = ωL ≈ 0.34 Ω (L ≈ 0.15 µH). R ≈ 0.2–0.5 Ω → I ≈ 2–3 A → **P ≈ 1–2.2 W**
  - Bunun yanında akıyı dışarı iterek kuplajı çökertir. Sonuç: FOD durdurması.
- Yaylar birbirine değmese bile halka bobin dış çapına (R = 27) yalnızca yaklaşık 1 mm uzakta. Dış sarımların yakın alanında yaklaşık 2 mT görür, yaklaşık 15 mW eddy kaybı oluşur.
- Halka 0.52 g. MagSafe/Qi2 referans tasarımlarındaki mıknatıs dizisine göre çok hafif. 68 g'lık gövdeyi dik tutma ve merkezleme kuvveti şüpheli. 4 yaya bölünmüş halkanın Qi2 MPP referans mıknatıs geometrisine uyduğu da **gösterilmemiş**.

### 4.6 Derzi dört kez geçen GND/VSYS halkası (gözden kaçan büyük kalem)
- 4–6 numaralı kontaklar (GND) dört yarı eksenin hepsinde var. Q1 → Q2 → Q3 → Q4 → Q1 toprak yolu **(0,0) noktasının çevresinde kapalı bir halka** oluşturur. VSYS ve bypass kondansatörleri üzerinden ikinci bir halka daha oluşur.
- Kontaklar R ≈ 15–25 mm'de ise halka iç akının büyük kısmını çevreler. EMF ≈ 1 V, X ≈ 0.25 Ω → I ≈ 4 A → kontak ve düzlem direnciyle **≈ 0.3–0.5 W** kayıp ve kuplaj düşüşü.
- Ayrıca bobin akımının harmonikleri bu toprak üzerinden MIPI (4 Gbit/s), dokunmatik (240 Hz) ve 1-Wire/NTC hatlarına karışır.

### 4.7 Diğer iletken katmanlar
| Katman | Hesap | Kayıp |
|---|---|---|
| AgNW/ITO, 12 Ω/sq, bobin alanının tamamı | P = πω²B²a⁴/(16·Rs). a = 27 mm, B = 1 mT | ≈ 45 mW; desen ve karo bölünmesiyle **≈ 5–20 mW**. Ama dokunmatik gürültüsü ciddi. |
| Mu-metal levha (Part 3) | Rs ≈ 0.02 Ω/sq. 0.2 mT kaçak alan | ≈ 0.3–1 W mertebesi. Ayrıca L ve Q'yu düşüren görüntü akımları oluşur. |
| Batarya akım toplayıcıları ve Li metal | Deri kalınlığıyla sınırlı rejim, ≈ 12 W/m² | Ferrit sağlamken ≈ 20 mW. Asıl etkisi L ve Q kaybı. |
| **Ferrit boşluğu** | Ferrit 34 × 74 mm, karo 40 × 80 mm → her kenarda 3 mm pay → derzde **6 mm genişliğinde haç biçimli ferrit boşluğu**, tam bobinin ortasından geçiyor | Akı bu boşluktan bataryaya ve derzdeki metallere kaçar. 4.2–4.6'daki tüm kayıpları artırır. |

### 4.8 Toplam bütçe ve sıcaklık (ortam 25 °C, cihazın genel ısınması §5'te ayrıca)

| Senaryo | Derzdeki kayıp (eddy + omik) | q' (108 mm) | Derzin yerel ΔT'si (Cu destekli … saf PC) | Derz sıcaklığı (genel +16…33 K dahil) |
|---|---|---|---|---|
| **A** – Kontaklar yüksek alan dışında, halka yok, yaprak düz | 0.15–0.3 W | 1.4–2.8 W/m | +1 … +14 K | **≈ 42–72 °C** |
| **B** – Dosyadaki D-sektör yapısı (14 mT), 24 mıknatıs, omik halka | 2–4 W | 19–37 W/m | +12 … +60 K (PC sınırı daha da yüksek); tek mıknatısta **+100 K üstü** | **≈ 60–105 °C**, yerel olarak 120 °C üstü |
| **C** – Kapalı halka (Qi2 yayları, GND ya da Nitinol) | B + 1–2.5 W, ve kuplaj çöker | — | — | Güç aktarımı kurulamaz. **FOD anında devreye girer** ya da halka elemanı aşırı ısınır |

### 4.9 FOD açısından anlamı
- Qi'nin güç kaybı FOD'u (P_tx − P_rx bildirimi) tipik olarak **birkaç yüz mW** mertebesinde eşiklerle çalışır. Senaryo B ve C bunu açıkça aşar: şarj durur ya da güç düşürülür.
- Kayıpları alıcının kalibrasyonuna "dost metal" olarak gömmek de çözüm değil:
  - Kalibrasyon **sabit bir geometri için** geçerli. Karolar her söküp takışta ±0.05 mm ve kontak direnci farkıyla yeniden dizilir, Q ve kayıp değişir. Sonuç ya sahte FOD ya da kaçan FOD.
  - Gerçek bir yabancı cisim (madeni para, anahtar, folyo) bu kalibrasyon hatasının içinde **gizlenir**. Bu bir güvenlik açığı.
  - Kalibrasyon ısıyı ortadan kaldırmaz. Derz yine ısınır.
- Q faktörü yöntemiyle yapılan FOD için de durum aynı: derz kendisi bir "madeni para" sınıfı yabancı cisim gibi davranıyor.

---

## 5. Soru 2: 5 W ısı 36.2 °C sınırını aşar mı? **Evet, büyük farkla.**

### 5.1 Öncülün düzeltilmesi
- 25 W **çıkış** ve %80 verimle giriş 31.25 W, kayıp **6.25 W**. Bunun yaklaşık %40–50'si vericide kalır.
- Ama alıcı tarafı aşağıdan yukarı toplandığında: bobin 1.9–4.9 W, doğrultucu 1.5–2 W, buck ≈ 1 W, batarya I²R 1–3 W, derz 0.15–4 W. **Cihazdaki gerçekçi toplam ≈ 5–13 W.** Yani sorudaki 5 W **iyimser**. Ayrıca bu toplamlar uçtan uca verimin yaklaşık %65–70 olduğunu gösteriyor, %86 değil.

### 5.2 Genel enerji dengesi (80 × 160 mm, tek yüz alanı 0.0128 m²)
- Isı taşınım katsayısı: yukarı bakan yüzde doğal taşınım ≈ 6.7 W/m²K (Ra ≈ 2.6e4) + ışınım 4εσT³ ≈ 5.8 W/m²K → **h ≈ 12.5 W/m²K**.

| Durum | ΔT = P/(h·A) | Yüzey sıcaklığı |
|---|---|---|
| İki yüz serbest, ısı mükemmel yayılıyor (pedin üstünde imkânsız) | 5 / (12.5 × 0.0256) = 15.6 K | **≈ 40.6 °C > 36.2** |
| Ped üzerinde, yalnızca ön yüzden atım (arka yüzü verici bobin de ısıtıyor) | 5 / (12.5 × 0.0128) = 31 K | **≈ 56 °C** |

### 5.3 Isı yayılamıyor: yerel ısınma
- Saf PC'de ısı yayılma uzunluğu: 1/m = √(k·t / 2h) = √(4e-4 / 24) ≈ **4 mm**. Isı neredeyse oluştuğu yerde kalır.
- **`+` derzi, ısı kaynağının tam ortasından geçen bir ısıl kesintidir.** Çapraz geçişte yalnızca nokta temaslı yapraklar var. Her sektörün ısısı kendi karosunun köşesine hapsolur.
- **Kalınlık boyunca:** 5 W'ın 1 mm PC'den, bobin izdüşümü kadar alandan (1.486e-3 m²) geçmesi R = t/(kA) ≈ 3.4 K/W, yani **+17 K** demek. Bu, yalnızca katman geçişinin farkı.
- Sonuç: genel ısınma, kalınlık farkı ve köşe hapsi birlikte bobin üstündeki ön yüzü yaklaşık **60–80 °C** aralığına taşır.

### 5.4 Ne kadar sürede?
- Tüm gövde: C ≈ 68 g × 1.1 J/gK ≈ 75 J/K → 5 W'ta 0.067 K/s. +11.2 K'ya adyabatik olarak yaklaşık **170 s**.
- Bobin bölgesi: C ≈ 6.5 J/K → 0.77 K/s. **15 s civarında** sınır aşılır. NTC kısıtlama döngüsü neredeyse anında başlar.

### 5.5 36.2 °C altında kalarak ne kadar şarj edilebilir?
- 25 °C ortamda izin verilen ΔT = 11.2 K.
  - Tek yüz, mükemmel yayılma: P_ısı ≤ 1.8 W
  - İki yüz: P_ısı ≤ 3.6 W
  - Gerçekçi sıcak bölge çarpanı (2–3) ile: **≈ 0.6–1.8 W**
- Bu topolojide alıcı tarafı kayıp oranı yaklaşık %20–30 → **sürekli şarj gücü ≈ 3–6 W**. 12 Wh için ≥ 2.5–4 saat.
- 30 °C ortamda sınır bunun yaklaşık yarısıdır. "25 W Qi2.2" pratikte bir pazarlama değeridir.

### 5.6 36.2 °C sınırıyla ilgili ek sorunlar
1. **PEO ile çelişki.** 25 W / 12 Wh ≈ **2.1 C**. Tek karo için 10 W / 3 Wh = **3.3 C**. PEO bazlı kompozit elektrolitlerin oda sıcaklığındaki iyonik iletkenliği düşüktür (yaklaşık 10⁻⁶–10⁻⁵ S/cm mertebesi). Bu tür hücreler tipik olarak 50–80 °C'de çalıştırılır. Ya hücre 36.2 °C'de bu akımı kabul etmez ve iç direnç ısısı patlar, ya da sınır ihlal edilir.
2. **Göz çevresi kipi.** Cilt sıcaklığı zaten yaklaşık 33–35 °C. Şarj olmasa bile vücut ısısıyla kalan pay yaklaşık 1–3 K. Sınırın şarj sırasında da geçerli olup olmadığı belirsiz. Geçerliyse şarj fiilen kullanılamaz. Değilse "ocular" sınır şarj sırasında anlamını yitirir. Karşılaştırma için: IEC 62368-1'in uzun süreli plastik temas yüzeyi sınırları kabaca 40'lı °C'ler mertebesindedir. 36.2 °C bunlardan çok daha sıkı.
3. **NTC yerleşimi ve gürültü.** Karo başına bir NTC var (QB bloğu). Konumu belirtilmemiş. En sıcak nokta olan derzde **sensör yok**. Derzdeki ısıl kesinti yüzünden komşu karonun NTC'si o sıcak noktayı göremez. Ayrıca NTC, ±0.1 °C hassasiyet için yaklaşık 4 mV çözünürlük ister. 14 mT ortamda 1 mm²'lik bir döngüye indüklenen gerilim ωBA ≈ **32 mV tepe**. Bu, ölçülecek sinyalin yaklaşık 8 katı. 15–16 numaralı kontaklar AC halkasının (7–8) yanında durduğu için filtrelenmeden "0.1 °C" iddiası geçersiz.

---

## 6. Diğer elektriksel/manyetik hatalar ve dosyalar arası çelişkiler

1. **Seam kaybı "<8 mW (18 mΩ)" (02, SB satırı):** 3 A için kayıp 3² × 18 mΩ = **162 mW**. Paralel 3 kontaklı en iyimser hesap: 3² × 6 mΩ × 2 (gidiş + dönüş) ≈ **108 mW** her yarı eksen için. 8 mW ancak yaklaşık 0.67 A'da tutar. Değer 1–2 basamak yanlış.
2. **"Bifilar ... <0.08 µT" (02):** 1–3 VSYS, 4–6 GND sırayla dizili, iç içe değil, yani bifilar değil. 3 A ve 1.5 mm ayrımla 10 mm mesafede yaklaşık 9 µT. Üstelik bu DC bir alan ve yaklaşık 50 µT'lik dünya alanının yanında anlamsız.
3. **Part 3, "ELF'i göze karşı keser, <0.08 µT":** 360 kHz ELF değildir. Kalkansız bobin eksen üzerinde 30 mm'de yaklaşık 0.2 mT üretir. 0.08 µT için yaklaşık 2500 kat sönümleme gerekir. 6 mm boşluklu, 0.09 mm'lik bir yığınla bu imkânsız. Gerçek referans değer ICNIRP 2010'da 3 kHz–10 MHz için genel halk sınırı olan **27 µT**.
4. **Part 3, "nanokristalin FeSiB":** FeSiB amorf bir alaşımdır. Nanokristalin olan FeCuNbSiB'dir (Finemet tipi). 360 kHz'de amorf malzemenin çekirdek kaybı daha yüksektir. 0.09 mm kalınlıkta akı hesabı: Φ ≈ 2.3 µWb, R = 16 mm'de B_ferrit ≈ 0.25 T. Mıknatısların DC kutuplamasıyla birlikte yerel doyma riski var.
5. **Mu-metal µr > 25 000:** DC değeri. 360 kHz'de etkin değer çok daha düşük, deri kalınlığı birkaç µm ile birkaç on µm arası. Malzeme yaklaşık 0.7–0.8 T'da doyar ve N52H yakınında doygundur. Kalkan değil kayıp kaynağıdır.
6. **Ters yüz şarjı:** Cihaz iki yüzden kullanılabilir şekilde tasarlanmış (+Z/−Z yerleştirme, PDLC). Pede ters yüzle konursa ferrit ve mu-metal verici ile bobin arasına girer. Şarj olmaz ve iletken levha yabancı cisim gibi **ısınır**. Bunu önleyen bir kural tanımlanmamış.
7. **AC halkası kontak sayısı:** 02'de 8 kontak (7–8 × 4). 14'te "x 8 pairs", yani 16. Çelişki.
8. **Frekanslar:** 02 "110–360 kHz", Part 7 "127.7 / 360 kHz", Part 2 "120–200 kHz". Tek bir bobinin hem BPP/EPP hem MPP'ye ayarlanması için anahtarlamalı rezonans ağı ve iletişim modülasyon devresi (ASK kondansatörleri/FET'ler) gerekir. BOM'da yok.
9. **AgNW "12 Ω/sq güç ağı" (02, DB satırı):** 40 × 80 mm'lik bir yol yaklaşık 2 kare, yani 24 Ω eder. Yalnızca 1 A bile 24 W kayıp demek. Bu ağ güç taşıyamaz.
10. **Gerinim (04, §2.1):** ε = t/(2R) = 2.00 / 51 ≈ **%3.9**, "0.38 %" değil. ITO yaklaşık %1'de, seramik LLZO yaklaşık %0.1'de kırılır. Bükülme bobin–ferrit aralığını ve dolayısıyla L değerini de değiştirir.
11. **Kalınlık:** 04'te "2.20. Mm thin", diğer her yerde 2.00 mm.
12. **Batarya hacmi:** 3 Wh hücre, yaklaşık 34 × 74 × ≤1.0–1.2 mm hacme sığmak zorunda (bobin, ferrit ve ekran da aynı 2 mm'de). Bu yaklaşık **1000–1200 Wh/L** demek, bugünkü üretim teknolojisinin üzerinde. Ayrıca bobin batarya köşesinin hemen üstünde.
13. **Desk Dock "27 W" (04):** Qi2.2'nin üst sınırı 25 W. Fark pedlerden kablolu güçse bu belirtilmemiş.
14. **40 W USB-C → VSYS:** 40 W / 4.4 V ≈ **9.1 A**, Ø1.0 pogo pinlerden geçecek. VSYS sınırı 3 A. Kablosuz ve kablolu güç aynı anda gelirse paylaşım kuralı yok.
15. **Yerel Ø22 bobinde 10 W:** Standart bir Qi vericisine (yaklaşık Ø43–50) Ø22 alıcıyla kuplaj düşük, verim yaklaşık %60–70. 17 g'lık tek bir karoda 3–4 W ısı oluşur. Bir de 3.3 C şarj oranı.
16. **Dokunmatik ve PDLC:** AgNW dokunmatik elektrotları bobinin hemen üstünde. 360 kHz taşıyıcı ve verici modülasyonu, bilinen "şarj sırasında hayalet dokunma" sorununun en ağır biçimini yaratır. "Düşük gerilim PDLC" ifadesi de tutarsız, çünkü PDLC tipik olarak onlarca V AC ister.
17. **MIPI 4 Gbit/s:** 9–12 numaralı kontaklar, yaklaşık 70 V tepe AC taşıyan 7–8'in hemen yanında. Ek olarak toprak halkası ve yay kontağı süreksizliği var. Kılavuz (guard) ya da ayırma kontağı tanımlanmamış.
18. **"Her Qi2/MagSafe şarj cihazında kendiliğinden merkezlenir" (Part 4):** 4'e bölünmüş, 0.52 g'lık halka ve bunun yanında B-modülün 8 N52H mıknatısı ile kenar tutucu mıknatısları var. Vericinin manyetik hizalama sensörlerini ve kutup desenini bozma riski doğrulanmamış.

---

## 7. Düzeltme önerileri

1. **Merkezi bobini tek bir karoya taşıyın** (sürekli spiral, kesintisiz). Ya da Qi2.2'yi B-modül tarafına alın. Derzden AC güç geçirmekten tamamen vazgeçin.
2. Bu yapılamıyorsa **D-sektör kullanmayın**. Derzden yalnızca doğrultulmuş DC geçirin: her sektöre kendi doğrultucusunu verin ve düşük kuplajı kabul edin. Ya da 25 W iddiasını yaklaşık 7.5–10 W'a indirin.
3. Derzde **R < 30 mm bölgesinde metal bırakmayın**: mıknatıs yok, kontak yok, Nitinol yok.
4. GND ve VSYS bağlantısını **bir yarı eksende açık bırakın** ("kırık halka", ağaç topoloji). Böylece bobini çevreleyen toprak halkası oluşmaz.
5. Qi2 halka yaylarını parylene ya da benzeri bir kaplamayla **birbirinden yalıtın**. Mıknatısları ayrı bloklar hâlinde tasarlayın.
6. Ferriti derz boyunca **kesintisiz** yapın (karolar arasında üst üste binen ferrit dili). Mu-metali bobin bölgesinden çıkarın.
7. Litz teli 40–80 µm damarlı seçin. Rezonans kondansatörlerini **0402/0603 C0G, ≥100 V** olarak, sektörlere dağıtılmış seri bağlantıyla tasarlayın.
8. Isı tarafında grafit ya da buhar odası ekleyin, PC yerine cam ya da alüminyum çerçeve değerlendirin, NTC'leri bobin ve derz yakınına koyun. **36.2 °C sınırının şarjda geçerli olmadığını açıkça tanımlayın**, ya da şarj gücü spesifikasyonunu yaklaşık 5 W'a çekin.
9. PEO kullanılıyorsa 2 C hedefinden vazgeçin. 25 W ancak oda sıcaklığında iyi iletken bir seramik ya da sülfür elektrolit hücreyle tartışılabilir.
10. Dosyalardaki sayıları düzeltin: <8 mW, 0.38 %, 0.08 µT, 86 %, 27 W, kontak sayısı 8/16, malzeme adları.

---

## 8. Varsayımlar ve belirsizlik
- Sarım sayısı, kontak konumları, derz mıknatıslarının boyutu ve sayısı, Nitinol geometrisi ve katman sıralaması dosyalarda tanımlı değil. Bu yüzden sonuçları senaryo aralığı olarak verdim.
- Mertebeler (W cinsinden kayıplar, K cinsinden ısınma) iyi temellidir. Kesin değerler için tam katman yığınıyla 3B manyetik ve ısıl FEM simülasyonu ile Qi2 referans vericisi üzerinde ölçüm gerekir.
- Hiçbir makul varsayım altında **25 W Qi2.2, %86 verim ve 36.2 °C sınırı aynı anda sağlanamıyor**. Bu, fiziksel bir uyumsuzluk.


---

## DALGA 4 · TERS ÇEVRİLİP BOŞLUKTAN 90° BÜKÜLEN `b` MODÜLÜ, 1.00 MM ÇUBUKTA TYPE-C VE KAMERA OPTİĞİ HATALARI (`HARDWARE/03, 05, 07, 09, 13, 18, 20`)

### W4_A3_SONNET_DOCK_AND_MODELS_AUDIT · Model: `claude-sonnet-5-5` (Router: `coding-router-preview`, Başlangıç: `2026-10-12 14:56:49 +03`, Bitiş: `2026-10-12 15:04:04 +03`, Süre: `434.9 sn`, Uzunluk: `25,935` karakter)

# BUDLUM LEAF Rev L.5.0 – Donanım Arayüzü, 3B Model ve Dock Denetim Raporu

**Kapsam ve sınırlar.** Bu rapor yalnızca verdiğiniz üç Markdown dosyasına ve sizin bildirdiğiniz üç gerçek STL üçgen sayısına dayanır. Hiçbir araç çalıştırmadım. STL, CAD ve script dosyalarını açmadım. Bu yüzden gerçek bounding-box ölçülerini doğrulayamadım ve yalnızca belgeler arası tutarlılığı ve fiziği denetledim.

Fiziksel hesaplarda varsayımlar şunlardır:
- Doğal taşınım ve radyasyon için h ≈ 10 W/m²K.
- Qi frekansı 140–205 kHz.
- Alüminyum yoğunluğu 2,70 g/cm³.

Varsayımların hangi sonuçta kullanıldığını ilgili yerde belirttim.

Önem etiketleri: **[K]** kritik, **[Y]** yüksek, **[O]** orta, **[D]** düşük.

---

## BÖLÜM A – STL üçgen sayıları ve 07 tablosu (Soru 1)

### A.1 Doğrudan sapmalar

| Dosya | 07 tablosu | Gerçek STL | Fark | Oran |
|---|---|---|---|---|
| `leaf160-device.stl` | 155 968 | 172 232 | **+16 264** | +%10,43 |
| `leaf160-frame.stl` | 73 792 | 72 184 | **−1 608** | −%2,18 |
| `leaf160-battery-bent.stl` | 21 568 | 108 376 | **+86 808** | **+%402,5 (5,02×)** |

Evet, üçünde de fark var. **[K]** `battery-bent` değeri en büyük sapmadır ve fiziksel olarak da çelişkilidir. Diğer ikisi de tablonun güncel olmadığını gösterir.

### A.2 Eski mimariden kalma izi: tablodaki `device` sayısı

Tablodaki 155 968 değeri tesadüf değildir:

```
73 792 (frame) + 21 088 (screen) + 57 056 (battery) + 4 032 (rail-module) = 155 968
```

Bu toplam birebir tutuyor. Yani 07'deki `device` sayısı, B modülü eklenmeden önceki alt-ray (`rail-module.stl`) mimarisinden hesaplanmış ve güncellenmemiş. Bu durum "eski alt-ray referansı kaldı mı" sorusunun ilk kanıtıdır. Ayrıca `frame` sayısı da eski, çünkü gerçek değer 72 184.

Gerçek dosyayla karşılaştırma:
- Gerçek `device` − (gerçek frame + screen + battery) = 172 232 − 150 328 = **21 904 üçgen**.
- Bu artık, `monogram-ring.stl` (22 176) büyüklüğüne yakın. Fark 272 üçgendir.
- Tam `monogram-letter/module` ise 49 856 üçgendir.
- Hipotez (kanıt değil): `device` STL'sine tam 90° bükümlü sap + `Ø32/Ø24` halka modülü değil, ring seviyesinde basitleştirilmiş bir modül girmiş olabilir. Bu durumda 07'deki "device = frame + screen + battery + B modülü (32 parça)" tanımı gerçek dosyada tutmaz.
- Tablodaki değerlerle toplam (frame + screen + battery + module) 201 792'dir ve 155 968'den %29 fazladır. Gerçek değerlerle toplam 200 184'tür ve 172 232'den %16 fazladır.
- Yani `device` ne eski toplamı ne yeni toplamı yansıtıyor. Birleştirme/decimation kullanılıyorsa belgelenmeli.

### A.3 `battery-bent` sayısı fiziksel olarak da imkânsız

- Düz batarya 57 056 üçgendir. Büküm, "Y-strip bending triangulation" ile (`render3d.py`) üçgen sayısını artırır, azaltmaz.
- Tablodaki bükülü sayı olan 21 568, düz olanın yalnızca %37,8'idir. Bu değer `screen.stl` (21 088) değerinden sadece 480 fazladır ve büyük olasılıkla yanlış satırdan kopyalanmıştır.
- Gerçek 108 376, düz bataryanın 1,90 katıdır. Strip tessellation için makul bir artıştır.

### A.4 `battery-bent` boyutları iç tutarsızlık gösteriyor

Tablodaki ölçüler `80.0 × 137.4 × 59.7` mm'dir ve R = 25,5 mm ile 160 mm uzunluk veriliyor. Hesap şöyledir:

- 160 / 25,5 = **6,27 rad ≈ 359,5°**. Yani 160 mm'lik levha neredeyse tam bir silindire sarılıyor (Ø51 mm).
- Tek sabit R = 25,5 mm'lik bir bükümde z-kapsamı ≈ 2R + t = 51 + 2,0 = **53,0 mm** olmalı. Tablo 59,7 mm veriyor.
- Aradaki fark 6,70 mm'dir ve B modülü kalınlığıyla birebir aynıdır. Bu bir çıkarımdır: bükülü dosyaya modül karışmış veya bükme formülü farklı olabilir.
- Açıklama sütunu "laminat" diyor, B modülünden söz etmiyor. Üretici script ile tablo açıklaması arasında bir uyumsuzluk var.

### A.5 Diğer 07 içi çelişkiler (üçgen/boyut tabloları)

1. **[Y] Kalınlık çelişkisi.**
   - Üst başlık ve §1: gövde 2,00 mm.
   - `leaf160-frame.stl`: 2,20 mm.
   - Tablodaki Leaf 80/160/480 gövdeleri: 2,20 / 2,20 / 2,40 mm.
   - §1'deki `leaf_geom.py` satırı: `leaf80-body` ve `leaf160-body` 2,00 mm.
   - Dock (18) yuvası 2,00 mm gövde varsayıyor. 2,20 mm'lik gerçek gövde için tolerans veya boşluk hiçbir yerde yok.

2. **[K] Z-yığını fiziksel olarak sığmıyor.**
   - `screen` 1,96 mm + `battery` 1,60 mm = **3,56 mm**. Bu, 2,00 mm'lik gövdeyi %78, 2,20 mm'lik çerçeveyi %62 aşıyor.
   - Aynı alanda Qi bobinleri, 24 adet N52H mıknatıs, Mu-metal kalkan, arka T-OLED (render-back) ve PCB'ler de var.
   - "2,00 mm 11 katmanlı yığın" iddiası mümkün değil. Ekran tek başına 1,96 mm tutarak boşluğun neredeyse tamamını dolduruyor.

3. **[K] Eğilme gerinimi 10× hatalı görünüyor.**
   - Simetrik bir plakada ε = (t/2)/R = 1,0/25,5 = **%3,92**. Dosyalardaki iddia **%0,38**.
   - %0,38 değeri t ≈ 0,2 mm için doğru olurdu (0,2/(2·25,5) = %0,39). Muhtemelen 2,00 yerine 0,20 mm kullanılmış.
   - 1,60 mm'lik LLZO hücresi için ε = 0,8/25,5 = **%3,1**. İddia edilen %0,22 değerinin 14 katı.
   - LLZO seramik kırılma gerinimi yaklaşık %0,05–0,1'dir (E ≈ 150 GPa, σ_f ≈ 100 MPa). İddia edilen %0,22 değeri bile kırılma sınırının üstünde.
   - ITO/AgNW kırılması ≈ %0,5–1 ve OLED ince film kapsülleme sınırları da bu aralıkta. %3,9 gerinimde bunlar çatlar.
   - PC (polikarbonat) %3,9 gerinimde akmaz ama 10 000 çevrimde craze ve sünme riski taşır.
   - Bu nedenle 09'daki `B-1..10, F-06` kapısı ("10 000 tam sarım, 0,38% dış PC gerinimi") yanlış temele dayanıyor.

4. **[O] `Leaf 80/160/480 bodies` için "2 916 each".** Tek çeyrek, 4 çeyrek ve çok karolu masa tabakası farklı topolojiye sahip. Aynı üçgen sayısı ya parametrik bir şablonun kaba kopyası ya da tablo hatası. Üç dosyanın üçgen sayısı aynı olamaz.

5. **[O] Kopya satırlar.** `monogram-module.stl` ve `monogram-letter.stl` aynı ölçü (40,0 × 44,0 × 6,70) ve aynı 49 856 üçgeni gösteriyor. İkisi aynı dosyaysa tablo şişirilmiş; farklıysa sayı kopyalanmış. §1'deki `monogram_detail.py` yalnızca `monogram-ring` ve `monogram-letter` üretiyor, `monogram-module`'ün üreticisi listelenmemiş.

6. **[O] "13 STL" sayısı tutuyor ama listedeki iki satır tek kalem.** Gerçekte 13 dosya var (device, module, frame, screen, battery, battery-bent, ring, letter, 3 body, rail-module, rail-receiver). `rail-module` ve `rail-receiver` satırı tek ölçü gösteriyor (76,8 × 35,6 × 3,00). Bu satır eski alt-raydır (bkz. B.7).

7. **[Y] Parça sayısı çelişkisi.** `leaf160-frame` satırı 4 kabuk + 1 hub + 8 Ti pin + 24 mıknatıs + 64 altın yaprak = **101 parça** sayıyor. Aynı dosyalar "84 internal subparts" diyor. Altın yapraklar tek tek parça sayılıyorsa 84 tutmaz.

8. **[Y] Device ölçüleri.**
   - `device` 80,0 × **172,0** × 6,70 mm. 160 + 12 = 172 ise sap/halka gövdenin üst kenarından 12 mm taşıyor. Bu, "sap üst kenarda 90° bükülü" tanımıyla çelişir: 90° bükülü bir sap +Y yerine +Z'de uzamalıdır.
   - Kalınlık 6,70 mm. Modülün tek başına kalınlığı da 6,70 mm. Gövde 2,00 mm ise bileşik z-kalınlığı **8,70 mm** olmalı. 6,70 mm, modülün gövde hacmine gömülü olduğu (çarpışma) veya ölçünün yanlış olduğu anlamına gelir.
   - 172 mm'lik cihaz, dock'taki "160 mm geniş" yuvaya sığmaz (bkz. B.4).

9. **[D] Dokümantasyon hijyeni.** "`4 x Ø22 mm` `Qi` coils, `U_QI`" ifadesi anlamsız bir kırıntıdır. Cümle başlarında "Also," ve "…, ." kalıntıları otomatik üretimden kalmıştır.

### A.6 Önerilen düzeltme

STL başına üçgen sayısı elle yazılmamalı, otomatik üretilmeli:
- Binary STL için `(dosya_boyutu − 84) / 50`.
- ASCII STL için `grep -c "facet normal"`.
- Bounding box için `numpy-stl` veya `trimesh`.

Sonuçlar `07` içine CI ile gömülmeli, tolerans %0 olmalı (üçgen sayısı deterministik olmalı).

---

## BÖLÜM B – Dock (18) ve portsuz 2,00 mm gövde (Soru 2)

### B.1 Portsuz gövde dock'ta nasıl şarj olur ve veri alır?

**Şarj:**
- Dosyalara göre tek mantıklı yol Qi2.2 kablosuz şarjdır: Ø54 mm MPP bobin (25 W) ve 4 × Ø22 mm bobin (karo başına 10 W).
- 18'in giriş paragrafı altın pedlerin de "portsuz gövdeyi kapsadığını" söylüyor. Ancak 07'de gövde üzerinde karşılık pedi yok. Gövde "zero USB-C" ve dış arayüzü yalnızca çeyrekler arası 64 altın yaprak + 8 Ti pindir. Bunlar iç kenar bağlantılarıdır, dock'a bakan kenar değil.
- Pedlerle şarj, ancak B modülü (12 pin) veya B sapı (USB-C) üzerinden mümkündür.

**Veri:**
- Qi in-band veri hızı yalnızca kbit/s düzeyindedir. 2,5 Gbit/s taşıyamaz.
- 60 GHz/UWB (`U2` SiP) B modülünün halka PCB'sindedir (09, §1). B modülü olmayan portsuz gövdenin veri yolu tanımsızdır.
- Dock'taki "2 veri pedi" 07'de hiçbir karşılığa sahip değil.

**Sonuç: [K]** Portsuz gövde tek başına dock'ta yalnızca Qi ile şarj olur. Veri aktarımı belgelenmemiştir. 18 giriş paragrafı gövde için 27 W ped ve 2,5 GbE vaat ediyor ama bunu sağlayan bir tasarım öğesi yok.

### B.2 Eski alt-ray altın kontak referansları kalmış mı?

**Evet, doğrudan ve dolaylı olarak kalmış. 18'de "rail" veya "alt-ray" kelimesi yok, ama mantık kalmış.**

1. **07 §1 ve §2 (doğrudan):**
   - `cad/rail_detail.py` ve `rail-detail.svg` hâlâ listede.
   - `rail-module.stl` (4 032 üçgen) ve `rail-receiver.stl` (656 üçgen) 76,8 × 35,6 × **3,00 mm** ölçüsünde.
   - 76,8 mm genişlik eski 80 mm'lik alt-raydan kalmadır. 3,00 mm kalınlık 2,00 mm'lik gövdeye sığmaz.
   - Satır başlığı "Qi2.2 / + seam & B stem dock" diye yeniden etiketlenmiş ama geometri değişmemiş.
   - Header'daki "bulky bottom-battery files are retired" ifadesi bu iki dosya için geçerli değil.

2. **18'de dolaylı kalıntılar:**
   - "four gold power pads (10 mm pitch) + two data pads" ve "27 W + 2,5 Gbit/s": eski alt-ray pedlerinin aynısı. Ped sayısı, aralığı ve yapısı kenar-kontak mantığına göre kurulmuş.
   - "anti-rotation guide pins … prevents torsional twist under cable pull" (parça 24): portsuz gövdede kablo yok. Kablo çekmesi USB-C'li alt-ray döneminden kalmış.
   - "lead-in chamfer … guides the body into the cradle with one hand" ve "seat land 160 mm wide × 12 mm deep" (parça 3, 8): kenardan oturan eski raya ait mantık.
   - "It uses the 90° B stem or dock seat": hangi arayüzün hangisi olduğu belirsiz.

3. **09 ile ilişkisi:** 18'deki hiçbir DK-1..DK-10 kapısı 09'da yok (bkz. B.9).

### B.3 Fiziksel ve geometrik çelişkiler

**B.3.1 [K] Pedler 2,00 mm kenara sığmıyor.**
- Güç pedleri Ø6,0 mm, veri pedleri 2,4 mm genişlikte.
- Gövde kenarı 2,00 mm. Chamfer varsa teması daha da küçük.
- Ø6,0 mm ped, 2,00 mm'lik kenara temas etse bile en fazla %33 örtüşür. Bu yüzden `0,5 mΩ` gibi bir iddia temas alanıyla çelişir.

**B.3.2 [Y] Temas direnci.**
- Hertz/Holm: 0,35 N, sert altın (H ≈ 1,5–2 GPa) için a = √(F/πH) ≈ 7,5 µm. Tek asperite ρ/(2a) ≈ 1,5 mΩ ve gerçek yüzeylerde film dirençleriyle genellikle 10–50 mΩ olur.
- 0,5 mΩ/ped değeri fiziksel olarak savunulamaz. Etkisi küçüktür çünkü 27 W için 9 V × 3 A varsayımıyla kayıp ≈ 0,2 W. Ama voltaj belirtilmemiş; bu bir eksiklik.
- 0,35 N temas kuvveti 6 yaylı sistemde toplam 2,1 N yapar. Titreşim ve oksit için düşüktür (tipik pogo 0,5–1,5 N).

**B.3.3 [K] Anti-rotasyon pimleri gövdeye sığmaz.** `2 × Ø3,0 mm` pim, 2,00 mm gövdeye kenardan girecekse delik 3,0 mm > 2,00 mm kalınlık olur. Yüzeyden girecekse ekran/batarya yığınını deler. Her iki durumda da geometrik olarak çelişkili.

**B.3.4 [K] "Seat land" ile Qi2.2 yönelimi çelişiyor.**
- Parça 3: 12 mm derin yuva, gövde kenardan 12 mm giriyor, yani gövde dik duruyor.
- Parça 1 ve 7: Qi bobini `80 × 160 × 1,8 mm`, yatay güvertede. Gövde yatay olsa bobinle eksenel hizalanır; dikse akı gövdeye dik düşer ve kuplaj çöker.
- Güvertenin toplam kalınlığı 12 mm olduğundan 12 mm'lik cep tüm güverteyi delmek anlamına gelir.
- Gövde yatay yatıyorsa cebin 12 mm derin olması gerekmez (2,00–2,20 mm yeter).
- Bu iki mod aynı anda olamaz. Hangisi gerçek, belirtilmeli.

**B.3.5 [Y] Gövde uzunluğu ile yuva genişliği.**
- Yuva 160 mm geniş; gövde 160,0 mm; B modülüyle cihaz 172 mm.
- Termal genleşme: PC ≈ 65–70 ppm/K, Al 6061 ≈ 23,6 ppm/K. ΔT = 20 K için 160 mm'de PC +213 µm, Al +75 µm. Fark ≈ 138 µm.
- Yuva toleransı belirtilmemiş. Sıfır boşlukla sıkışma veya fazla boşlukla oynama olur.
- Kalınlıkta da 2,00 mm yuvaya 2,20 mm kabuk (frame) = %10 interferans.

**B.3.6 [Y] B modülü ile düz dock.** B modülü (6,70 mm) ekranda dururken 2,00 mm gövdenin 4,70 mm üstüne çıkar. Cihaz güverteye düz yatamaz. Modülün çıkarılması veya yuvaya oyuk açılması gerekir; hiçbiri belgelenmemiş.

**B.3.7 [K] Güverte kesiti ve z-yığını.**
- Üst plaka 3,0 mm + duvar 2,0 mm = 5,0 mm. Geriye 7,0 mm iç yükseklik kalır.
- `validator bay` 8,0 mm. 7,0 mm'ye sığmaz.
- Qi katmanının altında olursa 3,0 + 1,8 + 8,0 = 12,8 mm > 12 mm.
- Yanında olursa: Qi katmanı 160 mm'yi kaplar, 240 − 160 = 80 mm kalır. Gerekli alan: bay (100×60 = 6 000 mm²) + fan (3 600) + fin yığını (3 600) = **13 200 mm²**. Mevcut kalan alan 80 × 120 = **9 600 mm²**.
- Parça 10 PCB'si de (180×70) bu alanlara taşıyor.
- Isı borusu için kesit, fan için hava giriş-çıkışı ve USB-C girişi de yer istiyor.

**B.3.8 [K] Rake (eğim) mümkün değil.** "8° eğim" için ayaklar farklı yükseklikte olmalı: 120 mm derinlikte Δh = 120·sin8° = **16,7 mm**, 240 mm boyunca 33,4 mm. Parça 25: dört ayak aynı, `Ø14,0 × 2,0 mm`. Sonuç 0°.

**B.3.9 [K] Kütle.**
- 3,0 mm Al üst plaka: 240×120×3,0 = 86,4 cm³ × 2,70 = **233 g**.
- 2,0 mm alt plaka: 57,6 cm³ → **155 g**.
- 2,0 mm yan duvarlar (7 mm yükseklik): ≈ 27 g.
- Yalnızca alüminyum ≈ 416 g > 310 g.
- Qi penceresi (160×80×3,0 = 38,4 cm³) tamamen kütlesiz sayılsa bile Al = 312 g, yani zaten 310 g'ı aşıyor.
- Seramik pencere (alümina ≈ 3,9 g/cm³) için +150 g eklenir.
- Fan, ısı borusu, fin yığını, PCB ve bobin eklenince gerçek kütle tahminen **450–600 g**. İddia edilen 310/360 g'ın üstünde.
- Doğrulayıcının 50 g farkı da şüpheli (96×56×4,5 mm kart ≈ 24 cm³).

### B.4 Elektrik ve veri darboğazları

**B.4.1 [K] 2,5 GbE ped fiziği.**
- 2,5GBASE-T 4 çift (8 iletken) ve manyetik (transformatör) gerektirir. Dock'ta 2 ped (12 mm arayla) ve 7×7 mm PHY var. Manyetik listede yok.
- İki ped en iyi ihtimalle tek diferansiyel çifttir; 12 mm aralık kontrollü empedans (100 Ω) vermez.
- 2,5 Gbit/s için SerDes (ör. 2,5GBASE-KX) gerekir. "2.5GBASE-T" PHY ile ped çifti bağdaşmaz.

**B.4.2 [Y] Switch/port uyuşmazlığı.** Parça 14: 4 portlu 2,5 GbE switch. Fiziksel olarak tek USB-C girişi var, RJ45 yok. Tek bir PHY (parça 13) listelenmiş. 4 port için 4 PHY yok, "wired LAN" fiziksel olarak yok.

**B.4.3 [Y] UWB ile 2,5 Gbit/s köprü.** UWB (802.15.4z) yaklaşık 6,8–31 Mbit/s verir; 2,5 Gbit/s taşıyamaz. Sadece 60 GHz (802.11ad/ay, pratikte 1–2 Gbit/s) yaklaşabilir. UWB menzil ölçümü için kalmalı.

**B.4.4 [Y] Post 10 Gbit/s.** Post "12-pad link" 10 Gbit/s veriyor ama dock'taki switch ve PHY 2,5 GbE. Yani 10 Gbit/s hat dock içinde 2,5 GbE'ye iniyor (bu yönde 4× darboğaz). 22,0 mm'de 12 ped ≈ 1,83 mm maksimum aralık; kontrollü empedans yok.

**B.4.5 [Y] 5 W / 40 W çelişkisi.** 09: B sapındaki USB-C "40 W PD 3.1 + DP 2.1". 18: post B modülüne yalnızca **5 W**. Gövdede başka port yok. Dock'tan B sapı üzerinden gövdeye giden güç 5 W ile sınırlı (12 Wh için ≈ 2,4 saat), oysa ped 27 W ve Qi 25 W diyor. Üç farklı hız; tutarlı bir güç haritası yok.

**B.4.6 [O] Güç dengesi.** Çıkışlar: 25 + 27 + 5 = 57 W, doğrulayıcı 28 W, toplam ≈ 85 W. Qi verimi (Tx→Rx) %70–80 olduğundan Tx girişi ≈ 31–36 W. Toplam giriş yaklaşık 100 W. 140 W yeterli ama gereksiz büyük; 28 V × 5 A EPR e-marked kablo gerektirir. 8,9 × 7,6 mm'lik "USB-C" ölçüsü de standart alıcı (≈ 8,94 × 3,26 mm) ile uyuşmuyor.

**B.4.7 [Y] Tek GaN bloğu.** 18×12 mm tek blok hem 25 W Qi inverter hem 27 W buck-boost sürüyor. Qi rezonansı ve buck-boost birbirine karışır; ayrı kontrol döngüsü ve termal alan gerekir.

### B.5 Termal darboğazlar

**B.5.1 [K] Doğrulayıcı ısısı.**
- 28 W, 240×120×12 mm Al güverteye veriliyor. Toplam yüzey ≈ 0,066 m², h ≈ 10 W/m²K → hA ≈ 0,66 W/K. Dock toplam kaybı ≈ 28 + 4 (Qi Tx) + 1,4 (ped) + 3 (switch/PHY) ≈ 37 W → ortalama ΔT ≈ 56 K (≈ 80 °C).
- Fanla bile 60×60 fin yığını için tipik R_th ≈ 1,5–2 K/W; 28 W → 42–56 K → fin ≈ 67–80 °C.
- IEC 62368-1 sınırlarıyla (dokunulan metal yüzey ≈ 48 °C) uyumsuz. Aynı güverte gövdeyi (NTC 36,2 °C kesme) taşıyor.

**B.5.2 [Y] Isı borusu.** Ø6 mm düzleştirilmiş Cu boru (≈ 2,5–3 mm) için tipik Qmax, 120 mm uzunlukta ≈ 15–25 W. 28 W bunu aşar.

**B.5.3 [Y] Fan ve IP52.** 60 mm × 7 mm fan ≈ 3–5 CFM verir. 28 W için 15 K hava artışıyla gerekli debi ≈ 1,55 L/s ≈ 3,3 CFM. Fin yığını basınç kaybıyla bu zor. Kapalı IP52 güvertede fan için havalandırma açıklığı gerekir; toz koruması (0,15 mm labirent) ile hava yolu bağdaşmıyor.

**B.5.4 [K] Gövde tarafı ısınma.**
- Tam gövde (iki yüz 0,0256 m², hA ≈ 0,256 W/K): Rx kayıpları (≈ 2,5 W) + batarya iç direnci (≈ 0,5 W) ≈ 3 W → ΔT ≈ 11,7 K → ≈ 36,7 °C (25 °C ortamda). NTC kesme 36,2 °C'ye zaten dayanır.
- Tek çeyrek (iki yüz 0,0064 m², hA ≈ 0,064 W/K), 10 W → kayıp ≈ 1,4 W → ΔT ≈ 22 K → **≈ 47 °C**. Kesme için yalnızca 0,72 W kayıp yeter (ΔT = 11,2 K). 5 W için de sınırda.
- Dock'un kendi ısısı bu yükün üstüne biner.

**B.5.5 [K] Şarj hızı ve LLZO/PEO.**
- 25 W / 12 Wh = **2,08 C**; 10 W / 3 Wh = **3,33 C**; 5 W / 3 Wh = 1,67 C; 27 W ped ≈ 2,25 C.
- PEO tabanlı elektrolit genelde 55–70 °C'de çalışır; 25–36 °C'de iletkenlik 10⁻⁶–10⁻⁵ S/cm mertebesine düşer. Bu koşullarda 2–3 C şarj lityum kaplama ve dendrit riski doğurur.
- PEO erime noktası ≈ 60–65 °C; 09'daki 150 °C fırın testi PEO'yu eritir. PC kabuk (HDT ≈ 130 °C) da deforme olur.
- LiTFSI tuzu flor içerir. "0,0 ppm HF" iddiası FTIR algılama sınırının altındadır, doğrulanamaz bir hedeftir.

**B.5.6 [O] Enerji yoğunluğu.** 12 Wh / (73,4×153,4×1,6 mm = 18,0 cm³) ≈ **667 Wh/L**. LLZO/PEO için hücre düzeyinde güncel en iyi değerlerin yaklaşık 1,5–2 katı. İnce formda (1,6 mm) kollektör ve paketleme payı bunu daha da zorlar.

### B.6 Qi2.2 ve manyetik/EMI sorunları

1. **[Y] Dock bobininde ferrit yok.** Parça 7: Litz bobin + N52H halka. 6061-T6 için ρ ≈ 4,0·10⁻⁸ Ω·m, skin derinliği 140 kHz'de ≈ **0,27 mm**, 205 kHz'de ≈ 0,22 mm. Alt plaka 2,0 mm (>7 δ) doğrudan bobinin altında ve ferrit korumasız. Verim ve Q düşer, plaka ısınır.

2. **[Y] Pencere kalınlığı.** Seramik pencere + Al = 3,0 mm. Rx bobini gövde içinde ≈ 0,5–1 mm derinlikte. Toplam mesafe ≈ 3,5–4 mm. Qi2 MPP için tipik nominal mesafe daha düşüktür; verim 25 W'ta daha da zayıflar.

3. **[Y] Gövdedeki Mu-metal ve N52H.** Mu-metal (μr ≈ 2·10⁴–10⁵) 24 N52H mıknatısın alanında doyar. Bir yandan Rx bobinini ekranlıyor. Qi akısını yönlendirmek için ferrit gerekir; Mu-metal bunu yapmaz.

4. **[O] Ø54 mm bobin ve çeyrek çıkarma.** Ø54 bobin merkezi (0,0) hub'a oturuyor ve dört karoya yayılıyor. Q4 çıkarıldığında bobin çeyreği kaybeder. 09 §2 "kalan 3 karo ekranı canlı tutuyor" diyor ama 25 W Ø54 bobin çalışmaz; yalnızca Ø22 bobinler kalır. Ayrıca Ø54 bobin Ti hub ve mıknatıs merkezinde alan maksimum noktasında. Ti hub (Ø8 mm, 2 mm) için yaklaşık eddy kaybı ≈ 0,1 W (B ≈ 1,5 mT varsayımıyla); küçük ama tespit edilmeli.

5. **[O] Ø22 mm bobinle 10 W.** Güç yoğunluğu ≈ 2,6 W/cm² (Ø22 → 3,8 cm²). Tipik 15 W Qi bobinleri ≈ 1 W/cm² civarı. Hizalama toleransı dar; dock'un ±1 mm yerleşimiyle bile verim düşer.

6. **[O] Ocular SAR.** 09 §1'de `SAR = 0,054 W/kg`, 60 GHz mmWave için anlamsız. 6 GHz üstünde ICNIRP/FCC güç yoğunluğu (≈ 10 W/m²) kullanır, SAR değil. Metrik düzeltilmeli.

### B.7 Optik dikiş ve malzeme sorunları (07/09 ile ilgili)

1. **[Y] Fresnel.** İndeks-uyumlu n = 1,585 arayüzde R = ((n₁−n₂)/(n₁+n₂))² < 10⁻⁶ için Δn < ≈ 0,003 olmalı. Hava boşluğunda (15 µm) her arayüzde R ≈ %5,1, toplam ≈ %10. R < %0,0001 yalnızca sıvı/jel dolgu ile mümkün. Jel ise "tool-free <3 s swap" sırasında kirlenir ve 64 altın yaprağın metal-metal teması (yalıtkan jel) ile çelişir.

2. **[K] Dikiş boşluğu termal olarak tutmaz.** PC 40 mm'de 65–70 ppm/K × 40 mm ≈ 2,7 µm/K, 80 mm'de 5,4 µm/K. ΔT = 2,8 K, 15 µm boşluğu doldurur veya açar. Nem emilimi (%0,15–0,3 → 0,04 % boyut) 80 mm'de ≈ 32 µm. "<2,5 µm Z-step" ve "<15 µm dikiş" kararlı tutulamaz.

3. **[O] Çizilmezlik.** "Zero-scratch" PC üstü için çelişkili; PC yüzey sertliği ≈ HB/2B (kalem). Kendini onaran PU ancak ince çizikleri giderir.

4. **[Y] IP68 ve altın yapraklar.** Su altında güç verilen açıkta altın/Ti/Ni kontaklar galvanik korozyon yapar. Dock'un IP52 değeri de gövdenin IP68'iyle uyumsuz; zayıf halka dock.

### B.8 B modülü iç tutarsızlıkları (07/09)

1. **[K] AMOLED ppi.** Ø22,4 mm üzerinde 480 px: 480 / 22,4 mm → piksel adımı 46,7 µm → **≈ 544 ppi**. 09 "300 ppi" diyor. 300 ppi için panel ≈ 40,6 mm olmalı.

2. **[K] Kamera.**
   - 12,8 × 9,6 mm sensör: köşegen 16,0 mm = 1" format, 50 MP için piksel adımı ≈ 1,57 µm.
   - Z zarfı `z = 0,90–3,60 mm` = **2,7 mm**. 16 mm görüntü çemberi için f ≈ 8–10 mm ve f/1,8'de apertür ≈ 5–5,6 mm olmalı. Prizma ve OIS ile 2,7 mm'ye sığmaz.
   - Katlanmış optikte sensör dik durursa 9,6 mm z-yüksekliği gerekir (sığmaz); düz yatarsa katlama anlamsızlaşır.
   - Referans: 1" 50 MP modüller (ör. IMX989) tipik olarak 9–10 mm z yüksekliğindedir.

3. **[Y] Halka PCB.** Ø32/Ø24 halka kalınlığı (32−24)/2 = **4 mm radyal**, alan π/4(32²−24²) ≈ 352 mm². 6 katmanlı TCON + 60 GHz SiP + 12 pin + Ti menteşe + OIS aktüatörü bu alana sığmaz. Ø24 delikte hem kamera (Ø≥16) hem Ø22,4 AMOLED var; z'de üst üste yığılmış olsa bile OIS ve kalkan için yer yok.

4. **[Y] Menteşe ve gövde esnemesi.** 6,70 mm'lik rijit modül, R = 25,5 mm'lik sarılmayla çarpışır; modül sarım sırasında nereye gidiyor belirsiz.

5. **[O] `rail-module` (3,00 mm).** 2,00 mm gövde içinde 3,00 mm'lik modül mümkün değil; eski alt-ray geometrisi.

### B.9 18 ile 09 ve 07 arası çapraz çelişkiler

| # | Çelişki | Önem |
|---|---|---|
| 1 | 18'deki DK-1…DK-10 kapılarının hiçbiri 09'da yok. Dock için bench doğrulama kalemi bulunmuyor. | **[Y]** |
| 2 | 09: Qi 15–25 W; 18: 25 W. Ped/Qi kapıları (RL-2, ENR-12) ile DK-2/DK-3 arasında bağ yok. | [O] |
| 3 | 07: Leaf 480 = **2,40 mm**; 18 post "2,00 mm edge profile". 2,40 mm levha 2,00 mm profile sığmaz (%20 interferans). | **[Y]** |
| 4 | 18: "Leaf 1400 / 2800" büyük levhalar; 07'de bu modeller yok. Üstelik Leaf 480 (320×480×2,4) bile ≈ 369 cm³ × 2,66 ≈ **≈ 980 g**. VESA 75 + 2 mm Al duvar bu yükü taşıyamaz. | **[Y]** |
| 5 | 18 post: 40×14×28 mm; B modülü 40×44×6,70. Post'taki 12 ped alanı 22,0×2,8 mm (2,8 mm > 2,00 mm kenar). | [O] |
| 6 | 07: 12 altın "dock pin" yalnızca B modülü arkasında; dock'taki 4+2 ped için karşılık yok. | **[K]** |
| 7 | 09: B sapında "sole USB-C 40 W + DP 2.1"; 18 post: 5 W. Tek USB-C iddiası ile dock'un 140 W USB-C girişi de "single port" mantığını bulanıklaştırıyor. | [Y] |
| 8 | 09: USB-C PD 3.1 "40 W" SPR aralığıdır. EPR (>100 W) ile karıştırılmamalı. 140 W yalnızca dock tarafında. | [D] |
| 9 | 09: eyewear NTC kesme 36,2 °C; 18'de 28 W doğrulayıcı güverteyi 48–80 °C'ye taşır. Bütün dock tasarımı eyewear/NTC sınırıyla çatışır. | **[K]** |
| 10 | EU 2023/1542 Madde 11: "<3 s" yönetmelikte yok; pil çıkarılabilirliği şartı vardır ve istisnalar mevcuttur. Atıf "<3 s" gerekçesi olarak kullanılamaz. | [D] |

---

## BÖLÜM C – Öncelikli düzeltme listesi

1. **[K]** `07` tablosundaki üç STL sayısını (172 232 / 72 184 / 108 376) otomatik üretimle güncelleyin. `device` sayısının hangi parçalardan oluştuğunu belgeleyin (21 904 artık üçgen). `battery-bent` boyutlarını (z = 59,7) yeniden üretin.
2. **[K]** Z-yığınını yeniden tasarlayın: ekran 1,96 + batarya 1,60 = 3,56 mm, 2,00/2,20 mm'ye sığmaz. Ya kalınlık artırılmalı ya da katman bütçesi çıkarılmalı.
3. **[K]** Eğilme gerinimini t = 2,00 mm ile yeniden hesaplayın (≈ %3,9 / %3,1). Rijit LLZO + ITO + OLED için bu R = 25,5 mm ile uyumsuz. Ya bükülme yarıçapı büyütülmeli (ε ≤ %0,3 için R ≥ 2,00/2/0,003 ≈ 333 mm) ya da bükülebilir katmanlar ince tutulmalı. Bu, "bükülebilir" iddiasını doğrudan etkiler.
4. **[K]** Dock'u yeniden tanımlayın:
   - Gövdenin dock'a bakan yüzeyinde ped karşılığı var mı, yoksa yalnızca Qi + B modülü üzerinden mi veri gidiyor? Net karar verin.
   - Yatay (Qi) mi, dik (kenar yuvası) mu? Seçin, 12 mm cep ya da 2,0–2,5 mm cep çizin.
   - Z-yığınını (3,0 + 1,8 + 8,0 > 12) ve kütle (≥ 450 g) iddialarını düzeltin.
   - Ayak yüksekliklerini 8° için hesaplayın (Δh ≈ 16,7 mm) veya eğimi kaldırın.
5. **[K]** Isıl bütçeyi sıfırdan çıkarın: 28 W doğrulayıcı + Qi Tx kaybı için aktif soğutma, havalandırma ve gövde NTC sınırı bir arada çözülmeli. Doğrulayıcı ya ayrı bir modül ya da güverteden ısıl olarak ayrılmış olmalı.
6. **[K]** LLZO/PEO şarj hızını (2–3,3 C, ≤ 36,2 °C) ve 150 °C testi (PEO erimesi) yeniden değerlendirin.
7. **[Y]** Eski alt-ray kalıntılarını temizleyin: `rail_detail.py`, `rail-module.stl`, `rail-receiver.stl`, `rail-detail.svg` yeniden adlandırılmalı ya da kaldırılmalı. 3,00 mm kalınlığı 2,00 mm gövdeyle uzlaştırın. Anti-rotasyon pimleri (Ø3,0 > 2,00 mm) ve "cable pull" mantığı kaldırılmalı.
8. **[Y]** 09'a DK-1…DK-10 kapılarını ekleyin; 18'deki gate'ler için bench hedefleri yazın.
9. **[Y]** Veri yolu: 2,5 GbE için 4 çift/manyetik ya da SerDes, 12 pedli 10 Gbit/s için kontrollü empedans, UWB'yi yalnızca ranging olarak tanımlayın. Switch port sayısı ile PHY sayısını eşleştirin.
10. **[Y]** B modülü: AMOLED ppi'sini düzeltin (544 ppi veya panel çapı), kamera z-zarfını gerçekçi bir modüle çevirin (1" sensör için ≥ 9 mm veya daha küçük sensör), 4 mm'lik halka PCB'nin sığabilirliğini doğrulayın.
11. **[Y]** Dikiş: Fresnel R için indeks-uyumlu dolgu ve swap uyumunu çözün; termal genleşme (5,4 µm/K, 80 mm) için kompanzasyon tanımlayın.
12. **[O]** Metrikler: 60 GHz için SAR yerine güç yoğunluğu; Leaf 480 (2,40 mm) ile dock profili (2,00 mm) uyumu; Leaf 1400/2800 için 07'de model ve kütle verisi.
13. **[D]** Dokümantasyon: "`U_QI`", "Also," kalıntıları, kopya `monogram-module/letter` satırları, "2 916 each" gibi tabloları temizleyin.

**Özet.** İki sorunun cevabı da "evet": üç STL sayısı gerçek dosyalardan sapıyor (özellikle `battery-bent`, 5×), ve `device` sayısı eski alt-ray modülüyle (4 032 üçgen) hesaplanmış. Dock tarafında portsuz 2,00 mm gövdenin kablolu veri yolu dosyalarda tanımsız; yalnızca Qi'nin çalışması belgelenebilir durumda. Alt-ray kalıntıları `rail_*` dosyalarında, ped/pim/yuva mantığında ve 18'in giriş paragrafında duruyor.

### W4_A1_OPUS_B_MODULE_PACKAGING_AND_USBC · Model: `claude-opus-5-5` (Router: `claude-coding-router-preview`, Başlangıç: `2026-10-12 14:56:44 +03`, Bitiş: `2026-10-12 15:04:12 +03`, Süre: `448.21 sn`, Uzunluk: `23,177` karakter)

# BUDLUM LEAF · B Modülü Denetim Raporu

**Kapsam:** `05-B-MODULE-CAMERA-AND-PANEL.md`, `13-B-MODULE-PART-BY-PART.md`, `20-THE-BUDLUM-MONOGRAM.md` (Rev. L.5.0)
**Konular:** USB Type-C paketleme, kablo yükleri, manyetik tutunma, Z-yığını, kütle bütçesi, ısı, RF ve dosyalar arası çelişkiler
**Not:** `pafta/*.svg`, `cad/models/monogram-module.stl` ve `uploads/b.png` bana verilmedi. Bu yüzden bu kaynaklarla karşılaştırma yapamadım. Aşağıdaki sonuçlar yalnızca üç Markdown dosyasındaki sayılara ve fizik/standart değerlerine dayanıyor.

---

## 0 · Özet

| # | Bulgu | Önem |
|---|---|---|
| 1 | USB-C prizi, gövdenin dosyalarda yazan `8.0 x 32.0 x 4.50 mm` ölçüsüne **tek bir yönde** sığıyor: fiş ekran yüzeyine dik (Z ekseninde) takılıyor. Kablo kullanıcının yüzüne ya da masaya doğru çıkıyor. Prizin bulunduğu bölümde mıknatıs, pogo ve anten için hiç yer kalmıyor. | KRİTİK |
| 2 | Sorudaki "`1.00 mm` çubuk / `2.80 mm` derinlik" değerleri **bu üç dosyada geçmiyor**. Bu değerler başka bir kaynakta (pafta/STL) varsa, USB-C bu kesite **hiçbir eksen eşleşmesiyle** sığmaz. | KRİTİK (dosyalar arası) |
| 3 | USB-C'nin standart çekme kuvveti (`8–20 N`) mıknatıs tutuşundan (`7.2 N ±%10`) büyük. Çekme yönünde mıknatısın yalnızca sürtünmesi direnç gösteriyor (`~1 N`). **Fişi her çıkarışta modül de fişle birlikte kopar.** | KRİTİK |
| 4 | Modülün en zayıf devrilme yönündeki dayanımı `~0.008 N·m`. Sorudaki `0.115 N·m` yalnızca en güçlü yön için geçerli. Kablonun sadece kendi ağırlığı (`~0.01–0.05 N·m`) bile modülü söker. | KRİTİK |
| 5 | Arka yuvarlak AMOLED hiçbir montaj durumunda görünmüyor: yüzü her zaman ana ekrana bakıyor. | KRİTİK (işlev) |
| 6 | Pil hacim başına `~4 960 Wh/L`, yoğunluk `13.2 g/cm³` (kurşundan ağır). Mıknatıslar `34 g/cm³`. Halka gövdesi, aynı ölçüdeki dolu alüminyum bloktan ağır. | KRİTİK (fizik) |
| 7 | Halka PCB'sinin halka genişliği `2.9 mm`, üzerindeki çiplerin hepsi `3.2–6.0 mm`. Hiçbiri sığmıyor. | KRİTİK |
| 8 | Katlanmış optik `2.7 mm` yüksekliğe sığmıyor (`Ø11.6 mm` yatay lens tüpü). Prizma yüzeyi f/1.8 ile çelişiyor. | KRİTİK |
| 9 | Kütle `20.0 g` mi `22.00 g` mi? Katlanmış zarf `40 x 44 x 6.70` hiçbir geometriyle uyuşmuyor. AMOLED `300 ppi` değil, `544 ppi`. | YÜKSEK |

---

## 1 · Sorudaki varsayımların düzeltilmesi

Hesaplara geçmeden önce birkaç düzeltme gerekiyor; düzeltmeler sonucu değiştirmiyor, yalnızca daha net hale getiriyor:

1. **"`1.00 mm` çubuk", "`z = -2.00..+0.80 mm`", "ekran `2.00 mm`":** Bu değerler üç dosyanın hiçbirinde yok. Dosyalar çubuğu her yerde `8.0 x 32.0 x 4.50 mm` veriyor (05 §1/§2, 13 kalem 11, 20 §1/§2). Halka ön tarafta `z = +1.10..+5.10`, arka tarafta `-1.10..-5.10` mm. Bu simetriden ekran kalınlığı **`2.20 mm`** çıkıyor (ekran `z = -1.10..+1.10`), `2.00 mm` değil. Bu değerler bir paftadan veya STL'den geliyorsa, bu ciddi bir dosyalar arası çelişki (§2.5).
2. **"Plug tongue":** USB-C fişinde dil (tongue) yok. Dil **prizde** bulunuyor (yaklaşık `0.70 mm` kalın, `~6.7 mm` geniş). Fişin metal kabuğu ise yaklaşık `8.25 x 2.40 mm`. Sorudaki `8.25 / 2.40` değerleri doğru, sadece parçanın adı yanlış.
3. **Fiş derinliği:** Fiş kabuğunun geçme boyu nominal `~6.65 mm` (sorudaki `6.50` yakın). Prizin iç ağzı `~8.34 x 2.56 mm`. `2.56` dış yükseklik değil, iç ağız yüksekliği. Ticari prizlerin dış kabuğu tipik olarak `~3.0–3.3 mm`. Su geçirmez (IP68) modellerde bu değer çoğunlukla daha büyük.
4. **Kablo torku `0.15–0.30 N·m`:** Bu aralık durağan değil, darbe/çekiştirme senaryosu için gerçekçi. Kablo masada dururken ya da sarkarken oluşan durağan tork daha küçük: `~0.005–0.05 N·m` (§3.1). Ama aşağıda göstereceğim gibi bu küçük değer bile modülü düşürmeye yetiyor.
5. **Devrilme torku `7.2 N x 16 mm = 0.115 N·m`:** Bu sadece tek bir dönme yönü (yaw) için geçerli. En zayıf yöndeki dayanım bunun yaklaşık 1/15'i (§3.2).

---

## 2 · Soru 1: USB Type-C boyut denetimi

### 2.1 Dosyalardaki geometri: bükülme sonrası eksenler

`b.png` açılımına göre çubuk düz haldeyken yaklaşık `8.0 (x) x 32.0 (y) x 4.50 (z)`. Halka `32 x 32 x 4.0`, ikisi yan yana toplam `40 x 32` (20 §1). Menteşe ekseni çubuk ile halkanın birleştiği 32 mm'lik kenar boyunca uzanıyor. Çubuk bu eksen etrafında 90° döndürülünce eksenler şöyle yer değiştiriyor:

| Çubuk boyutu | Düz hal | Bükülmüş hal (üst kenara takılı, ön yüz) |
|---|---|---|
| `8.0 mm` | düzlemde (x) | **Z ekseni** (ekran yüzeyine dik) |
| `32.0 mm` | y | **X ekseni** (kenar boyunca) |
| `4.50 mm` | kalınlık (z) | **Y ekseni** (kenardan dışarı taşma) |

Halka ön yüzde `z = +1.10..+5.10`. Çubuğun üstü halkanın üstüyle aynı hizada ise çubuk `z = -2.90..+5.10` aralığını kaplıyor ve **arka yüzden `1.80 mm` dışarı taşıyor**. Telefon arkası üstüne düz konamıyor, çubuk kenarı üzerinde sallanıyor. Ayrıca bu durumda çubuk kenardan dışarı `4.50 mm` taşıyor, `1.00 mm` değil.

### 2.2 Üç eksende karşılaştırma: dosyaların kendi prizi (kalem 10, `8.9 x 7.3 x 3.10 mm`)

Prizin sığması için: ağız yüzeyi `8.9 x 3.1` (artı en az `~0.5 mm` duvar) bir yüze oturmalı, `7.3 mm` derinlik ise üçüncü eksene sığmalı. Altı olası yerleşimi tek tek denedim:

| # | Takma ekseni (derinlik 7.3) | Ağız genişliği 8.9 | Ağız yüksekliği 3.1 | Sonuç |
|---|---|---|---|---|
| a | Y (kenardan dışarı, en doğal yön) | X (32) ✓ | Z (8.0) ✓ | **Olmaz:** `7.3 > 4.50` |
| b | Y | Z (8.0) ✗ `8.9 > 8.0` | X ✓ | **Olmaz** |
| c | X (çubuğun ucundan, kenar boyunca) | Z (8.0) ✗ | Y (4.5) ✓ | **Olmaz:** `8.9 > 8.0` |
| d | X | Y (4.5) ✗ | Z ✓ | **Olmaz:** `8.9 > 4.5` |
| e | **Z (ekrana dik)** | **X (32) ✓** | **Y (4.5) ✓**, duvar `(4.5−3.1)/2 = 0.70` | **Geometrik olarak tek mümkün yerleşim** |
| f | Z | Y (4.5) ✗ | X ✓ | **Olmaz** |

**Sonuç:** Dosyalardaki ölçülerle USB-C fişi **yalnızca Z ekseninde, ekran yüzeyine dik olarak** takılabiliyor. Ağız, çubuğun halka tarafındaki `32 x 4.5 mm` uç yüzünde duruyor. Fiş kabuğunun `8.25 mm`'si kenar boyunca (X), `2.40 mm`'si kenardan dışarı yönde (Y) duruyor, `6.65 mm` geçme boyu Z yönünde. Ön/arka çevirme simetrisi nedeniyle ağız her zaman halkanın olduğu yüze bakıyor:
- **Ön montaj:** kablo `+Z` yönünde, kullanıcının yüzüne doğru dikey çıkıyor.
- **Arka montaj:** kablo `−Z` yönünde, doğrudan masaya doğru çıkıyor. Telefon şarj olurken düz konamaz.

### 2.3 Bu tek yerleşimin yan etkileri

1. **Zemin payı:** Priz derinliği `7.3 mm`, çubuk Z yüksekliği `8.0 mm`. Arkada `0.70 mm` kalıyor. Bu payın içine priz bacakları, onları lehimleyecek bir PCB ya da flex, ve en az `0.3 mm` titanyum taban duvarı girmeli. **Gövde içinde PCB yok:** 32 kalemlik malzeme listesinde (BOM) gövde PCB'si geçmiyor, ama `U_PD` (`3.5 x 3.5`) ve prizin bir yere lehimlenmesi gerekiyor. Eksik parça.
2. **Fiş gövdesi (overmold) taşması:** USB-C fiş gövdesinin önerilen üst sınırı `~12.35 x 6.50 mm`. `6.50 > 4.50` olduğu için gövde çubuğun iki yanından `~1.0 mm` taşıyor. Fişin uzunluğu (`~15–20 mm`) ve kablo gerilim giderici kılıfı ile birlikte ekran yüzeyinden yaklaşık `25–30 mm` yükselen bir kule oluşuyor.
3. **Kamera görüş alanına giriş:** f = 8.9 mm, sensör 12.8 x 9.6 mm. Yatay yarım açı `atan(6.4/8.9) = 35.7°`, dikey yarım açı `atan(4.8/8.9) = 28.3°`. Fiş ekseni ile optik eksen arası yaklaşık `16 + 2.25 = 18.25 mm`. Kablo dik yükselirse yaklaşık `18.25/tan35.7° ≈ 25 mm` yükseklikten sonra yatay görüş alanına, yaklaşık `34 mm` sonra dikey görüş alanına giriyor. **Şarj sırasında ön kamera görüntüsünün kenarında kablo görünür.**
4. **Kalınlık bütçesi (Y = 4.50 mm):** Priz bölümünde `3.10` (priz) + `2 x 0.70` (duvar) = 4.50, yani boş yer sıfır. Aynı bölüme mıknatıs (`1.1`), pogo (`0.55`) ve anten (`0.25`) giremez. Bu üçü, priz bölümünün dışında kalan çubuk boyuna sığmak zorunda.
5. **Uzunluk bütçesi (X = 32.0 mm), halka tarafındaki uç yüz:** Menteşe `18.0` + flex `6.5` + priz ve duvarları `8.9 + 2 x 0.7 = 10.3` → **`34.8 mm > 32.0 mm`**. Çakışma: menteşe, flex geçişi ve priz ağzı aynı uç yüze sığmıyor.
6. **Kenar yüzü (ekrana bakan `32 x 8` yüz):** Pogo dizisi `22.0`, mıknatıslar `8 x 3.2 = 25.6 mm`. Priz bölümü (`10.3`) bu yüzün altına da uzanıyor (priz Z yönünde 7.3 mm iniyor). Kalan boy `32 − 10.3 = 21.7 mm`, bu da hem `22.0` pogoya hem `25.6` mıknatısa yetmiyor.
7. **Anten çakışması:** `29.4 mm` 3 bantlı anten çubuğun neredeyse tamamını kaplıyor. Aynı boyda `8.9 mm` metal priz kabuğu, NdFeB mıknatıslar (iletken, nikel kaplı) ve titanyum menteşe bulunuyor. Anten ile metal parçalar arasında gereken boşluk yok. Rezonans kayması ve verim düşüşü kesin. MON-11'deki `>62%` RF verimi hedefi bu yerleşimle gerçekçi değil.

### 2.4 Pogo ile ekran kenarı uyumsuzluğu

Pogo ve mıknatıslar çubuğun ekrana bakan yüzünde. Ama ekran kenarının Z yüksekliği yalnızca `2.20 mm`:
- Pogo dizisinin genişliği `3.0 mm > 2.2 mm`, kenara sığmıyor.
- Yaylı pogo pimi `0.55 mm` yükseklikte yapılamaz. Yay stroku ve gövdesiyle en kısa ticari pimler bile sıkışmış halde `~1.5 mm` civarında.
- `2.2 mm` kalınlığındaki ekran kenarına karşılık gelen mıknatıs/çelik ve pogo pedlerinin de sığması gerekiyor. Bunun ekran gövdesi tarafında karşılığı verilmemiş.

### 2.5 Sorudaki `1.00 mm / 2.80 mm` kesitinin denetimi

Pafta veya STL çubuğu gerçekten "kenardan `1.00 mm` taşan, Z'de `2.80 mm`" bir kesit olarak gösteriyorsa:

| Parça | Boyutlar (mm) | En küçük boyut | Kesite (1.00 x 2.80) sığar mı? |
|---|---|---|---|
| Priz (kalem 10) | 8.9 x 7.3 x 3.10 | 3.10 | **Hayır:** `3.10 > 2.80` ve `> 1.00`, altı yerleşimin hepsi başarısız |
| Fiş kabuğu | 8.25 x 2.40 x 6.65 | 2.40 | **Hayır:** 2.40, Z'deki 2.80'e sığsa bile kalan 8.25 boyutu Y'deki 1.00'e sığmaz |
| Priz dili | ~6.7 x 0.70 | 0.70 | Tek başına sığsa bile kabuksuz dil standart dışı ve işlevsiz |

Geçme boyu (`~6.65 mm`) en az `~7 mm` malzeme gerektiriyor. Bu kesitte bunu sağlayan tek eksen X (32 mm), yani fiş çubuğun ucundan takılmak zorunda. O zaman ağız yüzeyi `1.00 x 2.80` olur. Fiş kabuğu `8.25 x 2.40` olduğundan **alan olarak 7 kat, boyut olarak 8.25 kat büyük**. Fiziksel olarak imkânsız. Ayrıca 4.50 mm (MD dosyaları) ile 1.00 mm (pafta) arasındaki fark, "single source of truth" iddiasını geçersiz kılıyor.

---

## 3 · Soru 2: Kablo kaldıraç torku ve modülün tutunması

### 3.1 Yükler

| Yük | Fizik | Değer |
|---|---|---|
| Kablo ağırlığı (240 W / 40 Gbps sınıfı, ~Ø4.5–5 mm, ~30–50 g/m) | sarkan 1 m kablo ≈ `0.3–0.5 N`, fiş ucunda `~25 mm` kolla | **`~0.008–0.012 N·m`** |
| Bükülme rijitliği | EI ≈ `2–8 x 10⁻⁴ N·m²` (tahmin), R ≈ 25 mm'de M = EI/R | **`~0.01–0.03 N·m`** |
| Durağan toplam | ağırlık + bükülme | **`~0.01–0.05 N·m`** |
| Dinamik (çekiştirme, takılma, cepten çıkarma) | sorudaki aralık; USB-C 4 eksen testi yaklaşık `8 N x 15 mm ≈ 0.12 N·m` mertebesinde (değer revizyona göre değişebilir) | **`0.12–0.30 N·m`** |
| Takma kuvveti (USB-C standardı) | `5–20 N`, −Z yönünde | — |
| **Çekme kuvveti (USB-C standardı)** | yeni bağlantıda **`8–20 N`**, +Z yönünde | — |

### 3.2 Yöne göre tutma kapasitesi

Mıknatıslar (`7.2 N ±%10`, en kötü durumda `6.5 N`) ekran kenarına **normal yönde (−Y)** çekiyor. Temas yüzeyinin Z yüksekliği `2.2 mm`, X boyu en fazla `32 mm`. Halka ekran yüzeyine sadece oturuyor, yapışmıyor.

| Yük yönü | Dönme noktası ve direnç | Kapasite |
|---|---|---|
| **Pitch, dışarı (+Y yanal çekiş)** | Çubuk, kenar temasının alt köşesi (`z = −1.10`) etrafında döner, halka yüzeyden kalkar. Kol = mıknatıs merkezine `~1.1 mm` | `7.2 x 0.0011 ≈` **`0.008 N·m`** (−%10 ile `0.007`; `0.40 mm` FKM conta boşluğu çekişi tahminen %30–50 düşürür → **`~0.004–0.006 N·m`**) |
| **Pitch, içeri (−Y, kablo ekranın üstüne yatar)** | Halka uzak kenarı (`y = 48`) etrafında döner. Mıknatıs kuvveti kola neredeyse paralel; direnç sürtünmeden geliyor: μ ≈ 0.1–0.2 → `0.7–1.4 N x 32 mm` | **`~0.02–0.045 N·m`** |
| Roll (kenar boyunca, X yönünde çekiş) | Mıknatıslar ayrılmaz, kayar; direnç sürtünme ve halkanın yüzeye basması | `~0.02–0.04 N·m` |
| **Yaw (+Y çekiş, kuvvet X'te merkez dışında)** | Çubuğun bir ucu kenardan ayrılır; mıknatıs merkezi `16 mm` kolda | `7.2 x 0.016 =` **`0.115 N·m`** (sorudaki değer; **en iyi durum**) |
| **Fiş çekme (+Z)** | Mıknatıs yük yönüne dik; direnç sadece sürtünme | **`~0.7–1.4 N`** ≪ `8 N` |

### 3.3 Karar tablosu: kablo takılınca modül düşer mi?

| Senaryo | Yük | Kapasite | Güvenlik katsayısı | Sonuç |
|---|---|---|---|---|
| Kablo yana doğru serbest sarkıyor | 0.01–0.05 N·m | 0.005–0.008 N·m | **0.1–0.8** | **Düşer** |
| Sınır: yanal kuvvet × 25 mm kol | F_kritik = 0.008/0.025 = **0.32 N ≈ 33 gf** | — | — | 1 m kablonun ağırlığı (≈0.4 N) bu sınırı aşıyor |
| Dinamik çekiş, en iyi yön (yaw) | 0.15–0.30 N·m | 0.115 N·m | **0.38–0.77** | **Düşer** (sorudaki sonuç doğru) |
| Dinamik çekiş, pitch | 0.15–0.30 N·m | 0.008 N·m | **0.03–0.05** | **Kesin düşer** |
| Fişi çıkarma | 8–20 N | ~1 N (sürtünme) / 7.2 N (normal) | **0.05–0.9** | **Her çıkarışta modül fişle birlikte gelir** |

**Cevap:** Evet, modül düşer. Sorudaki hesap (0.115 < 0.15) aslında iyimser. En zayıf yönde dayanım yaklaşık **15 kat** daha düşük. Kablonun sadece kendi ağırlığı yeterli, dinamik yüke gerek yok. Asıl en temel sorun şu: **USB-C'nin standart en düşük çekme kuvveti (`8 N`), mıknatısın en yüksek tutuşundan (`7.2 N`) büyük.** Bu yüzden tasarım, kablo hiç hareket etmese bile kullanılamaz.

### 3.4 Menteşe üzerinden giden yük

- Pitch torku çubuktan halkaya `Ø2.2 mm` menteşenin kilit kamları (detent) üzerinden geçiyor. Bu ölçüde bir mikro kam kilidin tutma torku tipik olarak `~0.01–0.05 N·m`. 0.15–0.30 N·m'lik yük kilidi aşar: çubuk 90° konumundan çıkar, modül katlanır.
- Torkun pime eğilme olarak bindiği kötü durumda: σ = 32M/(πd³) = 32 x 0.3 / (π x (2.2 x 10⁻³)³) ≈ **287 MPa**. Ti-6Al-4V akma dayanımı (~880 MPa) aşılmıyor. Ama kam profilleri çentik etkisi yaratır ve yorulma dayanımını ~300–500 MPa mertebesine indirir. 50 000 çevrim hedefiyle sınırda.
- Prizi taşıyacak bir PCB veya ankraj yok, zemin payı `0.70 mm`. USB-C prizleri burulma yüklerine karşı kartın içinden geçen kabuk bacaklarıyla tutturulur. Burada tekrarlanan çekiştirmeler lehim pedlerini koparır.

### 3.5 Düşme ve günlük kullanım

- **1.5 m düşme (MON-12):** Sert zeminde çarpma ivmesi tipik olarak `~1 000–5 000 g`. Modüle etkiyen kuvvet `0.020 kg x 1 000 x 9.81 ≈ 196 N`, tutuşun 27 katı. Modül her düşmede kopar. "30 ünite kusursuz geçti" kriteri, modül takılıyken anlamsız.
- **Masaya hafif vurma (~50 g):** `0.02 x 50 x 9.81 = 9.8 N > 7.2 N`, yine kopar.
- **Cebe sokma:** Halka yüzeyden `4 mm` taşıyor. Kumaştan gelen birkaç N'luk kesme kuvveti, sürtünmeye dayalı ~1 N'luk direnci aşar ve modülü sıyırır.

---

## 4 · Diğer bulgular

### 4.1 Kütle ve yoğunluk (fiziksel imkânsızlıklar)

| Kalem | Hacim | Listedeki kütle | Çıkan yoğunluk | Gerçek malzeme | Durum |
|---|---|---|---|---|---|
| 15 · LLZO pil `18 x 4.2 x 1.2` | 90.7 mm³ | 1.20 g | **13.2 g/cm³** | kurşun 11.3; katı hal pil ~3–4 | **İmkânsız** |
| 15 · enerji | 0.45 Wh / 0.0907 cm³ | — | **~4 960 Wh/L** | bugünkü en iyi hücreler ~800–1 200 | **~4–6 kat fazla** |
| 6 · 8x N52H `3.2 x 1.6 x 1.1` | 45.1 mm³ | 1.55 g | **34.4 g/cm³** | NdFeB 7.5 → 0.34 g | **İmkânsız** (osmiyum 22.6) |
| 13 · Ti menteşe `Ø2.2 x 18` | 68.4 mm³ | 0.95 g | **13.9 g/cm³** | Ti-6Al-4V 4.43 → 0.30 g | **Zarfla çelişiyor** |
| 14 · halka gövdesi | dolu halka π(16²−12²)·4 = 1 407 mm³ | 4.50 g | 3.2 g/cm³ | 6061: 2.70 → **dolu blok 3.80 g** | **İçi boş gövde, dolu bloktan ağır** |
| 19 · PCBA halkası | 136.9 mm³ | 1.45 g | 10.6 g/cm³ | HDI ~1.9–2.2 → ~0.28 g (çipler ayrı listelenmiş) | aşırı |
| 32 · ön safir `Ø24 x 0.40` | 181 mm³ | 0.45 g | 2.49 | safir 3.98 → **0.72 g** | olması gerekenden hafif |

**Toplam kütle:** BOM satırlarını tek tek topladım, sonuç **22.00 g**. Ama dosya 05 §2, dosya 20'nin başlığı ve dosya 13'ün başlığı **20.0 g** diyor. %10'luk fark kapanmıyor. Yukarıdaki imkânsız yoğunluklar düzeltilirse toplam yeniden hesaplanmalı.

### 4.2 Halka içi paketleme

- **Halka genişliği:** (32 − 24)/2 = **4.0 mm** radyal.
- **PCB halkası:** (30.2 − 24.4)/2 = **2.9 mm** radyal. U1 (`5.2 x 5.2`), U2 (`6.0 x 5.5`), U3/U4 (`3.2 x 3.2`) yongalarının **hiçbiri** 2.9 mm genişliğe sığmıyor.
- **Pil:** `4.2 mm` genişlik > `4.0 mm` halka (duvarlar düşülmeden bile). Düz kabul edilirse, 18 mm'lik bir kirişin r = 12 mm'deki sarkıklığı `12 − √(144 − 81) = 4.06 mm`. Yani pil kalınlığı sıfır olsa bile halkaya girmiyor. "Eğri LLZO" ise seramik elektrolit nedeniyle 1.2 mm kalınlıkta kırılgan, üretimi ayrı bir risk.
- **Hoparlör `9.0 x 3.2`:** Kiriş sarkıklığı 0.88 mm + 3.2 = **4.08 mm > 4.0 mm**. PCB ve pille de aynı radyal hacmi paylaşıyor.
- **Parça sayısı:** "32 parça" denmiş, ama 16 ve 28 numaralı kalemler ikişer adet (fiziksel olarak 34), 5 ve 6 numaralı kalemler dizi. Dosya 05 ise pilin kendisi için "32 internal parts" diyor, kopyala-yapıştır hatası gibi duruyor.

### 4.3 Optik (MON-2 / MON-3)

- **Yatay lens tüpü `Ø11.6 x 13.8 mm`:** Toplam optik yüksekliği 2.7 mm (`z = 0.90..3.60`). Yatay yatan bir tüp **11.6 mm yükseklik ister**. İmkânsız.
- **Katlanmış yol ile yatay sensör çelişkisi:** Prizma ışığı yataya katlıyorsa sensör dik durmalı ve en az 9.6 mm yükseklik ister. Sensör yatay (`z = 0.90..1.55`) olacaksa ikinci bir 45° katlama gerekir. Görüntü düzlemine yakın bu ayna/prizma da yaklaşık görüntü boyutunda (≥ 9.6 mm) olmalı. İki yol da 2.7 mm'ye sığmıyor.
- **Açıklık:** Giriş göz bebeği D = f/N = 8.9/1.8 = **4.94 mm > 3.4 mm prizma yüzeyi**. f/1.8 elde edilemez, ciddi vinyetleme olur.
- **Tutarlı olan kısım:** Sensör köşegeni 16 mm ve f = 8.9 mm ile 2·atan(8/8.9) = 83.9°. MON-3'teki 84° doğru hesaplanmış.
- **Dikey yığın toplamı:** Sensör 0.65 + IR filtre 0.35 + G1 1.35 + diyafram 0.35 = 2.70 mm, bütçeyi tek başına dolduruyor. VCM (0.9), prizma (2.6), bezel (2.30) ve hoparlör (2.2) aynı Z aralığında. MON-2'deki "sıfır Z-çakışma" iddiası tutmuyor.
- **OIS ile ekran çakışması:** OIS taşıyıcısı (0.85 mm) sensörün altında olmalı, yani `z ≈ 0.05..0.90`. Bu aralık ekran yığınının (`0.00..0.90`) içinde. MON-3'teki "rear AMOLED ile sıfır çarpışma" iddiasıyla çelişiyor.

### 4.4 Arka AMOLED (MON-4)

- **Piksel yoğunluğu:** 480 px / 22.4 mm = 21.4 px/mm = **544 ppi**, belirtilen 300 değil.
- **Kenarlık:** Panel Ø23.2, aktif alan Ø22.4 → 0.4 mm kenarlık. Yuvarlak AMOLED'lerde gate sürücü devresi ve sızdırmazlık için tipik olarak 1 mm'den fazla gerekir. Sürücü yonganın ve FPC kuyruğunun yolu da tanımsız.
- **Görünürlük:** Arka safir "against screen". Ön montajda panel ana ekrana bakıyor, arka montajda telefonun arkasına bakıyor. **Hiçbir montaj durumunda görünmüyor.** MON-4'teki "selfie viewfinder" imkânsız.

### 4.5 Yüzey hasarı

Arka pencere safir (Mohs 9), ana ekranın kapak camı tipik olarak alüminosilikat (Mohs ~6–7). Takma, çıkarma ve kablo kaynaklı kaymalarda safir **ana ekranı çizer**. Kalem 4'teki "soft screen pad" ile kalem 1'deki "safir ekrana temas ediyor" ifadeleri birbiriyle çelişiyor.

### 4.6 Isı

- **Yüzey alanı:** Açık yüzey yaklaşık `~1 800 mm²`. Konveksiyon + ışınım için h ≈ 12 W/m²K alınırsa toplam ısıl iletkenlik ≈ 0.022 W/K.
- **Isı kaynağı:** 60 GHz verici + TCON + kodek için 1–2 W varsayarsam (dosyalar güç vermiyor), kararlı durumda **ΔT ≈ 45–90 K**. Bu, IEC 62368-1'in elle tutulan metal yüzeyler için sınırlarını ciddi biçimde aşar.
- **Grafit katman:** 1 200 W/m·K grafit sadece ısıyı yayar, dışarı atmaz. Tek iletim yolu, safir üzerinden ana ekrana gitmek, bu da ekranı lokal olarak ısıtır.
- **Pil süresi:** 0.45 Wh / ~1.5 W ≈ **18 dakika**.

### 4.7 Elektrik ve RF

- **Menteşe flex'i (20 hat):** DP alt-mode için 4 diferansiyel çift (8 hat) + D± (2) + CC1/CC2 (2) + SBU (2) + VBUS/GND (en az 4). Bu 18 hat sadece USB-C için. 12 pogo hattı ve anten beslemeleri de buna ekleniyor. **20 hat yetmez.**
- **60 GHz yolu:** 60 GHz dizisi çubukta, U2 yongası halkada. 60 GHz sinyali menteşedeki flex'ten geçecekse LCP mikroşeritte yaklaşık 0.5–1 dB/cm kayıp ve büküm kaybı oluşur. 60 GHz verici-alıcının antenle aynı yerde olması gerekir.
- **Flex geçişi:** 6.5 mm genişliğindeki flex, Ø2.2 menteşenin içinden geçemez. Yanından geçecekse §2.3'teki uzunluk bütçesini aşıyor.
- **SAR:** 6 GHz üzerinde (FCC/ICNIRP) SAR değil, güç yoğunluğu (W/m²) ölçülür. "60 GHz için SAR = 0.054 W/kg" metrik olarak yanlış.
- **"PD 3.1 40 W":** 40 W, SPR (≤ 20 V) sınırları içinde. PD 3.1'in getirdiği EPR (28/36/48 V) gereksiz. Etiket yanıltıcı ama zararsız.
- **IP68:** Menteşede dönen bir flex geçişini 1.5 m su altında sızdırmaz tutmak çok zor. Tek bir `30.0 x 3.6 x 0.40` FKM conta hem çubuğu hem halkayı kapatamaz.

### 4.8 Zarf ve dosyalar arası çelişkiler

| Konu | Dosya A | Dosya B | Çelişki |
|---|---|---|---|
| Kütle | 05/20: 20.0 g | 13 BOM: 22.00 g | %10 |
| Katlanmış zarf | 13 toplam: `40 x 44 x 6.70` | Geometriden: `(32 + 4.5) x 32 x 8.0` = **`36.5 x 32 x 8.0`** (ekranla birlikte Z: 8.0) | 44 ve 6.70 hiçbir ölçüye karşılık gelmiyor |
| Çubuk genişliği | 20 §1: "4.0..8.0 mm bridge" (4 mm mi?) | Aynı yerde: 8.0 x 32 ve toplam 40 = 8 + 32 | Belirsiz |
| Çevrim ömrü | Menteşe 50 000, flex 100 000 | MON-12: 50 000 | Flex aşırı, tutarlı ama gereksiz |
| Çubuk kesiti | MD dosyaları: 4.50 mm | Soru (pafta?): 1.00 / 2.80 mm | §2.5 |
| Ekran kalınlığı | ±1.10'dan çıkarım: 2.20 mm | Soru: 2.00 mm | 0.2 mm, kenar temasını etkiliyor |
| Görünür arka AMOLED | MON-4 | Rev. L.5.0 yerleşimi | §4.4 |

---

## 5 · Düzeltme önerileri

1. **USB-C'yi modülden çıkarın, ekran gövdesine taşıyın.** USB-C prizi için en az şu iç ölçüler gerekiyor: kalınlık ≥ ~4.3 mm (3.1 + 2 x 0.6), derinlik ≥ ~8.5 mm (7.3 + PCB + taban), genişlik ≥ ~10.5 mm. Bunları sağlayan yer ekran gövdesi. Gövdede port istenmiyorsa, modüle **bilerek kopan manyetik bir kablo** (MagSafe tarzı, pogo tabanlı) kullanın: kablonun kopması bir arıza değil, tasarım özelliği olur.
2. **USB-C modülde kalacaksa mekanik kilit şart.** Çubuk, kenarı her iki yüzden saran ve en az 3–4 mm dudaklı bir U-klips olmalı. Bu, pitch torkunu ~1.1 mm yerine ~4–8 mm kolla karşılar. 0.3 N·m için 0.3/0.006 ≈ **50 N** temas kuvveti çifti gerekiyor; bu mıknatısla değil, ancak mekanik geometriyle sağlanabilir. Ayrıca fiş çekme yönünde ≥ 25 N tutan bir kilit (yaylı mandal veya tırnak) ekleyin.
3. **Mıknatıs kuvvetini yeniden tanımlayın.** Hem normal hem kesme yönünde, conta boşluğu dahil, karşısında çelik veya mıknatıs olacak şekilde ölçün. Pitch yönü için gereken tutuş (0.05 N·m / 1.1 mm ≈ 45 N) 2.2 mm'lik bir kenarda mıknatısla elde edilemez.
4. **Halka mimarisini baştan ele alın:** halka genişliğini en az 7–8 mm'ye çıkarın ya da çipleri merkez diske taşıyın. Pil enerjisini ~0.08–0.1 Wh'e düşürün. Optiği 2.7 mm yerine en az ~6–8 mm yüksekliğe göre tasarlayın.
5. **Arka AMOLED'i ya kaldırın ya da halkayı ters çevrilebilir yapın** (ekran dışa baksın).
6. **Ekrana temas eden yüzeyi** safir yerine TPU veya silikon ped yapın.
7. **"Single source of truth" ilkesini gerçekten uygulayın.** BOM toplamı, zarf ölçüleri, çubuk kesiti ve ppi tek bir parametrik CAD modelinden üretilsin. Paftalar ve STL bu üç dosyayla aynı revizyona getirilsin.

**Sonuç:** Rev. L.5.0'daki B modülü mevcut haliyle üretilemez. USB-C, mıknatısla tutunan bir parçaya konmuş. Standardın gerektirdiği çekme kuvveti tutuşu aşıyor, kablonun kendi ağırlığı en zayıf devrilme yönünü yeniyor. Halka içi paketleme, pil enerjisi ve optik yığın da fizik sınırlarının dışında.

### W4_A2_OPUS_CAMERA_OPTICS_AND_THERMAL_AUDIT · Model: `claude-opus-5-5` (Router: `coding-router-preview`, Başlangıç: `2026-10-12 14:56:47 +03`, Bitiş: `2026-10-12 15:04:12 +03`, Süre: `445.71 sn`, Uzunluk: `23,555` karakter)

# Budlum Leaf `b` modülü denetimi: optik, termal, akustik ve belgeler arası çelişkiler

**Kapsam:** `03-PART-CATALOGUE.md`, `05-B-MODULE-CAMERA-AND-PANEL.md`, `13-B-MODULE-PART-BY-PART.md` (Rev. L.5.0)
**Yöntem:** Araç çalıştırmadım. Tüm sayılar bu üç dosyadan alındı, hesaplar elle yapıldı.

---

## 0 · Önce iki önemli tespit

### 0.1 `HARDWARE/20` bana verilmedi
İkinci görevde `HARDWARE/20` dosyası da geçiyor ama içeriği bu mesajda yok. O dosya hakkında satır uyduramam. Aşağıdaki çelişki listesi yalnızca 03, 05 ve 13 için geçerli. 20 numaralı dosyayı taramak için Bölüm 7'de bir `grep` komutu var.

### 0.2 Brief'teki "yeni mimari" bu üç dosyada hiç yok
Brief'te geçen değerler ile dosyalardaki değerler şöyle:

| Brief'teki değer | 03 / 05 / 13'teki gerçek değer | Sonuç |
|---|---|---|
| Halka `2.00 mm` (`z = 0.00..2.00`) | Üç dosyada da halka **`4.00 mm`**. `2.00 mm` yalnızca **ekran gövdesinin** kalınlığı (03 §1) | Halka 2.00 mm diyen hiçbir satır yok. Ya 20 numaralı dosyada ya da henüz yazılmamış bir revizyonda |
| "Bazı tablolarda halka `4.50 mm`" | `4.50 mm` hiçbir yerde halka değil, hep **çubuk** (`8.0 x 32.0 x 4.50`) | Brief'te çubuk ile halka karıştırılmış |
| LTPO AMOLED `0.36 mm` | **`0.40 mm`** (`z = 0.35..0.75`, parça #2 `Ø23.2 x 0.40`) | Uyuşmuyor |
| Cu-Grafit kalkan `0.10 mm` | **`0.15 mm`** (`z = 0.75..0.90`, parça #3) | Uyuşmuyor |
| Optik yükseklik `1.50 mm` | Üst yığın **`3.10 mm`** (`z = 0.90..4.00`) | Uyuşmuyor |
| `1.00 mm` yatay çubuk, ek menteşe yok | Çubuk **`4.50 mm`**, **`90°` bükülü**, ayrı **`±90°` Ti menteşe** parçası var (#13), menteşe flex'i var (#12) | Belgeler tamamen eski mimaride |
| Sensör "`1/1.28 inç` sınıfı" | Parça #21: **"1-inch class"** | **Dosya doğru, brief yanlış.** Ayrıntı 1.1'de |

Bu yüzden optik hesabı **iki senaryoda** yaptım:
- **Senaryo A (belgelerdeki hâli):** 4.00 mm halka, 3.10 mm optik yükseklik.
- **Senaryo B (brief'teki hedef):** 2.00 mm halka, ≈1.50 mm optik yükseklik.

**Sonuç: iki senaryoda da 50 MP / 16 mm görüntü çemberli kamera fiziksel olarak mümkün değil.**

---

## 1 · Optik Z-yığını, EFL/TTL ve etendü denetimi

### 1.1 Sensör sınıfı: brief'teki "1/1.28 inç" etiketi yanlış
- Köşegen: √(12.8² + 9.6²) = **16.0 mm**.
- Eski vidikon kökenli "1 inç tipi" sensörlerin köşegeni yaklaşık **16 mm**. Yani 12.8 x 9.6 mm, 4:3 oranlı **1 inç tipi** bir sensör. Sony LYT-900 sınıfı: 8192 x 6144 piksel, **1.6 µm** piksel. Hesap: 12.8 mm / 8192 ≈ 1.5625 µm, toplam 50.3 MP.
- 1/1.28" sınıfı bir sensörün köşegeni yalnızca ≈ **12.5 mm**.
- Parça #21'deki "1-inch class" ifadesi doğru. Brief'teki etiket, sorunu olduğundan **daha küçük** gösteriyor.

### 1.2 Bu lens aslında 24 mm eşdeğerinde ana kamera lensi
- Parça #24: `f = 8.9 mm`, `f/1.8`.
- Kırpma faktörü: 43.27 / 16.0 = 2.70. Eşdeğer odak: 8.9 × 2.70 ≈ **24 mm**.
- Köşegen yarım görüş açısı: atan(8.0 / 8.9) = **41.9°**, tam köşegen ≈ **84°**. Bu bir **geniş açı** lens.
- Giriş göz bebeği: D = f / N = 8.9 / 1.8 = **4.94 mm**.
- Görüntü tarafı NA: 1 / (2N) = **0.278**.

Bu tam olarak Xiaomi 14 Ultra veya vivo X100 Ultra'nın ana kamera tarifi. O telefonlarda modül yüksekliği **≈ 9–11 mm** ve gövdeden birkaç milimetre taşan dev bir kamera çıkıntısı var. Üstelik **katlanmış optik, geniş açılı ana kamerada kullanılmaz.** Periskoplar dar görüş açılı telefoto lenslerde kullanılır, çünkü katlama ancak ışın demeti dar olduğunda düz bir prizmaya sığar.

### 1.3 Optik yol topolojik olarak kopuk (KRİTİK)
Dosya 13 şu sırayı tarif ediyor: ön pencere (`z = 3.60..4.00`), obtüratör, G1 dubleti, **tek bir 45° prizma**, **yatay** 5P namlu (`Ø11.6 x 13.8`) ve son olarak **yatay yatan** sensör (`z = 0.90..1.55`, 12.8 x 9.6 alanı XY düzleminde).

- Prizma, +Z'den gelen ışığı yatay eksene çeviriyor ve ışık yatay namludan geçiyor.
- Ama sensör **yüzü yukarı bakacak şekilde yatıyor.** Yatay eksendeki ışığı ona göndermek için **ikinci bir katlama aynası veya prizması** gerekir. BOM'da böyle bir parça yok.

Yollar şunlar:
- **(a) Sensör dik durursa:** Sensörün en az 9.6 mm'lik kısa kenarı Z ekseninde durur. Seramik paketle birlikte ≈ 11–12 mm eder. Bu 4.00 mm'ye de 2.00 mm'ye de sığmaz.
- **(b) İkinci katlama eklenirse:** 45°'lik aynanın Z yüksekliği, odağa yakın demet kesitine, yani görüntünün o eksendeki boyutuna yaklaşık eşittir. Bu en az **9.6 mm**.

Her iki durumda da sensör ekseninde gereken Z yüksekliği **en az ≈ 10 mm**. Bu, Senaryo A'nın 3.2 katı, Senaryo B'nin 6.7 katı.

### 1.4 Lagrange değişmezi: tek boyutlu etendü kanıtı
Optik değişmez H = n · u · y, sistemin her düzleminde korunur.

**Görüntü tarafında gereken H:**
- Kısa kenar (yarım yükseklik 4.8 mm): H = 4.8 × 0.278 = **1.33 mm**
- Uzun kenar (yarım yükseklik 6.4 mm): H = **1.78 mm**
- Köşegen (yarım 8.0 mm): H = **2.22 mm**

**Yüksekliği h olan bir yarıktan geçebilecek en büyük H:**
Işının yarım genişliği en fazla h/2 olabilir ve sin θ ≤ 1'dir. Bu yüzden H_max ≤ n · h / 2.

| Optik yükseklik | Havada teorik üst sınır (θ = 90°, sıyırma) | Pratik sınır (sin θ ≈ 0.5) | Pratikte sığabilecek en büyük sensör kenarı |
|---|---|---|---|
| **h = 1.50 mm (Senaryo B)** | **0.75 mm**. Gereken 1.33 mm'nin altında: **teoride bile imkânsız** | 0.375 mm | 2 × 0.375 / 0.278 ≈ **2.7 mm** (≈ 1/6" sınıfı) |
| **h = 3.10 mm (Senaryo A)** | 1.55 mm. Sınırda, ama ancak 90° ışınlarla | 0.78 mm | ≈ **5.6 mm** (≈ 1/2.5", tam olarak sanayideki periskop boyutları) |
| n = 1.88 prizma camı içinde, h = 1.5 mm | 1.41 mm. Ancak cam içinde ≈ 90° ışın gerekir, bu da TIR ve Fresnel yüzünden gerçekleşemez | 0.70 mm | ≈ 5 mm |

İki boyutlu etendü: G = π · A · NA² = π × 122.9 × 0.0772 ≈ **29.8 mm²·sr**. İki boyutlu sınır tek başına ihlal edilmiyor, çünkü yarık genişliği yeterli. Ama **Z ekseninde tek boyutlu sınır** iki senaryoyu da eliyor. Kısacası 1.50 mm'lik bir yarıktan 16 mm görüntü çemberini f/1.8'de aydınlatmak termodinamik olarak (parlaklığın korunumu) imkânsız.

### 1.5 Bileşen boyutları ile Z bütçesi çakışıyor
Üst yığında yalnızca **3.10 mm** yer var (`z = 0.90..4.00`). Senaryo B'de bu ≈ 1.50 mm.

| Parça | Z kalınlığı |
|---|---|
| #32 ön safir | 0.40 |
| #27 obtüratör | 0.35 |
| #26 G1 dubleti | 1.35 |
| #25 prizma | 2.60 |
| #24 5P namlu (yatay, **çap Z'de**) | **11.60** |
| #23 VCM | 0.90 |
| #22 IR filtre | 0.35 |
| #21 sensör | 0.65 |
| #20 OIS tablası | 0.85 |
| **Yalnızca seri optik yol (namlu hariç)** | **7.45 mm** |
| **Namlu dahil, alt sınır** | **≥ 11.6 mm** |

**Ek çakışmalar:**
- **Namlu çelişkisi.** Dosya 05 tablosu namluyu `z = 0.90..3.60`, yani **2.70 mm** yüksekliğe koyuyor. Parça #24 ise namlunun çapını **Ø11.6** veriyor. Aynı parça için 4.3 kat fark var.
- **Sensör ile namlu aynı Z'de başlıyor.** Sensör `z = 0.90`, namlu `z = 0.90`. Yan yana durmaları gerekir. OIS tablası (15.2 x 12.2) ile namlu (13.8 x 11.6) yan yana konursa zarf 23.8 x 15.2 mm olur. Köşegeni √(23.8² + 15.2²) = **28.2 mm**. Bu **Ø24 bore'a sığmaz.**
- **Prizma ile göz bebeği uyuşmuyor.** Prizma yüzü 3.4 mm, oysa giriş göz bebeği 4.94 mm. Prizma göz bebeği düzleminde olsa bile N_etkin ≥ 8.9 / 3.4 = **f/2.6**. Görüş açısı yüzünden demet büyüdükçe durum daha da kötüleşir. **f/1.8 bu prizmayla mümkün değil.**
- **G1 ile prizma uyuşmuyor.** Ø12.0 G1 dubletinin altındaki prizma yalnızca 3.4 mm. Demet ya kırpılır (vinyet) ya da G1'in çok kısa odaklı olması gerekir, bu da büyük sapınçlar demektir.
- **Görüntü çemberi.** Namlunun dış çapı Ø11.6, görüntü çemberi 16 mm. Gerçek 1 inç telefon lenslerinde son "W" asferik eleman **Ø17–20 mm** olur. Bu namlu sensör köşelerini aydınlatamaz.
- **OIS sensörün altında.** Sensör yüzeyi `z = 0.90`'da kalkanın hemen üstünde, ama OIS tablası (0.85 mm) altta olmalı. O zaman `z = 0.05..0.90` aralığına düşer. Burası AMOLED (`0.35..0.75`) ve kalkanın (`0.75..0.90`) yeri: **fiziksel çakışma.**

### 1.6 Prizmada TIR sınırı (YÜKSEK)
- n = 1.88 için kritik açı: arcsin(1/1.88) = **32.1°**.
- 45° katlamada TIR'ın korunması için cam içindeki açı en fazla 45° − 32.1° = **±12.9°** olabilir. Havada bu ±24.8°'ye karşılık gelir.
- f/1.8 marjinal konisi havada zaten ±16.1° harcıyor. Görüş açısına kalan yalnızca ≈ **±8.7°**.
- Katlama düzleminde gereken yarım görüş açısı: atan(4.8 / 8.9) = **28.3°**.
- **Sonuç:** Prizma TIR ile çalışamaz. Hipotenüs Ag/Al ile kaplanmalı (≈ %5–8 kayıp). Belgede bu belirtilmemiş.

### 1.7 Odak, OIS ve tolerans
- **VCM stroku 200 µm.** Odak kayması Δ = f² / (u − f) formülüyle hesaplanır.
  - 200 µm, en yakın odak mesafesi olarak **≈ 405 mm** verir.
  - 300 mm'lik selfie mesafesi için **272 µm**, 250 mm için **329 µm** gerekir.
  - **Selfie mesafesinde odaklanamaz.**
- **OIS ±1.8° eğim.** Sensör kenarında defokus = 8 mm × tan(1.8°) ≈ **251 µm**. Alan derinliği ise ±2 · N · c = ±2 × 1.8 × 3.1 µm ≈ **±11 µm**. Hata 22 kat. "Sensor-shift" ötelemeyle çalışmalı, eğimle değil.
- **Sensörün Z toleransı ±20 µm**, alan derinliği ±11 µm. Aktif hizalama (AA) şart, ama süreç tanımlı değil.
- **40 cm, f/1.8'de alan derinliği:** 2 · N · c · u² / f² ≈ **22 mm**. Yüzün tamamı net olmaz.
- **Kırınım.** f/4'te Airy çapı 2.44 × 0.55 × 4 = 5.4 µm, yani 3.4 piksel. Bu diyafram değerinde 50 MP fiilen ≈ 12 MP'ye düşer.

### 1.8 Senaryo B'de gerçekçi tavan
Varsayımlar: 1.50 mm − 0.3 mm COB sensör − 0.2 mm kapak, yani TTL ≤ 1.0 mm. Bu f ≈ 0.85 mm ve ≈ 1.4 mm görüntü çemberi demek.

- Sensör en fazla ≈ 1.1 x 0.85 mm olur. 0.7 µm pikselle teorik ≈ 1.9 MP. Kırınım hesaba katılınca etkin değer ≈ **0.3 MP**.
- Gerçek dünyadaki örnek: OmniVision OVM6948 (0.65 x 0.65 x 1.16 mm, 200 x 200 piksel).
- **2.00 mm'lik bir halkaya ancak endoskop sınıfı bir kamera sığar, 50 MP değil.**

---

## 2 · Mekanik çakışmalar ve tolerans

| # | Sorun | Hesap | Önem |
|---|---|---|---|
| M1 | PCBA halkasına çipler sığmıyor | Halka genişliği (30.2 − 24.4) / 2 = **2.9 mm**. U1 5.2 x 5.2, U2 6.0 x 5.5, U3/U4 3.2 x 3.2: **hiçbiri sığmaz** | KRİTİK |
| M2 | Pil duvara sığmıyor | Duvarın tamamı (32 − 24) / 2 = 4.0 mm, pil genişliği **4.2 mm** | KRİTİK |
| M3 | Hoparlör duvara sığmıyor | Hoparlör 3.2 mm genişliğinde. Duvar et payları düşülünce ≤ 3.2 mm kalıyor ve PCBA da aynı halkada | YÜKSEK |
| M4 | USB-C çubukta yer yok | Çubuk 8.0 x 4.50. Soket 8.9 x 7.3 x 3.10. Geriye 1.4 mm kalıyor; anten (0.25) + 60 GHz (0.30) + mıknatıs (1.1) + pogo (0.55) + duvarlar **> 2.2 mm** ister | KRİTİK |
| M5 | Senaryo B'de 1.00 mm çubuk | USB-C fişinin dili ≈ 2.4 mm, soket ağzı ≥ 2.56 mm. Mıknatıs 1.1 mm. **Çubuk 1.00 mm olursa USB-C ve mıknatıs fiziksel olarak sığmaz** | KRİTİK |
| M6 | Aynı nominal çaplı üç parça | Bore Ø24.0, pencere Ø24.0 (#32), bezel Ø24.0 (#31). Pencere aynı dış çaplı bezelin içine oturamaz; ±0.02 toleransta 0.04 mm'ye kadar sıkı geçme olur | YÜKSEK |
| M7 | Al ile safir arasında genleşme farkı | ΔD = 24 × (23 − 5.5) × 10⁻⁶ × 40 K ≈ **17 µm**. Ya safir çatlar ya da IP68 açıklığı oluşur | YÜKSEK |
| M8 | Pogo dizisi ekran kenarından geniş | Dizi 3.0 mm genişliğinde, gövde kenarı 2.00 mm. r = 0.65 köşe yuvarlatmaları çıkınca düz temas alanı **0.70 mm**. 12 pin tek sırada ≈ 1.83 mm aralıkla dizilmek zorunda | YÜKSEK |
| M9 | Halka ekranın üstünde havada mı? | Halka `z = +1.10`'da başlıyor, gövde yüzeyi `+1.00`'da: **0.10 mm** boşluk. Ama FKM ped **0.40 mm** ve arka safir "ekrana temas ediyor" diye geçiyor. Üçü aynı anda doğru olamaz | ORTA |
| M10 | Zarf boyutu | 05'te plan "40.0 x 32.0", 13'te "40 x 44 x 6.70". Çubuk 8.0 dik dursaydı yükseklik 8.0 olurdu, 6.70 değil. Değer hiçbir geometriden türetilemiyor | ORTA |
| M11 | "Bore" mu, dolu mu? | 03 "Ø24.0 mm bore" (açık delik) diyor, ama bore'un içi optik ve AMOLED ile dolu | ORTA |
| M12 | AMOLED çerçevesi | Aktif alan Ø22.4, dış çap Ø23.2. Kenar başına **0.4 mm**. Yuvarlak AMOLED'de GOA ve kapsülleme için ≥ 1–1.5 mm gerekir | ORTA |

---

## 3 · Termal denetim

### 3.1 Güç bütçesi tahmini (belgede hiç güç bütçesi yok)

| Kaynak | Güç |
|---|---|
| U2: 60 GHz + Wi-Fi 7 | 1.5–3 W |
| U1 TCON | 0.5–1 W |
| 50 MP sensör @30 fps | 0.4–0.7 W |
| AMOLED + ses | 0.3–0.8 W |
| **Toplam (çalışırken)** | **≈ 3–5 W** |
| Ek: 40 W PD dönüşüm kaybı (%92 verimle) | **+≈ 3.2 W** |

### 3.2 Sıcaklık yükselmesi
**Modül yalıtılmış kabul edilirse:**
- Açık yüzey ≈ 1.2 × 10⁻³ m² (halka üstü 804 mm² + kenar 402 mm²).
- Isı transfer katsayısı h ≈ 16 W/m²K (konveksiyon + ışınım).
- ΔT ≈ 3 W / (16 × 1.2 × 10⁻³) ≈ **156 K**. İmkânsız; ağır termal kısma (throttling) kaçınılmaz.

**Isı ekrana akıtılırsa:**
- Gövdeye ısıl direnç ≈ 5–6 K/W (safir/PC arayüzü, 0.2 mm PC, OCA, grafen yayılma direnci ≈ 2.65 K/W).
- 3 W, **+15–18 K** eder. Ekranda yerel olarak ≈ **45–50 °C** sıcak nokta oluşur.
- Bu, 03'teki "**≤ 36.2 °C** göze güvenli" iddiasını doğrudan çiğner.
- OLED ömrü her 10 °C artışta yaklaşık yarıya iner. Sonuç: ekranda **dairesel yanma izi**.

### 3.3 Diğer termal hatalar
- **"Bariyer" aslında yayıcı.** Parça #3, 1200 W/m·K Cu-grafit için "thermal barrier" diyor. Yüksek iletkenlikli bir malzeme yalıtmaz, ısıyı yayar. Sensörün ısısını doğrudan altındaki AMOLED'e taşır. Bariyer isteniyorsa aerojel gibi düşük k'li bir malzeme gerekir.
- **Sensör karanlık akımı.** Karanlık akım her ≈ 6.5 °C'de ikiye katlanır. 25 °C'den 60 °C'ye çıkınca ≈ **42 kat** artar: sıcak pikseller ve renk gürültüsü.
- **SMA OIS.** SMA tellerinin çalışması için ≈ 70–90 °C'ye ısıtılıp Mf sıcaklığının altına soğuması gerekir. 50 °C'yi aşan kapalı bir halkada teller gevşeyemez ve OIS çalışmaz. Isı da doğrudan sensöre gider.
- **Grade-5 Ti çubuk.** k ≈ **6.7 W/m·K**, alüminyumun (167) yaklaşık 1/25'i. 40 W şarjın kaybı çubuğun içinde hapsolur.
- **LLZO/PEO köprü hücresi.** PEO'nun iletkenliği 25 °C'de ≈ 10⁻⁶ S/cm. Pratikte 60 °C civarında çalışması gerekir. 0.45 Wh ve 3 W yük ≈ **6.7C** eder; oda sıcaklığında bu akım çekilemez, verilse bile ≈ 9 dakika dayanır.
- **Sistem çapraz kontrolü.** 03'teki 12 Wh / 14.1 saat, sistemin ortalama **0.85 W** çektiği anlamına gelir. Yalnızca B modülü 3–5 W çekiyor. Gerçekçi pil ömrü ≈ **2–3 saat**.

---

## 4 · Akustik denetim

- **Arka hacim yok.** 4 mm'lik IP68 kapalı halkada arka hacim ≈ 0.05 cc kalır.
  - Hesap: k = ρc² · Sd² / Vb ≈ 640 N/m, hareketli kütle ≈ 20 mg.
  - Sonuç: rezonans **f₀ ≈ 0.9 kHz**, süspansiyonla **> 1.2 kHz**. Konuşmanın temel frekansları kaybolur.
  - "78 dB" için mesafe belirtilmemiş, dolayısıyla doğrulanamaz.
- **Senaryo B'de hoparlör sığmıyor.** Hoparlör **2.20 mm**, halkanın tamamı 2.00 mm.
- **Yankı ve titreşim.** Mikrofonlar ile hoparlör ≤ 25 mm arayla aynı alüminyum gövdede. Yapı yoluyla gelen yankı ve titreşim hem MEMS mikrofonlara hem OIS jiroskopuna ulaşır; görüntüde mikro titreme oluşur.
- **Tıkırtı.** Halka yalnızca çubuktan tutturulmuş, yani konsol durumda ve ekranın PC yüzeyi üzerinde yatıyor. Hoparlör tepkisiyle ses yapar.
- **Manyetik girişim.** Hoparlörün neodimyum mıknatısı, VCM'nin Hall sensörünün yakınında. Odak ve OIS konum hatasına yol açar.
- **IP68 membran kaybı.** ePTFE membran ≈ 1–3 dB kayıp ve ek akustik kütle getirir.

---

## 5 · Elektrik, RF ve kullanım hataları

- **USB-C fişi modülü söker (KRİTİK).** USB Type-C spesifikasyonunda takma kuvveti 5–20 N, çıkarma kuvveti 8–20 N. Manyetik tutma yalnızca **7.2 N**. Kablo takıldığında ya da çekildiğinde modül ekrandan kopar.
- **Menteşe flex'i yorulur.** Ø2.2 mm menteşe, R ≈ 1.1 mm bükülme yarıçapı demek. Gerinim ε = t / (2R) = 0.18 / 2.2 ≈ **%8.2**. Bakırın dinamik yorulma sınırı ≈ %0.2–0.3. "100 000 çevrim" imkânsız. IPC-2223 dinamik bükülme yarıçapı olarak ≈ 100 × t ≈ 18 mm önerir.
- **Çevrim ömürleri birbirini tutmuyor.** 05'te menteşe **50 000** çevrim, 13'te flex **100 000** çevrim.
- **60 GHz sinyali menteşeden geçiyor.**
  - Anten çubukta, U2 halkada. 60 GHz sinyal 16 mm'lik flex'ten geçmek zorunda: ≈ 3–6 dB kayıp.
  - λg ≈ 3.1 mm olduğundan 50 µm'lik yol farkı ≈ 6° faz hatası demek. Hüzme yönlendirme kalibrasyonu bozulur.
- **SAR yanlış metrik.** 6 GHz üzerinde maruziyet SAR (W/kg) ile değil, güç yoğunluğuyla (W/m²) ölçülür. "SAR 0.054 W/kg", 60 GHz için anlamsız.
- **Bant genişliği darboğazı.**
  - Ekran: 1592 x 3192 piksel × 24 bit × 144 Hz ≈ **17.6 Gbps**.
  - Kamera ham verisi: 50 MP × 10 bit × 30 fps ≈ **15 Gbps**.
  - "Zero-CPU" denildiği için modülde ISP yok, ham veri dışarı gitmek zorunda.
  - Tek bir 1x4 60 GHz bağlantı pratikte ≈ 4–8 Gbps taşır.
  - Görüntü verisi ayrıca 12 pogo pinin üzerinden geçecek. Ön/arka simetri yüzünden yalnızca 6 benzersiz pin var; buradan çok Gbps'lik sinyal geçirmek gerçekçi değil.
- **Pogo üzerinden güç.**
  - 40 W, 3.85 V'ta ≈ 10.4 A eder.
  - 6 güç/GND pinine dağıtılırsa pin başına ≈ 3.5 A düşer. Tipik pogo pin 1–2 A için tasarlanır.
  - Kayıp: I²R ≈ 0.22 W/pin, toplam ≈ **1.3 W**.
- **Mıknatısın tutunacağı yüzey yok.** Gövde kenarında ferromanyetik bir hedef tanımlı değil. N52H mıknatıslar Qi alanında da ısınır.
- **Safir PC'yi çizer.** Mohs 9 safir, oleofobik kaplamalı olsa da sertliği HB–2H olan PC ekran kabuğuna sürtünüyor. Araya kum girerse ekran kalıcı olarak çizilir.
- **Arka AMOLED ekrana bakıyor.** Arka AMOLED yığının en altında ve ana ekrana dönük, yani **kullanıcı onu göremez.** Gövdenin şeffaf olduğu da iddia ediliyor ama içinde Mu-metal ve kalın grafen ısı yayıcı var; bunlar opaktır. Bu da 03'teki "> %88 şeffaflık" iddiasıyla çelişir.
- **Halka ekranı kapatıyor.** Ø32 mm halka, 80 mm'lik ekran genişliğinin **%40'ını** kaplıyor (alanın %6.3'ü).
- **Flaş parlaması.** Flaş aynı Ø24 safir pencerenin altındaysa ışık pencere içinde TIR ile lense sızar. Optik bariyer tanımlı değil.
- **Modülsüz ekran kör.** 05 kural 5'e göre TCON B modülünde. Modül çıkarılınca ekran kararır.

---

## 6 · Kütle ve yoğunluk denetimi (fiziksel imkânsızlıklar)

| Parça | Hacim | Beklenen kütle | Listelenen | Örtük yoğunluk / sonuç |
|---|---|---|---|---|
| #6 mıknatıslar 8 × (3.2 x 1.6 x 1.1) | 45 mm³ | 0.34 g | **1.55 g** | **34 g/cm³**, osmiyumdan (22.6) bile ağır. İmkânsız |
| #15 pil 18 x 4.2 x 1.2 | 90.7 mm³ | ≈ 0.25 g | **1.20 g** | **13.2 g/cm³**, kurşundan ağır. Enerji yoğunluğu **4960 Wh/L**, en iyi Li-ion hücrenin (≈ 800 Wh/L) yaklaşık 6 katı |
| #21 sensör | 80 mm³ | 0.19–0.3 g | **0.85 g** | 10.6 g/cm³ |
| #14 halka gövde | Açık bore'lu tam dolu halka 1407 mm³ | 3.80 g | **4.50 g** | Bore gerçekten açıksa içi tamamen dolu metal halkadan bile ağır |
| #25 prizma | 15–30 mm³ | 0.08–0.15 g | **0.55 g** | 4–7 kat fazla |
| #32 / #1 safirler | 181 / 158 mm³ | 0.72 / 0.63 g | 0.45 / **0.20 g** | 1.6 ile 3.2 kat eksik |
| **BOM toplamı (13)** | | 32 kalemin toplamı **22.00 g** | 03/05 **20.0 g** diyor | Çelişki |
| **Gövde (03 §1)** | | 12.8 + 8.4 + 6.8 + 34.4 + 4.8 + 4.8 = **72.0 g** | **68.0 g** | Çelişki. Gerçek toplam 72 + 22 = **94 g**, iddia edilen 88 g |
| Gövde pilleri | 4 × 2.835 cm³ | 12 Wh / 11.34 cm³ = **1058 Wh/L** | **750 Wh/L** | İç tutarsızlık |
| PC kabuklar 8 × 40 x 80 x 0.2 | 5120 mm³ | 6.1 g | **12.8 g** | 2.1 kat fazla |

---

## 7 · Eski mimariden kalan ve yeni hedefle çelişen satırlar

Yeni hedef: halka 2.00 mm, `1.00 mm` yatay çubuk, menteşe yok.

### 03-PART-CATALOGUE.md
1. Başlık: "**`20.0 g` `90°`-bent-stem B module (`32` parts)**". Kütle 22.00 ile çelişiyor. "90° bükülü" ifadesi yatay çubukla, 32 parça sayısı menteşesiz mimariyle çelişiyor.
2. §2 madde 1: "stem `8.0 x 32.0 x 4.50 mm` is bent `90°`" ve "reversible `±90°` Grade-5 Titanium micro-hinge".
3. §2 madde 2: "live inside the `90°`-bent stem".
4. §2 madde 3: "Round ring `32.0 x 32.0 x 4.00 mm`, `Ø24.0 mm` bore".
5. §2 madde 4: "`20.0 g` B module = **`88.0 g` total**". Gerçek değerler 22 g ve 94 g.
6. Revizyon başlığı: "`88.0 g` total, `84` subparts". Menteşe çıkarılırsa 83 olur.

### 05-B-MODULE-CAMERA-AND-PANEL.md
1. Başlık ve giriş: "90°-BENT-STEM", "bends only ... stem at a `90°` right angle", "only the stem stays up along the screen edge".
2. Giriş: "`40.0 x 32.0 mm` plan silhouette". 13'teki "40 x 44" ile çelişiyor.
3. Kural 1: "reversible `±90°` Grade-5 Titanium micro-hinge (`Ø2.2 x 18.0 mm`)", "`8.0 x 32.0 x 4.50` stem stand perpendicular", "`32.0 x 32.0 x 4.00 mm` ring", "`z = +1.10..+5.10` / `-1.10..-5.10`".
4. Kural 2: "hooking the `90°`-bent stem".
5. Kural 3: "inside the `90°`-bent stem".
6. Kural 4: "`4.00 mm` thick", "upper stack `z = 0.90..4.00`", "lower stack `z = 0.00..0.90`", "`0.15 mm` Cu-graphite", "`0.35 mm` rear sapphire". Brief'teki 0.10 mm ve 0.36 mm ile çelişiyor.
7. Kural 6: "stem and ring 90-degree edges". Çubuk artık yatay; ifade gözden geçirilmeli.
8. Tablo, "Flat ring envelope": `32.0 x 32.0 x 4.00 mm`.
9. Tablo, "stem envelope": `8.0 x 32.0 x 4.50 mm`, "`±90°` Ti micro-hinge (`50 000` cycles)".
10. Tablo, "Sole USB-C ... in the `90°`-bent stem".
11. Tablo, "Front camera": "`5P` lens barrel (`z = 0.90..3.60 mm`)". Hem 2.00 mm hedefiyle hem namlunun Ø11.6 çapıyla çelişiyor.
12. Tablo, "Rear AMOLED": "`300 ppi`, `z = 0.35..0.75`". 480 piksel / 22.4 mm = **544 ppi**, 300 değil.
13. Tablo, son satır: "**`20.0 g` total mass**".

### 13-B-MODULE-PART-BY-PART.md
1. Başlık ve §1 girişi: "90°-BENT-STEM", "bent at a `90°` right angle".
2. §1 çubuk: "`8.0 x 32.0 x 4.50 mm`", "reversible `±90°` Grade-5 Titanium micro-hinge".
3. §1 halka: "`32.0 x 32.0 x 4.00 mm`".
4. §1 üst yığın `z = 0.90..4.00`; alt yığın `z = 0.00..0.90`, kalkan "`0.15 mm` (`z = 0.75..0.90`)", AMOLED `z = 0.35..0.75`, safir `z = 0.00..0.35`.
5. §2 başlığı: "(`22.00 g` total)". 03/05'teki 20.0 g ile çelişiyor.
6. #32: `z = 3.60..4.00`.
7. #31: bezel `Ø24.0 x 2.30`. Yüksekliği 2.00'den büyük.
8. #29: hoparlör `2.20`. 2.00'den büyük.
9. #24: namlu `Ø11.6 x 13.8`.
10. #21: `z = 0.90..1.55`.
11. #14: "`32.0 x 32.0 x 4.00`".
12. **#13: `±90°` Ti menteşe.** "Ek menteşe parçası yok" hedefinde bu satırın tamamen silinmesi gerekir.
13. **#12: "`±90°` stem bend" flex, `100 000` cycles.** Hem menteşesiz mimariyle çelişiyor hem de 05'teki 50 000 değeriyle.
14. #11: "`90°`-bent stem housing `8.0 x 32.0 x 4.50`".
15. #10: USB-C `3.10` mm, "inside `90°` B stem". 1.00 mm çubuğa sığmaz.
16. #8 ve #7: "in `90°` stem".
17. #6: mıknatıslar `1.1` mm, "in `90°` stem clip". 1.00 mm'den büyük.
18. #3: `Ø23.6 x 0.15`, `z = 0.75..0.90`.
19. #2: `Ø23.2 x 0.40`, `z = 0.35..0.75`.
20. #1: `0.35`, `z = 0.00..0.35`.
21. Toplam satırı: "`40 x 44 x 6.70 mm` bent", "`22.00 g`", "32 internal parts". Menteşesiz mimaride 31 parça olur.

### `HARDWARE/20` ve diğer dosyaları taramak için önerilen komut
```bash
grep -nE "4\.00 ?mm|4\.50|±90|micro-hinge|hinge|90°-bent|bent stem|20\.0 g|88\.0 g|22\.00 g|z = 0\.90|5\.10|0\.15 mm|0\.40|300 ppi|50 000|100 000" HARDWARE/*.md
```

---

## 8 · Sonuç ve düzeltme yolları

1. **2.00 mm halkada 50 MP / 1 inç / f/1.8 kamera imkânsız.** Lagrange sınırına göre 1.5 mm'lik yarıktan teoride bile en fazla H = 0.75 mm geçer; gereken 1.33 mm. Seçenekler:
   - (a) Sensörü **≤ 1/6"** sınıfına (≈ 0.3–2 MP) indirmek.
   - (b) Halkayı **≥ 10–11 mm** yapmak.
   - (c) Kamerayı ekran gövdesinin dışına almak.
2. **4.00 mm'de bile tavan ≈ 1/2.5" periskop.** Bu durumda f ve görüş açısı telefotoya kaydırılmalı ve **ikinci katlama** elemanı BOM'a eklenmeli.
3. **Termal:** Bir güç bütçesi yazılmalı, 1200 W/m·K'lik "bariyer" yerine gerçek bir yalıtkan kullanılmalı, Ti çubuktan ısı yolu tasarlanmalı.
4. **Yoğunluk ve kütle tablosu yeniden hesaplanmalı:** mıknatıs, pil, sensör, safir. Toplamlar 94 g'ye göre düzeltilmeli.
5. **USB-C ile 7.2 N mıknatıs uyumsuz.** Ya mekanik bir kilit gerekir ya da USB-C'nin halkaya taşınması.
6. **Belgeler eski mimaride.** 03, 05 ve 13'teki **40'tan fazla satır** hâlâ eski 4.00 / 4.50 / ±90° menteşe mimarisini anlatıyor. Bölüm 7'deki liste düzeltme listesi olarak kullanılabilir. Ayrıca 2.00 mm halka mimarisi bu dosyalarda hiç tanımlanmamış; önce o tanımın yazılması gerekiyor.


---

## DALGA 5 · SIFIR-CPU AĞ MİMARİSİ, `FINAL/00..20` ANA DİREKTİF, PAFTALAR VE `RG-1..RG-17` AR-GE PROTOKOL HATALARI (`FINAL/00..20`, `pafta/`, `MASTER/`)

### W5_A3_SONNET_PAFTA_AND_MASTER_AUDIT · Model: `claude-sonnet-5-5` (Router: `coding-router-preview`, Başlangıç: `2026-10-12 15:04:17 +03`, Bitiş: `2026-10-12 15:10:50 +03`, Süre: `392.32 sn`, Uzunluk: `25,785` karakter)

# BUDLUM LEAF · Pafta ve MASTER Denetimi (Rev L.5.0)

**Kapsam ve sınırlar.** Bu denetim yalnızca verilen metne dayanır. Dört scriptin ve `STATE.md`'nin "ORTA KISIM KISALTILDI" bölümleri görünmüyor. Bu yüzden `sheet_e01`, `sheet_e02`, `sheet_p12`, `sheet_p22` ile `sheet_p21` panel A/B'nin koordinat gövdelerini okuyamadım. Orada yalnızca başlık, yorum ve etiketlerden çıkarım yapabildim. Okuyabildiğim kod ve metindeki bulguları kesin, görünmeyen kısımlara dair olanları "doğrulanamadı" diye işaretledim.

Bir not: `make_l3_sheets.py` içinde `d = "M " + " L ".jo` satırı kesik görünüyor. Metin kesilirken bozulmuş olabilir. Dosyada gerçekten böyleyse `AttributeError` verir ve `E01` hiç üretilmez.

---

## 1 · Özet: gate'ler geçiyor ama paftalar iç tutarsız

`OVER 0, COVERED 0, COLLIDE 0` yalnızca sözdizimsel ve piksel düzeyinde bir kontrol. Aşağıdakileri **yakalamaz**:

- Anlam çelişkileri.
- Boyut çelişkileri.
- Fizik ihlalleri.

En ağır sorunlar şunlar:

| # | Şiddet | Sorun |
|---|---|---|
| 1 | KRİTİK | **1.00 mm çubuğa USB-C sığmaz.** Alıcı gövdesi 3.2 mm yüksekliğinde, çubuk 1.00 mm. |
| 2 | KRİTİK | **Mimari ikiye bölünmüş.** E02/E03/P14/P15 "çubuk dik yukarıda + ±90° Ti menteşe" diyor. P21/P22/STATE "çubuk yatay + sıfır menteşe parçası" diyor. |
| 3 | KRİTİK | **P11 katman toplamı 2.00 mm değil.** Etiketler 2.20 mm, koddaki sayısal değerler 2.48 mm ediyor. |
| 4 | KRİTİK | **Kamera yolu 4.00 mm halkaya sığmaz.** 7.6 × 7.6 mm prizma ve 12.8 mm sensör yolu 4 mm içinde yer bulamaz. |
| 5 | KRİTİK | **Termal ve elektrokimyasal iddialar tutmuyor.** ≤36.2 °C, PEO elektrolit ve 15–25 W Qi2 birlikte çalışmaz. |
| 6 | YÜKSEK | Paftalarda "6.4 × 44.0 × 4.5", "1.5 × 22 × 4.0 titanyum menteşe" ve "Grade-5 Titanyum Artı Göbek" gibi eski mimari kalıntıları var. |

---

## 2 · Soru 1: Eski mimariden kalan ifadeler

### 2.1 Doğrudan kalıntılar

| Yer | Metin | Neden eski mimari |
|---|---|---|
| `make_l3_sheets` başlık yorumu (E02) | "±90° reversible Ti hinge", "90° L-stem" | L.5.0 kararı "ek menteşe bloğu yok, boşluktan büküm". |
| `make_l3_sheets` E02/E03 yorumları | "round ring ON screen", "only stem above edge" | Çubuk "yukarıda dik" olarak tarif ediliyor. P21'de çubuk "yatay" ve kenar üstünde. |
| `make_l3c` STACK `"17"` | "±90° tersinir Grade-5 Titanyum boyun menteşesi" | **titanyum menteşe**. Parça P21'de yok. |
| `make_l3c` TABLE_A `"17"` | "±90° titanyum menteşe · 1.5 x 22.0 x 4.0 · 1.2 g" | Aynı. |
| `make_l3c` TABLE_A `"16"` | "90° dik bükümlü çubuk · **6.4 x 44.0 x 4.5**" | Eski kalın çubuk. STACK'te aynı parça 32.0 × 4.0 × 1.00. |
| `make_l3c` P15 C satırı | "±90° titanyum menteşe ile ön/arka ve 4 yöne takılır" | Aynı kalıntı. |
| `make_l3c` P15 D `MON-5` ve `MON-13..20` | "±90° menteşe", "50.000 çevrim menteşe" | P21 kapısı: "ek parçasız". Menteşe çevrim kapısı anlamsız. |
| `make_l3c` P15 D `MON-1..2` | "Sadece çubuğu 90° dik bükülen" | P21'de "boşluktan, ters çevrilip, yatay". |
| `make_l3b` P13 | "Merkez (0,0) **Grade-5 Titanyum Artı (+) Göbek** + 12 µm optik dudak" | **titanyum göbek**. Gövde artık polikarbonat çeyrek karolar. |
| `make_l3b` P13 | "8 adet konik **Titanyum** mikro-kırlangıç pim" | STATE: "24 Nitinol/Ti-PEEK yapboz". Sayı ve malzeme farklı. |
| `make_l3b` P13 D | 15° / 30° / 60° eğimli üçgenler | Eski açı mimarisi. Bkz. 3.5. |
| `make_l3b` P11 başlığı | "**2.20 MM** 4-KARO…", "(**18 G** / KARO)" | Her yerde 2.00 mm ve 17 g (4×17 = 68 g). 4×18 = 72 g. |
| `make_l3b` P11 | "ön AgNW/ITO + **Corning** kenar-sarımlı" | Corning cam üreticisidir. Gövde cam değil PC. |
| `make_l3c` STACK `"18"`, `"16"` | "**32.0 x 32.0 x 4.00** halka", "32.0 x 4.0 x 1.00" çubuk | Halka dairesel (Ø32/Ø24), "32×32" kare gibi okunur. Çubuk boyu 32.0, 40.0 ve 44.0 diye üç farklı değerde geçiyor. |
| `make_l3c` TABLE_A `"28 mikrofo…"` | Parça no 28 = mikrofon | STACK'te 28 = **hoparlör**, 27 = mikrofon. Numara kaymış. |
| `make_l3c` yorumu, P14 | "all **32** parts" | STACK'te yalnızca **31** giriş var (31…1). 32. parça eksik. STATE de 32 diyor. |
| Dosya adları | `make_l3`, `l3b`, `l3c`, `l40` | Adlar eski sürümlerden kalma, hepsi "Rev L.5.0" üretiyor. İzlenebilirlik zayıf. |

### 2.2 Aynı büyüklüğün farklı değerleri (tek kaynak yok)

| Büyüklük | Değerler |
|---|---|
| Karo/gövde kalınlığı | 2.00 mm (STATE, P21/P22, P11 gövde metni), 2.20 mm (P11 başlık ve H2), 2.48 mm (P11 koddaki `t` toplamı) |
| Karo kütlesi | 17 g (STATE, P21/P22), 18 g (P11 H2) |
| Çubuk kalınlığı | 1.00 mm (P21, STACK 16), 4.0 mm (P15, "32x4x1" hattı), 4.5 mm (TABLE_A 16) |
| Çubuk boyu | 32.0 (STACK), 40.0 (b.png 2B ölçü), 44.0 (TABLE_A) |
| Çubuk genişliği | 4.0 (STACK), 6.4 (TABLE_A), USB-C yuvası 4.8 (TABLE_A) |
| Optik dudak / dikiş | 12 µm (P13), <15 µm (P21/P22/STATE), "<2.5 µm eşdüzlemlilik" (P13) |
| Yapboz kilit sayısı | 8 Ti pim (P13), 24 çift Nitinol/Ti-PEEK (STATE, P22 F-02) |
| Mıknatıs sayısı (gövde) | "24 N52H" etiketi, çizimde 8 dikdörtgen (`range(8)`) |
| Altın kontak | "64 mikro-yaprak" etiketi, çizimde tek `gd` şeridi |
| Çubuk yönü | "yukarıda dik" (E03, P15) ve "yatay, kenar üstünde" (P21, STATE) |
| Ekranın "üst kenarına takılma" | P21: sadece üst kenar. P13 D / E03: "4 kenar, ön/arka". |
| Kenar yumuşatma | B: r 0.55 mm, gövde: r 0.62 mm (STATE) |

---

## 3 · Fizik, geometri ve ölçek hataları

### 3.1 USB-C ve 1.00 mm çubuk (KRİTİK)

- USB-C alıcı gövdesi (TABLE_A 12): **4.8 × 8.8 × 3.2 mm**. Standart alıcı yaklaşık 8.94 × 3.26 mm. Fiş ağzı 8.34 × 2.56 mm.
- Çubuk kalınlığı 1.00 mm. Port **3.2 kat daha kalın**. Ağız yüksekliği 2.56 mm bile 1.00 mm'ye girmez.
- Hacim: çubuk 4.0 × 32.0 × 1.0 = **128 mm³**. USB-C tek başına 135 mm³ ve çubuktan büyük.
- Antenin (31.0 × 3.2 × 0.6 = 59.5 mm³) ve USB-C'nin toplamı 194 mm³. Bu, çubuk hacminin **%152'si**.
- Çubuğa ayrıca şunlar da sığmak zorunda: 1×4 60 GHz yama dizisi, RF eşleme ağı, LCP koaksiyel köprü, PD denetleyici ve 2.2 µH indüktör.
- Kütle: çubuk 2.6 g ve 128 mm³ ise yoğunluk **20.3 g/cm³**. Bu tungstenden (19.3) yoğun. 40 mm boy için 16.3 g/cm³ çıkar, yine imkânsız.
- 4.5 mm kalınlıkla (TABLE_A) yoğunluk makul çıkıyor (≈2.05 g/cm³). Yani **tablo eski kalın çubuğa göre kurulmuş**, STACK/P21 ise ince çubuğa. İkisi aynı sayfada duruyor.
- Fiş tarafı: takılı fişin gövdesi (8.25 × 4.5 mm civarı) 2.00 mm ekran kenarından da kalın. Kablo yatay bir çubuğa çıkıyorsa kenarın dışına taşar.

### 3.2 r 0.55 mm yuvarlatma 1.00 mm çubukta imkânsız

Kalınlık 1.00 mm iken iki yüz kenarında r = 0.55 mm yarıçap kullanılırsa 2 × 0.55 = **1.10 mm > 1.00 mm** olur. Tam yuvarlamanın üst sınırı r = 0.50 mm. STACK 16 ("r 0.55"), P15 C satırı ve MON-9 buna dayanıyor.

### 3.3 Çubuğun "2.00 mm kenara tam oturması" geometrik olarak tutmuyor

- Çubuk genişliği 4.0 mm (veya 6.4 mm), kenar kalınlığı 2.00 mm. Çubuk kenara "tam oturmaz", **2.0–4.4 mm taşar**.
- Düz bir b silüeti çubuğu halkayla aynı düzlemdedir. Çubuğu 90° büküp ekran **yüzeyinden dışarı** çevirirsiniz. Yatay şekilde kenar üstüne yatması için bükme ekseninin ve kenar normalinin ayrıca tanımlanması gerekir.
- P21 metni bunu tanımlamıyor. Çıkış: "bize bakan halka" ile "yatay çubuk" aynı anda var. Hangi eksen etrafında 90° olduğu belirsiz.
- "Boşluktan büküm" de sorunlu. Boşluk malzeme olmayan yer demek. Bükülen şey ya LCP koaksiyel köprü ya da ince bir boyun olmalı. Ama MON-9 "ek parça yok" diyor. Köprü malzemesi, bükme yarıçapı, sızdırmazlık ve güç/veri geçişi hiçbir yerde çizilmemiş.
- **Esnek köprü yorulması.** 50 µm LCP flex'in r = 0.55 mm yarıçapta gerinimi ε = t/(2R) = 0.05/1.1 ≈ **%4.5**. Bakır yorulma sınırı ~%0.3 civarı. MON-13..20'deki "50 000 çevrim" bu yarıçapta mümkün değil.
- Aynı köprüden 40 W VBUS ve DP 2.1 (UHBR10/20) yüksek hızlı çiftler geçiyor. 90° dar yarıçaplı büküm empedans süreksizliği yaratır. UHBR20 için bu fiilen kabul edilemez.

### 3.4 Kamera yolu 4.00 mm halkaya sığmaz (KRİTİK)

- Halka kalınlığı 4.00 mm. Arka yarı: Ø24 kapak 0.35 + OCA 0.025 + AMOLED/dokunma, yani P15'e göre z = 0…0.85 mm. Ön safir pencere 0.35 mm. PCB 0.6 mm ve EM kalkan 0.15 mm de var. Bu da kamera için **yaklaşık 2.4 mm dikey boşluk** bırakıyor (4.00 − 0.85 − 0.35 − 0.6 ≈ 2.2 mm, hesaba göre).
- Katlanmış optikte prizma 7.6 × 7.6 mm. Yani dikeyde **7.6 mm**, yaklaşık 3 kat fazla.
- "14.0 mm yatay yol" içinde sensör (12.8 mm) neredeyse tüm yolu kaplıyor. 5P lens ve OIS için ~1.2 mm kalıyor.
- 12.8 × 9.6 mm sensörün görüntü çemberi ≥16 mm. Son lens elemanı da ~10 mm çapında olmalı. 2.4 mm yüksekliğe sığmaz.
- Ø24.0 mm safir pencere, Ø24.0 mm iç delikle aynı çapta. **Oturma omzu ve yapıştırma payı yok.** ±0.03 mm toleransla pencere ya gevşek ya sıkışık olur. FKM sızdırmazlık için yer yok.
- PCB iç çapı Ø24.4 mm, halka deliği Ø24.0 mm. Radyal pay yalnızca **0.2 mm**. Bu payda 0.15 mm Cu-grafit kalkan, FKM conta ve ±0.03 mm tolerans birlikte sığmaz.
- Ø27.2 mm mıknatıs dairesi, 4 mm'lik halka duvarı (r 12…16 mm) içinde. Aynı bölgede 8 mıknatıs + 12 pogo + hoparlör (9.0 × 3.2) + 2 mikrofon + flaş + PCB var. Çevre uzunluğu yaklaşık 88 mm. Bu işlerin çoğu aynı halkada üst üste biniyor.

### 3.5 Kamera mı AMOLED mi: hangisi ekran önüne bakıyor?

- Halkanın bir yüzünde kamera, arka yüzünde AMOLED (Ø22.4) var. Mıknatıs ve pogo "ekran yüzeyine kenetlenen" parça 9/8, yani arka tarafta.
- Halka ekranın **önüne** takılırsa AMOLED ekrana bakar ve **görünmez**, kamera dışarı bakar. **Arkaya** takılırsa durum aynı kalır, kamera dünyaya bakar.
- AMOLED'in hiçbir takılış durumunda görünür olduğu gösterilmemiş. "Kamera dönmez" cümlesi (P15 D) bunu daha da netleştiriyor.
- Mıknatıs halkası ve pogo ekranın PC yüzeyine (200 µm) kenetleniyor. PC'nin arkasında T-OLED ve opak LLZO batarya var. Pogo'nun karşı kontak yeri yok. Karşı kontak varsa yüzeyde açık pad olur. Bu da "portsuz, düğmesiz, IP68, çiziksiz" ile çelişir.

### 3.6 P11: katman istifi ve çizim ölçeği

Kod katman kalınlıkları (`t`, µm): 220, 60, 160, 40, 60, **1400**, 60, 40, 160, 60, 220. **Toplam 2480 µm.**

Etiketlerdeki µm değerleri: 200, 50, 140, 40, 90, **1160**, 90, 40, 140, 50, 200. **Toplam 2200 µm.**

- Her iki toplam da hedef 2.00 mm'yi aşıyor. 11 katmanın 2.00 mm'ye sığdığı iddiası **doğrulanamıyor**.
- Kodda PDLC'nin `t`'si 60, etiketinde 90 µm. Merkez katman kodda 1400, etikette 1160.
- Çizim yüksekliği `max(t/1000*60, 17)` px. 60 px/mm ölçeğinde 200 µm ≈ 12 px olması gerekirken 17 px'e çıkıyor. 40 µm'lik katman 2.4 px yerine 17 px (**≈7× abartı**). Merkez 84 px. Toplam yaklaşık 254 px, gerçek ölçekte (2.48 mm) 149 px. Yani çizim **~1.7× şişirilmiş**.
- Yatayda X0..X1 = 490 px, 80 mm karşılığı. Bu 6.1 px/mm, dikey ölçek 60 px/mm, **~10× anizotropik**. Pafta üzerinde "ÖLÇEKSİZ / dikey abartılı" notu yok (görünen kısımda).
- Merkez katman gerçekçi değil. 1.16 mm × 40 × 80 mm = 3.71 cm³ ve 3.0 Wh için **808 Wh/L** gerekir. En iyi Li-ion cep hücreleri ~700 Wh/L, LLZO/PEO kompozitler çok daha düşük. Aynı katmanda Qi2 bobin + ferrit (0.1–0.3 mm) de var. Bobinden sonra pil kalınlığı 0.5–0.7 mm kalır ve enerji **yarıdan aza** düşer.
- Katman 4 "AgNW/ITO + Corning kenar sarımlı" PC üstünde anlamsız. Katman 5/7 "PDLC + grafen/Mu-metal" 90 µm içine sığmaz. PDLC iki ITO-PET taşıyıcı ister (tipik toplam 100–350 µm), Mu-metal de en az ~25 µm.
- T-OLED şeffaftır. Ama ortada opak LLZO batarya var. Şeffaf ekranın anlamı yok. "Gözlük vizörü" iddiası da bununla çelişiyor: batarya karoları opak.

### 3.7 R 25.5 mm esneme: gerinim ve çizim çelişkisi

- 2.00 mm kalınlıkta nötr eksenden yüze uzaklık 1.00 mm. ε = 1.00/25.5 = **%3.9**. Pafta "%0.38 gerinim" diyor.
- %0.38, yalnızca yaklaşık **0.194 mm** kalınlığındaki tek bir film için tutar (200 µm PC). Katmanlar kayarak ayrışırsa ince filmler için doğru olabilir.
- Ama merkez LLZO katmanı tek parça 1.16 mm. Yüz gerinimi: 0.58/25.5 = **%2.3**. LLZO seramiğin kırılma gerinimi ~%0.1. Yani yaklaşık 20× aşım.
- ITO çatlama gerinimi ~%0.5–1, T-OLED ince film kapsülleme ~%0.3–0.5. İnce katmanlar kayma katmanıyla kurtulur, ama seramik batarya ve bobin kurtulamaz.
- Çizim (P13 C): `M 110 850 C 160 690 360 690 410 850`, kalınlık `stroke-width=10`. 2.00 mm = 10 px varsa 5 px/mm olur. Eğrinin kirişi 300 px = **60 mm**. Etiket "R 25.5 mm" için çapı 51 mm, yani **çap < kiriş**. Böyle bir daire çizilemez.
- Çizilen eğrinin gerçek yarıçapı yaklaşık 154 px ≈ 30.8 mm, etiketten %20 fazla.
- 160 mm uzun kenar R 25.5 mm'ye sarılırsa tam bir tüp olur (çevre ≈ 160.2 mm). "Gözlük vizörü" olarak makul değil.

### 3.8 Termal: ≤36.2 °C ve Qi2 uyumsuz

- Alan: 80 × 160 mm iki yüz = 0.0256 m². Doğal taşınım + ışıma h ≈ 10–11 W/m²K.
- Qi2 25 W, verim %75: toplam kayıp 6.25 W. Alıcı tarafına düşen yarısı ≈ 3 W olsa bile ΔT = 3/(11 × 0.0256) ≈ 10.6 K. 25 °C ortamda 35.6 °C.
- Şarj pedi bir yüzü kapatır, alan yarıya iner: ΔT ≈ **21 K**, yani ≈46 °C. 30 °C ortamda sınır zaten aşılır.
- 36.2 °C NTC kesme sınırı, kablosuz şarjda sürekli tetiklenir.
- B modülü: halka iki yüz ≈ 0.0016 m², çubuk ihmal edilebilir. 1 W kayıp için ΔT ≈ 1/(10 × 0.0032) ≈ **31 K**. 3 W için ~90 K. 50 MP ISP, OIS, 60 GHz TX, TCON, 40 W PD, hoparlör ve AMOLED aynı 20 g'lık gövdede. Isı yayma yolu yok: PC k ≈ 0.2 W/mK.
- LLZO/PEO: PEO bazlı katı elektrolit 25–36 °C'de ~10⁻⁶–10⁻⁵ S/cm, iyi iletkenlik için 60–80 °C ister. **≤36.2 °C sınırında batarya çalışmaz.**
- 12 Wh'ı 25 W ile doldurmak = **2.1C**, 40 W PD = **3.3C**. Katı hal LLZO/PEO için gerçekçi değil, özellikle 36 °C altında (≲0.2–0.5C).

### 3.9 Qi2 bobin ve metal katmanlar

- Ø54 mm Qi2.2 bobinin önünde ve arkasında **grafen/Mu-metal** kalkan katmanları var. İletken tabaka, 127 kHz'de alan akısını keser ve girdap akımı kaybı yapar. Qi2'nin ferrit arkalığı gerekir, bunun yeri tarif edilmiyor.
- P13'teki **Grade-5 Titanyum Artı Göbek** bobinin tam merkezinde. Ti özdirenci ≈ 0.42 µΩ·m, 127 kHz'de skin derinliği δ = √(ρ/(π f µ₀)) ≈ **0.92 mm**. Göbek kalınlığı bu mertebede, yani ciddi ısınma ve akı kaybı yaratır. Bu kalıntı hem mimari hem fizik hatası.
- Ø54 mm bobin dört karoya yayılıyor (merkezden her yöne 27 mm). Her karo kendi Ø22 mm bobinini de taşıyor. İkisi aynı katmanda ve üst üste biniyor.
- Karolardan biri çıkarılırsa Ø54 mm bobin kırılır. E03: "3 karo çalışırken 1 karo hot-swap" ile bu bir arada tutmuyor. Üç karoyla merkez bobin da şarj sağlayamaz.
- Ø22 mm bobin Qi alıcı bobin için küçük. Qi referans alıcılar ≥30–40 mm. Tekil karo şarjı için 5 W gerçekçi değil.
- Qi2 mıknatıs dizisi gerekir. Pafta ayrı N52H sayıları veriyor (24 etiket, 8 çizim).

### 3.10 Dikiş, optik ve toleranslar

- **n = 1.585 elastomer.** Optik silikonlar tipik 1.41–1.57. 1.585 yumuşak bir elastomer için ticari değil.
- Fresnel: R = (Δn/2n̄)². %0.0001 = 10⁻⁶ için Δn < **0.0032**. PC Abbe sayısı ≈ 30, nF−nC ≈ 0.0195. Elastomer V ≈ 50 olsa dispersiyon farkı 0.0078. Görünür bantta uçlarda R ≈ 1.5 × 10⁻⁶ (%0.00015), iddianın biraz üstü. dn/dT: PC ≈ −10⁻⁴/K, silikon ≈ −3×10⁻⁴/K. 10 K'de ek Δn ≈ 0.002. Marj yok.
- **CTE.** PC ≈ 65–70 ppm/K, Ti ≈ 8.6 ppm/K. 40 mm karo, ΔT = 20 K: 40 × 67×10⁻⁶ × 20 ≈ **54 µm**. "<15 µm dikiş" ve "<2.5 µm eşdüzlemlilik" bu sıcaklık aralığında tutmaz. Üstelik parça toleransları ±0.03 mm (TABLE_A) = ±30 µm. Dikiş boşluğu parça toleransından küçük olamaz.
- **Çiziksiz.** Başlıklar "zero-scratch" diyor. PC üzerinde SiO₂ sert kaplama ile yüzey sertliği Mohs 7 olan toza karşı çizilmeyi sıfırlamaz. Pafta "dikişte çizik yok" mu "yüzeyde çizik yok" mu demek istediğini ayırmıyor.
- **IP68 ve 3 saniyede aletsiz tak-çıkar** aynı anda: dişsiz bir kenar konnektör arayüzü, açık altın kontaklar ve 15 kPa (1.5 m) basınç. 64 altın kontak enerjili ve terde/tuzlu suda galvanik/elektroliz riski taşıyor. Sökülmüş karo da IP68 olamaz.
- **Hot-swap.** Çalışırken bir çeyrek ekran kaybolur, TCON 4 karoyu sürüyor. Güç alanı ve görüntü kesintisi tarif edilmemiş.

### 3.11 Elektrik ve RF

- **"40 W PD 3.1 EPR"** (STACK 10, 12): PD 3.1 EPR en az 28 V × 5 A = **140 W**'tır. 40 W (20 V × 2 A) SPR'dir (PD 3.0 sınıfı). Etiket yanlış.
- **DP 2.1** (UHBR10/20) için 4 şerit, retimer ve empedans kontrolü gerekir. 4 mm genişlik, 1 mm kalınlık ve 31 mm anten aynı alanda. 90° bükümlü flex.
- **"SAR 0.054 W/kg" 60 GHz için geçersiz.** 6 GHz üstünde (ICNIRP: 6–300 GHz) soğurulan güç yoğunluğu (W/m²) kullanılır, SAR değil. "37× güvenli" = 2.0/0.054 = 37.0 (ICNIRP 10 g). FCC 1.6 W/kg için 29.6×.
- **3-bant LCP anten** (Wi-Fi 7, BT, UWB) 3.2 mm genişlikte, N52H mıknatıs halkası, Ti menteşe ve Cu-grafit kalkana bitişik. Uyumsuzluk (detuning) ve verim kaybı yüksek.
- **N52H mıknatıslar** hem OIS bobin aktüatörlerini (4 eksen ses bobini) hem Mu-metal kalkanı etkiler. Mu-metal yerel doyuma gidebilir. Pafta dış mıknatısı OIS ile birlikte ele almıyor.
- **"Zero-CPU".** Uygulama CPU'su olmadan görüntü, kamera ve ses akışı nasıl çalışıyor? 50 MP ham veri (50 Mpx × 10 bit × 30 fps ≈ 15 Gb/s) 12 pogo üzerinden geçecek. Hiçbir paftada "kimin hesapladığı" gösterilmiyor.
- **B modülü ≈ 20 g + gövde 68 g = 88 g** gözlük gibi burunda taşınmak için ağır (tipik gözlük 30–50 g).

### 3.12 P13 D: yön diyagramı 90° iddiasıyla çelişiyor

```
M x 800 L x+100 800 L x+100 (800 − a*2) Z      a ∈ {15, 30, 60}
```

- Çizilen eğimler: atan(30/100) = **16.7°**, atan(60/100) = **31.0°**, atan(120/100) = **50.2°**. Etiketler 15/30/60, çizim ise gerçek açıyı bile tutturmuyor.
- Asıl sorun şu: bunlar **rampa/kama** çizimleri. Paftanın iddiası "90° dik büküm, ön/arka, 4 kenar". 90° gösteren bir çizim yok. Kullanıcı bunu eğik takılan bir modül diye okur.
- "Sol/Sağ Yana" etiketi 60° rampa olarak çizilmiş. P21 ise yalnızca "üst kenar" diyor.

### 3.13 Çizim ölçeği (P14/P15)

- P14 STACK üçüncü alanı (52, 68, 34, 56 …) çizilen yükseklik ise: 0.025 mm OCA (parça 3) 52 px, 4.00 mm halka (parça 18) 72 px. Orantı yok. Sayılar satır aralığıysa sorun değil, ama pafta bunu belirtmiyor.
- P15 kesit dikdörtgenleri: lens 24 px, OIS 20, **Cu-Grafit kalkan 14 px (gerçek 0.15 mm)**, **CMOS 18 px (gerçek 0.65 mm)**. Kalkan sensörün %78'i kadar çizilmiş (gerçekte %23). Kalkan genişliği 40 px, sensör 48 px. Yani kalkan, koruduğu sensörden **dar**. Toplam dikey yığın 76 px; 4.00 mm halka bu ölçekte yaklaşık 15 px tutar. Çizim halkadan ~5× büyük.

### 3.14 Çizelge kalitesi: görünür sorunlar

- P13: `"iç + barasına"` yazım hatası ("bara"). İki ayrı sayı satırı da tutarsız: "24 mıknatıs" etiketi / 8 çizim.
- P11: `&lt;415 nm` gibi kaçışlar önceden yapılmış. Aynı metin `lines()` içinden geçerse `&amp;lt;` olur ve ekranda "&lt;" yazısı görünür. Bu `STACK`'teki `&amp;` için de geçerli. Dosyalarda iki farklı kaçış yolu var (elle `&lt;` ve `lines()` içindeki otomatik). Karışırsa çift kaçış riski var.
- `lines()` yalnızca karakter sayısına göre sarar, yazı tipi ölçülmüyor. Helvetica yoksa fallback fontlar (DejaVu) %10–15 daha geniştir.

---

## 4 · Çapraz dosya çelişkileri (STATE ↔ paftalar)

| Konu | STATE | Paftalar |
|---|---|---|
| Menteşe | "ek menteşe parçası yok" (özet), P21 "zero extra hinge blocks" | STACK 17, TABLE_A 17, MON-5, MON-13..20 |
| Çubuk yönü | "yatay, 1.00 mm" | E02/E03/P15: "yukarıda dik" |
| Takılış | "üst kenar" (P21) | "4 yön, ön/arka" (P13 D, E03, P15) |
| Parça sayısı | 32 | P14 STACK = 31 |
| Karo kütlesi | 17 g | P11 H2 18 g |
| Kalınlık | 2.00 mm | P11 2.20 mm (başlık) |
| Kapı sayısı | "251 gate" | Tablodaki aralıklar: MEC 38 + B 10 + ENR 21 + DSP 16 + CLR 11 + FLD 6 + CAM 20 + MON 20 + RL 18 + RF 20 + SW 19 + DST 10 + DUO 7 + SZ 5 + PRG 16 + RG 17 = **254**. Üstüne F-01..F-10 (10 kapı) tabloda yok, hepsi sayılırsa 264. |
| P14..P22 tarifi | "P14..P22 part-by-part" | P21/P22 birincil sayfa. P16..P20 bu girdide görünmüyor, denetlenemedi. |
| "MASTER/00..18" | (STATE'te yok) | STATE `FINAL/00..20` ve `HARDWARE/00..20` diyor. MASTER dizini tanımsız. |
| Dikiş | "<15 µm" | P13 "12 µm", "<2.5 µm" |
| Yapboz | 24 Nitinol/Ti-PEEK, 10 N/mm | P13: 8 Ti mikro-kırlangıç |

Ek notlar:

- **2022/2380 "tam karşılar" iddiası.** Direktif cihazın kendisinde USB-C alıcısı arar. Kutudaki ayrı modülün karşılayıp karşılamadığı hukuki yoruma açık. Pafta bunu kesin cümleyle yazmamalı.
- **AB 2023/1542 Md. 11.** Su/nem istisnaları ve "ısısız, çözücüsüz" koşulu için pafta bir dayanak vermiyor. IP68 ile aletsiz çıkarma birlikte iddia ediliyor.
- **`corner_cut(80.0)` + `outline(160, 80, c, 0)`.** Bu `leaf_geom` çağrıları eski yaprak kontürünün parçaları. "R = 6.35 mm" yorumu ile `corner_cut(80.0)` arasındaki ilişki doğrulanmadı. 80 mm girdi olarak R 6.35 mm yay üretmiyor olabilir.
- **IoU = 0.999987.** Raster `Group 911.png` ile böyle bir hassasiyet gerçekçi değil. Ölçüm yöntemi yazılmalı.

---

## 5 · Script ve araç hataları

1. **Kodlama.** `open(..., "w")` kodlama belirtmiyor. Windows'ta cp1252/cp1254 ile "ş, ğ, İ, µ, Ø, °" yazılırken `UnicodeEncodeError` olabilir. `encoding="utf-8"` zorunlu olmalı. `make_l3_sheets`'te `open(...).write(...)` dosyayı kapatmıyor, `with` kullanılmalı.
2. **XML başlığı yok.** SVG'de `<?xml ... encoding="UTF-8"?>` yok. Bazı araçlar Türkçe karakterleri yanlış okur.
3. **Paketler arası bağımlılık.** `make_l3b` ve `make_l3c`, `make_l3_sheets`'ten `head, lines` içe aktarıyor. L3 değişince hepsi etkilenir. Ortak bir `sheet_common.py` olmalı.
4. **Semantik gate yok.** `check_crossrefs.py` + `canon.json` yalnızca "sayım" kontrolü yapıyor. "2.20 mm", "18 g", "6.4 x 44.0 x 4.5", "titanyum menteşe", "Titanyum Artı Göbek", "4.00 mm halka" gibi kalıntıları yakalamıyor.
5. `ML` ve `math` içe aktarımları bazı dosyalarda görünürde kullanılmıyor (görünen kısımlarda).
6. **`multi_agent_optimize.py`.** STATE'e göre CAD, Pafta, Hardware ve QA ajanlarını koordine ediyor ve bu kadar çok revizyon kalıntısı bırakıyorsa, ajanların bir tek-kaynak (single source of truth) sözlüğüne bağlanması gerekir. Şu an her script kendi sabitlerini taşıyor.

---

## 6 · Soru 2: kesit çizimlerinde yanlış anlaşılabilecek veya ölçek dışı detaylar

| Pafta | Sorun | Kullanıcı/üretici ne anlar |
|---|---|---|
| **E02** (B kesit) | Başlıkta "±90° Ti hinge", "L-stem". Gövdesi görünmüyor ama etiketler 4.00 mm halka ve 1.00 mm çubuğu birlikte veriyor. | Üretici menteşe bloğu ve 4 mm çubuk çizer. P21 ise bunları kaldırmış. |
| **P11** | Katman yüksekliği ≥17 px zorlaması (7× abartı), 10× anizotropik ölçek, etiket/kod toplamı 2.20 / 2.48 mm. | Üretici katmanların eşit kalınlıkta olduğunu, toplamın 2.00 mm'ye uyduğunu sanar. |
| **P14** | 31 parça, 32 denilmiş. Parça 28/27 numaraları tabloyla kaymış. TABLE_A 6.4 × 44.0 × 4.5 çubuk ve titanyum menteşe satırları. | Satınalma yanlış parça numarasını ve eski çubuğu sipariş eder. |
| **P15** | Kalkan/sensör kalınlık oranı bozuk, kalkan sensörden dar. 4 mm halkaya sığmayan 7.6 mm prizma. | Optik kesit yanlış. Kamera mühendisi 4 mm'ye sığmayacağını fark etmeden çizimi onaylar. |
| **P13 C** | Yarıçap R 25.5 mm etiketi, ama kiriş 60 mm (çap 51 mm). Eğri R ≈ 30.8 mm. | R 25.5 mm'ye esneyebilme sınırı yanlış kodlanır. |
| **P13 D** | 15/30/60° kamalar, 90° iddiası, 16.7°/31°/50° çizim. | Modülün eğik takıldığı sanılır. |
| **P13 B** | "24 N52H" etiketi, çizimde 8 dikdörtgen. "64 kontak", tek şerit. Ti göbek. | Mıknatıs ve kontak sayısı çizimden okunursa üçte bir eksik üretilir. |
| **P21** (A/B görünmüyor) | Metin: "2.00 mm kenara tam oturur" ama çubuk 4–6.4 mm geniş, USB-C 3.2 mm. "Ters çevirip boşluktan bükme" eksensiz tarif. | Üretici eksiksiz bir bükme tarifi bulamaz. |
| **P22** (görünmüyor) | R = 6.35 mm, 68 g, 12 Wh, <15 µm dikiş iddiaları var. Yukarıdaki çelişkiler (3.6–3.10) buraya da taşınıyor. | Aynı. |

**Sheet'lerin doğrulanamayan kısmı için kontrol listesi** (E01, E02, P12, P21 A/B, P22 gövdeleri):

- 1.00 mm çubuk ile 3.2 mm USB-C aynı ölçekte çizilmiş mi?
- 2.00 mm ekran kenarı ile 4.0 mm çubuk genişliği aynı ölçekte mi?
- Ø32/Ø24 halka, çubuk ve ekran aynı px/mm ile mi çizilmiş? "ÖLÇEKSİZ" notu var mı?
- Boşluk büküm yarıçapı, menteşesiz iddia ile birlikte çizilmiş mi?

---

## 7 · Öncelikli düzeltme listesi

1. **Karar ver:** USB-C 1.00 mm çubukta kalacaksa port kalınlığı ≥ 3.3 mm olan bir muhafaza (çubukta lokal kalınlaşma) kabul et ya da USB-C'yi halkaya taşı. Paftalardaki "1.00 mm" çubuk iddiasını buna göre değiştir.
2. **Menteşeyi tek karara bağla.** P14/P15/E02/E03'ten parça 17, TABLE_A 17, MON-5, MON-13..20 menteşe ifadelerini çıkar veya P21'e menteşeyi geri koy.
3. **Çubuk geometrisini tek tabloya indir:** boy (40.0?), genişlik, kalınlık, yön (yatay/dik), bükme ekseni, köprü malzemesi ve bükme yarıçapı. r 0.55 mm yerine ≤0.45 mm kullan.
4. **P11 katman tablosunu düzelt.** Kod `t` değerleri ile etiket µm değerleri aynı olsun, toplam gerçekten 2.00 mm olsun. Başlıklardaki 2.20 mm ve 18 g'ı 2.00 mm ve 17 g yap. Dikey ölçek abartısı için not ekle.
5. **Kamera kesitini yeniden boyutlandır:** ya halka kalınlığı ≥ 8–9 mm olsun ya da sensörü/optiği küçült (örn. 1/2.55" sensör, ≤4 mm toplam yükseklik).
6. **Termal ve batarya iddialarını yeniden yaz.** ≤36.2 °C ile PEO elektrolit birbirini dışlıyor. Qi2 25 W şarj için termal bütçe hesabı ekle.
7. **Dikiş toleransı.** "<15 µm", "12 µm", "<2.5 µm" yerine tek bir değer ve CTE hesabı koy.
8. **Mimari kalıntıları temizle:** "Titanyum Artı Göbek", "8 Ti pim", "15/30/60°" rampaları, "Corning", 6.4 × 44.0 × 4.5, 1.5 × 22.0 × 4.0.
9. **SAR yerine 60 GHz için güç yoğunluğu (W/m²)** ver.
10. **"PD 3.1 EPR" etiketini kaldır** veya gücü 140 W'a çıkar.
11. **Kod:** `encoding="utf-8"`, `with open`, XML başlığı, ortak sabitler modülü, `.jo` satırı kontrolü.
12. **Yeni semantik gate:** yasaklı ifade listesi (regex), tek-kaynak boyut sözlüğü ve P14 parça sayısı (31 ≠ 32) kontrolü. `canon.json`'a boyutlar da girsin.

**Sonuç.** Bu sürümdeki paftalar, kendi başlarına geçerli `OVER/COVERED/COLLIDE` gate'ini sağlıyor. Ama üretime verilirse çubuk geometrisi, USB-C yerleşimi, kamera yığını ve termal/elektrokimyasal iddialar üretici tarafından "yapılamaz" diye geri döner. Önce 1–5 numaralı maddeler çözülmeden P21/P22'nin 20 g, 68 g ve 12 Wh sayıları da güvenilir kabul edilemez.

### W5_A1_OPUS_ZERO_CPU_NETWORK_AND_LATENCY_AUDIT · Model: `claude-opus-5-5` (Router: `exo`, Başlangıç: `2026-10-12 15:04:12 +03`, Bitiş: `2026-10-12 15:11:09 +03`, Süre: `416.54 sn`, Uzunluk: `37,239` karakter)

# BUDLUM LEAF: Dağıtık Sistem, Protokol, Gecikme ve RF Denetimi

**İncelenen dosyalar:** `BUDLUM-LEAF-ARGE-PLAN.md` (Rev. L.5.0), `FINAL/05`, `FINAL/08`, `FINAL/09`, `FINAL/10`

**Okuma kapsamı:** Dosyaların bazı orta bölümleri kısaltılmış geldi. `U1` (Quad-Tile TCON), `U2` çip listesi, `RG-4` için "500 ms ile 3 s" ve `Q4` karo tanımı elimdeki metinde doğrudan görünmüyor. Bu öğeleri sizin verdiğiniz bilgi olarak kabul ettim. Metinde kendim doğrulayabildiğim bulguları **[DOĞRULANDI]** ile, sizin bilginize dayananları **[ÖNCÜL]** ile işaretledim.

---

## 0 · Özet: kritik bulgular

| # | Bulgu | Şiddet | Kaynak |
|---|---|---|---|
| K1 | Cihazda hücresel radyo yok. Bu yüzden dışarıda, araçta ve uydu üzerinden oturum kurulamıyor. `05` ise 5G'yi "dış mekânda ana yol" olarak tanımlıyor. | **Ürünü durduran** | 05 §5.1 ile §5.2.4 çelişiyor **[DOĞRULANDI]**, U2 **[ÖNCÜL]** |
| K2 | Kapalı-portal (captive portal) çıkmazı: Portal sayfasını açacak tarayıcı uzaktaki validator'da. Validator'a ulaşmak için de önce portalı geçmek gerekiyor. | **Ürünü durduran** | 09 §9.1, 10 §10.7 |
| K3 | `choose()` işlevi boş aday kümesinde tanımsız davranıyor. Dosyadaki biçimiyle panic, statik havuzlu firmware'de ise reset ve boot döngüsü demek. | Kritik | 08 §8.3 |
| K4 | Devam jetonu (resume token) "tek kullanımlık ve tek adlı operatöre" bağlı. Bu haliyle planlanmamış devirde B'nin oturumu devralması **imkânsız**. | Kritik | 09 §9.3 |
| K5 | Yerel eko girdiyi yalnızca gösteriyor, girdinin dayanıklılığını garanti etmiyor. A çökerse "eko yapıldı ama kalıcılaşmadı" girdiler kaybolur ya da yanlış hedefe uygulanır. | Kritik | 08 §8.6.4, 09 §9.3 |
| K6 | Karo çıkarma ile anten toprağı ve güç yolu aynı anda değişiyor. Karo çıkarılınca bağlantı kopabilir ve voltaj çökmesi reset'e yol açabilir. | Kritik | 05 §5.2.3, ARGE P3 |
| K7 | Panel etiketleri (`R10/RG-16`) çıkarılan karonun üzerinde kalırsa değişmez kural ihlal edilir. | Yüksek | 08 §8.6.3 |
| K8 | `R = 25.5 mm`'de 160 mm'lik gövde **tam bir silindir** oluyor (2π·25.5 = 160.2 mm). Üst kenardaki anten alt kenara ya da bileğe yaslanır. | Yüksek | 05 §5.2.1 |
| K9 | "Zero-CPU" iddiası teknik olarak yanlış: firmware'de dört görev, 1 GB bellek, Rust crate'leri ve gömülü çekirdekli radyolar var. Bu, D7 dürüstlük kuralını da ihlal ediyor. | Yüksek (dürüstlük) | 08 §8.1 |
| K10 | Gecikme tablosu kendi içinde tutarsız. Yerel olması gereken "girdiden göze" süresi mesafeyle artıyor (uyduda 25–60 ms). | Yüksek | 10 §10.1 ile §10.4 |
| K11 | "Sıfır rijit bölge" kuralı ile çelik karo, metal omurga, prizma çerçevesi ve perimetre çerçevesi aynı belge setinde çelişiyor. Bobin hem kaldırılmış hem de Qi2.2 olarak duruyor. | Yüksek | ARGE §0 ile 05 §5.3 ve RF-10 |

---

## 1 · SORU 1: Hücresel modem yoksa sokakta ve arabada nasıl bağlanılacak?

### 1.1 Belgelerin kendi içindeki çelişki [DOĞRULANDI]

- `05 §5.1`: "5G, standalone, sub-6 GHz, 4×4 MIMO… **the main path outdoors**."
- `05 §5.1`: "Satellite, non-terrestrial **through the cellular radio**, no extra antenna."
- `05 §5.2.4`: "The upright B bar houses **Wi-Fi 7, BT 5.4, and UWB**." Bu listede 5G yok.
- `05 §5.2.2`: "**Every antenna stays in the upright B bar and perimeter frame**."
- `08 §8.3`: `PathCandidate.kind` içinde `Cell` ve `Satellite` var.
- `09 RG-10 / SW-10`: Testler "carrier address translation" (CGNAT) arkasında yapılıyor. CGNAT yalnızca hücresel taşıyıcı ağında karşınıza çıkar.
- `RF-17` 5G ile bir arada çalışmayı, `RF-18` ise 0.7–3.8 GHz açıklık ayarlayıcısını (aperture tuner) test ediyor. Bu tamamen hücresel bir bant aralığı.

Sonuç: Firmware, testler ve RF kuralları hücresel radyo varmış gibi yazılmış. Donanım listesi **[ÖNCÜL: U2]** ve §5.2.4 ise hücreseli dışarıda bırakıyor. Bu, belge setinin en büyük ürün düzeyi çelişkisi. Ayrıca uydu yolu da **dolaylı olarak siliniyor**, çünkü belgeye göre uydu hücresel radyo üzerinden çalışıyor.

### 1.2 Elde kalan radyolar dışarıda neden işe yaramıyor?

| Radyo | Fiziksel menzil ve kapasite | WAN yolu olur mu? |
|---|---|---|
| Wi-Fi 7 | Dış mekân AP yarıçapı tipik olarak 30–80 m. Erişim izni gerekiyor (WPA3/portal). | Yalnızca kapsama adacıklarında |
| 60 GHz mmWave | 5 m'de serbest uzay kaybı: 20·log10(4π·5/0.005) ≈ **82 dB**. İnsan gövdesi bloklaması 20–35 dB. Hüzme hizalama gerekiyor. | Hayır. Yalnızca dock yolu (RF-19) |
| UWB (802.15.4z) | Konum belirleme. Veri hızı ≤ 27 Mbit/s, onlarca metre. Altyapısı yok. | Hayır |
| BLE 5.4 | 1–2 Mbit/s PHY, gerçek verim < 1.4 Mbit/s | Hayır. Ancak telefonla tethering yapılırsa olur, ki bu da ikinci cihaz demek |
| Optik yol | Makbuz ve küçük yük (RF-7) | Hayır. Oturum taşıyamaz |

### 1.3 Yürüyüş ve araç senaryosu: Wi-Fi devir aritmetiği

- **Yaya (1.4 m/s):** 50 m yarıçaplı bir AP hücresinin çapı (100 m) yaklaşık 70 s'de geçilir. AP'ler bitişik ve açık olsa bile dakikada bir devir gerekir.
- **Araç (50 km/h = 13.9 m/s):** Aynı hücre yaklaşık **7 s**'de geçilir. 120 km/h'te süre **3 s**'ye iner.
- **İlişkilendirme maliyeti:** Tarama (6 GHz'te PSC kanalları dahil) 100–500 ms, WPA3-SAE el sıkışması 50–300 ms, DHCP ve ARP 100 ms–2 s, portal varsa manuel adım ve 10 s'den fazlası. Yani 120 km/h'te kapsama süresinin **%30–100'ü** yalnızca ilişkilendirmeye gider.
- **Kapsama oranı:** Şehir yollarında sürekli ve açık Wi-Fi kapsaması %10'un altında. Kırsal ve otoyolda pratikte sıfır.
- **Sonuç:** `C2` video ve `C1` delta akışı kesintisiz sürdürülemez. `10 §10.4`'teki altı satırın hiçbiri "hücresel yok, dışarıda" durumunu kapsamıyor. Sınıf merdiveninin 7. satırı eksik: **"bağlantı yok, yalnızca yerel taban"**.

### 1.4 Kapalı-portal (captive portal) çıkmazı [K2]

Halka açık Wi-Fi'ların çoğu bir HTTP portalının arkasında. Bu portal bir web sayfası ve sayfayı render edecek motor `Budscan`/page engine **validator'da** çalışıyor (`09 §9.7`: "the browser engine, through Budscan"). Validator'a ulaşmak için ise önce portalı geçmek gerekiyor. Bu bir döngüsel bağımlılık.

Yerel sahne renderer'ı (`10 §10.2.1`) yalnızca **imzalı display list** render ediyor. HTML, CSS ya da JS çalıştıramaz. Bunu sağlamaya çalışmak `9.7` sınır kuralını ("a duty that crosses the line is a defect") ihlal eder.

Kısmi çıkış yolları:

- **Passpoint/OpenRoaming (Hotspot 2.0, 802.1X/EAP)** portalsız kimlik doğrulama sağlar. Ancak bunun için EAP yığını firmware'e girmeli ve kapsama yine sınırlı.
- **RFC 8910/8908 Captive Portal API** yalnızca JSON durumu verir, ödeme veya onay ekranını yine çözmez.

### 1.5 `choose()` işlevi boş kümede çöküyor [K3, DOĞRULANDI]

```text
let best    = usable.min_by(...)          // Rust'ta Option<PathCandidate> döner
PathPlan { primary: best, ... }           // primary: PathCandidate, Option değil
let mirrors = usable.filter(...).take(2)  // 0, 1 ya da 2 eleman; [PathCandidate; 2] sabit dizi
```

- Dışarıda ve hücresel yokken `usable = ∅` olur. Bu durumda `best = None` ve `.unwrap()` panic verir. "Statik havuz, dört görev" mimarisinde panic, reset ve boot zinciri demek. Step 3'te bağlantı yine bulunamaz ve **boot döngüsü** riski doğar. Bu, "A Leaf is never a brick" kuralıyla çelişiyor.
- `mirrors` sabit iki elemanlı bir dizi. Bir veya sıfır aday olduğunda tip hatası çıkar ya da boş değer uydurulur.
- Seçim ölçütü `(rtt_ms, energy_mw)` sözlüksel sıralaması. Yani 1 ms daha düşük RTT, enerjisi 10 kat yüksek bir yolu kazandırır. Bu, §8.3'teki enerji politikasıyla çelişir: politika tanımlanmış ama `choose()` içinde kullanılmıyor.
- **Histerezis yok.** RTT'leri birbirine yakın iki AP arasında yol seçimi sürekli gidip gelir. Her geçiş bir IDR karesi, yeniden şifreleme ve NAT yeniden bağlaması demek.
- `trusted` filtresi ve R6, güven testinden geçmeyen operatörün yolunu "asla kullanma" diyor. Ama oturum zaten uçtan uca şifreli olmalı. Bu durumda IP taşıyıcısına güvenmek gereksiz, üstelik halka açık Wi-Fi'ı tümden yasaklayarak **ulaşılabilirliği daha da azaltıyor**.

### 1.6 Çift yol tekrarı (`09 §9.3`) hücresel olmadan anlamsız

"Duplicated on two paths when the link is unstable" deniyor. Hücresel yoksa iki yol aynı AP'nin MLO bağlantıları ya da iki Wi-Fi bandı olur. Bunlar **korelasyonlu arızalar**: AP gidince ikisi birden gider. Tekrar, radyo enerjisini iki katına çıkarır ama erişilebilirliği artırmaz.

### 1.7 Ek kayıplar

- **GNSS:** `05 §5.1`'de "Navigation, multi-constellation" var ama U2 listesinde yok **[ÖNCÜL]**. Dışarıda konum yok, RF-18 test edilecek bir şey bulamıyor.
- **Acil çağrı ve SMS 2FA** yok. Telefon yerine geçme iddiası varsa bu yasal ve güvenlik açısından bir boşluk.
- `mobile.rs`'teki "battery-aware challenge policy" ve RG-11 "storage serving" görevleri, cihaz çevrimdışı kaldığı her an challenge kaçırma ve kredi kaybı demek.

### 1.8 Hücresel eklendiğinde ortaya çıkacak fizik sorunları

Hücresel eklemek K1'i çözer ama yeni darboğazlar açar:

1. **Anten toprağı:** 617–960 MHz düşük bantta anten şasi modunda çalışır ve ≥ λ/4–λ/2 boyunda iletken toprak ister (700 MHz'te λ/4 ≈ 107 mm, λ/2 ≈ 214 mm). Gövdenin toprağı `AgNW/ITO`, yani 12 Ω/sq. 1 GHz'te bakırın yüzey direnci yaklaşık 8 mΩ/sq. Fark yaklaşık **1500 kat**. Ohmik kayıp düşük bant verimini tahminen 5–10 dB düşürür. Modül söküldüğünde (RF-13) 20 g'lık modülün kendi toprağı birkaç cm'dir. Düşük bant pratikte çalışmaz.
2. **4×4 MIMO:** 3.5 GHz'te λ/2 ≈ 43 mm. 80 mm'lik üst kenara korelasyonu düşük en fazla 2–3 anten sığar. 700 MHz'te tek bir anten bile zor. Belgedeki "4×4" ifadesi kâğıt üzerinde kalıyor.
3. **Bantlar:** RF-18'deki 0.7–3.8 GHz ayarlayıcı n77'nin üst kısmını (3.8–4.2 GHz) ve n79'u (4.4–5.0 GHz) kapsamıyor.
4. **Isı:** Tüm radyolar 20 g'lık `b` modülünde. Kenar hücrede 23 dBm TX, %30–40 PA verimi ve baseband ile modem ~1.5–2.5 W çeker. Wi-Fi 7 ile birlikte toplam yaklaşık 2 W. Modülün yüzeyi ~40 cm² ve h ≈ 15 W/m²K (doğal taşınım + ışınım) alınırsa R ≈ 1/(15·0.004) ≈ **17 K/W**, yani **+33 K**. 25 °C ortamda yüzey 58 °C olur. IEC 62368-1'in uzun süreli temas sınırı (~43–48 °C) aşılır. PC'nin ısıl iletkenliği ~0.2 W/m·K olduğu için gövdeye ısı yayılımı da yok.
5. **Pil:** Sürekli `C2` akışında radyo DRX uykusuna giremez. Yaklaşık panel 1–1.5 W + hub 0.45 W + Wi-Fi/5G 1.5–2.5 W = 3–4.5 W. 12 Wh ile **2.7–4 saat**. "Zero-CPU güç tasarrufu" anlatısı sürekli radyo maliyetinin altında kalıyor.
6. **eSIM/iSIM:** GSMA SGP.22/SGP.32 için LPA, TLS ve ASN.1 yığını firmware'e girer. Bunu 4 MB'lık flash'ta ve statik havuzda yapmak mümkün ama GCF/PTCRB ve operatör sertifikasyonu ciddi bir maliyet. Ayrıca bir hücresel modem, kendi RTOS'unu çalıştıran **bir CPU'dur**. Bu da K9'u kesinleştirir.

### 1.9 Önerilen düzeltme

- Bir NR sub-6 modem ekleyin: tam SA ya da en az Rel-17 **RedCap**. RedCap 20 MHz ve 1–2 Rx ile 10–150 Mbit/s verir, `C2` için yeterli. iSIM'i secure element içine koyun.
- `PathPlan.primary` alanını `Option` yapın. Boş kümede `LocalFloor::offline()` görünür durumuna geçilsin. Seçime histerezis ekleyin (ör. ≥ 20% RTT farkı ve ≥ 2 s kalıcılık).
- Sınıf merdivenine "çevrimdışı" satırını ekleyin.
- Passpoint/EAP'i firmware'e koyun. Portal durumunda "bu ağ tarayıcı gerektiriyor, telefonla geçin" mesajı görünür bir durum olarak gösterilsin.
- Yeni gate'ler: **RF-21** (araç içinde 120 km/h'te 30 dakikalık oturum sürekliliği), **SW-14** (boş aday kümesinde boot döngüsü olmaması).

---

## 2 · SORU 2: RG-4 devri sırasında (500 ms – 3 s) yazma ve kaydırma girdileri ne olur?

### 2.1 Belgenin verdiği sözler

- `10 §10.1`: Etkileşim bütçesi < 10 ms, "inside the device", mesafe önemsiz.
- `08 §8.6.4`: Dokunma ve kalem "local echo, 3–8 ms".
- `08 SW-5`: "no stuck screen, no lost state, the token rules hold."
- `09 §9.3`: Delta karesi "acknowledged version"a karşı render ediliyor. Devam jetonu "single use, short lived, **one named operator**".

### 2.2 Yerel eko ile dayanıklılık aynı şey değil [K5]

Yerel eko girdiyi yalnızca **gösterir**. Girdinin yetkili kaydı (metin tamponu, form durumu, uygulama durumu) validator A'nın belleğinde durur. A çöktüğünde girdiler dört gruba ayrılır:

| Grup | Durum | Belgenin davranışı | Sonuç |
|---|---|---|---|
| G1 | A aldı, uyguladı ve B.U.D. checkpoint'ine yazıldı | B görür | Doğru |
| G2 | A aldı ve onayladı (ack), ama checkpoint'e yazılmadı | Tanımsız | **Kayıp.** Kullanıcı ekranda gördüğü harflerin B devraldığında silindiğini görür |
| G3 | Cihaz gönderdi, A almadan çöktü | Tanımsız | Kayıp ya da yanlış tekrar |
| G4 | Devir sırasında yazılanlar (≤ 3 s) | Tanımsız | Hedef sürüm belirsiz |

Rakamlarla: hızlı yazımda 8–10 karakter/s, yani 3 s'de **~30 karakter**. Checkpoint aralığı belirtilmemiş. 5 s olsa G2 penceresinde ~50 karakter daha var. Toplamda **80 karakter** kaybolabilir. SW-5'teki "no lost state" maddesi bu tasarımla geçilemez.

**Kök neden:** Ack semantiği tanımsız. Ack "A uyguladı" anlamına mı geliyor, yoksa "kalıcı olarak checkpoint'lendi" anlamına mı? Cihaz girdi günlüğünü ancak **kalıcılık ack'i** gelince silmeli. Bunu yapmak her ack'e bir B.U.D. yazma gecikmesi ekler (Pollen depolama düğümüne RTT tipik olarak 20–100 ms). Bu gecikme yerel eko sayesinde kullanıcıdan gizlenebilir, ama tasarımda yer almalı.

**Statik havuz boyutu:** Kalem örneklemesi 480 Hz × ~32 B (x, y, basınç, eğim, zaman, seq) ≈ 15.4 KB/s. 30 s'lik kalıcılık penceresi için ≈ **460 KB** halka tampon gerekir. Tampon taşarsa ne olacağı (en eski girdiyi düşürmek mi, girdiyi kilitlemek mi) tanımlanmamış. "No allocator beyond a static pool" kuralı bu sayının **önceden** belirlenmesini zorunlu kılıyor.

### 2.3 Devam jetonu B'nin devralmasını engelliyor [K4, DOĞRULANDI]

- Jeton "one named operator" ve "single use". Planlanmamış devirde jeton A adına kesilmiş, **B kullanamaz**.
- Yeni jeton kullanıcı yetkisiyle imzalanmalı. Kullanıcı yetkisi secure element'teyse ML-DSA-87 imzası gerekir. Cortex-M4 sınıfı bir çekirdekte bu 10–30 M döngü sürer; 100 MHz'te **100–300 ms**, düşük saatli bir SE'de daha uzun. Yalnız bu adım 500 ms bütçesinin büyük kısmını yer.
- "Binding" (operatör, süre, **bildirim süresi**) B ile önceden kurulmamışsa, keşif, binding imzası ve kayıt toplamda 500 ms'ye sığmaz. Bildirim süresi plansız çöküşte zaten uygulanamıyor.
- B.U.D. okuması "No read without a Pollen grant" kuralına tabi. B'nin grant'i yoksa yeni bir grant imzası ve yayılımı gerekir.
- Oturum durumu kullanıcı yetkisi altında şifreli. B'ye **çözme anahtarı** devredilmeli. Önceden devredilirse saldırı yüzeyi büyür, sonradan devredilirse gecikme artar. Belge bu ödünleşimi hiç ele almıyor.

### 2.4 Durum boyutu ve 500 ms iddiasının fiziği

Budscan bir tarayıcı motoru (DOM, JS heap, GPU dokuları). Tipik bir sekme durumu 50–300 MB. 500 Mbit/s etkin hızla 50 MB **0.8 s**, 300 MB **4.8 s** sürer. Bu, B.U.D. erişim gecikmesi ve şifre çözme eklenmeden önceki rakam.

Gerçekçi bir devir "canlı heap göçü" olamaz. Olabilecek şey: **URL, form alanları, kaydırma konumu ve uygulama düzeyi checkpoint'ten yeniden yükleme**. Bunun bedelleri:

- A'nın üçüncü taraf sunuculara açtığı TLS oturumları, WebSocket ve WebRTC bağlantıları **göç edemez**. Görüntülü arama düşer.
- Device-Bound Session Credentials (DBSC) ya da DPoP ile A'nın anahtarına bağlanmış çerezler B'de geçersizdir. Kullanıcı oturumdan atılır.
- Uçuşta olan idempotent olmayan POST'lar (ödeme, mesaj gönderme) **çift gönderim** riski taşır. Belgede idempotency anahtarı kuralı yok.

### 2.5 Split-brain: A ölmemiş, yalnızca ulaşılamıyor olabilir

Wi-Fi roaming ya da yol değişimi sırasında A'nın heartbeat'leri 200–500 ms gecikebilir. Bu durum "A çöktü" diye yanlış yorumlanırsa:

- A da B de aynı oturuma yazar. B.U.D.'de **çatışan sürümler** oluşur.
- A, gecikmeli olarak üçüncü taraf yan etkileri (mesaj gönderme gibi) işlemeye devam edebilir.

Gerekenler:

- **Fencing epoch:** Oturumdaki `counter`'ı epoch olarak kullanın. B.U.D. compare-and-swap ile eski epoch'tan gelen yazmaları reddetsin.
- **Hatayı yanlış ilan etmemek:** Devir başlatmadan önce A, ayna yol üzerinden yoklanmalı. Tek yolun kaybı devri tetiklememeli.
- Algılama süresi: 50 ms heartbeat × 3 kayıp ≈ 150 ms + yoklama ≈ **250 ms**. Bu da 500 ms bütçesinin yarısı.

### 2.6 Yazma davranışı: ne yapılabilir, ne yapılamaz?

Yerel renderer **konumlandırılmış bir display list** render ediyor. Düzen motoru (layout) yok, çünkü `9.7` "page engine and layout" görevini ağa veriyor. Buradan çıkanlar:

- **Satır kaydırma ve reflow yapılamaz.** Yazılan metin satır sonuna gelince yerel renderer yeni satırı nasıl düzenleyeceğini bilmez. Belge, düzenlenebilir alanlar için "yerel düzenleme bölgesi" (satır kırma, imleç, seçim, silme) tanımlamalı. Bu, sınırlı bir layout yetkisini cihaza vermek demek. `9.7` tablosu buna göre güncellenmeli, yoksa kendi kuralını ihlal eder.
- **Metin şekillendirme (shaping):** Türkçede `ı/İ` büyük-küçük harf dönüşümü yerel olarak sorunsuz. Arapça bidi, Hint yazıları ve CJK IME (sözlükle dönüşüm) ise yerel 2 MB önbellekle ve "2 mm² sabit fonksiyon" ile yapılamaz. DST-1 "üç dilde" test istiyor ama hangi dillerde olduğu belirtilmemiş. CJK'de devir sırasında IME **tamamen ölür**.
- **Glif önbelleği:** 2 MB / (32×32×8 bit ≈ 1 KB/glif) ≈ 2 000 glif. Renkli emoji ve CJK'de önbellek ıskası olursa glifin ağdan alınması gerekir ve devir sırasında ağ yok. Sonuç: **boş kutular (tofu)**.
- **CRDT/OT birleştirme:** B eski bir checkpoint'ten (`v_k`) başlar. Cihaz ise `v_k+m` üzerinde yerel düzenlemeler yapmıştır. Yeniden temellendirme (rebase) için düzenlenebilir alanlarda bir CRDT (RGA ya da Yjs benzeri) ya da OT gerekir. Belgede bu yok. "Difference against the acknowledged version" modeli tek yazıcı varsayıyor.

### 2.7 Kaydırma davranışı

- **Metin yüzeyi:** Yerel renderer yalnızca gönderilmiş display list kadar içerik bilir. Fırlatma (fling) kaydırması 3 s'de birkaç ekran yol alır. Önbelleğin sonuna varılınca **boş alan (checkerboard)** görünür. Gereken: ekranın ±3 katı ön-getirme (prefetch) ve bunun statik havuzda boyutlandırılması.
- **Video yüzeyi:** Reprojeksiyon 10–40 ms'lik gecikmeyi gizlemek için tasarlanmış. 500 ms–3 s boyunca ekranın kenarlarından boşluk girer, bu yüzden reprojeksiyon "below the quality threshold" kuralıyla kapanır ve **kare donar**. SW-5'teki "no stuck screen" maddesi geçilemez. Görünür bir "devir" durumu ve ilerleme göstergesi gerekir.
- **Kaydırma konumu cihazda yetkili olmalı.** B devraldığında kendi kaydırma konumunu değil, cihazın bildirdiğini benimsemeli.
- **Video çözücü:** B'nin kodlayıcısında referans kare yok. İlk kare IDR olmalı, bu da bant genişliğinde 5–10 katlık bir sıçrama demek. Belgede tanımlı değil.

### 2.8 En tehlikeli durum: devir sırasında yapılan dokunuşun yanlış yere uygulanması

Kullanıcı devir sırasında bir butona dokunur. Dokunuş kuyruğa alınır ve B'ye **koordinat olarak** tekrarlanır. B ise farklı bir düzen render etmiştir (reklam yüklenmiş, sayfa kaymış). Dokunuş **başka bir öğeye** isabet eder; bu "Sil" ya da "Öde" olabilir.

Gerekenler:

- Her girdi şu bilgilerle bağlanmalı: `(session_epoch, seq, doc_version, target_node_id, t_local)`.
- B, `doc_version` uyuşmazsa semantik girdiyi **reddetmeli**. İdempotent olmayan eylemler devir sırasında görünür biçimde kilitlenmeli.
- Cüzdan onayı yerel kalır. Ama `10 §10.1`'deki "wallet < 10 ms" iddiası ML-DSA-87 imza süresiyle (100–300 ms) çelişiyor. "Yerel" doğru, "< 10 ms" yanlış.

### 2.9 Önerilen protokol

1. **Cihazda girdi günlüğü:** Her girdi seq ve sürüm numarasıyla tutulur. Silme işlemi yalnızca kalıcılık ack'iyle yapılır. Tampon statik olarak boyutlandırılır ve taşma politikası tanımlanır.
2. **Sıcak yedek:** B önceden imzalanmış bir binding ve önceden devredilmiş, kapsamı daraltılmış bir oturum anahtarı ile bekler. Alternatif olarak t-of-n eşik anahtar kullanılabilir (`threshold_mldsa.rs` zaten mevcut).
3. **Sürekli işlem günlüğü:** A, işlem günlüğünü (op-log) B.U.D.'ye sürekli akıtır. Yalnızca periyodik checkpoint'e güvenmez. Hedef RPO ≈ 0.
4. **Fencing:** Epoch ve CAS. Hata ilanı öncesi ayna yoldan doğrulama.
5. **Düzenlenebilir alan:** CRDT ve yerel düzenleme bölgesi. `9.7` tablosu buna göre güncellenir.
6. **Görünür durum:** `handoff` durumu sınıf satırında gösterilir. Kare donması belirli bir süreyi geçerse üst katman (overlay) çıkar.
7. **Yeni gate SW-5b:** 3 s'lik devir sırasında 30 karakter yazma, fling kaydırma ve bir buton dokunuşu. Ölçütler: sıfır karakter kaybı, sıfır yanlış hedef, sıfır çift POST.

---

## 3 · SORU 3: Q4 karosu çalışırken sökülürse TCON ve C2 ne yapar?

### 3.1 Ekran geometrisi ve ölçekleme aritmetiği

Panel 80×160 mm (en-boy 1:2). 2×2 bölündüğünü varsayıyorum: her karo 40×80 mm. Q4 çıkınca kalan L-şeklinin içine sığan en büyük dikdörtgenler:

| Seçenek | Boyut | Alan | Tam kareyi "fit" ile sığdırma ölçeği | Görünen içerik alanı |
|---|---|---|---|---|
| Üst iki karo (yatay) | 80×80 | %50 | 0.5 | 40×80 = **%25** |
| Sol iki karo (dikey) | 40×160 | %50 | 0.5 | 40×80 = **%25** |
| Kırpma (Q4 bölgesi siyah) | L-şekli | %75 | 1.0 | %75, ama içeriğin %25'i **kayıp** |

0.5 kat ölçekte 3 mm'lik font 1.5 mm'ye iner ve okunmaz. Sabit fonksiyonlu ölçekleyici (TCON ya da hub) **görüntüyü kurtarmaz**. Asıl gereken, içeriğin yeniden düzenlenmesi (reflow).

Reflow ise yapılamıyor, çünkü:

- Yerel renderer layout yapamıyor (`9.7`).
- Web düzen motorları yalnızca dikdörtgen viewport tanır. CSS `viewport-segments` katlanabilir cihazlar için yan yana iki dikdörtgen sunar, L-şekli desteklemez.
- Validator bir dikdörtgen (80×80 ya da 40×160) seçmeli, kalan karo yardımcı panel (klavye, bildirim) olarak kullanılmalı.

Zaman bütçesi: viewport değişimi + layout + kodlayıcıyı yeniden yapılandırma + IDR. Yakın validator ile ≈ 50–150 ms, uzak validator ile 300 ms'den fazla. Bu sürede görüntü kırpılmış kalır.

### 3.2 C2 akışı çöker mi? İki mimari olasılık

**(a) Tüm panel için tek bit akışı:** Çözücü bütün kareyi çözer, TCON Q4 bölgesini taramaz. **Çökme olmaz**, ama bit hızının ve çözme enerjisinin %25'i boşa gider. Çözücü yeniden yapılandırılmamalı, çünkü referans kareler tutarlı kalmalı.

**(b) Karo başına akış ya da HEVC tile/slice:** Karo zamanlayıcısının (`08 stream/: the panel and tile scheduler`) Q4 hedefini düşürmesi gerekir. Kritik nokta: hareket vektörleri karo sınırlarının ötesini referans alabilir. Kodlayıcı **MCTS (motion-constrained tile sets)** kullanmıyorsa Q4 bölgesinin çözülmesi durdurulamaz. Durdurulursa Q1–Q3'te sınır boyunca bozulma (smearing) görülür ve bir sonraki IDR'a kadar sürer. Belgede MCTS şartı yok.

**İmzalı oturum nesnesi sorunu [DOĞRULANDI]:** `09 §9.3`'e göre oturum nesnesi "decoder profile" ve "class set" içeriyor ve **wallet authority tarafından imzalanıyor**, B.U.D.'de saklanıyor. Çözünürlük ya da viewport değişikliği decoder profile değişikliği sayılırsa her karo sökme işlemi yeniden imza ve B.U.D. yazması gerektirir; bu da saniyeler sürer. Çözüm: viewport'u imzalı profilden ayırın ve sunum düzeyinde imzasız bir parametre yapın.

**R7 ve "never degrade in silence":** Q4 çıkınca sınıf fiilen düşer (alan %75'e iner, çözünürlük değişir). Bu görünür bir olay olmalı. Belgede tanımlı değil.

### 3.3 Etiket ve güvenli ekran ihlali [K7, DOĞRULANDI]

`08 §8.6.3` dört etiket tanımlıyor: kanıt etiketi, sınıf satırı, pil durumu, kamera durumu. Kural: "A page cannot cover a label" ve RG-16 "the label renders on every page class".

Etiketler Q4'e çiziliyorsa karo söküldüğünde **görünmez olurlar**. Bu bir sayfanın değil fiziksel bir eylemin sonucu ama etkisi aynı: kamera durumu etiketi görünmeden kamera çalışabilir. Bu bir gizlilik ihlali.

Gerekenler:

- TCON ya da firmware etiketleri **kalan karolara taşımalı**.
- Safe screen (`8.2`) hangi karoda? O karo sökülürse "Leaf is never a brick" kuralı gereği safe screen başka bir karoya geçmeli.
- Yeni gate: **DSP-x**, her karo sökme durumunda dört etiketin görünür kalması.

### 3.4 Elektriksel hot-swap fiziği

**Sinyal:** Her karo için kabaca 450 ppi alınırsa: 80 mm ≈ 1417 px, 160 mm ≈ 2835 px. Tam panel ≈ 4.0 Mpx × 144 Hz × 24 bit ≈ **13.9 Gbit/s** sıkıştırılmamış veri, karo başına ≈ **3.5 Gbit/s**. DSC ile ~3 kat sıkıştırılsa bile karo başına ≥ 1.2 Gbit/s'lik bir SerDes hattı, esneyen PC-PDMS ve NiTi geçme kilit (dovetail) eklemi üzerinden geçiyor. Kontak empedansı bükülmeyle değişir, belgede konnektör tanımı yok.

**Bağlantıyı kesme sırası:** Kontaklar rastgele sırayla ayrılırsa:

- OLED besleme rayları (ELVDD ≈ +4.6 V, ELVSS ≈ −3 V civarı) toprak hattından önce koparsa kaynak sürücüde latch-up olur.
- Toprak hattı sinyal hatlarından önce koparsa sinyal hatları üzerinden geri akım ve ESD hasarı oluşur.
- Gereken: kademeli pinler (toprak ilk takılır, son ayrılır), karo başına hot-swap denetleyicisi ve TCON'da hızlı "lane-down" algılaması. Belgede hiçbiri yok.

**Güç [K6]:** 12 Wh / 3 200 mAh ≈ 3.75 V, yani dört hücre **paralel**.

- Q4 yük altında çıkarsa kalan üç hücrenin akımı +%33 artar.
- PEO tabanlı elektrolitin iyon iletkenliği 25–36 °C'de yaklaşık 10⁻⁶–10⁻⁵ S/cm. Kullanışlı 10⁻⁴ S/cm ancak kristalin faz eridikten sonra, ~60 °C'nin üzerinde elde edilir. ARGE'deki **≤ 36.2 °C** sınırı, hücrelerin yüksek iç dirençle çalışmasını garanti ediyor. Ani yük artışında voltaj çöker, hub reset atar, oturum ölür.
- Gerekli tutma (hold-up) enerjisi: 3 W × 50 ms = 0.15 J. 3.8 V'tan 3.0 V'a izinli düşüşle C = 2E/(V₁² − V₂²) = 0.3 / 5.44 ≈ **55 mF**. Bu, 2 mm'lik esnek gövdede ince film süperkapasitör ve hücre başına ideal diyot (OR-ing) gerektirir.
- **Yeniden takma:** Yeni karonun hücresi farklı SoC'de olabilir (ΔV ≈ 0.2–0.3 V). Doğrudan paralel bağlantıda dengeleme akımı oluşur. Her hücre için ayrı DC-DC ya da şarj yolu gerekir.

### 3.5 RF ile çapraz etki [K6, DOĞRULANDI]

- `05 §5.2.3`: "Transparent AgNW/ITO layers inside the 2.00 mm body **couple to the 90° B stem**" ve RF sisteminin parçası.
- `RF-10`: "the tiled steel as the RF ground… **the mosaic** behaves as solid ground."

Q4 çıkarıldığında toprak düzleminin %25'i gider. Anten uyumu (match) ve şasi modu değişir. Düşük bantta bu birkaç dB'lik bir kayıp olur. **Karo sökme anı ile bağlantı kopması aynı anda yaşanır.** RF-10 ve RF-13 testleri "eksik karo" durumunu hiç içermiyor.

Ayrıca §5.2.2'deki "No radiator over the pixel area" kuralı ile §5.2.3'teki "AgNW/ITO RF sisteminin parçası" ifadesi kendi içinde çelişiyor: piksel alanındaki iletken katman ışımaya katılıyor.

### 3.6 Mekanik çelişki: geçme kilit tutma kuvveti

- ARGE P2'ye göre 24 diş, diş başına 100 N (10 N/mm).
- Dikiş uzunluğu "+" şeklinde 80 + 160 = 240 mm, yani 24 dişte 10 mm aralık. Q4'ün kendi dikişleri 40 + 80 = 120 mm, yani **12 diş × 100 N = 1 200 N** tutma kuvveti.
- 1.4 N ile bükülen 2 mm'lik bir levhaya 1 200 N uygulayarak "< 3 s" içinde karo sökmek fiziksel olarak mümkün değil. Levha kilit açılmadan önce bükülür.
- Bu kuvvet yalnızca düzlem içi kuvvete karşı tanımlanmış ve Z ekseninde çıkarma kolaysa, bu sefer bükülme sırasındaki soyulma momenti dişleri açar. Bu da "bend continuously without separating" iddiasıyla çelişir.
- Sonuç: Bükülme bütünlüğü ile hızlı sökülebilirlik aynı geçme kilidinden beklenemez.

**Dokunmatik giriş:** Q4'ün dokunmatik ağı da gider. Dikişi geçen bir hareket (ör. kaydırma) yarıda kesilir. Koordinat eşlemesi değişmeli.

**Yeni karonun doğrulanması:** RG-6 ve SW-7'ye göre karo bileşen kaydı ve imzası doğrulanmalı. RG-13'e göre iptal (revocation) durumu "ağın gördüğü" bilgiye bağlı. Soru 1'deki çevrimdışı durumda **iptal kontrolü yapılamaz**. Çevrimdışıyken takılan karonun kabul ya da red politikası belgede yok. SE üzerinde ML-DSA doğrulaması 50–200 ms sürer, bu da "< 3 s" bütçesine dahil edilmeli.

**AB 2023/1542 atfı:** Tüzük, taşınabilir pillerin son kullanıcı tarafından "readily removable" olmasını istiyor. "< 3 s hot-swap" ya da çalışırken değiştirme şartı yok. Atıf yanlış bağlamda kullanılmış.

---

## 4 · Diğer çapraz dosya çelişkileri ve fiziksel hatalar

### 4.1 Gecikme tablosu tutarsız [K10, DOĞRULANDI]

**10.1 ile 10.4 çelişiyor.** 10.1'e göre etkileşim bütçesi "< 10 ms, inside the device, distance: **no**". 10.4'te ise girdiden göze süre mesafeyle artıyor:

| Senaryo (10.4) | Girdiden göze |
|---|---|
| Kıta ötesi, yakın düğüm yok | 8–20 ms |
| Yalnızca uydu | 25–60 ms |

Yerel bir eko mesafeye bağlı olamaz. Ya tablo yanlış, ya da eko aslında yerel değil.

**Fiber hesabı yanlış uygulanmış:**

| Mesafe | Tek yön yayılım (200 km/ms) | Belgedeki rakam |
|---|---|---|
| 15 km | 0.075 ms (RTT 0.15 ms) | "1–5 ms" |
| 1 500 km | 7.5 ms (RTT 15 ms) | — |

"1–5 ms"lik süre mesafeden değil **erişim ağından** geliyor:

- Wi-Fi hava gecikmesi ve çekişme 2–10 ms.
- 5G SA kullanıcı düzlemi tipik olarak 10–20 ms. 1 ms'lik URLLC tüketici cihazlarında yok.

"Wherever the user is" iddiası bu yüzden erişim ağına bağlı ve garanti edilemez.

**"3–8 ms" tuş vuruşu bir dağılım değil, en iyi durum:**

| Bileşen | Ortalama | En kötü |
|---|---|---|
| Dokunmatik tarama (240 Hz) | 2.1 ms | 4.2 ms |
| İşleme | 0.5 ms | 0.5 ms |
| 144 Hz vsync beklemesi | 3.5 ms | 6.9 ms |
| Tarama ile ilgili satıra ulaşma | 3.5 ms | 6.9 ms |
| **Toplam** | **≈ 9.6 ms** | **≈ 18.5 ms** |

Belgedeki aralık ancak beam-racing ya da kısmi güncelleme ile tutturulabilir. P4'te tanımlanan **PDLC katmanı** devredeyse PDLC'nin tepki süresi 10–100 ms. Bu durumda 10 ms bütçesi tamamen çöker.

### 4.2 Yakın validator kendisiyle çelişiyor (`10 §10.2.3`)

- Bir yandan "does not hold the user's data in the clear" deniyor. Öte yandan "the document model, the video buffer, the input predictor, composition" tutuyor. Kullanıcının e-postasının render edilmiş hali **açık kullanıcı verisidir**. Kompozisyon yapabilmek için de şifre çözmek gerekir.
- **DST-4 (değiştirilmiş kare tespiti):** Her kare ML-DSA-87 ile imzalanırsa imza başına ≈ 4 627 B × 60 fps ≈ **2.2 Mbit/s** ek yük oluşur. Bu, `C1` delta bant genişliğiyle aynı mertebede. Üstelik yakın düğüm kompozisyon yaparsa imza kırılır. Hash-zinciri ile toplu imza ya da yakın düğümü "yalnız röle" yapmak gerekir.
- **Yakın düğüm her yerde 15 km içinde** olamaz: kırsalda, denizde ve havada bu yoğunluk yok. Yürüyen ya da araçtaki kullanıcı için yakın düğüm değişimi de **ikinci bir RG-4 devri** demek.

### 4.3 "Zero-CPU" iddiası yanlış [K9]

`08 §8.1`'de şunlar var: dört görev, sabit öncelikler, Rust crate'leri, 1 GB "working memory inside the hub", A/B boot, statik havuz. Bunları çalıştıran bir CPU ya da MCU olmak zorunda. Wi-Fi 7 kombo çipi, secure element ve olası bir modem de kendi gömülü çekirdeklerini taşıyor.

Doğru ifade "genel amaçlı uygulama işlemcisi ve kullanıcı kodu yok" olur. Mevcut haliyle iddia D7'deki "the product's honesty is its differentiator" kuralını ihlal ediyor.

### 4.4 Boot zamanlaması (`08 §8.2`)

- **Step 1, 20 ms:** 4 MB'lık imajın SHA-512 özeti donanımda yaklaşık 8 ms. ML-DSA-87 doğrulaması M4 sınıfında 2–3 M döngü (100 MHz'te 20–30 ms). Düşük saatli bir SE'de 100 ms'yi aşabilir.
- **Step 2, 60 ms:** 1 GB LPDDR bellek eğitimi (DRAM training) ve OLED güç sıralaması tek başına 50–100 ms'yi doldurabilir. 60 ms iddiası ölçümle desteklenmeli.

### 4.5 Geometri: 25.5 mm sarım bir tam silindir [K8]

2π × 25.5 = **160.2 mm**, yani 160 mm'lik gövde R 25.5'te **kapalı bir tüp** oluşturuyor. Belgeler buna "wrap" diyor; tüpün çevresi bir yetişkin bileğinin çevresiyle (~160 mm) neredeyse aynı.

- Üst kenardaki `b` çubuğu alt kenara yaslanır ya da cilde değer. Gövde kaybı 3–6 dB, örüntü bozulur.
- `05 §5.2.1`'deki "antenna never bends" ifadesi kenar çizgisi için doğru. Ama anteni çevreleyen geometri tamamen değişiyor.
- **SAR = 0.054 W/kg** değeri §5.2.3'te bir **olgu** gibi yazılmış. RF-16 ölçümü yapılmadan bu bir hipotez, `[HYPOTHESIS]` etiketiyle yazılmalı.

### 4.6 Malzeme ve mekanik çelişkiler [K11]

- **"Sıfır rijit metal" kuralına karşı:** RF-10 "tiled steel", §5.3 "metal spine", §5.2.5 "prism frame", §5.2.2 "perimeter frame". Hub SoC, 1 GB LPDDR, U1 ve U2 de rijit ve kırılgan silikon kalıplar. "Zero rigid zones" fiziksel olarak mümkün değil. Doğrusu "rijit adalar, nötr düzlemde ve tanımlı boyutta" demek.
- **LLZO seramik** dolgusu "no brittle ceramic" kuralıyla gerilim içinde (kompozit olsa bile).
- **Qi2.2 bobinleri:** `05 §5.3` "The coil left the design" diyor. ARGE P4/D5 ise Ø54 + 4×Ø22 Qi2.2 bobin listeliyor. Ayrıca 80 mm'lik gövdede Ø54 bobin ve µr = 12 000'lik nanokristal kalkan, arkasındaki anten ve NFC ile manyetik etkileşime girer (RF-20). Nanokristal FeSiB alaşımının geçirgenliği bükülme gerilimi altında manyetostriksiyon nedeniyle değişir. R 15 mm'de µ kayması test edilmemiş.
- **Enerji yoğunluğu:** 1 680 × 6.25 mm² = 10 500 mm² hücre alanı × 1.06 mm ≈ 11.1 cm³. 12 Wh / 11.1 cm³ ≈ **1 080 Wh/L**. Tüm hacim (13.6 cm³) kullanılsa bile ≈ 884 Wh/L. Ticari sıvı elektrolitli pouch hücreler ~700–780 Wh/L. Mikro-hücreler arasındaki elastomer, akım toplayıcılar ve paketleme de hesaba katılınca hedef **gerçekçi değil**.
- **USB-C:** Sözde tek port "1.00 mm `b` çubuğunda". USB-C dişi konnektörün yüksekliği ≈ 2.6–3.5 mm. 1.00 mm'ye **sığmaz**.
- **15×15 mm mmWave AiP**'nin 1 mm'lik çubuğa yerleşimi tanımsız.
- **Bant genişliği tutarsızlığı:** RF-19 5 m'de 800 Mbit/s, §5.2.5 ve RF-14 400 Mbit/s diyor.

### 4.7 Modül sökülünce gövde [DOĞRULANDI]

§5.2.5'e göre "When detached, the B module uses its 400 Mbit/s link". Tüm radyolar `b` modülündeyse ve gövdede anten yoksa (§5.2.2), bu bağlantının **gövde tarafındaki alıcısı** yok. İki olasılık var:

- Gövdede ayrı bir radyo var. Bu durumda "U2 tek çip" önermesi ve anten kuralı çelişir.
- Gövdede radyo yok. Bu durumda modül söküldüğünde gövde çevrimdışı kalır ve yalnızca safe screen gösterir. RF-13'teki "10 m'de bağlantı" testinin bir ucu eksik.

### 4.8 Terim disiplini (ASD-STE100, "one term one meaning")

- "B bar", "B stem", "`b` module" ve "çubuk" aynı parça için kullanılıyor.
- "R" hem köşe yarıçapı (6.35 mm) hem bükülme yarıçapı (25.5 mm) anlamına geliyor. D1'de iki anlam aynı satırda.
- "cassette" (`05 §5.3`, `08 §8.2`) tanımsız. Önceki revizyondan kalmış bir terim.

### 4.9 Ağ ve protokol ayrıntıları

- **Ack'e dayalı delta:** Paket kaybında bir RTT beklenir. Uzak validator ile 150 ms'lik kare duraklamaları olur. FEC ya da referans seçimi (RPS/LTR) tanımlı değil.
- **RG-10 ve SW-10:** Hücresel olmadan CGNAT testi yapılamaz. Wi-Fi'daki çift NAT ise farklı bir durum.
- **Enerji tablosu:** "< 5%: safe screen and optical path only" deniyor. Optik yolun alıcı tarafı (kamera) `b` modülünde ve modül sökülmüşse bu da yok.
- **"No private key custody" değişmezi:** Cihazın SE'sinde anahtar tutulmasıyla bağlam olarak karışıyor. Kuralın kimin için geçerli olduğu (operatörler) açıkça yazılmalı.

---

## 5 · Önerilen düzeltmeler ve yeni gate'ler

| # | Değişiklik | Gate |
|---|---|---|
| 1 | NR sub-6 (en az RedCap) modem, iSIM, gövdede bakır mesh toprak | RF-21 (120 km/h'te sürekli oturum), RF-22 (düşük bant verimi ≥ %20) |
| 2 | `PathPlan.primary: Option`, offline taban, seçimde histerezis ve enerji ağırlığı | SW-14 |
| 3 | Passpoint/EAP, portal durumu için görünür yönlendirme | SW-15 |
| 4 | Girdi günlüğü, kalıcılık ack'i, statik halka tampon (≥ 512 KB) | SW-5b |
| 5 | Sıcak yedek B: önceden imzalı binding, eşik anahtar, sürekli op-log, fencing epoch | RG-4b (algılama ≤ 250 ms, RPO = 0) |
| 6 | Sürüme ve öğeye bağlı semantik girdi, idempotency anahtarı | SW-5c (sıfır yanlış hedef) |
| 7 | Düzenlenebilir alanlarda yerel düzenleme bölgesi ve CRDT. `9.7` tablosunda bu yetki açıkça yazılmalı | DST-1b |
| 8 | Viewport'u imzalı decoder profile'dan ayırmak. Kodlayıcıda MCTS | DSP-x1 |
| 9 | Karo sökülünce etiket ve safe screen'in taşınması | DSP-x2 / RG-16b |
| 10 | Kademeli pinler, karo başına hot-swap denetleyicisi, 55 mF hold-up, hücre başına DC-DC | ENR-x |
| 11 | RF-10 ve RF-13'ü "eksik karo" ve "tam sarım (bilek)" durumlarıyla yeniden koşmak | RF-10b, RF-12b |
| 12 | "Zero-CPU" yerine "uygulama işlemcisi yok, kullanıcı kodu yok" | D7 uyumu |
| 13 | 10.4 tablosunda girdiden göze sütununu sabit yerel değere çekmek. Erişim ağı gecikmesini ayrı bir sütun yapmak | DST-2b |

---

## 6 · Sonuç

1. **Soru 1:** Cihaz bugünkü haliyle **bir ev ve ofis cihazı**. Sokakta ve araçta, ikinci bir cihaz olmadan validator'a ulaşamıyor. Belgelerin kendisi 5G'yi "dış mekânda ana yol" ve uyduyu "hücresel üzerinden" tanımladığı için bu bir tasarım boşluğu değil, **belge seti ile donanım arasında bir çelişki**. Kapalı-portal döngüsü ve `choose()` işlevinin boş kümede çökmesi durumu daha da kötüleştiriyor.
2. **Soru 2:** Yerel eko, devir sırasında kullanıcıya "çalışıyor" görüntüsü veriyor. Ama dayanıklılık, sürüm bağlama ve fencing olmadığı için yazılan karakterler **sessizce kaybolabilir**, dokunuşlar **yanlış öğeye uygulanabilir**, video donar. Tek operatöre bağlı devam jetonu planlanmamış devri sözleşme düzeyinde imkânsız kılıyor. 500 ms ancak sıcak yedek ve sürekli op-log ile, ve yalnızca canlı heap göçü yerine "yeniden yükle ve geri yükle" yaklaşımıyla tutturulabilir.
3. **Soru 3:** C2 akışı mimariye bağlı olarak çökmeyebilir. Ama TCON'un sabit ölçeklemesi görüntüyü **%25 alana** küçültür. Gerçek çözüm validator tarafında yeniden düzenleme. Asıl tehlike görüntü değil, aynı anda gerçekleşen **voltaj çökmesi, anten toprağı kaybı ve etiket ihlali**. Ayrıca 1 200 N tutma kuvvetiyle "< 3 s" söküm mekanik olarak tutarsız.

Belge seti kendi yöntemini de ihlal ediyor: "A result without data is an opinion" diyor, ama SAR, 500 ms, 1–5 ms ve 3–8 ms gibi değerleri ölçüm olmadan olgu diliyle sunuyor. Bu değerlerin `[HYPOTHESIS]` olarak yeniden etiketlenmesi gerekiyor.

### W5_A2_OPUS_FINAL_DIRECTIVE_CONSISTENCY_AUDIT · Model: `claude-opus-5-5` (Router: `claude-coding-router-preview`, Başlangıç: `2026-10-12 15:04:15 +03`, Bitiş: `2026-10-12 15:11:16 +03`, Süre: `420.92 sn`, Uzunluk: `28,474` karakter)

# Budlum Leaf FINAL/ Direktif Denetimi: Kalıntı Değerler, Fiziksel Sınırlar ve 251 Kapı Tutarlılığı

**Kısa sonuç:** İki sorunun cevabı da olumsuz.
- **Soru 1:** Eski değerlerin dördünün de kalıntısı var. R 3.20 mm iki yerde, titanyum göbek dört yerde, 4.0/4.5 mm `b` kalınlığı beş yerde geçiyor. Yeni "tamamı esnek PC-PDMS + NiTi" ifadesi incelenen sekiz dosyanın hiçbirinde yok.
- **Soru 2:** 251 kapı yüzde yüz uyumlu değil. En az 9 sayısal çelişki, 2 çakışan kapı kimliği (aynı numara, iki farklı tanım) ve tamamen eksik iki kapı ailesi (MON, RL) var.

Ayrıca belgelerin kendi sayılarıyla bile fiziksel olarak tutmayan birkaç iddia çıktı: 12 Wh'lik pilin 2.00 mm gövdeye sığmaması, 36.2 °C kesme sınırı, 8 mm sapa USB-C'nin sığmaması ve halkanın arka panelinin hep ekrana bakması.

---

## 0. Kapsam ve yöntem

- Dosyaların her birinde `... [ORTA KISIM KISALTILDI] ...` bölümü var. Görünmeyen metin hakkında "yok" diyemem. Aşağıdaki her tespit görünen metne dayanıyor. "Bulunamadı" dediğim yerler de yalnızca görünen kısım için geçerli.
- Satır numarası verilmediği için her bulguyu **dosya + bölüm + tablo satırı + aynen alıntı** ile gösteriyorum.
- Ölçüt olarak sizin tanımınızı aldım: köşe **R = 6.35 mm** (Group 911.png), **tamamı esnek PC-PDMS + NiTi** (titanyum göbek yok), **ek menteşe parçası olmadan doğal boşluktan 90° büküm**, ve 4.00/4.50 mm `b` kalınlığının artık geçersiz olması.

---

## 1. SORU 1: Eski değerlerin kalıntıları

### 1A. Eski köşe radyusu `R 3.20 mm`

| # | Dosya / konum | Aynen alıntı | Sorun |
|---|---|---|---|
| 1 | `02-panel.md` §2.2, tablo satırı **Cover** | "cut to the outline, printed with the **R 3.20 mm corner** and r 0.80 mm softened edge" | Kesim talimatı hâlâ 3.20 mm. Kalıp ve kesim aparatı yanlış ölçüyle sipariş edilir. |
| 2 | `02-panel.md` §2.8, **DSP-10** | "the cut quality of the **R 3.20 mm corner** and the r 0.80 mm softened rectangular prism edges" | Kabul kapısı yanlış geometriyi doğruluyor. 6.35 mm'lik bir parça bu kapıyı tanım gereği geçemez. |
| 3 | `01-product.md` §1.3 | "**R = 6.35 mm** on Leaf 160 (`R 2.80 mm` on Leaf 80, `R 3.60 mm` on **Leaf 240**, `R 4.50 mm` on Leaf 480)" | Leaf 160 doğru. Ancak **Leaf 240** §1.2 aile tablosunda yok, öksüz bir üye. Buradaki `4.50 mm` bir köşe radyusu, `b` kalınlığı değil. Yanlış alarm olarak işaretliyorum ama metin aramasında takılacağı için not edilmeli. |

**İlgili geometrik çelişki.** `03`/`04` Leaf 80'i "tek çeyrek, 40 × 80 mm, 17 g" olarak tanımlıyor ve Leaf 160'ın Q1..Q4 parçasıyla aynı parça sayıyor. Oysa 6.35 mm köşeli bir Leaf 160'da her çeyreğin **yalnızca bir** dış köşesi yuvarlak, üçü keskin (birleşim yerinde). Tek başına satılan Leaf 80 ise dört köşesi R 2.80 mm olan bir parça olmalı. Yani "Leaf 80 = Q1" denemez. Ayrıca çeyrekler serbestçe yer değiştiremez: 180° dönme simetrisiyle en az iki farklı parça tipi gerekir.

### 1B. Eski "titanyum merkez göbek" (PC-PDMS + NiTi yerine)

| # | Dosya / konum | Aynen alıntı |
|---|---|---|
| 1 | `03-body.md` §3.1.1, satır **Metal frame or midframe** | "3.9 g (`(0,0)` **Ti hub** + `8` **Ti pins** + `24` N52H)" |
| 2 | `03-body.md` §3.1.1, aynı satırın son sütunu | "zero-scratch `+` seam and **Ti micro-dovetail locks**" |
| 3 | `04-energy.md` §4.1, satır **Tool-free quadrant hot-swap** | "**`(0,0)` Ti hub + `8` Ti pins** + `24` N52H (`11.2 N`) + `64` gold leaves" |
| 4 | `04-energy.md` §4.8, adım 5 | "**`(0,0)` Ti hub seat, tapered Ti pins**, `6` bipolar `N52H` magnets, and `16` gold micro-leaf contacts are fitted on each internal edge" |

"PC-PDMS" ve "NiTi" incelenen sekiz dosyanın görünen kısmında **hiç geçmiyor**. Yeni karar FINAL/ dizinine hiç işlenmemiş.

**Bu bir isim meselesi değil, fiziksel bir hata.** Q46 tam sarımı istiyor: `R 25.5 mm`. 2π × 25.5 = **160.2 mm**, yani 160 mm'lik gövde kendi üzerine kapanıp tam bir silindir oluyor.
- Bükme yönüne (x ekseni) paralel duran bir Ti pim de aynı R'ye bükülmek zorunda.
- Ø0.8 mm pimde dış lif gerinimi: ε = 0.4 / 25.5 = **%1.57**.
- Ti-6Al-4V akma gerinimi: σ_y / E ≈ 880 MPa / 114 GPa ≈ **%0.77**.
- Sonuç: pim ilk büküşte kalıcı şekil alır, ve Q46'nın "5 000 döngü hasarsız" iddiası daha ilk döngüde düşer.
- Süperelastik NiTi %6–8 geri dönüşlü gerinim taşır. Tam da bu yüzden değiştirilmesi gerekiyordu.

`(0,0)` göbeği iki birleşim çizgisinin kesiştiği yerde duruyor. Kısa birleşim çizgisi tam bükülme ekseninde. Rijit bir göbek burada sürekli eğriliği keser ve yerel bir kırık köşe oluşturur. Bu durumda "<2.5 µm Z-step" iddiası bükülü halde anlamsızlaşır.

### 1C. Eski "±90° titanyum menteşe varili"

- **Görünen metinde bu ifade aynen geçmiyor.**
- `18` §18.12 kapanış cümlesi "bends with no hinge" diyor. Bu yeni kararla uyumlu.
- **Şüpheli kalıntılar.** Bunlar menteşe döneminden kalma mekanizmalara işaret ediyor ve tanımları görünen kısımda yok:
  - `20` **MEC-29 to MEC-32**: "**the joint**, the three seats, the pen dock and the retired field record".
  - `20` **DSP-14**: "**the joint** against the panel: the touch map and the antenna efficiency".
  - "Joint" ve "three seats" ifadeleri, `06`'daki "4 kenarda × ön/arka = 8 konumlu 90° sap" yapısıyla eşleşmiyor.
- `20` madde 2: "**The upright B module stands on the top edge** … `40 x 32 x 4 mm`, the `b` attaches at its bottom (`y = 0 mm`)". Bu dik duran, üst kenara takılan eski mimari. `06`'daki "halka ekranın üstüne düz yatar" modeliyle doğrudan çelişiyor.
- `01` §1.7: "seals the **bottom slot** with or without a module fitted". Alt yuva da eski yuva/kaset mimarisinin kalıntısı. `04` gövdeyi "portless" ve modülü manyetik sapla tutulan bir parça olarak tanımlıyor.

### 1D. Eski `b` modülü kalınlığı 4.00 / 4.50 mm

| # | Dosya / konum | Aynen alıntı | Not |
|---|---|---|---|
| 1 | `06-module.md` giriş paragrafı | "only the stem (`çubuk`, `8 x 32 x **4.5** mm`) bends" | 4.5 mm |
| 2 | `06-module.md` giriş paragrafı | "circular ring (`yuvarlak`, `32 x 32 x **4.0** mm`) lies flat" | 4.0 mm |
| 3 | `06-module.md` **CAM-14** | "flush fit at `z = 1.60..**4.00** mm`" | 4.00 mm, üstelik aynı dosyadaki "`z = 0.90..3.60 mm`" ile de çelişiyor |
| 4 | `20-charge-path…` madde 2 | "`uploads/b.png` (`40 x 32 x **4** mm`)" | 4 mm. Aynı `b.png` kaynağı `06`'da farklı ölçüyle (sap 32 mm + halka 32 mm) anılıyor |
| 5 | `18-screen-fold-seal.md` §18.10 | "the reference envelope: **3.90 to 4.00 mm** stays as the fallback envelope" | Bu gövde zarfı, `b` değil. Yine de 4.00 mm araması burada takılır, ve 2.00 mm'lik ana tasarımla birlikte yaşaması ayrı bir belirsizlik yaratıyor |
| 6 | `01` §1.3 "`R 4.50 mm` on Leaf 480" | | Yanlış alarm, köşe radyusu |

**Kendi içindeki geometri tutmuyor.**
- **Sapın uzunluğu.** `06` sapı 8 × 32 mm, halkayı 32 × 32 mm diyor. Bu toplamda 64 mm uzunluk eder. `20` ise aynı görsele dayanarak 40 × 32 mm diyor (8 + 32). Sapın uzunluğu 8 mi, 32 mi belli değil.
- **Tek 90° büküm sorunu.** Halka gövde yüzeyinde düz yatıyor ve sap tek bir 90° bükümle kenardan aşağı iniyor. Kenarı kaplayan bacak yalnızca 2.00 mm gövde kalınlığı kadar işe yarar. 32 mm'lik bir sapta kalan **yaklaşık 30 mm arka yüzün ötesine dik olarak taşar**. Masa üstünde ve cepte çarpar, ayrıca kaldıraç oluşturur. Kenarı kavramak için U biçiminde iki büküm gerekir.
- **Sap halkadan kalın.** Sap 4.5 mm, halka 4.0 mm. Sap, halka düzleminden 0.5 mm taşar.

---

## 2. Dosyalar arası mimari çelişkiler

### 2.1 Aynı anda yaşayan üç enerji mimarisi

| Mimari | Nerede |
|---|---|
| (a) **Kaset** | `03` "legacy cassette … Feather/Standard", MEC-3 (kaset çıkarma, 1 000 döngü), §3.8 "the cassette is the unit"; `01` §1.8 adım 2 "choose the cassette fill (default: Feather)" |
| (b) **Sürekli lamine enerji tabakası** (nötr eksende) | `17` Q37/Q38 "removable sheet", "slip sheet 0.06 mm"; `01` §1.7 "dual-lip FKM collar on the **continuous battery sheet**"; `18.10` "the energy sheet, with no cassette" |
| (c) **Dört geçmeli çeyrek** | `03` §3.1, `04` tamamı, `20` ENR-11..13 |

- `01` §1.8 varsayılan olarak kaset seçtiriyor. `18.10` ise "first product: no cassette" diyor.
- `03` §3.8 "pil değiştirilemez, kaset birimdir" diyor. `04` "<3 s çeyrek sıcak değişim" diyor.
- Üçü aynı anda doğru olamaz.

### 2.2 Modüldeki pil için üç farklı değer

| Dosya | İddia |
|---|---|
| `17` Q42 | "**the module carries no cell**" |
| `06` tablo, satır **the cells** | "`0.45 Wh` bridge cell in the B ring" |
| `18` §18.10 | "the module **keeps its 20 Wh**" |
| `06` kural | "Every row that names … a **20 Wh cell** … is **struck**" |

`18.10`, `06`'nın kendi üstü çizme kuralını ihlal ediyor. Ortada 0 Wh, 0.45 Wh ve 20 Wh olmak üzere üç ayrı değer var.

### 2.3 Kablosuz şarj: aynı dosyada hem kaldırılmış hem zorunlu

- `20` madde 1: "**The wireless path is withdrawn** … *Kablosuz şarj olmasın, boşver*". §20.1 bobin + ferrit + yapıştırıcı için "yaklaşık 0.65 mm ve 6 g" kazanç sayıyor.
- **Aynı dosyada** ENR-11..13: "`Qi2.2` (`Ø54 mm`) + `4 x Ø22 mm` wireless coils".
- `03`, `04` §4.1, ENR-6 ve `18.11` CAD maddesi de Qi2.2'yi zorunlu tutuyor.
- `20` MEC-6 "wired and contact charge bench, **in place of the wireless bench**". `03` MEC-6 ise "10, 25, 45, 60 and 80 W". Aynı kimlik, iki farklı tanım.

### 2.4 Portun yeri

- `06` başlık ve tablo: "**sole USB Type-C** … inside the `90°`-bent B stem".
- `20` madde 4: "a detachable module on the **side rail** provides the chosen ports … USB-A … kulaklık".
- `01` §1.1-2: "the jack live[s] in the module".
- Yani tek port sapta mı, ayrı satılan yan port rayında mı, belli değil.

### 2.5 Su geçirmezlik sınıfı

- **IP67 iddia, IP68 hedef:** `01` §1.7, `03` MEC-7, `18` Q43.
- **IP68 geçti diyenler:** `04` §4.8 adım 5 ve 7 ("passes `IP68` (`1.5 m`, `30 min`)"), ENR-5, ENR-11..13, CAM-19, CAM-20.
- MEC-7 "the class claimed is the class measured" diyor. Yani diğer kapılar MEC-7 ile çelişiyor.

### 2.6 Aile geometrisi

| Üye | `01` §1.2 | `03`/`04` | Çelişki |
|---|---|---|---|
| Leaf 80 | **80 × 80**, 2 × P80 | **40 × 80**, 1 çeyrek | Alan iki kat farklı. `01` §1.6-6'daki "iki Leaf 80 = bir Leaf 160" yalnızca 80 × 80'de doğru. 40 × 80'le iki Leaf 80, 80 × 80 eder. |
| Leaf 160² | 4 × P160 | 8 karo, **144 g** | 8 × 17 = **136 g**. 8 g açıklanmamış. |
| Leaf 480 | **480 × 240**, 72 × T40 B | **320 × 480 × 2.40 mm, 48 karo** | 72 × 40 × 40 = 115 200 mm² (480 × 240 ✓). 48 × 40 × 80 = 153 600 mm² (320 × 480). İki farklı ürün tanımlanmış. |
| Leaf 240 | yok | `01` §1.3'te R 3.60 | Öksüz üye |

### 2.7 "Tek hub" kuralı ile hub kapasitesi

- `01` §1.2: "one bus, one or more cassettes and **one hub**".
- `02` §2.7 adım 5: "hub H3 … **128 tiles maximum**".
- Leaf 1400 = 700 karo, bu da **en az 6 hub** demek. Leaf 2800 = 2 800 karo, **en az 22 hub**. Aile kuralı en büyük iki üyede bozuluyor.

### 2.8 Ekran katmanı ve malzeme çelişkileri

- **Kapak kalınlığı.** `02` §2.2'de 250 µm. `03`/`04`'te "`8 x 0.20 mm` PC" ve "PC (`0.20 mm`)".
- **ITO.** `02` §2.2 "with **no indium tin oxide in a bend**" diyor. `04` §4.8 adım 3 "`AgNW/ITO` (`0.04 mm`)" diyor. ITO yaklaşık %1 çekme geriniminde çatlar. Tam sarımlı bir üründe ITO kullanılması `02`'nin kendi gerekçesini çiğniyor.
- **Ekran teknolojisi.** `02` "organic stack with a quantum dot colour layer" diyor. `04` "front/back `T-OLED` … `PDLC`" diyor. İki farklı ekran yığını tanımlanmış.

### 2.9 TCON modülde; modülsüz gövde görüntü veremez

- `04` §4.1 ve `06`: "`U1` Master **TCON** … in the B ring".
- `01` §1.7: gövde ağ olmadan "the safe screen, the wallet" ile çalışmalı. Sızdırmazlık da "with or without a module fitted" olarak tanımlı.
- Zamanlama denetleyicisi çıkarılabilir modüldeyse, **modül takılı değilken gövde hiçbir görüntü üretemez**. Güvenli ekran iddiası düşer.

**Bant genişliği hesabı:**

| Kalem | Değer |
|---|---|
| 508 ppi'de bir yüzün çözünürlüğü | 160 mm → 3 200 px; 80 mm → 1 600 px; toplam 5.12 Mpx |
| Bir yüz, 144 Hz, 24 bit | ≈ **17.7 Gbit/s** |
| İki yüz | ≈ **35.4 Gbit/s** (30 bit ile ≈ 44 Gbit/s) |
| 3:1 sıkıştırma (DSC) ile bile | ≈ 11.8 Gbit/s |
| CAM-15'te tanımlı kablolu bağlantı | **5 Gbit/s** "on top-edge pads" |

- Bu veri 12 manyetik pimden ve birleşim yerlerindeki yaprak yay kontaklardan geçmek zorunda. Hiçbiri 10 Gbit/s üzeri diferansiyel hat için uygun değil.
- "Top-edge pads" ifadesi de 8 konumlu (4 kenar × 2 yüz) sap modeliyle uyumsuz. Her konumda bu pedlerin tekrarlanması gerekir.

### 2.10 Leaf 160'ın alanı

`17` §17.1 "the 256 cm² of a Leaf 160" diyor. Tek yüz 160 × 80 = **128 cm²**. 256, iki yüzün toplamı. Masada yatan bir cihazın bir yüzü kapalıdır, yani hasat hesabı 2 kat iyimser. Sonuç (ışık hasadı yetmez) değişmiyor ama sayı yanlış.

---

## 3. Fiziksel imkânsızlıklar ve sayısal hatalar

### 3.1 Kalınlık bütçesi: 12 Wh, 2.00 mm'ye sığmıyor (en kritik bulgu)

**Hesap 1 (`02` §2.2 katmanlarıyla).**
- Bir yüz: 10 + 250 + 50 + 50 + 20 + 30 + 30 + 120 = **560 µm**. İki yüz **1.12 mm**.
- 2.00 mm gövdede pile kalan pay: 0.88 mm × 12 800 mm² = 11.26 cm³.
- 750 Wh/L'de, %100 paketleme verimi varsayılsa bile: **8.45 Wh**.
- `20` §20.1'deki 0.65 mm bobin + ferrit de eklenirse kalan 0.23 mm → **≈2.2 Wh**.

**Hesap 2 (`04` §4.8 katmanlarıyla).**
- 2 × (0.14 + 0.04 + 0.20) + 0.09 = **0.85 mm**. Buna en az 6 ara yüzde 25–50 µm yapıştırıcı eklenmeli: 0.15–0.30 mm.
- 2.00 mm'de kalan ≈ 0.85–1.0 mm → **en fazla 8.2–9.6 Wh**. Bobinle birlikte ≈ 2.5–3.4 Wh.

**Ek sorunlar:**
- 12 Wh / 750 Wh/L = 16 cm³, yani gövde hacminin (25.6 cm³) **%62.5'i**. Görüntü katmanlarına yer kalmıyor.
- 1 mm altındaki hücrelerde akım toplayıcı ve paketleme payı büyüktür. Paket düzeyinde 750 Wh/L ince formatta gerçekçi değil.
- **Kalınlık çelişkisi:** `04` §4.8 adım 3 "`2.20 ± 0.02 mm` tile stack" diyor, gövde ise 2.00 mm.
- **Kütle:** 68 g / 25.6 cm³ = 2.66 g/cm³ ortalama yoğunluk. Seramik bir hücreyle kâğıt üzerinde mümkün ama mıknatıs, Ti, bobin (6 g) ve kapak için neredeyse pay kalmıyor.

### 3.2 Kapak kütlesi iki kat şişirilmiş

- `03` §3.1.1: "12.8 g (`8 x 0.20 mm` PC)".
- Hesap: 8 × 40 × 80 × 0.20 = 5 120 mm³ = 5.12 cm³ × 1.20 g/cm³ = **6.14 g**.
- 250 µm alınsa bile 7.7 g. 12.8 g ancak 0.42 mm kalınlıkla ya da cam yoğunluğuyla (≈2.5 g/cm³) çıkar. Hata payı ≈ 2.1 kat.

### 3.3 Güç ve çalışma süresi: 0.85 W, direktifin kendi tabanının altında

- `18` §18.2 toplamı: 0.60 + 0.70 + 0.40 + 0.20 + 0.12 = **2.02 W** ✓.
- `17` §17.1 tablosu adresleme terimini (0.20 W) atlıyor: dört terim 1.82 W ediyor, ama metin yine 2.02 W diyor.
- `03`/`04` "**0.85 W Zero-CPU draw**". Yalnızca hub (0.70) ve kimlik/bakım (0.12) toplamı 0.82 W. Işık ve radyoya **0.03 W** kalıyor. Bu fiziksel olarak tutmaz.
- **Aynı tabloda iki farklı güç değeri.** `03` §3.1'de kaset satırı "16 Wh → 7.9 h" diyor: 16 / 2.02 = 7.92, yani 2.02 W kullanılmış. Çeyrek satırı ise 12 / 0.85 = 14.1, yani 0.85 W. Elma ile armut karşılaştırılıyor.
- **Gerçekçi süre:** 12 / 2.02 = **5.9 saat** (delta oturumu), 12 / 3.27 = **3.7 saat** (video). `17`'nin kendi "8 saatlik gün = 16–26 Wh" hesabına göre 12 Wh bir günü karşılamıyor.
- "Delivered" denilen enerjide DC-DC kaybı (≈%10) da düşülmemiş.
- **Leaf 160²:** 24 / 0.85 = **28.2 h**, tablo ">22.0 h" diyor. Kendi formülüyle bile tutmuyor.
- **DSP-5 tasarım gereği kalır.** "Total inside 10 percent" şartı var. 0.85 W iddiasına karşı 2.02 W ölçülürse hata %138 olur.

### 3.4 Isıl sınır: 36.2 °C kesme ürünü kilitler

- Elde tutulan bir yüzeyin derisi ≈ 33–34 °C. Cihaz pasif olarak bu sıcaklığa yakınsar.
- 2.02 W, iki yüz toplam 0.0256 m², h ≈ 10 W/m²K ile: ΔT ≈ 2.02 / 0.256 ≈ **7.9 K**.
  - 25 °C ortamda yaklaşık 33 °C.
  - **30 °C ortamda yaklaşık 38 °C, yani kesme devreye girer.**
- **MEC-11** "35 °C ambient" testi istiyor. Kesmeye **1.2 K** pay kalıyor; cihaz test başlar başlamaz kapanır.
- **Kablosuz şarj:** `20` §20.1'e göre 25 W'ta %83 verimle yaklaşık 5 W ısı. 36.2 °C sınırı ve 25 °C ortamla ΔT ≤ 11 K. Pedde tek yüzden ısı atımı: 10 × 0.0128 × 11 ≈ **1.4 W**. 5 W sürdürülemez; Qi2.2 25 W iddiası bu sınırla çelişiyor.
- **Kamera:** 1.4 W yakalama ısısı, yaklaşık 20 g'lık bir halkada. Yalnızca halka yüzeyiyle (≈16 cm², iki yüz) ΔT ≈ 1.4 / (10 × 0.0016) ≈ **87 K**. Isının gövdeye akması şart. Ama `06` §6.4 0.15 mm, 1 200 W/m·K Cu-grafit tabakanın ısıyı arka AMOLED'den "yalıttığını" söylüyor. **Fiziksel hata:** yüksek düzlem içi iletkenlik ısıyı yayar, yalıtmaz. Grafitin kalınlık yönündeki iletkenliği 5–15 W/m·K, düzlem içinde 1 200. Isı panelin içine yayılır.
- **MEC-6** 60 ve 80 W test istiyor. En yüksek yol USB-C 40 W, Qi 25 W, Dock 27 W. Var olmayan güç seviyeleri test ediliyor.

### 3.5 LLZO/PEO kimyası ile 36.2 °C, 40 W ve 28 mΩ bir arada olamaz

- PEO esaslı elektrolitin iyon iletkenliği 25 °C'de ≈10⁻⁶–10⁻⁵ S/cm. Kullanılabilir 10⁻⁴ S/cm için 60–80 °C gerekir (PEO erime sıcaklığı ≈60 °C'nin üstü). 36.2 °C tavanla hız kapasitesi ≈ **0.1–0.2C**.
- İstenen: 25 W / 12 Wh ≈ **2.1C**, 40 W ≈ **3.3C**. Bu 10–30 kat fazla.
- ENR-1 "<28 mΩ" istiyor. Sıvı elektrolitli 3 Ah'lik telefon hücreleri bile tipik olarak 30–60 mΩ. Oda sıcaklığında PEO-kompozitle ulaşılamaz.
- **Lityum dendrit sınırı:** LLZO'nun oda sıcaklığındaki kritik akım yoğunluğu ≈ 0.5–1 mA/cm². 4 mAh/cm²'lik katmanlarla 3.3C şarj ≈ 13 mA/cm² eder, yani 10 katın üzerinde. Dendrit oluşur ve kısa devre riski doğar. Bu, "0.0 ppm HF, no fire" iddiasının dayandığı kimyanın kendi sınırı.

### 3.6 Bükülme: yapıştırıcı kesme gerinimi ve LLZO kırılması

- **Bağlı yığın.** R 25.5'te 2.00 mm'lik bağlı yığının dış lifi: ε = 1.00 / 25.5 = **%3.9**. İnce film kapsülleme ve TFT ≈ %1'de çatlar.
- **Ayrıştırılmış katmanlar.** "%0.38 PC gerinimi" ancak her katman kendi orta düzlemi etrafında bükülürse çıkar: 0.1 / 25.5 = %0.39 ✓.
- **LLZO %0.22** iddiası, her LLZO alt katmanının 2 × 0.0022 × 25.5 ≈ **0.112 mm** kalınlıkta ve tamamen ayrık olmasını gerektiriyor. Ayrıca LLZO kırılma gerinimi (E ≈ 150 GPa, σ_f ≈ 100–200 MPa) ≈ **%0.07–0.13**. %0.22 bunun üzerinde; seramik çatlar.
- **Yapıştırıcının kesme gerinimi (kaymalı katman ilkesi).**
  - Kayma miktarı: δ = d · s / R, burada s simetri noktasından uzaklık.
  - 80 mm'lik çeyrek, d = 0.2 mm, s = 40 mm → δ ≈ 0.31 mm.
  - 50 µm'lik yapıştırıcıda γ ≈ **6.3 (%630)**, τ = G·γ ≈ 0.5 MPa.
  - Sürekli 160 mm'lik tabakada γ ≈ **%1 250**.
  - Optik yapıştırıcılar tipik olarak %300–1 000 arasında kopar ve sürünür. G = 0.08 MPa'lık bir yapıştırıcı tam sarımda ya katman ayrılmasına ya da kalıcı kaymaya yol açar.
  - Gerçek ayrışma için yağlanmış bir kayma katmanı gerekir. Bu da optik ve sızdırmazlık açısından ayrı bir problem.
- **Halka bükülü ekrana oturmaz.** Ø32 mm kirişin R 25.5'teki sehimi: 25.5 − √(25.5² − 16²) = **5.64 mm**. CAM-7'deki R 60'ta bile **2.17 mm**. Halka bükülü ekrana oturamaz; 7.2 N'luk mıknatıs tutuşu soyulur. Ayrıca 4.0 mm halka, 2.00 mm gövdenin yerel kalınlığını **6.0 mm**'ye çıkarıyor.

### 3.7 Toleranslar: 2.5 µm Z-adımı kendi toleransıyla çelişiyor

- `04` §4.8 adım 3: tek karo "`2.20 ± 0.02 mm`". Komşu iki çeyrek arasında en kötü durum adımı **40 µm**. ENR-5 ise "**<2.5 µm**" istiyor. Kendi üretim toleransı hedefin 16 katı.
- **Isıl genleşme uyumsuzluğu.** PC ≈ 65–70 ppm/K, Ti-6Al-4V 8.6, LLZO ≈ 15.
  - Göbek–pim aralığı 40 mm ve ΔT 40 K için uyumsuzluk: 40 × 60·10⁻⁶ × 40 ≈ **96 µm**.
  - 12 µm'lik birleşim dudağı ve <15 µm birleşim yeri bunun yanında küçük kalıyor. Pimler sıkışır ya da boşluk açılır.
  - PC ile LLZO arasındaki ≈55 ppm/K fark, lamine hücrede döngüsel gerilme yaratır.
- **12 µm dudak ile IP68.** Kalıplanmış PC'nin tipik toleransı ±20–50 µm, 80 mm'lik parçada çarpılma onlarca µm. 12 µm'lik bir elastomer dudak bu toleransı karşılayamaz. Ayrıca toplam birleşim uzunluğu ≈ 240 mm ve parçalar 3 saniyede çıkarılabiliyor. 1.5 m su basıncı (14.7 kPa) altında böyle bir sızdırmazlık sınıfı ölçülmeden IP68 yazılmış.
- **"Zero internal bezel".** İnce film kapsüllemenin kenar mührü genellikle 0.3–1 mm ölü bant ister. 508 ppi'de piksel aralığı 50 µm, yani bu ölü bant **6–20 piksellik** bir koyu çizgi demek. Fresnel hesabı doğru: n 1.585 / 1.586 için R ≈ 1·10⁻⁷. Ama görünürlüğü belirleyen kırılma indisi değil, bu ölü bant. Ayrıca fenil-fluorosilikonla n = 1.585 elde etmek sınırda bir iddia: flor indisi düşürür.
- **Sıcak değişimde akım darbesi.** Paralel bağlı çeyreklerden biri farklı şarj durumundayken takılırsa: ΔV 0.3 V / (28 + 18 mΩ) ≈ **6.5 A** ani akım. Ayrıca bir çeyrek çıkarılınca ekranın %25'i kaybolur ve merkezdeki Qi bobini bölünür. "Zero reboot" ifadesi görüntü açısından anlamsız.
- **ENR-3 "Dead-Pad".** "Pins remain at 0 V until handshake" deniyor. Ama el sıkışmayı yapacak kripto elemanın da beslemeye ihtiyacı var. Ayrı bir düşük güçlü kimlik doğrulama hattı tanımlanmamış.

### 3.8 Kablosuz şarj geometrisi

- Ø54 mm'lik "4-sector" merkez bobin, dört çıkarılabilir çeyreğe bölünmüş. Sargıların AC akımını birleşim yerlerindeki kontaklardan geçirmesi gerekir. Sertifikalı Qi bobini tek parça olmak zorunda.
- **Bobinin merkezinde metal.** `(0,0)` Ti göbek ve 24 adet N52H tam bobin merkezinde. Ti göbek yabancı cisim gibi ısınır, mıknatıslar ferriti doyurur.
- **Pil ekranlaması.** Bobin iki ekran arasında, tam alanlı pilin yanında. Pilin Cu/Al akım toplayıcıları bir yüzden gelen alanı keser. Diğer yüzde de dokunmatik metal ağı ve OLED katodu var.
- "<0.08 µT ELF" metriği anlamsız. Qi 110–205 kHz'te çalışır, ELF bandının dışındadır. N52H'nin yüzeydeki statik alanı da ≈0.1–0.5 T.

### 3.9 B modülünde geometrik çakışmalar

- **USB-C sapa sığmıyor.**
  - USB Type-C spesifikasyonunda fiş ağzı 8.34 × 2.56 mm, dişi soket dış kabuğu ≈ **8.9 mm** genişlik.
  - Sap **8.0 mm** geniş. Gövde duvarı için yer bir yana, soketin kendisi bile girmiyor.
- **Kablo çekilince modül düşer.** USB-C'nin ayırma kuvveti dayanıklılık testinden sonra 8–20 N aralığında. Sapın manyetik tutuşu **7.2 N**. Kablo çekildiğinde modül gövdeden ayrılır, fiş sokulurken de itilir.
- **Katlamalı optik sığmıyor.** CAM-18 "3.4 + 14.0 mm" yol istiyor. 3.4 mm'lik dikey bacak, `06`'daki kamera penceresine (z 0.90..3.60 = **2.7 mm**) ve CAM-14'teki pencereye (1.60..4.00 = **2.4 mm**) sığmıyor.
- **Ø24 delik iki işe birden ayrılmış.** Aynı delikte Ø22.4 mm aktif alanlı arka AMOLED (paneli ≈Ø24+, 0.6–1.0 mm kalınlık), kamera, piezo OIS ve odaklama var. Kalan z yüksekliğinde 3.4 mm'lik prizma bacağı için yer yok.
- **Halkanın içi aşırı dolu.** Halka (Ø32 dış / Ø24 iç × 4 mm) ≈ **1 407 mm³**. 0.45 Wh pil 750 Wh/L'de ≈ 600 mm³, yani **%43**. Kalan ≈800 mm³'e 9 × 3.2 × 2.2 mm hoparlör, 2 mikrofon, flaş, 6 katmanlı kart, TCON, UWB/mmWave modülü ve ekran sığmalı.
- **Arka panel her zaman ekrana bakıyor.** Halka ekranın **üstüne düz yatıyor**, yani bir yüzü daima Leaf ekranına dayalı. CAM-17'deki "rear round AMOLED … selfie viewfinder" ve CAM-20'deki "rear polycarbonate O-ring" yüzü ön yüze de takılsa arka yüze de takılsa **her zaman Leaf yüzeyine bakar**. Hiçbir zaman görünmez.
- **Kenar kalabalığı.** Kalem "side edge" boyunca manyetik tutunuyor (`06`). Aynı kenarlarda sapın konumları ve `20`'deki yan port rayı da var. Ayrıca yaklaşık 6 mm çaplı bir kalem 2.00 mm'lik kenarda kararsız durur: temas genişliği yalnızca 2 mm.

### 3.10 MEC-28 tork hesabı yaklaşık 10 kat hatalı

- 21 g → F = 0.021 × 9.81 = **0.206 N**.
- 40 N·mm için kaldıraç kolu = 40 / 0.206 ≈ **194 mm**. Bu cihazın kendisinden uzun.
- Gerçekçi kol ≈ 20 mm → **≈4.1 N·mm**.
- 56 N·mm şartı güvenli tarafta kalıyor, ama türetimi yanlış. Ayrıca 21 g, `06`'nın 20.0 g değeriyle çelişiyor.

### 3.11 Görüş açısı başına piksel (ppd) hatası, Leaf 160²

Formül: ppd = ppi × mesafe (inç) × tan 1°.

| Üye | Hesap | Belge |
|---|---|---|
| Leaf 80, 25 cm | 508 × 9.84 × 0.01746 = 87.3 | 87 ✓ |
| Leaf 160, 30 cm | 104.7 | 104 ✓ |
| **Leaf 160², 40 cm** | 508 × 15.75 × 0.01746 = **139.6** | **130 ✗** |
| Leaf 480 / 1400 / 2800 | 62.7 / 104.8 / 167.7 | ✓ |
| Field modu, 20 mm | ham ≈ 7.0 | "about 27". Yaklaşık 3.9× büyüten bir optik gerekiyor, ama tanımlı değil |

### 3.12 Leaf 1400 ısı ve kapak kütlesi

- **Isı akıl yürütmesi yanlış.** "73 W, %20 kayıp, 15 W" deniyor. OLED'in elektrikten ışığa verimi ≈ %15–25, yani yaklaşık **55–62 W panelde ısıya döner**. Sonuç değişmiyor (≈0.005 W/cm², doğal taşınım yeterli, ΔT ≈ 5 K), ama gerekçe hatalı.
- **Kapak kütlesi.** 1.12 m² × 0.15 mm × 1.2 g/cm³ ≈ **0.20 kg**, belge 0.9 kg diyor. 0.9 kg için yaklaşık 0.67 mm PC gerekir. Kapak satırı kısaltılmış bölüme denk geldiği için 0.15 mm'nin kapağa ait olduğu kesin değil, ama kütle bütçesi tutmuyor.

### 3.13 Diğer küçük tutarsızlıklar

- `17` §17.17: "Bare tier, **1.2 mm**, 20 g". İki yüzlü ekran yığını tek başına 0.85–1.12 mm. Pile yaklaşık 0.1–0.35 mm kalıyor.
- `03` §3.1'de iki "The rule" paragrafı neredeyse aynı (kopyala-yapıştır kalıntısı).
- `01` §1.7 "the weld is a workshop operation" diyor; `04` ise aletsiz geçme tanımlıyor.
- `01` §1.7 "dual-lip FKM collar … bottom slot". Kayan bir modül için dudaklı sızdırmazlık contası IP68'de nadiren tutar. Kaldı ki gövdede yuva yok.

---

## 4. SORU 2: 251 kapının sayısal tutarlılığı

### 4.1 Doğrulanabilirlik

- **MON-1..20:** Yalnızca `HARDWARE/20`'ye referans olarak geçiyor. Görünen metinde **tek bir eşik yok**.
- **RL:** Görünen metinde **hiç geçmiyor**.
- **B-1, B-2:** Yalnızca MEC-1'de "carry the product claim" olarak anılıyor, tanımları yok.
- **Referansı olup tanımı görünmeyenler:** MEC-16, MEC-19 ("owns the number"), ENR-7, DSP-11, DST-5.
- **CAM:** `06` CAM-1..20 diyor, ama görünen kısımda CAM-10..13 yok.
- Bu yüzden **251 sayısı bu dosyalardan yeniden kurulamıyor**. Sayının kendisi doğrulanamıyor.

### 4.2 Eşik çelişkileri

| Parametre | Çelişen kapılar | Değerler |
|---|---|---|
| Su geçirmezlik | MEC-7 / Q43 ↔ ENR-5, ENR-11..13, CAM-19, CAM-20, §4.8 | IP67 iddia ↔ IP68 geçti (1.5 m / 30 dk) |
| Bükülme döngüsü | ENR-2 · DSP-8 · Q46 · §4.8 adım 7 | 10 000 · 10 000 sonra 100 000 · **5 000** · 10 000 |
| Bükülme radyusu | MEC-1 · ENR-2 · CAM-7 | R 25.5 ve R 70 · R 25.5 · **R 60** |
| B modülü kütlesi | `06` / `03` · CAM-14 · MEC-28 | 20.0 g · **21.0 g** · **21 g** |
| Kamera z aralığı | `06` tablosu · CAM-14 | 0.90..3.60 · 1.60..4.00 |
| Şarj gücü | MEC-6 (`03`) · ENR-6 · `20` MEC-6 | 10–80 W · Qi 25 / USB-C 40 / Dock 27 W · yalnızca kablolu ve kontaklı |
| Sıcaklık | ENR-4 / ENR-6 ≤36.2 °C ↔ MEC-11 35 °C ortam | 1.2 K pay; test başlarken kesme |
| Güç modeli | DSP-5 / MEC-9 (±%10) ↔ 0.85 W iddiası | Ölçüm 2.02 W olursa hata %138 |
| Z-adımı | ENR-5 <2.5 µm ↔ §4.8 ±0.02 mm | En kötü durum 40 µm |
| Hizalama | DSP-3 ±20 µm ↔ birleşim yeri <15 µm | 15 µm'lik boşluk ≤±7.5 µm hizalama ister |
| Kütle yasası | MEC-2 "law of §3.1" | §3.1'de iki yasa var (Rev A formülü ve 68/88 g). Hangisine göre ölçüleceği belirsiz |
| Kablosuz şarj | `20` madde 1 ↔ `20` ENR-11..13 | Aynı dosyada kaldırıldı ve zorunlu |

### 4.3 Çakışan kimlikler

- **MEC-6:** `03`'te "seated and removed, 10–80 W", `20`'de "in place of the wireless bench". Aynı numara, iki farklı test.
- **DSP-10:** Geçersiz R 3.20 mm geometrisini doğruluyor. Kapı numarası aynı kalsa da içeriği yanlış.

---

## 5. Öncelikli düzeltme listesi

1. **Hemen düzeltilecek metinler:** `02` §2.2 ve DSP-10'da R 3.20 → R 6.35. `03` §3.1.1, `04` §4.1 ve §4.8'de Ti göbek/pim → PC-PDMS + NiTi. `06` başlığı ve CAM-14 ile `20` madde 2'de `b` ölçüleri.
2. **Mimari karar:** Kaset, sürekli tabaka ve çeyrek yapısından **tek birini** bırakmak gerekiyor. Diğer ikisi ve onlara bağlı kapılar (MEC-3, `01` §1.8 adım 2, §3.8) üstü çizilmeli. `18.10`'daki "20 Wh module" satırı silinmeli.
3. **Kablosuz şarj kararı:** `20` ile `04` uzlaşmalı. Kablosuz şarj kalacaksa kalınlık bütçesine 0.65 mm eklenmeli; kaldırılacaksa ENR-11..13 ve ENR-6 revize edilmeli.
4. **Fiziksel bütçenin yeniden kurulması:** 2.00 mm'de pil en fazla ≈8 Wh (bobinsiz). Çalışma süreleri 2.02 W ile yeniden hesaplanmalı. 36.2 °C kesme sınırı ile PEO kimyası uyumsuz: sınırın gerekçesi gözden geçirilmeli (IEC 62368-1'in uzun süreli temas sınırları 43–48 °C civarında), ya da kimya değiştirilmeli.
5. **B modülü:** Sap genişliği USB-C için ≥10.5 mm olmalı. Tutuş kuvveti >20 N olmalı, ya da port sapın dışına taşınmalı. Arka panelin hep ekrana bakması ve bükülmede halkanın açılması (5.6 mm) geometrik olarak çözülmeli.
6. **TCON:** Zamanlama denetleyicisi gövdeye alınmalı. Yoksa modülsüz ekran ve güvenli ekran iddiası düşer.
7. **Sayısal hatalar:** Leaf 160² için ppd 130 → 140, MEC-28 torku (≈4 N·mm), kapak kütlesi (≈6 g), Leaf 160² kütlesi (136 g) ve süresi (formülle 28 saat), Leaf 480 geometrisi, Leaf 80 tanımı, hub sayısı kuralı.
8. **Kapı kaydı:** MON, RL ve B eşikleri FINAL/ içine işlenmeli. Ardından 251 kapının tam listesi tek tabloda, çakışan kimlikler temizlenmiş haliyle yeniden çıkarılmalı.


---

## DALGA 6 · KIRMIZI TAKIM (RED-TEAM) 20 GERÇEK KULLANIM SENARYOSU STRES TESTİ VE NİHAİ HATA KAYIT DEFTERİ (`claude-opus-5-5` BAŞDENETÇİ SENTEZİ)

### W6_A1_OPUS_CHIEF_RED_TEAM_SYNTHESIS · Model: `claude-opus-5-5` (Router: `claude-coding-router-preview`, Başlangıç: `2026-10-12 15:11:16 +03`, Bitiş: `2026-10-12 15:21:08 +03`, Süre: `591.99 sn`, Uzunluk: `45,291` karakter)

# BUDLUM LEAF 160 · REVİZYON L.5.0: RED-TEAM KULLANIM SİMÜLASYONU VE NİHAİ HATA/ÇÖZÜM MATRİSİ

**Denetlenen dosyalar:** `AUDIT/ARENA-MULTI-AGENT-QUAD-PLUS-AND-BENT-B-REPORT.md`, `HARDWARE/00-HARDWARE-INDEX.md`, `NEREDE-NE-VAR.md`
**Yöntem:** Araç çalıştırmadım. Ölçüm, simülasyon ya da CAD sorgusu yok. Tüm sayılar belgelerde yazan değerlerden ve standart malzeme ve fizik sabitlerinden elle hesaplandı. Belgelerin "[ORTA KISIM KISALTILDI]" diye kesilen bölümlerini göremedim. Bu bölümlere dayanan yargıları **(K)** ile işaretledim. Orada çelişkiyi çözen bir bilgi olabilir.
**Denetçi tutumu:** Belgede yazan hiçbir sayıyı doğru kabul etmedim. Her iddiayı fizik sınırına, endüstri standardına ve öteki dosyalarla tutarlılığa karşı sınadım.

---

## 0 · YÖNETİCİ ÖZETİ

L.5.0 mimarisi bu haliyle **üretilemez, sertifikalandırılamaz ve günlük kullanımda çalışmaz.** Sorun tek bir hata değil. Birbirini dışlayan beş temel tasarım ilkesi aynı anda isteniyor:

1. **"Tamamen esnek (2.00 mm, R 25.5 mm)"** ile **"< 15 µm görünmez optik derz"** bir arada olamaz. Polikarbonatın ısıl genleşmesi tek başına 80 mm'de 20 K için **112 µm** oynama yaratır.
2. **"Şeffaf T-OLED / gözlük"** ile **"tüm alana yayılmış 1.06 mm pil + nanokristalin kalkan"** bir arada olamaz. Pil ve ferromanyetik kalkan opaktır.
3. **"≤ 36.2 °C termal kilit"** ile **"25 W Qi2.2 / 40 W USB-C"** ve **"LLZO/PEO katı-hal pil"** bir arada olamaz. PEO, 36 °C'de iyon taşıyamayacak kadar yavaştır. 25 W şarjda çıkan ısı da bu sıcaklık sınırında atılamaz.
4. **"Sıfır-CPU"** ile **Wi-Fi 7, 50 MP kamera, video akışı, PD 3.1, kriptografik el sıkışma ve DP 2.1** bir arada olamaz. Bu işlevlerin her biri bir işlemci gerektirir.
5. **"1.00 mm yatay çubuk"** ile **"USB Type-C prizi"** bir arada olamaz. Prizin ağzı 8.34 × 2.56 mm, derinliği yaklaşık 6.6 mm'dir.

**Toplam:** 21 KRİTİK, 22 MAJÖR, 15 MİNÖR bulgu (ayrıntısı Bölüm 4'te).

---

## 1 · HESAPLARDA KULLANILAN SABİTLER

| Büyüklük | Değer | Kaynak / not |
|---|---|---|
| PC elastisite modülü E | 2.3–2.4 GPa | Lexan/Makrolon sınıfı |
| PC akma gerinimi | ~%6–7 | "> %30 elastik uzama" iddiası buna aykırı |
| PC ısıl genleşme katsayısı (CTE) | 65–70 ppm/K | |
| PC ısıl iletkenliği k | 0.20 W/m·K | |
| PC su buharı geçirgenliği | ≈ 4 g·mm/(m²·gün), 38 °C / %90 RH | |
| OLED için gereken WVTR | ≤ 10⁻⁶ g/(m²·gün) | Endüstri hedefi |
| PC çevresel gerilme çatlağı (ESC) kritik gerinimi | ~%0.3–0.5 (IPA, güneş kremi, el kremi) | |
| Silikon (PDMS) kırılma indisi | 1.40–1.43 (fenil-silikon en fazla ~1.53) | 1.585'lik silikon OCA gerçekçi değil |
| NdFeB özdirenci ρ | ~1.5 µΩ·m | |
| Altın ρ / NiTi ρ | 0.0244 / 0.82 µΩ·m | |
| USB-C priz ağzı / fiş kabuğu | 8.34 × 2.56 mm / 8.25 × 2.40 mm | USB Type-C Spec R2.x |
| USB-C takma / çıkarma kuvveti | 5–20 N / 8–20 N | Aynı spec |
| İnsan gözü uyum gücü | 25 yaşta ~10 D (yakın nokta 100 mm), 45 yaşta ~3–4 D | |
| Doğal taşınım + ışınım ısı transfer katsayısı h | ≈ 10–11 W/m²·K | Düz yüzey, 25 °C ortam |

---

## 2 · 20 GERÇEK KULLANIM SENARYOSU

### SENARYO 1: 1.00 mm yatay üst çubuğa standart USB-C kablosu takmak

**Geometri (rapor §1.2):** Çubuk `x ∈ [0, 32]`, `y_local ∈ [36.0, 37.0]` (1.00 mm), `z_local ∈ [−2.00, +0.80]` (2.80 mm).

**a) Fiziksel sığma.** Fişin iki takılma yönü var, ikisi de olmuyor:
- **Uçtan, x yönünde takmak:** 8.34 × 2.56 mm'lik ağız, 1.00 × 2.80 mm'lik kesite girmek zorunda. Genişlikte **8.34 / 1.00 = 8.3 kat** taşma var. Geometrik olarak imkânsız.
- **Üstten, −y yönünde takmak:** 32 × 2.80 mm'lik üst yüze 8.34 × 2.56 mm ağız sığar, ama z yönünde duvar başına yalnızca **0.12 mm** kalır. Priz metal kabuğunun dış yüksekliği zaten ~3.0–3.2 mm olduğundan bu bile tutmaz. Asıl engel derinlik: priz 1.00 mm'lik çubuğa değil, altındaki ekran gövdesine **~5.6 mm** gömülür. Oysa belgeye göre gövdede "zero USB-C, zero port" var ve o hacmi pil dolduruyor. Bu doğrudan bir CAD çakışması.
- IP68 sınıfı bir priz, ağız ile gövde arasına sızdırmazlık plakası ve O-ring ister (+0.3–0.5 mm). Yer yok.

**b) Mıknatıs kopma kuvveti ve torku.** B modülünün kenar klipsi **7.2 N** (`HARDWARE/10`).
- USB-C çıkarma kuvveti en az **8 N**. Fiş çekildiğinde modül her seferinde fişten önce gövdeden kopar. Takma kuvveti (5–20 N) aşağı, gövdeye doğru bastırdığı için takma sırasında sorun yok. Sorun çıkarmada.
- Yan yük: fiş kalıbı ve kablo boynu yaklaşık **25 mm** kaldıraç kolu yaratır. Modülü tutan moment kabaca `7.2 N × 16 mm (halka yarıçapı) ≈ 0.115 N·m`. Kritik yan kuvvet `0.115 / 0.025 ≈ 4.6 N`. Şarjdayken telefonu elde kullanan biri kabloyu 5–10 N ile rahatça çeker, modül ayrılır.
- Kopma anında VBUS 20 V / 2 A yük altında açılır. Altın pedlerde ark ve pitting oluşur. 3 ms Dead-Pad el sıkışması kopmayı **algılayıp önlemez**, ancak kopma olduktan sonra fark eder.

**c) Ek tutarsızlıklar.**
- "40 W PD 3.1" sınıflandırması yanlış değil, PD 3.1 SPR kapsamında. Ama PD anlaşması bir PD denetleyicisi, yani bir MCU ister. Bu "Sıfır-CPU" iddiasıyla çelişir.
- DP 2.1 (UHBR20, 20 Gbit/s/hat) sinyali 1 mm'lik çubuk, 4.381 mm'lik boğaz köprüsü ve mıknatıslı yay pedler üzerinden empedans kontrolüyle geçirilemez.

**Hüküm:** KRİTİK. B-01, B-02, B-03.

---

### SENARYO 2: Yapbozda 4. karoyu (0,0) köşesine takmak (aşırı kısıtlama)

**Kinematik.** Düzlemdeki rijit bir karonun 3 serbestlik derecesi vardır (x, y, θz).
- **Kırlangıç kuyruğu kalınlık yönünde kilitliyse** (Z'de tutuyorsa), diş ancak kendi derz ekseni boyunca kaydırılarak takılabilir. 4. karo bir kenarda Q2'ye (x derzi), öbür kenarda Q3'e (y derzi) aynı anda girmek zorunda. Bir derz x yönünde, öteki y yönünde kaydırma ister. **Kapalı halkadaki son parçanın montajı** kinematik olarak imkânsızdır (burr bulmacasının son parçası sorunu). Aynı problem 4×4 ızgarada 3 iç düğümde tekrarlanır.
- **Diş düzlem içinde trapez ise** (Z'den indirilen tip, belgedeki "+Z ve −Z'den takılabilir" ifadesi bunu ima ediyor), montaj mümkündür. Ama bu durumda **Z yönünde hiçbir mekanik tutma yoktur.** Karoyu Z'de tutan tek şey 24 mıknatısın toplam 11.2 N'u, yani tutturma yerinde **karo başına yaklaşık 2.8 N** kalır. Bükme sırasında derzde Z yönünde kesme kuvveti oluşur, karolar yerinden fırlar.
- İki kenardan kenetleme, 3 serbestlik derecesine karşı 4 kısıt (2 × 2) koyar. Fazla olan kısıt θz dönüşüdür ve toleransı emecek yer kalmaz.

**Tolerans yığılması:**
- Kalıplama: 80 mm'de ISO 20457 TG4 ≈ ±0.05–0.10 mm.
- 4×4 ızgarada x ve y zincirlerinin birleştiği noktada kapanma hatası ≈ `√3 × 50 µm ≈ 87 µm` (RSS). Derz boşluğu ise 15 µm. Bu **72 µm'lik zorlamalı geçme** demek.
- 3 mm'lik diş yanağında 72 µm, yaklaşık **%2.4 yerel gerinim** üretir. Bu PC'nin akmasına (%6) uzak, ama çevresel gerilme çatlağı eşiğinin (%0.3–0.5) **5–8 katı**. Sonuç: gerilme beyazlaması ve çatlama (craze).
- Isıl genleşme: 160 mm'de `70×10⁻⁶ × 160 × 20 K = 224 µm`. Bir kış sabahı ile yazın araç içi arasındaki fark tek başına derzi 15 kat aşar.

**Diş mukavemeti:**
- Ağız başına 100 N, 3 mm × 0.9 mm (2.7 mm²) boyun kesitinde **37 MPa** gerilme yaratır. PC-PDMS'in akma dayanımı ~45–55 MPa. Emniyet katsayısı yalnızca **~1.3**.
- 80 µm'lik NiTi telin kesiti 0.005 mm². 800 MPa plato geriliminde taşıyabildiği yük **~4 N**, yani 100 N'un %4'ü. "NiTi çekirdekli 100 N/diş" iddiasında yükün asıl taşıyıcısı tel değil polimer.

**Hüküm:** KRİTİK. M-01, M-02, M-03.

---

### SENARYO 3: Qi2.2 pedinde (360 kHz, 25 W) mıknatıs, altın yaprak ve NiTi'de girdap (Eddy) akımı ısınması

**Deri derinliği** `δ = √(ρ / (π f µ))`, f = 360 kHz için:
- NdFeB (ρ 1.5 µΩ·m, µr ≈ 1.05): δ ≈ **1.0 mm**. Mıknatıs boyutuyla aynı mertebede, yani hacim tümüyle ısınır.
- Altın: δ ≈ **131 µm**. Yapraklar ~2 µm kalınlıkta, δ'dan çok ince.
- NiTi: δ ≈ **0.76 mm**. 80 µm'lik tel δ'dan çok ince.

**Isıl güç**, ince levha yaklaşımıyla `P/V = π² f² B² d² / (6ρ)`:
- **N52H mıknatıs** (d = 1 mm, 2 mm³): Bobin sargısının hemen yanında, kalkanın yoğunlaştırdığı akıda B ≈ 10 mT olur. Bu durumda mıknatıs başına **~28 mW**. Ø54 bobin içinde kalan 6–8 mıknatıs için toplam **0.2–0.7 W**. PC içine gömülü 2 mm³'lük bir cismin ısıl direnci ≈ `1/(4π k r) ≈ 500 K/W`. Yerel ısınma **ΔT ≈ 14 K**. 36.2 °C kilidi yalnızca bu yüzden bile tetiklenir.
- **Altın yapraklar** tek başına ihmal edilebilir: yaklaşık 3.5 kW/m³, yaprak başına µW mertebesi. Asıl tehlike, yaprakların ve derz bus izlerinin **kapalı iletken halka** oluşturması.
- **NiTi tel** de tek başına ihmal edilebilir: 10 mm'lik tel parçasında ~8 µW. Ama tel 10 × 10 mm'lik kapalı bir çerçeve oluşturursa, B = 2 mT'de indüklenen gerilim `EMF = 2π f B A ≈ 0.45 V` olur. Halka direnci ~6.5 Ω, halka başına kayıp **~31 mW**.

**Bunlardan büyük sorunlar:**
1. **Yabancı cisim algılama (FOD):** Qi2 vericisi, hesaba katılmayan ~0.3–0.5 W kaybı yabancı cisim sayar ve gücü düşürür ya da şarjı keser. Mıknatıslar ve kalkan doygunluğu bu eşiği tek başına aşar. Pratikte 25 W hiç görülmez.
2. **Kalkan doygunluğu:** FeSiBCuNb'nin doyum akısı ~1.2 T. N52H'nin kalıcı akısı (Br) 1.43 T. Mıknatısa komşu kalkan bölgeleri doyar, µr yerel olarak ~1'e düşer. Kuplaj çöker, kalkan ısınır.
3. **µr = 12 000 iddiası:** Mikro-kırıklı nanokristalin şerit 360 kHz'de tipik olarak µ' ≈ 1 000–3 000 değerindedir ve yüksek µ'' (kayıp) taşır. Bu frekansta 12 000 gerçekçi değil.
4. **Bobin derzi kesiyor:** Ø54 bobin "4 çeyrek sektörün birleşmesiyle" oluşuyor. N sarımlı (tipik 10–14) bir bobin, her sarımda 4 derz geçişi demek, yani 40–56 kontak. Kontak başına 10–30 mΩ eklenince toplam direnç ~1 Ω olur. Bu, Q faktörünü ve verimi çökertir. Derz başına ayrılmış altın yaprak sayısı (64 / 4 = 16) bunu karşılamaz.
5. **Qi2 MPP mıknatıs halkası:** Qi2 spesifikasyonu belirli bir manyetik profil ister. Merkezden geçen "+" şeklindeki 24 mıknatıs bu profili bozar. Sertifika alınamaz.

**Hüküm:** KRİTİK. Q-01, Q-02, Q-03; MAJÖR Q-04.

---

### SENARYO 4: %100 ve %15 doluluktaki karoları birleştirmek (dengeleme akımı)

ΔV ≈ 4.20 − 3.60 = **0.60 V** (NMC katot varsayımıyla).

Burada bir ikilem var. Belgedeki iki iddia aynı anda doğru olamaz:
- **A) 40 W şarj iddiası doğruysa:** 40 W toplamda ~10.5 A, karo başına 2.6 A (3.3C) eder. Bunu 0.1 V'tan az aşırı gerilimle kabul etmek için karo iç direnci ≤ 40 mΩ olmalı. Bu durumda birleşme anındaki akım `I = 0.6 / (0.04 + 0.04 + ~0.01 kontak) ≈ **6.7 A = 8.3C**`. Lityum metal anotta bu dendrit üretir. Mikro altın kontaklar (tipik 0.3–0.5 A/kontak) aşırı yüklenir. Kontak sekmesi (bounce) sırasında ark oluşur.
- **B) Gerçekçi PEO kimyası (25–36 °C):** Alan başına direnç (ASR) ≈ 50–500 Ω·cm². 32 cm²'lik karoda R ≈ **1.5–15 Ω**. Dengeleme akımı 20–200 mA ile sınırlı, güvenli. Ama karo başına sürekli çekilebilecek güç ≈ 0.75 W'tan az olur. Bu durumda 40 W, 25 W, ekran, Wi-Fi 7 ve 60 GHz hiçbiri çalışmaz.

**Ek sorunlar:**
- 3 ms'lik Dead-Pad yalnızca kontak geldikten sonra gücü açar. O anda ΔV'yi bir yük anahtarının (MOSFET) güvenli çalışma alanı karşılamak zorunda. Yumuşak açılış (slew) ve akım sınırlama belirtilmemiş.
- Her karonun **kendi çift yönlü DC-DC dönüştürücüsü** olmadan karoları güvenli şekilde paralel bağlamak mümkün değil. 2 mm'lik yığında bu dönüştürücünün bobini (≥ 0.6 mm) için yer ayrılmamış.
- 1 680 mikro-hücrenin karo içinde kendi aralarında dengelenmesi ayrı bir sorun. Seri ve paralel topoloji tanımsız.

**Hüküm:** KRİTİK. E-01; MAJÖR E-02.

---

### SENARYO 5: Gözlük modunda 15 mm'den T-OLED'e odaklanmak

- 15 mm'ye odaklanmak **1/0.015 = 66.7 D** uyum gücü ister. Göz en iyi ihtimalle (çocuk) ~10–14 D, 45 yaşında ~3 D sağlar.
- Eksik kalan odak gücü ΔD ≈ 57–64 D. 3 mm'lik gözbebeğinde açısal bulanıklık `β ≈ p · ΔD = 0.003 × 57 ≈ 0.17 rad ≈ **9.7°**`. Bir metin karakteri ~0.3° tutar. Bulanıklık lekesi karakterden ~30 kat büyük. Hiçbir şey okunamaz, ekran yalnızca ışıklı bir sis olarak görünür.
- Kolimasyon için f ≈ 15 mm'lik (+67 D) bir pancake, birdbath ya da freeform optik gerekir. Bu en az 8–20 mm kalınlık ekler ve "2 mm gözlük" iddiasını geçersiz kılar.
- Optik eklense bile çözünürlük kaba kalır. 400 ppi'de piksel aralığı 63.5 µm, f = 15 mm ile **14.5 açısal dakika/piksel** eder. Normal görme ~1 açısal dakikadır, yani 14.5 kat kaba. Belirgin ızgara (screen-door) etkisi görülür.
- Ergonomi: Göz bebekleri arası mesafe ~63 mm. 80 mm'lik karo her göze 8.5 mm kenar payı bırakır. Kirpik boyu 8–12 mm, 15 mm'lik göz mesafesi sınırda.

**Hüküm:** KRİTİK. O-01. Senaryo 20 ile birlikte gözlük modu bütünüyle çöküyor.

---

### SENARYO 6: Polikarbonatın nem bariyeri yetersizliği (T-OLED kararması)

- 0.18 mm'lik PC kabuğun su buharı geçirgenliği ≈ `4 / 0.18 ≈ **22 g/(m²·gün)**`. OLED gereksinimi 10⁻⁶. Fark **2.2 × 10⁷ kat, yani 7 mertebe**.
- Silikon OCA ve PC-PDMS kopolimeri durumu daha da kötüleştirir. PDMS, su buharını en kolay geçiren polimerlerden biridir. Kenarlardan nemin yanal sızması OCA katmanı boyunca hızla ilerler.
- Her karonun 4 kenarı açık. Sökülüp takılabilir tasarımda kenar boyu 4 × 240 mm = **960 mm**, tek parça bir telefonun ~480 mm'lik kenarının iki katı.
- T-OLED'in yarı saydam katodu (Mg:Ag 10–15 nm veya IZO) nemle **saatler ile günler içinde** karanlık nokta ve kenardan büzülme gösterir.
- **LLZO** nem ve CO₂ ile H⁺/Li⁺ değişimine girer, yüzeyde Li₂CO₃ ve LiOH oluşur ve ara yüz direnci artar. Lityum metal anot varsa suyla tepkime H₂ gazı açığa çıkarır.
- Çözüm ince film kapsülleme (ALD Al₂O₃ ile çok katmanlı organik). Ama bu katmanlar **~%0.5–1 gerinimde çatlar**. Çekirdekte R 25.5 mm'de gerinim (aşağıda) çok daha yüksek. Esneklik ile bariyer çelişiyor.

**Hüküm:** KRİTİK. W-01, W-02.

---

### SENARYO 7: 0.04 mm silikon OCA'nın kayması ve sürünmesi

Çok nötr düzlemli tasarımda dış kabuk çekirdeğe göre kayar. Kayma miktarı `δ = d · θ / 2`. Burada d, kabuk nötr düzleminin çekirdek ortasına uzaklığı: `1.00 − 0.09 ≈ 0.91 mm`.
- **Tam büküm (R 25.5 mm, L 160 mm):** θ = 160 / 25.5 = 6.27 rad. Bu neredeyse tam bir silindir: çevre 2π × 25.5 = 160.2 mm. Uçlarda kayma `δ ≈ 0.91 × 3.14 ≈ **2.85 mm**`. OCA'da kayma gerinimi `γ = 2.85 / 0.04 ≈ **71, yani %7 100**`. Belgede verilen %400 uzamanın **18 katı**.
- **Kısmi büküm (yalnızca 40 mm'lik bölge):** θ = 1.57 rad, δ ≈ 0.71 mm, γ ≈ **%1 780**. Bu da sınırın 4.5 katı.
- **Sürünme:** Telefon cepte bükülü bekletilince G = 0.035 MPa ile kayma gerilmesi küçük kalır, ama viskoelastik sürünme ile kabuk kalıcı olarak kaymış kalır. Görünür etkiler: kenarda kabuk ile çekirdek arasında **milimetrik basamak**, kenar mührünün yırtılması ve yapboz dişinin hizalamayı kaybetmesi.
- **< 15 µm derz ile çelişki:** Kabukların karo başına bağımsız kayması, komşu karoların yüzeylerini 100–1000 µm kaydırır.
- **Kesme modülü tutarsızlığı:** Ajan 3'te G = 0.05 MPa, Ar-Ge tablosunda G = 0.035 MPa.
- **Çekirdek hâlâ gerilmiş:** Kabuklar ayrıştırılsa bile 2.00 − 2 × 0.18 − 2 × 0.04 = **1.56 mm'lik çekirdeğin** yüzeyinde gerinim `1.56 / 51 = **%3.06**`. "%3.92 ortadan kaldırıldı" iddiası yanıltıcı. Pil, T-OLED ince film transistörleri ve ITO bu çekirdekte. ITO ~%1'de, ince film kapsülleme %0.5–1'de çatlar.

**Hüküm:** KRİTİK. F-01, F-02.

---

### SENARYO 8: Cep tüyü ve tozun < 15 µm derzi bozması

- Pamuk lifinin çapı 11–22 µm, polyester 12–25 µm. PM10 tozu ≤ 10 µm. Kum taneleri 60–2 000 µm. Tek bir pamuk lifi 15 µm'lik derzi tam kapanmaz hale getirir. Diş yanağına sıkışan lif ortalama 10–20 µm'lik bir kalıcı aralık bırakır.
- **Mıknatıslar demirli tozu çeker.** Derzdeki N52H'ler kumdaki manyetit ve demir talaşı gibi parçacıkları toplar. Kuvars (Mohs 7) PC'yi (kurşun kalem sertliği ~2B–HB) çizer. "Çiziksiz, kendini onaran dudak" iddiasının malzeme karşılığı yok. Kendini onaran polimerler yalnızca µm derinliğindeki çizikleri ve genellikle ısıyla onarır, PC bu sınıfta değil.
- Altın yapraklarda sebum, ter ve tozla birlikte temas direnci mΩ'lardan Ω'lara çıkar. Bu, daha önce hesaplanan güç ve sinyal sorunlarını büyütür.
- **Derz kenarı yuvarlatmaları (MİNÖR değil, KRİTİK geometri hatası):** `00-INDEX` her karoda "12 kenar r 0.65 mm" diyor. Komşu iki karonun yuvarlatılmış kenarları derzde **1.30 mm genişliğinde, 0.65 mm derinliğinde bir oluk** oluşturur. Bu oluk tüy ve kir tuzağıdır ve kendi başına "görünmez derz" iddiasını çürütür.

**Hüküm:** MAJÖR D-01, D-02; KRİTİK G-03 (oluk).

---

### SENARYO 9: Tek karo çıkarıldığında L şeklindeki ekranda video izlemek

Kalan alan, birinin çıkarılmasıyla oluşan 3 × (40 × 80 mm) = 9 600 mm²'lik bir L.
- Yatay 16:9 en iyi yerleşim: 80 mm genişlikteki 2×1 blok içinde 80 × 45 mm = 3 600 mm². Kullanım oranı **%37.5**.
- Dikey kolonda yatay video: 40 mm yüksekliğe 71 × 40 = 2 844 mm² sığar.
- Her iki durumda da görüntünün ortasından **siyah bir derz çizgisi** geçer. OLED'in kapsülleme ve kapı sürücü (GOA) sınırı her kenarda ~0.3–1.0 mm ölü bant bırakır. İki karo yan yana gelince 0.6–2.0 mm'lik **görünür siyah haç** oluşur. Bu, sistemin "sıfır görünür çizgi" iddiasını her senaryoda çürütür.
- Ø54 Qi2.2 bobinin bir sektörü gider. Bobin açık devre kalır, **Qi2.2 çalışmaz.** Ø22'lik yerel bobinle ~5 W'a düşülür, bu da Senaryo 12'deki ısıl sınırla daha da azalır.
- B modülü çıkarılan karoya bağlıysa ekran bağlantısı kopar. B modülüne komşu olmayan bir karo, görüntü verisini başka bir karonun derzinden geçirerek almak zorunda.
- **Bant genişliği:** 1260 × 2520 px'lik ekranda karo başına ≈ 0.79 Mpx × 24 bit × 120 Hz ≈ **2.3 Gbit/s**. Bunun derz yapraklarından empedans kontrollü diferansiyel çiftlerle taşınması gerekir. Derz kolu başına 16 yaprak güç, toprak, Qi sarımları, I²C ve görüntü verisi için yetmez.
- **Video çözme:** Sıfır-CPU bir sistemde H.264/HEVC/AV1 çözücü yok. Video akışı hiç başlayamaz (Senaryo 16).

**Hüküm:** MAJÖR V-01, V-02; KRİTİK S-01 (CPU yokluğu).

---

### SENARYO 10: Hücresel modem yokken dış ortamda bağlantı

- Radyo listesi Wi-Fi 7, BLE 5.4, UWB ve 60 GHz'den ibaret. **LTE/5G, GNSS ve eSIM yok.**
- Wi-Fi erişim noktası olmayan her yerde (sokak, araç, doğa) internet yok, navigasyon yok. **Acil çağrı (112) yapılamaz.** Cihaz "telefon" olarak pazarlanırsa bu hukuki risktir: AB'de 112 erişimi (EECC 2018/1972) ve eCall beklentisi.
- 60 GHz'in pratik menzili ~5–10 m ve insan vücudu sinyali ~20–30 dB zayıflatır. UWB konumlandırma sabit çapalar ister.
- Telefona bağlı kullanım (hotspot) ikinci bir cihaz gerektirir. "Tek cihaz" iddiası düşer.
- Anten yerleşimi: 2.4 GHz'de λ/4 = 31 mm. 32 mm'lik çubuk uzunluk olarak yeterli. Ama 1 mm yüksekliğinde, AgNW ağı ve Cu kalkanının 0–2 mm yakınında duruyor. Toprak düzlemine bu yakınlık verimi −6 ile −10 dB arasında düşürür, ele tutunca uyumsuzluk ek kayıp getirir.
- **Maruziyet ölçütü yanlış:** "SAR 0.054 W/kg" 6 GHz üzeri (60 GHz) için uygun ölçüt değil. ICNIRP 2020 ve FCC bu bantta **soğurulan güç yoğunluğu (W/m²)** ister. Gözün önündeki 60 GHz dizisi için bu ölçüm hiç yok.

**Hüküm:** KRİTİK R-01 (pazar ve yasal); MAJÖR R-02, R-03.

---

### SENARYO 11: Belgeler arasında kalan eski revizyon izleri

| # | Konu | Dosya A | Dosya B | Etki |
|---|---|---|---|---|
| X1 | Dış köşe radyusu | `R = 6.35 mm` (Rapor, NEREDE) | `R 3.20 mm` (`00-INDEX` §3, dosya 06 açıklaması) | Kalıp ve STL tanımsız |
| X2 | Karo köşe radyusu | Leaf 80 `R 2.69` / 160 `R 3.20` / 160² `R 3.81` | Hepsi aynı 40 × 80 karodan oluşuyor | Aynı karo üç farklı radyusa sahip olamaz (G-01) |
| X3 | B modülü yönelimi | "Çubuk ekran üst kenarına **yatay** oturur, 1 mm yükselir" (Rapor) | "Only the stem bends 90° **up**, ring lies **flat on the screen**" (`00-INDEX`) | İki farklı ürün |
| X4 | Halka yönü | "Bize doğru bakan yuvarlak" | "Ring lies flat on the screen" | Ön ya da arka kamera ve AMOLED belirsiz |
| X5 | Menteşe | "Ek menteşe parçası eklemeden doğal boşluktan büküm" | `13`: "`±90°` **Ti hinge**" | Parça listesi ve kütle çelişkili |
| X6 | (0,0) göbeği | Ar-Ge tablosu: "**hiçbir rijit metal blok yoktur**" | P13 ve `leaf160-frame.stl`: "**(0,0) Ti göbek**" | CAD ile şartname uyuşmuyor |
| X7 | Kabuk gerinimi | `%0.35` (Rapor) | `%0.38` (`12-THE-BEND-LAW`) | Bükme yasası belirsiz |
| X8 | OCA kesme modülü | `G = 0.05 MPa` (Ajan 3) | `G = 0.035 MPa` (Ar-Ge 2) | |
| X9 | Şeffaf iletken | `AgNW/ITO` (INDEX, P-serisi) | `AgNW/IZO` (Ar-Ge 5) | |
| X10 | Diş malzemesi | `Nitinol/Ti-PEEK` (NEREDE, Ajan 2) | `NiTi + PC-PDMS` (Ar-Ge 3) | |
| X11 | Kalkan kalınlığı | `0.10 mm Cu-Grafit` (Rapor §5) | `0.15 mm kalkan` (P15) | |
| X12 | STL sayısı | "13 STL" (INDEX 07, NEREDE) | Listede 3 + 1 + 4 + 3 = **11** | Teslimat eksik |
| X13 | Render sayısı | "8 render" | Listede **7 PNG** | |
| X14 | Pafta sayısı | "toplam 25 temiz SVG + STACK" = **26** | `check_sheets.py`: "tüm **32** SVG" | Doğrulama aracı başka bir kümeyi sayıyor |
| X15 | Leaf 160² kütlesi | `144 g` | 8 × 17 g = **136 g** | 8 g açıklanmamış |
| X16 | Leaf 480 kalınlığı | `2.40 mm` | Aynı `2.00 mm` karodan 48 adet | Karo tanımı değişmiş |
| X17 | Malzeme | "Tamamen polikarbonat" | P18: "**Corning** kenar-sarmalı iletkenler" | Cam ile PC çelişkisi |
| X18 | 60 GHz kalkanı | P20: "**Mu-metal** göz kalkanı" | 60 GHz'de µr'nin anlamı yok, iyi bir iletken yeter | Yanlış malzeme gerekçesi |
| X19 | Çubuk genişliği | b.png çubuğu `u = 0..4.0 mm` | Büküm: `u ∈ [0, 3.6]`, z kalınlığı `2.80 mm` | 4.0, 3.6 ve 2.8 aynı ölçü olamaz |
| X20 | Vadi geometrisi | Halka merkezi `(24, 16)`, R_in 12 | "Vadi `(16,16)` merkezli R 12" | Vadi, halka gövdesini u = 4..28 aralığında keser |
| X21 | Zarf | b.png `40 × 32`, çubuk 1 mm | STL zarfı `40 × 44 × 6.70 mm` | 44 mm ve 6.70 mm'nin kaynağı tanımsız; "2 mm cihaz" halkada 6.7 mm |
| X22 | Görsel ölçeği | `Group 911.png` 800 × 1920 px ↔ 80 × 160 mm | x: **10 px/mm**, y: **12 px/mm** | Anizotrop: R = 63.5 px x'te 6.35 mm, y'de 5.29 mm (eliptik köşe) |
| X23 | IoU hassasiyeti | `IoU = 0.999987` | Kenar piksel nicemlemesi (~4 800 px çevre × 0.5 px) IoU'yu ≈ 0.998 ile sınırlar | Uydurma hassasiyet |
| X24 | Parça sayımı | Port rayı "42 parça" (14 + 28) | Çubuktaki USB-C B modülünün 32 parçasında da sayılıyor | Ürün ağacında çift sayım |

**Hüküm:** MAJÖR DOC-01 ile DOC-05 arası; MİNÖR'ler matriste.

---

### SENARYO 12: Qi2.2 ile 25 W şarj ve 36.2 °C termal kilit

- İzin verilen sıcaklık artışı 25 °C ortamda `36.2 − 25 = 11.2 K`. 35 °C'lik yaz ortamında **1.2 K**.
- Bir yüz pede yatıyor (ve ped de ısınıyor). Isı yalnızca öbür yüzden atılabilir: `Q = h · A · ΔT ≈ 11 × 0.0128 × 11.2 ≈ **1.6 W**`.
- 25 W giriş, alıcı bobin, doğrultucu ve şarj devresinin toplam ~%85 verimiyle cihaz içinde **~3–4 W** ısı üretir. Bunun üzerine pilin I²R kaybı eklenir.
- Isıl kapasite ≈ 88 g × 1.2 J/g·K ≈ 105 J/K. Fazladan ~2 W ısı ile kilit **~10 dakikada** devreye girer. Sonrasında sürekli şarj gücü ~5–8 W'a düşer. Yazın sıfıra yaklaşır.
- **PEO kimyası:** PEO-LiX'in iyon iletkenliği 25 °C'de 10⁻⁶–10⁻⁵ S/cm. Kristal bölgelerin eridiği ~60 °C'nin altında kullanışlı değil. 36.2 °C'lik kilit, pilin çalışma sıcaklığına ulaşmasını kendisi engelliyor. LLZO dolgulu kompozitlerde en iyi laboratuvar değerleri ~10⁻⁴ S/cm. Gerçekçi şarj hızı C/10–C/5, karo başına 80–160 mA.
- **Enerji yoğunluğu:** 3.0 Wh / (40 × 80 × 1.06 mm = 3.39 cm³) = **885 Wh/L**. Ticari en iyi Li-ion hücreler ~750–800 Wh/L. Hele 2.5 mm adımlı 420 mikro-hücrenin hücre arası boşluk ve kenar mührüyle aktif alanı ≤ %75 olur. Bu durumda aktif malzemenin **~1 180 Wh/L** vermesi gerekir. Fiziksel olarak savunulamaz.
- "Flor içermeyen LiBOB" tuzu doğru olabilir, ama elektrot bağlayıcısı (PVDF) genellikle florlu. "0.0 ppm HF" iddiası ölçümle desteklenmemiş.

**Hüküm:** KRİTİK P-01, P-02, P-03.

---

### SENARYO 13: Bükerken derzde kıvrılma ve (0,0)'da çift eğrilik

- Derzde kabuklar karo bazında kesik. Eğilme momentini yalnızca 0.9 mm'lik çekirdek dişleri taşır.
- `EI_diş / EI_karo ≈ (0.9 / 1.56)³ ≈ 0.19`. Ayrıştırılmamış monolit karoya göre `(0.9 / 2.0)³ ≈ 0.09`. "EI_derz / EI_karo = 1.00 ± 0.01" iddiası **5 ile 11 kat** hatalı.
- Aynı moment altında eğrilik `κ = M / EI`, yani derzde **5–11 kat** artar. Karoda R 25.5 mm iken derzde **R ≈ 2.3–5 mm** olur. Dişin dış lifinde gerinim `0.45 / 2.3 ≈ **%19.6**`. PC kopma ve akma bölgesinde. Beyazlama ve kopma ilk birkaç yüz çevrimde gelir. "200 000 çevrim, sıfır beyazlama" iddiası desteksiz.
- (0,0)'da 4 karo birleşir. Bir levha iki eksende aynı anda bükülürse (Gauss eğriliği) düzlem içi gerinim kaçınılmazdır. "+" haçının merkezi en zayıf ve en yüklü düğüm. Bir yerde rijit "Ti göbek" (P13), başka bir yerde "metal yok" deniyor (X6).
- Parmakla bükme kuvveti "1.4 N" diye verilmiş, ama 1.56 mm'lik pil ve ekran çekirdeğinin rijitliği hesaba katılmamış.

**Hüküm:** KRİTİK M-04; MAJÖR M-05.

---

### SENARYO 14: Güneş kremi, el antiseptiği ve kozmetiğe maruz kalma

- PC; IPA, etanol, oktokrilen ve oksibenzon (güneş kremi), el kremindeki esterler ve sebumla **çevresel gerilme çatlağı (ESC)** gösterir. Kritik gerinim ~%0.3–0.5.
- Tasarım gerinimi tam bu aralıkta: kabukta %0.35–0.38. Derz ve dişte %2.4 (Senaryo 2) ile %19.6 (Senaryo 13). Pandemi sonrası yaygın alkol jeli kullanımıyla haftalar içinde craze ağı ve sonunda gevrek kırılma beklenir.
- PC UV altında sararır (YI artar). UV kararlılaştırıcı veya UV-sertleştirilmiş üst kaplama gerekir. Ama sert kaplamalar %1–2 gerinimde çatlar, esneklikle çelişir.
- PC-PDMS kopolimerinde PDMS oranı arttıkça kırılma indisi (~1.57'ye) ve geçirgenlik düşer, puslanma artar. Aynı anda "n = 1.585, %T ≥ %90" ve "> %55 kopma uzaması" tutturulamaz.
- **Silikon OCA kırılma indisi:** Silikonlar 1.40–1.43, fenil-silikonlar en fazla ~1.53. 1.585'lik silikon OCA yok. PC (1.585) ile n 1.41 arasındaki ara yüzde Fresnel yansıması ara yüz başına ~%0.34. Daha önemlisi derz kenarında indis atlaması derz çizgisini **görünür** kılar.

**Hüküm:** KRİTİK C-01; MAJÖR C-02, C-03.

---

### SENARYO 15: Yağmur, yüzme, ter: IP68 derzi ve kontak korozyonu

- 15 µm'lik derzde kılcal giriş basıncı, θ = 100° (hidrofob) için: `ΔP = 2γ|cos θ| / w = 2 × 0.072 × 0.17 / 15×10⁻⁶ ≈ **1.6 kPa**`, yaklaşık **16 cm su sütunu**. IP68 tipik olarak 1.5 m+ (≥ 15 kPa) ister. Derz contasız olduğu için **~10 kat yetersiz**. Hidrofilik veya kirlenmiş yüzeyde (θ < 90°) su kendiliğinden içeri çekilir.
- El sıkışmadan sonra beslenen kontaklar terde (NaCl) elektrolitik korozyona uğrar. Altın yaprağın altındaki Ni bariyerinin gözeneklerinden galvanik korozyon başlar. Kontak direnci yükselir, Senaryo 4 ve 9'daki sorunlar büyür.
- Kenar klipsi 7.2 N olan B modülü suda dalgayla kolayca ayrılır. Çubuktaki USB-C IP68 sızdırmazlığı için hacim yok (Senaryo 1).

**Hüküm:** KRİTİK W-03; MAJÖR W-04.

---

### SENARYO 16: Sıfır-CPU ile fotoğraf ve video çekmek

- 50 MP sensör, 10 bit, 30 fps ham akış ≈ **15 Gbit/s**. Demosaik, gürültü azaltma, HDR birleştirme ve kodlama bir ISP ve bir video kodlayıcı ister. Listede yok: U1 TCON, U2 UWB/60 GHz SiP, U3 Ses DSP, U4 PMIC.
- Bir TCON video çözemez ya da kodlayamaz. "Sıfır-CPU" ise Wi-Fi 7 sürücüsü, TCP/IP, TLS, PD denetleyicisi ve kriptografik el sıkışma ile çelişir. Bunların her biri bir veya daha fazla işlemci çekirdeği gerektirir. Wi-Fi 7 çipinin kendi içinde zaten Arm/RISC-V çekirdekleri var.
- **Sensör boyutu ve optik kalınlık:** 12.8 × 9.6 mm sensörün köşegeni **16 mm**, yani **1 inç tipi** sensör. ~80° görüş açısı için odak uzaklığı f ≈ 9.5 mm, toplam optik yol (TTL) ≥ 9–11 mm olur. P15'te optiğe ayrılan pay `z = 0.90..3.60`, yani **2.70 mm**. "Katlanmış optik" geniş açıda uygulanamaz, prizma yanal 12+ mm ister.
- **Halkanın içi:** Sensör (12.8 × 9.6), halkanın 4 mm'lik et kalınlığına sığmaz. Ø24 mm'lik iç boşluğa yerleşirse "açıklık" kalmaz. Ø22.4 mm'lik AMOLED de aynı boşluğa konulmuş. Bu bir çakışma.
- 3 ms'lik ECDSA P-256 doğrulaması Cortex-M0 sınıfında 10–100 ms sürer. 3 ms için donanım hızlandırıcı gerekir, yani yine bir işlemci.

**Hüküm:** KRİTİK S-01, S-02, S-03.

---

### SENARYO 17: B modülü önde, cepte taşıma ve düşürme

- Halka ön yüze düz yatarsa Ø32 mm, yani **804 mm²** ekran alanını (%6.3) kapatır. T-OLED saydam olduğundan kapanan bölge görünür bir leke gibi durur.
- **Arka AMOLED ana ekrana bakar.** Halka ön yüze yatınca "arkada" kalan Ø22.4 mm'lik AMOLED doğrudan T-OLED'e dönüktür, işlevsiz. Halka arka yüze takılınca bu sefer kamera dışarı, kullanıcının tersine bakar. Ön ve arka kullanım kurgusu tutarsız.
- Halkada cihaz kalınlığı 2.00 + ~4.70 = **6.70 mm**. Cepte takılma, kumaşa sürtünme ve 7.2 N'luk manyetik klipsin kopması beklenir.
- **Düşme:** 1.5 m'den düşen 88 g'lık cihazın çarpma enerjisi ≈ `0.088 × 9.81 × 1.5 ≈ 1.3 J`. Üst kenara düşerse ilk temas, USB-C ve antenin bulunduğu 1 × 2.8 mm'lik çubuktur. Kesme yükü çubuğun kesitini aşar. Mıknatıslar ayrılır, 4 karo da ayrı ayrı saçılabilir (kilit 2.8 N/karo).
- **Isı:** 40 W girişte modüldeki 20 V'tan pil gerilimine dönüşüm ~%92 verimle **~3.2 W** ısı çıkarır. 20 g'lık modül bu ısıyı ekranın üstünde, sıcak nokta olarak bırakır. 36.2 °C kilidi yine tetiklenir.

**Hüküm:** MAJÖR B-04, B-05, B-06; KRİTİK B-07 (çubuk düşme kesmesi).

---

### SENARYO 18: Mıknatıslar: kartlar, kalp pili, kutup çevirme

- Manyetik şeritli kartların koersivitesi düşük (300 Oe / 2 750 Oe). N52H'nin 1–3 mm yakınındaki alan 0.3–0.5 T, şeritli kartları siler.
- Kalp pili ve ICD'ler için ISO 14117 uyarınca ~1 mT (10 G) üzerinde mıknatıs modu tetiklenebilir. Gömlek cebinde taşıma için kullanıcı uyarısı ve 15 cm kuralı gerekir. Belgede bunun izi yok.
- B modülü 4 kenar × 2 yüz = **8 yönelimde** takılabiliyor. Ters çevrilince kutuplar ya iter ya yanlış pede hizalanır. Ped haritasının yansıma ve dönme simetrik olması gerekir (USB-C mantığı), bu da ped sayısını ikiye katlar. Tanımlı değil.
- NiTi'de nikel açığa çıkması: PC içine gömülü olduğu için düşük risk. Ama aşınma veya kopmada EN 1811 sınırı (0.5 µg/cm²/hafta) sorgulanmalı.

**Hüküm:** MAJÖR MG-01, MG-02; MİNÖR MG-03.

---

### SENARYO 19: Kışın −10 °C dış ortam

- PEO, −10 °C'de iletkenliği 10⁻⁸ S/cm mertebesine düşer. **Cihaz fiilen kapanır.** Kendini ısıtmak için gereken enerjiyi de pil veremez.
- Süperelastik NiTi'nin Af sıcaklığı tipik olarak 10–25 °C. Bunun altında malzeme martensitiktir ve bükülme şeklini kendiliğinden geri almaz. Takılıp çıkarılan dişler kalıcı biçim değiştirir. Ayrıca PC'nin ~280–300 °C enjeksiyon sıcaklığı NiTi'yi yaşlandırarak Af'yi kaydırabilir.
- −10 °C'den +22 °C'ye girince derzde ve OCA kenarında yoğuşma olur. Bu, Senaryo 6'daki nem sorununu hızlandırır.
- 32 K'lik sıcaklık farkı 160 mm'de **~360 µm** ısıl genleşme farkı demek. Derz ya açılır ya kasılır (Senaryo 2).

**Hüküm:** KRİTİK P-04; MAJÖR M-06.

---

### SENARYO 20: Gözlükte saydamlık, ağırlık ve güvenlik

- Her karoda tüm alana yayılmış **1.06 mm katı-hal pil ve FeSiBCuNb kalkan** var. İkisi de **opak**. Leaf 80'i gözlük olarak takan kullanıcı **hiçbir şey göremez.** Şeffaf T-OLED, PDLC ve AgNW'nin şeffaf olmasının bir anlamı kalmaz. Bu mimarinin en temel çelişkisi.
- Pil ve kalkan saydam olsaydı bile (olamaz) T-OLED ~%40, PDLC açıkken ~%80, AgNW ~%90, iki PC kabuk ~%90 × 0.9 geçirir. Toplam ≈ **%23**. ISO 12312-1'e göre kategori 2–3 güneş gözlüğü sınıfı. Gece sürüşü için ≥ %75 gerekir, yani **yasak.**
- **PDLC mahremiyet sağlamaz.** PDLC ışığı açılı bir panjur gibi kesmez, her açıda saçar. Kapalı halde süt beyazıdır ve OLED görüntüsü bulanır. Sürülmesi 30–60 V AC ister, yani göze 15 mm mesafede bir yükseltici dönüştürücü.
- Ağırlık: 17 g karo ve 20 g B modülü toplam **37 g**. Tipik gözlük ağırlığının (~20–30 g) üstünde. Ağırlık merkezi önde, burun pedi basıncı yüksek.
- Leaf 80'in 4 köşesi de yuvarlaksa, 4'lü birleşimde (0,0)'da bir delik oluşur (G-01). Köşeler keskinse göz çevresinde kesik ve göz yaralanması riski doğar.

**Hüküm:** KRİTİK O-02, O-03; MAJÖR O-04, O-05.

---

## 3 · GEOMETRİK ÇAKIŞMA VE TOLERANS ÖZETİ

| Kod | Çakışma | Sayısal kanıt |
|---|---|---|
| G-01 | Karo köşe radyusları ile "+" merkezi | Her karonun 4 köşesi R yuvarlaksa merkezde kalan boşluk `(4 − π) R²`. R 2.69 için **6.2 mm²**, R 3.20 için **8.8 mm²**, R 6.35 için **34.6 mm²** delik. Yalnızca dış köşesi yuvarlak tutulursa 4 karo **aynalı ve farklı** parça olur. O durumda "4 eşit karo" iddiası düşer ve yedek parça 4 ayrı SKU gerektirir. |
| G-02 | USB-C prizi ile ekran gövdesi | Priz derinliği ~6.6 mm, çubuk 1.0 mm. **5.6 mm gövdeye ve pile girer.** |
| G-03 | r 0.65 kenar yuvarlatmaları ile derz | 1.30 × 0.65 mm'lik oluk. < 15 µm iddiasının 87 katı genişlik. |
| G-04 | b.png vadi yayı ile halka gövdesi | Vadi (16,16) merkezli R 12, u = 4..28 aralığını kaplar. Halka u = 8..40 aralığında. **Kesişir.** |
| G-05 | Boğaz köprüsü (u 4..12.5, v 0..4.381) | 4.381 mm'lik büküm hattından USB-C'nin 24 sinyali, VBUS 2 A (≥ 0.5 mm iz), 4 yüksek hızlı çift, 60 GHz besleme ve anten hatları geçmeli. 60 GHz esnek hatta ≥ 1 dB/cm kaybeder. |
| G-06 | Kamera sensörü ile halka iç boşluğu ve AMOLED | Sensör 12.8 × 9.6 mm (köşegen 16) ve Ø22.4 AMOLED aynı Ø24 boşlukta. Optik yol 2.7 mm ayrılmış, ≥ 9 mm gerekli. |
| G-07 | 2.00 mm'lik Z yığını | 0.36 (kabuk) + 0.08 (OCA) + 1.06 (pil) = 1.50 mm. T-OLED + PDLC (0.2–0.4), AgNW, Litz-FPC (0.10–0.15), kalkan (0.06 + yapıştırıcı), BMS ve NTC için yalnızca **0.50 mm** kalıyor. PDLC filmi tek başına 0.2–0.4 mm. **Taşar.** |
| G-08 | Kalıplama, ısıl ve nemle genleşme | Kalıp ±50 µm. Isıl 80 mm'de 20 K için 112 µm. Nemle şişme ~%0.1, 80 mm'de **80 µm**. Toplam ≫ 15 µm. |

---

## 4 · NİHAİ HATA VE ÇÖZÜM MATRİSİ

### 4.1 · KRİTİK (BLOCKER): ürün çıkışını engelleyen bulgular

| ID | Senaryo | Bulgu | Fizik ve sayı | Çözüm | Doğrulama kapısı |
|---|---|---|---|---|---|
| **B-01** | 1 | USB-C 1 mm'lik çubuğa sığmıyor | Ağız 8.34 × 2.56 mm, kesit 1.0 × 2.8 mm; derinlik 6.6 mm, gövdeye 5.6 mm giriyor | Çubuğu ≥ 3.3 mm kalınlık × ≥ 7.5 mm derinlik yap ya da USB-C'yi halkaya taşı. "1.00 mm" iddiasını kaldır. | CAD girişim analizi: sıfır çakışma; USB-IF mekanik uyumluluk |
| **B-02** | 1 | Modül tutma kuvveti fiş çıkarma kuvvetinin altında | 7.2 N < 8 N (min), yan yükte kritik kuvvet 4.6 N | Mekanik kilit (bayonet, mandal) ve ≥ 25 N tutma; ya da USB-C'yi gövdeye al | 10 000 çevrim tak/çıkar + 15 mm kolla 8 N yan yük testi |
| **B-03** | 1 | Yük altında açılmada VBUS arkı | 20 V / 2 A, kopmayı önceden algılama yok | Önden gelen kısa algılama pimi (first-break) ve VBUS'u µs mertebesinde kesen sıcak takma denetleyicisi | Kopma testi, ped erozyon mikroskopisi |
| **B-07** | 17 | Düşmede ilk temas 1 × 2.8 mm'lik çubuk | 1.3 J darbe, kesit kesmede yetersiz | Çubuğu gövde içine göm ya da paslanmaz/Ti iç takviye koy | IEC 60068-2-31, 1.5 m × 26 yön |
| **M-01** | 2 | Kapalı halkada son karo montaj kinematiği | Z'de tutan kırlangıç kuyruğu dik iki eksende aynı anda kayamaz | Dişi Z'den indirilen geçmeye çevir ve Z tutmayı ayrı mandalla sağla; ya da tek eksenli raylı montaj | Montaj sırası simülasyonu, < 3 s montaj testi |
| **M-02** | 2, 19 | < 15 µm derz ile ısıl/nemli/kalıp toleransı uyumsuz | 112 µm (ısıl) + 80 µm (nem) + ±50 µm (kalıp) | Derzi görünür ve tasarlanmış bir çizgi olarak kabul et (≥ 0.2 mm, contalı); "görünmez" iddiasını kaldır | −20…+60 °C, %95 RH döngüsünde derz ölçümü |
| **M-04** | 13 | Derzde rijitlik 5–11 kat düşük, gerinim %19.6 | `(0.9/1.56)³ = 0.19`, R_yerel ≈ 2.3–5 mm | Derzi nötr düzlemde sürekli bir alt taşıyıcıyla (PI veya ince çelik folyo) köprüle; ya da derzin bükme bölgesinden geçmesini yasakla | 4 noktalı eğme, DIC gerinim haritası, 200 000 çevrim |
| **G-01** | 11, 20 | Köşe radyusu ile "+" merkez deliği ve karo eşliği | 6.2–34.6 mm² boşluk ya da 4 farklı SKU | Tek bir R değeri seç; iç köşeler keskin ya da < 0.2 mm; ayrı SKU'ları kabul et | CAD ve STL tutarlılık betiği |
| **G-03** | 8 | r 0.65 kenar yuvarlatması derzde oluk açıyor | 1.30 × 0.65 mm oluk | Derz kenarlarında r ≤ 0.05 mm pah; r 0.65'i yalnızca dış çevreye uygula | Profilometre |
| **Q-01** | 3 | Ø54 bobin 4 derzden geçiyor | 40–56 kontak, ~1 Ω ek direnç, Q çöküşü | Ana Qi bobinini tek karoya ya da B modülüne taşı; sektör bobin olmasın | Qi2.2 sertifika ön testi (WPC) |
| **Q-02** | 3 | Mıknatıslarda girdap akımı ve FOD | Mıknatıs başına 28 mW, ΔT 14 K, FOD eşiği 0.3–0.5 W | Bobin alanında mıknatıs yasakla; segmentli ve lamine NdFeB kullan | Termal kamera, FOD kalibrasyonu |
| **Q-03** | 3 | Kalkan doygunluğu ve Qi2 MPP profili bozuk | Bsat 1.2 T < Br 1.43 T; MPP halkası çakışıyor | Mıknatısları bobin halkasının dışına al; MPP spesifikasyonuna uyan halkayı kullan | WPC MPP hizalama testi |
| **E-01** | 4 | Farklı SoC'deki karolar birleşirken akım veya güç ikilemi | 6.7 A (8.3C) ya da < 0.75 W/karo | Karo başına çift yönlü DC-DC dönüştürücü, yumuşak paralelleme, ideal diyot | ΔV 0.6 V ile sıcak takma testi, MOSFET SOA ve ark ölçümü |
| **O-01** | 5 | 15 mm'de odaklanılamaz | 66.7 D gerekli; bulanıklık 9.7° | Kolimasyon optiği (pancake veya dalga kılavuzu) ekle ya da gözlük modunu iptal et | MTF ve göz kutusu ölçümü |
| **O-02** | 20 | Pil ve kalkan opak, gözlük saydam değil | 1.06 mm opak katman tüm alanda | Gözlükte pili sapa veya çerçeveye taşı, optik alanı tamamen pasif bırak | Işık geçirgenliği ölçümü (ISO 12311) |
| **O-03** | 20 | Toplam geçirgenlik %23, gece sürüşü yasak | ISO 12312-1 kategori 2–3 | Optik alanda yalnızca T-OLED (≥ %70), PDLC yok | ISO 12312-1 testi |
| **W-01** | 6 | PC'nin su buharı geçirgenliği OLED için 7 mertebe yüksek | 22 g/m²/gün'e karşı 10⁻⁶ | İnce film kapsülleme (ALD ve çok katman) ve kenar mührü; gerinim < %0.5 olacak biçimde nötr düzlem tasarımı | Ca testi, 85 °C / %85 RH'de 1 000 saat |
| **W-02** | 6 | LLZO ve Li metal nemden etkileniyor | Li₂CO₃ ve H₂ oluşumu | Hermetik metal-polimer laminat kese (pouch) | 60 °C / %90 RH'de empedans izleme |
| **W-03** | 15 | Derz ancak 16 cm su basıncına dayanıyor | 1.6 kPa, IP68 için ≥ 15 kPa gerekli | Karo başına sızdırmaz kenar mührü, derzi "ıslak bölge" kabul et; kontaklar su altında pasif | IEC 60529 IPX8 |
| **F-01** | 7 | OCA'da kayma gerinimi %1 780–7 100 | δ 0.7–2.85 mm, h 0.04 mm | OCA'yı ≥ 0.2 mm'ye çıkar, büküm bölgesini ve maksimum açıyı sınırla; ya da monolit laminat ve ince çekirdek | Kayma sürünmesi testi, 72 saat bükülü bekletme |
| **F-02** | 7 | Çekirdekte gerinim %3.06 | ITO ~%1'de, ince film kapsülleme %0.5–1'de çatlar | Çekirdeği ≤ 0.4 mm yap, aktif katmanları nötr düzleme yerleştir | Çatlak mikroskopisi, ±R 25.5 döngüsü |
| **P-01** | 12 | PEO 36.2 °C'de iyon taşıyamıyor | 10⁻⁶–10⁻⁵ S/cm, C/10 | Kimyayı değiştir (sülfit katı elektrolit ya da yarı katı jel) ya da hedefleri 5 W'a indir | Hız kabiliyeti testi (25 °C, 1C) |
| **P-02** | 12 | 885 Wh/L (aktifte ~1 180 Wh/L) | Ticari tavan ~800 Wh/L | Kapasiteyi 1.2–1.5 Wh/karo olarak yeniden belirle | Hücre kalorimetrisi, gerçek Wh ölçümü |
| **P-03** | 12 | 25 W ile 36.2 °C ısı atılamıyor | 1.6 W sürekli atılabilir, 3–4 W üretiliyor | 36.2 °C'yi yüzey sınırı olarak değil, IEC 62368-1 TS1 sınırı olarak tanımla; şarjı 7.5 W'a indir | Termal kamera, 25/35 °C ortamda 60 dakika |
| **P-04** | 19 | −10 °C'de cihaz ölü | PEO 10⁻⁸ S/cm | Düşük sıcaklıkta çalışan elektrolit ve ön ısıtma | IEC 60068-2-1 soğuk çalışma |
| **S-01** | 9, 16 | "Sıfır-CPU" ile video, TLS, Wi-Fi ve PD bir arada olamaz | H.264/AV1 çözümü ve TLS işlemci ister | B modülüne bir uygulama işlemcisi (SoC) koy ya da cihazı açıkça "harici host ekranı" olarak tanımla | Fonksiyonel demo |
| **S-02** | 16 | 50 MP ham akış için ISP yok | 15 Gbit/s | ISP'li SoC ya da 12 MP sensöre in | Görüntü hattı testi |
| **S-03** | 16 | Optik yol 2.7 mm'ye karşı ≥ 9 mm | 1" sensör, f 9.5 mm | 1/2.8"–1/3" sensör ve TTL ≤ 4 mm | Lens tasarımı (Zemax) |
| **C-01** | 14 | Gerinim altındaki PC'de ESC | Kritik %0.3–0.5; tasarım %0.35 ile %19.6 arası | Kopoliester veya TPU dış katman ya da kimyasala dayanıklı PC kaliteleri | ISO 22088-3 bükülü şerit testi (IPA, güneş kremi) |
| **R-01** | 10 | Hücresel bağlantı ve 112 erişimi yok | EECC 2018/1972 | Ürünü "telefon" diye pazarlamayı kaldır ya da LTE Cat-1bis/NB ve GNSS ekle | Hukuki inceleme |

### 4.2 · MAJÖR

| ID | Bulgu | Sayı | Çözüm |
|---|---|---|---|
| M-03 | Diş emniyet katsayısı 1.3; NiTi yükün yalnızca %4'ünü taşıyor | 37 MPa'ya karşı 45–55 MPa | Diş kesitini büyüt, tel yerine paslanmaz yay şerit kullan |
| M-05 | (0,0)'da Gauss eğriliği | Düzlem içi gerinim | İki eksende aynı anda bükmeyi mekanik olarak engelle |
| M-06 | NiTi'nin Af sıcaklığı ve kalıplamada yaşlanma | Af 10–25 °C | Af ≤ −20 °C kalitesi, kalıplamada sıcaklık-süre doğrulaması |
| Q-04 | 360 kHz'de µr = 12 000 gerçekçi değil | Gerçekte µ' ≈ 1 000–3 000 | Ölçülmüş µ'/µ'' eğrisi |
| E-02 | Mikro-hücre topolojisi ve hücre içi dengeleme tanımsız | 1 680 hücre | Seri/paralel şeması ve her hücre grubu için sigorta |
| D-01 | Tüy ve tozun 15 µm derzi açması | Lif 11–22 µm | Derzi temizlenebilir ve contalı tasarla |
| D-02 | Mıknatısların demirli toz toplaması, çizilme | Kuvars Mohs 7, PC ~2B–HB | Sert kaplama ve mıknatısa kapak |
| V-01 | L şeklinde ekranda kullanım %37.5 | 3 600 / 9 600 mm² | Yazılımda çoklu pencere; video için en az 2 karo kuralı |
| V-02 | Derz başına 16 yaprak görüntü verisine yetmiyor | 2.3 Gbit/s/karo | Kısa menzilli 60 GHz karo arası bağlantı ya da optik bağlantı |
| R-02 | Anten verimi -6 ile -10 dB | Toprak düzlemi 0–2 mm yakında | Anten boşluğu ≥ 3 mm, ayarlanabilir eşleştirme |
| R-03 | 60 GHz için SAR yanlış ölçüt | Güç yoğunluğu (W/m²) gerekir | ICNIRP 2020 / FCC soğurulan güç yoğunluğu testi |
| W-04 | Terde kontak korozyonu | Ni gözenekliliği | Kalın altın üstünde Pd-Ni, yalnızca bağlıyken besleme |
| C-02 | PC-PDMS'te n ve %T ile uzama birlikte tutmuyor | n ≈ 1.57'ye düşer | Malzeme veri sayfası ile doğrula |
| C-03 | n = 1.585 silikon OCA yok | Silikon 1.40–1.43 | Akrilik OCA (n 1.47–1.50) ve indis eşleme tabakası |
| B-04 | Halka ekranın %6.3'ünü kapatıyor | 804 mm² | Halkayı ekran dışına (çerçeve köşesine) al |
| B-05 | Arka AMOLED ana ekrana dönük | Yön mantığı tutarsız | Yönelim matrisini yeniden tanımla |
| B-06 | 40 W'ta modülde 3.2 W ısı | 20 g kütle | Şarj elektroniğini gövdeye taşı |
| MG-01 | Kalp pili ve kart riski | 1 mT eşiği, 0.3–0.5 T alan | Kullanıcı uyarıları, uzak alanı ölçülmüş mıknatıs yerleşimi |
| MG-02 | 8 yönelimde kutup ve ped eşleşmesi | Tanımsız | Simetrik ped haritası ve Halbach dizisi |
| O-04 | PDLC mahremiyet sağlamıyor, 30–60 V AC göz yakınında | Saçıcı, panjur değil | Mikro-panjur filmi |
| O-05 | Gözlük 37 g | Gözlükler tipik 20–30 g | Hafifletme, karşı ağırlık |
| DOC-01…05 | X1–X6, X14 çelişkileri | Bölüm 2, Senaryo 11 | Tek doğruluk kaynağı (`canon.json`) ve CI'da geometri ve sayı denetimi |

### 4.3 · MİNÖR

| ID | Bulgu |
|---|---|
| m-01 | X7 gerinim farkı (%0.35 ve %0.38) |
| m-02 | X8 OCA kesme modülü farkı (0.05 ve 0.035 MPa) |
| m-03 | X9 ITO ve IZO karışıklığı |
| m-04 | X11 kalkan kalınlığı (0.10 ve 0.15 mm) |
| m-05 | X12 STL sayısı (13 ve 11) |
| m-06 | X13 render sayısı (8 ve 7) |
| m-07 | X15 Leaf 160² kütlesi (144 ve 136 g) |
| m-08 | X16 Leaf 480 kalınlığı (2.40 ve 2.00 mm karo) |
| m-09 | X17 Corning ve "tamamen PC" çelişkisi |
| m-10 | X18 60 GHz için Mu-metal gerekçesi |
| m-11 | X22 Group 911.png anizotrop ölçek (10 ve 12 px/mm) |
| m-12 | X23 uydurma IoU hassasiyeti (0.999987) |
| m-13 | "< 3 s" montaj süresi EU 2023/1542 Madde 11'de yer almıyor; pil ile ekranın aynı parça olması değiştirme maliyetini artırıyor |
| m-14 | Leaf 480'in 144 Wh'lik paketi, IATA'nın 100 Wh üstü için havayolu onayı istediği sınıfa giriyor |
| m-15 | MG-03 NiTi nikel salımı (EN 1811) belgelenmemiş |

---

## 5 · SÜREÇ BULGUSU: ÇOK AJANLI ÇIKTILAR DOĞRULAMA SAYILMAZ

Rapor §0, Arena API üzerinden 5 dil modeli ajanının "HTTP 200 OK" yanıtlarını ve 9–11 bin karakterlik çıktılarını "tüm nicel çıktılar doğrulanmıştır" diye sunuyor. Bu bir **mühendislik doğrulaması değildir.**
- HTTP 200 yalnızca isteğin iletildiğini gösterir.
- Çıktı uzunluğu kalitenin ölçüsü değildir.
- IoU = 0.999987, ε = %0.35, 885 Wh/L gibi değerlerin hiçbirinin arkasında ölçüm, FEA ya da test raporu yok.
- `check_sheets.py` 32 SVG sayarken belge 26 listeliyor. Yani doğrulama aracı bile belgedeki kümeyi denetlemiyor.

**Öneri:** Her nicel iddiaya bir kanıt sınıfı atanmalı: hesap, simülasyon, prototip ya da test. Kanıtı olmayan sayılar `canon.json`'da "hedef" olarak işaretlenmeli. Belgeler arası sayısal çelişkiler (Senaryo 11 tablosu) CI'da otomatik yakalanmalı.

---

## 6 · ÖNCELİKLİ YOL HARİTASI

1. **Mimari karar (1. hafta):** Gözlük modunu ya iptal edin ya da tamamen ayrı bir ürün yapın (O-01/02/03). "Sıfır-CPU" yerine bir SoC kararı verin (S-01).
2. **Pil kimyası (2–6. hafta):** PEO yerine oda sıcaklığında çalışan bir elektrolit seçin. Kapasiteyi 1.2–1.5 Wh/karo olarak yeniden belirleyin (P-01/02).
3. **Derz (2–8. hafta):** "Görünmez derz" iddiasını kaldırın. ≥ 0.2 mm'lik, contalı, görünür ve tasarlanmış bir çizgiye geçin. Derzde rijitlik sürekliliği için nötr düzlemde bir taşıyıcı ekleyin (M-02, M-04, W-03).
4. **Qi (4–8. hafta):** Bobini tek parçaya taşıyın, mıknatısları bobin alanından çıkarın, hedefi 7.5–15 W'a indirin (Q-01/02/03, P-03).
5. **B modülü (4–10. hafta):** USB-C'yi halkaya alın, mekanik kilit ekleyin, çubuğu ≥ 3.3 mm yapın (B-01/02/07).
6. **Bariyer (paralel):** İnce film kapsülleme ve hermetik pil kesesi; gerinim ≤ %0.5 olacak şekilde yığını yeniden tasarlayın (W-01/02, F-01/02).
7. **Belgeler (sürekli):** X1–X24 çelişkilerini tek bir kaynakta çözün ve CI kapısı ekleyin.

**Sonuç:** Belgelerdeki temel iddiaların (2.00 mm tam esneklik, görünmez derz, saydam gözlük, 25/40 W şarj, Sıfır-CPU, 1 mm çubukta USB-C) **hiçbiri** fizik sınırları içinde aynı anda sağlanamıyor. Ürünün yeniden tanımlanması gerekiyor. Tolerans iyileştirmesiyle kapatılabilecek bir açık değil.

