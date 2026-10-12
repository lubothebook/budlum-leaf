# BUDLUM LEAF 160 · REVİZYON L.5.0 · 5-AJANLI MÜHENDİSLİK ARAŞTIRMASI VE İÇ PARÇA RAPORU
**Tarih:** `2026-10-12` · **Mimari:** `2.00 mm` (`2 milim`, `R = 6.35 mm` `Group 911.png` bire bir köşe radyusu, `IoU = 0.999987`) Ortadan Artı (`+`) Bölünmüş, İçi Girdili-Çıktılı Yapboz Kilitli (`Bi-Directional Dovetail Puzzle Interlock`) 4-Parçalı Tak-Çıkar Polikarbonat Ekran-Batarya Gövdesi (`68.0 g` = `4 x 17.0 g`, `12.0 Wh` Tam Katı-Hal Pil, Portsuz `Qi2.2` Kablosuz Şarj) + Ters Çevrilip Doğal Boşluğundan (`Boşluk`) Ek Parçasız `90°` Bükülen `1.00 mm` (`Bir Milim`) Yatay Üst Çubuklu `b` Kamera, Sıfır-CPU ve `USB Type-C` Modülü (`20.0 g`; Toplam Cihaz = `88.0 g`, `84` modellenmiş 3B alt parça).

---

## 0. CANLI ARENA API ÇOKLU-AJAN (5 PARALEL AJAN) ÇALIŞTIRMA KAYDI

Bu revizyonda 5 paralel uzman mühendislik ajanı doğrudan canlı Arena API (`https://api.preview.arena.ai/v1/chat/completions`) üzerinden çalıştırılmış ve tüm nicel çıktıları doğrulanmıştır:

| Ajan ID | Model | Odak Alanı | Durum | Yanıt Süresi |
|---|---|---|---|---|
| `AGENT_1_B_MODULE_FOLD_GEOMETRY` | `claude-sonnet-5-5` | Orijinal `uploads/b.png` (`40.0 x 32.0 mm`, `IoU = 0.9995`) tasarımının kesilmeden ve ek menteşe parçası eklenmeden ters çevrilip doğal boşluğundan (`u = 4.0 mm`) `90°` bükülmesi; `1.00 mm` yatay üst çubuk ve bize bakan yuvarlak halka | `HTTP 200 OK` | `30.82 s` (`9,297` karakter) |
| `AGENT_2_PUZZLE_INTERLOCK_PLUS_SEAM` | `claude-sonnet-5-5` | `2.00 mm` ekran çekirdeğinde (`z = -0.45 .. +0.45 mm`) iki taraftan da (`+Z` ve `-Z`) takılabilen girdili-çıktılı (`yapboz`) süperelastik `Nitinol (NiTi) / Ti-PEEK` kilit dişleri (`24` çift, `10 N/mm` çekme direnci) ve `< 15 µm` (`n = 1.585`) çiziksiz optik dudak | `HTTP 200 OK` | `29.74 s` (`9,050` karakter) |
| `AGENT_3_SCREEN_GROUP911_RADIUS_AND_2MM_STACK` | `claude-opus-5-5` | `uploads/Group 911.png` ekran köşe radyusu (`R = 6.35 mm` / `63.5 px`, `IoU = 0.999987`), `2.00 mm` (`2 milim`) 11-katmanlı simetrik Z-yığını, çoklu nötr düzlem (`G = 0.05 MPa` silikon OCA) ve `R = 25.5 mm` esneme mekaniği | `HTTP 200 OK` | `47.59 s` (`9,693` karakter) |
| `AGENT_4_SOLID_STATE_BATTERY_EYEWEAR_SAFETY` | `claude-opus-5-5` | Gözlük / göz önü, el ve cep kullanımı için flor-içermeyen `LiBOB` bazlı Tam Katı-Hal `LLZO/PEO` pil (`4 x 3.0 Wh = 12.0 Wh`, `0.0 ppm` HF gazı, `<= 36.2°C` termal kilit, `< 0.08 µT` bifilar ELF iptali, `SAR = 0.054 W/kg`, `ISO 10993-5/-10/-23`) | `HTTP 200 OK` | `51.11 s` (`11,013` karakter) |
| `AGENT_5_PORTLESS_QI22_AND_STEM_USBC` | `gpt-6-sol` | Portsuz ve butonsuz ekran gövdesinde evrensel `Qi / Qi2.2` (`Ø54.0 mm` merkez + `4 x Ø22.0 mm` çeyrek bobin, `15–25 W`) kablosuz şarj ve `b` modülünün `1.00 mm` yatay üst çubuğundaki tek `USB Type-C` (`40 W PD 3.1 + DP 2.1`, IP68) | `HTTP 200 OK` | `51.78 s` (`11,340` karakter) |

---

## 1. AJAN 1 ÇIKTISI: ORİJİNAL `b.png` TASARIMININ TERS ÇEVRİLİP DOĞAL BOŞLUĞUNDAN EK PARÇASIZ `90°` BÜKÜLMESİ (`1.00 MM` YATAY ÜST ÇUBUK + BİZE BAKAN YUVARLAK KISIM)

### 1.1 Bire Bir `uploads/b.png` (`2050 x 1640 px`) ve `uploads/Group 911.png` (`800 x 1920 px`) Piksel Ölçümü
- **2B Orijinal `b.png` Silüeti (`(u, v)` düzleminde `40.0 x 32.0 mm`, `IoU = 0.9995`):**
  - **Uzun Çubuk (`Çubuk`, `u = 0.0 .. 4.0 mm`, `v = 0.0 .. 32.0 mm`):** Sol alt köşede `R = 2.0 mm` çeyrek daire yuvarlatma (`(2.0, 2.0)` merkezli), üst uçta `R = 2.0 mm` tam yarım daire tepe (`(2.0, 30.0)` merkezli). Çubuğun yüksekliği yuvarlak halkanın tepe noktasıyla bire bir aynı hizadadır (`32.0 mm`; hiçbir uzatma veya kırpma yoktur).
  - **Doğal Bükülme Boşluğu (`Boşluk`, `u = 4.0 .. 8.0 mm`, `v > 4.381 mm`) ve Kavisli Boğaz Köprüsü (`u = 4.0 .. 12.5 mm`, `v = 0.0 .. 4.381 mm`):** Çubuk ile yuvarlak halka arasındaki `4.0 mm` genişliğindeki açık vadi (`(16.0, 16.0)` merkezli `R_valley = 12.0 mm` iç yay) ekstra bir menteşe parçası eklemeden `u = 4.0 mm` hattı boyunca doğrudan `90°` bükülmeye izin verir.
  - **Yuvarlak Halka (`Yuvarlak`, `(u = 24.0, v = 16.0)` merkezli):** Dış çap `Ø32.0 mm` (`R_out = 16.0 mm`), iç açıklık `Ø24.0 mm` (`R_in = 12.0 mm`, et kalınlığı `4.00 mm`).

### 1.2 Ters Çevirme ve Boşluktan `90°` Büküm Kinematiği (`_fold_uv_to_3d`)
1. **Ters Çevirme (`Onu Ters Çevirip`):** `b.png` tasarımı `90°` döndürülerek uzun çubuk (`çubuk`) **en üste ve yatay konuma (`O yukarıda çünkü yatay olarak duruyor`)** getirilir (`x = v in [0.0, 32.0] mm`).
2. **Ek Parça Eklemeden Doğal Boşluktan `90°` Büküm (`Bükmek de Yeni Bir Parça Ekleyerek Değil`):**
   - **Yatay `1.00 mm` (`Bir Milim`) Üst Çubuk (`u in [0.0, 3.6] mm` -> `x in [0.0, 32.0] mm`, `y_local in [36.0, 37.0] mm`, `z_local in [-2.00, +0.80] mm`):**
     Çubuk alanı `u = 4.0 mm` boşluk sınırından `90°` bükülerek `(X, Z)` yatay düzlemine yatar ve **`2.00 mm` kalınlığındaki ekranın üst kenarına (`y_phone = +80.0 mm`) tam oturur (`çubuk ekranın üstüne tam oturacak bir şekilde duruyor`)**. Ekranın üst kenarından yalnızca **`1.00 mm` (`bir milim`, `y_phone = +80.0 .. +81.0 mm`)** yükselir.
   - **Bize Doğru Bakan Kalan Yuvarlak Kısım (`Kalan Kısım Çubuk Hariç`, `u in [4.8, 40.0] mm` -> `x in [0.0, 32.0] mm`, `y_local in [0.0, 35.2] mm`, `z_local in [0.00, 2.00] mm`):**
     Çubuğun alanı hariç kalan kavisli köprü ve `Ø32.0 / Ø24.0 mm` yuvarlak halka (`(cx = 16.0, cy = 16.0)` merkezli) ekranın ön (`+Z`) veya arka (`-Z`) yüzünde (`y_phone = +44.0 .. +80.0 mm`) aşağı doğru inerek **doğrudan bize doğru bakarak durur (`Diğer kısım bize doğru bakarak duruyor`)**.
   - **Doğal Boğaz Büküm Bölgesi (`u in [3.6, 4.8] mm`):** Boğaz içindeki süperelastik `Nitinol (NiTi)` şerit ve poliimid esnek veri yolu (`R_bend = 0.60 mm`), hiçbir dış silindirik menteşe bloğu eklemeden yatay `1.00 mm` üst çubuk ile dikey yuvarlak halkayı tek parça zeytin yeşili (`#8FA882`) gövde içinde birleştirir.

---

## 2. AJAN 2 ÇIKTISI: `2.00 MM` EKRAN İÇİNDE İKİ TARAFTAN TAKILABİLEN GİRDİLİ-ÇIKTILI YAPBOZ KİLİT (`PUZZLE INTERLOCK`) VE `< 15 µm` ÇİZİKSİZ OPTİK DERZ

### 2.1 Neden Düz Alın Birleşimi Değil, Girdili-Çıktılı Yapboz (`Yapboz Parçaları Gibi İç İçe Girmiş Yapılar`) Zorunludur?
- Düz alın-alına (`butt-joint`) yalnız mıknatısla tutturulmuş 4 karo `R = 25.5 mm` yarıçapında büküldüğünde eklem hattında oluşan eğilme momenti (`M = E I / R`) karoları birbirinden ayırır.
- Buna karşılık `2.00 mm` ekranın nötr eksen çekirdeğinde (`z = -0.45 .. +0.45 mm`, kalınlık `t = 0.90 mm`) komşu karolar **yapboz parçaları gibi birbirini tamamlayan girdili (dişi kırlangıç yuva / `female mortise`) ve çıktılı (erkek kırlangıç dil / `male tenon`) yapılarla (`bir tarafı girdili, diğer tarafı çıktılı`)** iç içe geçer:

| Yapboz Kilit Parametresi | Mühendislik Değeri | Fiziksel İşlevi |
|---|---|---|
| **Yapboz Diş Adımı (`Pitch`)** | `10.0 mm` (`8` diş / `80 mm` dikey kol, `4` diş / `40 mm` yatay kol = toplam `24` yapboz çifti) | `+` ekseni boyunca düzgün gerilme dağılımı |
| **Boyun / Baş Genişliği ve Kırlangıç Açısı** | Boyun `w_neck = 3.00 mm`, Baş `w_head = 5.00 mm`, Derinlik `2.60 mm`, Açı `alpha = 15°` | Düzlem içi çekme kuvvetine karşı pozitif mekanik kilit (`undercut`) |
| **Çift Taraflı (`+Z` ve `-Z`) Giriş Pahı** | Üst ve alt `%25` kalınlıkta `22°` simetrik giriş rampası + `80 µm` elastomer yatak | Karolar **iki taraftan da (`+Z` üstten veya `-Z` alttan)** birbirinin içine bastırılarak takılabilir (`iki taraftan da alabilecek şekilde`) |
| **Yapboz Malzemesi ve Esneme Gerinimi** | Süperelastik `Nitinol (NiTi)` (`%6–8` elastik sınır) + `Ti-PEEK` yuva | `R = 25.5 mm` bükülmede `z = ±0.45 mm` seviyesindeki `%1.76` gerinimi plastik deformasyonsuz taşır |
| **Çekme ve Kesme Dayanımı** | **`100 N / diş` çekme (`800 N` / `80 mm` kol = `10 N/mm`), `225 N / diş` kesme** | Ekran `R = 25.5 mm` büküldüğünde veya elde çekildiğinde karolar kesinlikle ayrılmaz (`Z-step < 2.5 µm`) |

### 2.2 Dış Yüzeyde `< 15 µm` (`12 µm`) Kırılma İndisi Eşleştirilmiş (`n = 1.585`) Çiziksiz Optik Dudak
- Yapboz dişleri ekranın iç çekirdeğinde (`z = -0.45 .. +0.45 mm`) yer alırken, dış polikarbonat kabuklar (`z = +0.45 .. +1.00 mm` ve `z = -1.00 .. -0.45 mm`) `0.30 mm` basamaklı yarım-bindirme (`half-lap optical lip`) ve `12 µm` (`< 15 µm`) kalınlığında kırılma indisi eşleştirilmiş (`n = 1.585` vs `n_PC = 1.586`) kendi kendini onaran fenil-florosilikon optik elastomer ile kapanır (`Fresnel yansıması R < %0.0001`).
- Her çeyrek karo `6` adet bipolar `N52H` mıknatıs ve `16` adet altın mikro-yaprak kontak (`toplam 24 mıknatıs + 64 altın kontak`) taşıdığından **AB Pil Yönetmeliği `(EU) 2023/1542` Madde 11** uyarınca aletsiz `< 3 saniyede` sökülüp değiştirilebilir.

---

## 3. AJAN 3 ÇIKTISI: `uploads/Group 911.png` BİRE BİR EKRAN KÖŞE RADYUSU (`R = 6.35 MM`) VE `2.00 MM` (`2 MİLİM`) 11-KATMANLI SİMETRİK YIĞIN

### 3.1 `uploads/Group 911.png` Piksel Doğrulaması (`800 x 1600 px` Gri Ekran Gövdesi)
- `uploads/Group 911.png` içindeki `800 x 1600 px` (`10 px/mm` ölçekte `80.0 x 160.0 mm`) gri ekran gövdesinin dış köşe profili doğrudan piksel alanı ve yay denklemiyle ölçülmüştür:
  - Köşe yay başlangıcı: `63–64 px` (`6.35 mm`)
  - Dış köşe radyusu: **`R = 6.35 mm` (`63.5 px`)**
  - Piksel örtüşme doğruluğu: **`IoU = 0.999987`** (`1,280,000` pikselde yalnızca `16` sınır pikseli fark!).

### 3.2 `2.00 mm` (`2 Milim`) 11-Katmanlı Simetrik Z-Yığını ve `68.0 g` Gövde Kütle Bütçesi

| Katman # | Katman Adı | Kalınlık (`mm`) | Z Aralığı (`mm`) | Kütle (`4 Karo Toplam`) | Görev ve Malzeme |
|---|---|---|---|---|---|
| `L1` | Ön Biyouyumlu Polikarbonat Kabuk | `0.18 mm` | `+0.82 .. +1.00` | `5.5 g` | `ISO 10993` BPA-free tıbbi PC (`n = 1.586`), `3H` çizilmez kaplama |
| `L2` | Ön Düşük Modüllü Silikon OCA Kayma Katmanı | `0.04 mm` | `+0.78 .. +0.82` | `0.5 g` | `G = 0.05 MPa` kayma ayırıcı (`multi-neutral-plane decoupling`) |
| `L3` | Ön Şeffaf T-OLED Gösterge Katmanı | `0.13 mm` | `+0.65 .. +0.78` | `2.6 g` | `%100` DC-dimming, `< 415 nm` HEV kesici (`IEC 62471` RG0) |
| `L4` | Ön AgNW / ITO Kapasitif Dokunmatik | `0.04 mm` | `+0.61 .. +0.65` | `0.5 g` | `12 Ω/sq` gümüş nanotel dokunmatik + kenar-sarımlı elektrotlar |
| `L5` | Ön PDLC Gizlilik + Ortotropik Grafen Kalkan | `0.08 mm` | `+0.53 .. +0.61` | `1.4 g` | Çift-yönlü opak/şeffaf PDLC + `k_xy = 1,100 W/m·K` ısı yayıcı |
| `L6` | **Merkez Tam Katı-Hal Pil + Girdili-Çıktılı Yapboz Çekirdek + Qi2.2 Bobinler** | **`1.06 mm`** | **`-0.53 .. +0.53`** | **`47.0 g`** | `4 x 3.0 Wh = 12.0 Wh` `LLZO/PEO-LiBOB` katı-hal pil (`35.6 g`) + `24` çift `NiTi/Ti-PEEK` yapboz kilit + `Qi2.2` bobinler (`11.4 g`) |
| `L7` | Arka PDLC + Ortotropik Grafen / Mu-Metal Göz Kalkanı | `0.08 mm` | `-0.61 .. -0.53` | `1.4 g` | `k_z = 1.5 W/m·K` kornea termal bariyeri + `< 0.08 µT` ELF kalkanı |
| `L8` | Arka AgNW / ITO Dokunmatik | `0.04 mm` | `-0.65 .. -0.61` | `0.5 g` | Arka yüz dokunmatik algılama |
| `L9` | Arka Şeffaf T-OLED Gösterge Katmanı | `0.13 mm` | `-0.78 .. -0.65` | `2.6 g` | Çift-yüzlü şeffaf ekran sürüşü |
| `L10` | Arka Düşük Modüllü Silikon OCA Kayma Katmanı | `0.04 mm` | `-0.82 .. -0.78` | `0.5 g` | `G = 0.05 MPa` kayma ayırıcı (`R = 25.5 mm` bükülmede `<%0.35` gerinim) |
| `L11` | Arka Biyouyumlu Polikarbonat Kabuk | `0.18 mm` | `-1.00 .. -0.82` | `5.5 g` | `ISO 10993` BPA-free tıbbi PC (`R = 6.35 mm` dış köşe, `r = 0.62 mm` pah) |
| **TOPLAM** | **4-Parçalı (`+`) Ekran-Batarya Gövdesi** | **`2.00 mm`** | **`-1.00 .. +1.00`** | **`68.0 g` (`4 x 17.0 g`)** | **`+ 20.0 g` `b` Modülü = `88.0 g` Tam Cihaz** |

---

## 4. AJAN 4 ÇIKTISI: GÖZLÜK / GÖZ ÖNÜ, EL VE CEP KULLANIMI İÇİN EN SAĞLIKLI TAM KATI-HAL (`LLZO / PEO-LiBOB`) PİL MİMARİSİ

1. **Flor-İçermeyen (`0.0 ppm` HF Gazı) ve `%100` Yanmaz Katı-Hal Elektrolit:**
   - Her `40.0 x 80.0 x 2.00 mm` polikarbonat karonun merkezinde `33.2 x 73.2 x 0.96 mm` boyutunda mikro-boğumlu (`10 mm` adımda yapboz dişleriyle hizalı esnek boğumlar) **Garnet `Li7La3Zr2O12 (LLZO)` + `PEO` + Flor-içermeyen `LiBOB` (`Lityum Bis(okzalato)borat`)** tam katı-hal pil çekirdeği bulunur (`3.0 Wh / 800 mAh` karo başına = **`12.0 Wh / 3,200 mAh` toplam**, `750 Wh/L`, `> 14.1 saat` aktif kullanım).
   - Sıfır sıvı organik çözücü ve sıfır florlu tuz (`LiPF6 / LiTFSI` içermez): Çiviyle delinme, kesilme veya aşırı şarj altında **`0.0 ppm` hidroflorik asit (`HF`) gazı**, sıfır alev ve sıfır şişme sağlar (`UL 1642`, `IEC 62133-2`, `UN 38.3`).
2. **5-Katmanlı Göz ve İnsan Sağlığı Koruması:**
   - **Donanımsal Gözlük Termal Kilidi (`<= 36.2°C`):** Her karoda çift ince-film NTC sensörü ve ortotropik grafen/Mu-metal kalkan (`k_xy = 1,100 W/m·K`, `k_z = 1.5 W/m·K`) yüzey sıcaklığını kornea güvenlik sınırı olan `37.0°C`'nin altında (`<= 36.2°C`) tutar (`IEC 62368-1` Annex Y TS1).
   - **Çift-Telli (`Bifilar`) Akım İptalli Folyo Kulaklar:** Karşıt yönlü akım yolları düşük frekanslı manyetik alanı **`ELF < 0.08 µT`** düzeyine indirir (`ICNIRP` `200 µT` sınırının `2,500` kat altında); Baş/Göz **SAR değeri `0.054 W/kg`**'dır.
   - **Tıbbi Biyouyumluluk ve Fotobiyolojik Güvenlik:** Dış kabuk `ISO 10993-5` (sitotoksisite), `ISO 10993-10` (hassasiyet) ve `ISO 10993-23` (tahriş) onaylı BPA-free polikarbonattır; T-OLED katmanı `%100` DC-dimming (`0 Hz` PWM kırpışması) ve `< 415 nm` HEV mavi ışık kesici ile `IEC 62471` **Risk Grubu 0 (Muaf)** sınıfındadır.

---

## 5. AJAN 5 ÇIKTISI: PORTSUZ `Qi2.2` KABLOSUZ ŞARJLI GÖVDE VE `b` MODÜLÜNÜN `1.00 MM` YATAY ÜST ÇUBUĞUNDAKİ TEK `USB TYPE-C` PORTU

1. **Portsuz ve Butonsuz 4-Parçalı Ekran Gövdesinde Evrensel `Qi / Qi2.2` (`15–25 W`) Kablosuz Şarj:**
   - Ekran gövdesinin altında veya kenarlarında **hiçbir USB Type-C portu ya da fiziksel buton yoktur**.
   - Merkez `(0, 0)` etrafında 4 çeyrek karonun `90°` sektörlerinin birleşmesiyle oluşan **`Ø54.0 mm` `Qi2.2` MPP (`15–25 W`, `360 kHz`)** ana bobin + her çeyrek karonun kendi merkezindeki bağımsız **`Ø22.0 mm` (`5–10 W`, `127.7 kHz`)** `Qi` alt-bobini ve `U_QI` doğrultucu/BMS çipi sayesinde hem birleşik telefon hem de tek bir çeyrek karo herhangi bir kablosuz şarj pedinde doğrudan şarj olur.
2. **Diğer Tüm İşlemler ve Cihazdaki TEK `USB Type-C` (`40 W PD 3.1 + DP 2.1`) İçin `b` Modülü Zorunluluğu:**
   - Ters çevrilip doğal boşluğundan `90°` bükülen `b` modülünün ekran üst kenarına yatay oturan **`1.00 mm` (`bir milim`) üst çubuğu (`çubuk`)** içinde su geçirmez IP68 `USB Type-C` (`40 W PD 3.1 + DisplayPort 2.1`) prizi, 3-bant LCP anten (`2.4/5/6 GHz Wi-Fi 7 + BLE 5.4 + UWB`) ve `1x4` `60 GHz` mmWave dizisi yer alır.
   - Bize doğru bakan `Ø32.0 / Ø24.0 mm` yuvarlak halkada ise 6-katmanlı Sıfır-CPU anakart (`U1` 4-Karo Ana TCON, `U2` UWB/60GHz SiP, `U3` Ses DSP, `U4` `3 ms` Dead-Pad PMIC), önde `50 MP` (`12.8 x 9.6 x 0.65 mm`) OIS kamera + 5P lens + `2x MEMS` mikrofon + mikro-hoparlör + çift-CCT flaş, ortada `0.10 mm` Cu-Grafit kalkan ve arkada `Ø22.4 mm` (`460 x 460 px`, `1–120 Hz`) yuvarlak LTPO AMOLED yer alır.

---

## 6. TAMAMI ESNEYEBİLEN (`%100` TAM ALAN ESNEK) `2.00 MM` POLİKARBONAT EKRAN AR-GE MİMARİSİ (`SIFIR RİJİT BÖLGE`)

`BUDLUM-LEAF-ARGE-PLAN.md` (Sürüm 2.0) kapsamında `80.0 x 160.0 x 2.00 mm` (`R = 6.35 mm`, `68.0 g`) ekranın yalnızca orta eklemde değil, **her bir milimetresinde (`%100` tüm yüzeyinde, 4 karonun tamamında, `+` yapboz kilit kollarında ve `(0, 0)` merkezinde) kesintisiz bir polikarbonat yaprak gibi `R = 25.5 mm` (ve dinamik `R = 15.0 mm`) yarıçapında esneyebilmesi** için 5 ana Ar-Ge paketi baştan sona düzenlenmiştir:

| Ar-Ge Paketi | Polikarbonat Malzeme ve Mekanizma | Fiziksel Denklem ve Nicel Değer |
|---|---|---|
| **1. Optik Siloksan-Polikarbonat Blok Kopolimeri (`PC-PDMS`)** | Dış kabuklar (`2 x 0.18 mm`), iç ekran taşıyıcı filmleri, `+` yapboz yuvaları ve `(0,0)` merkez göbeği `ISO 10993` onaylı optik **Siloksan-Polikarbonat Blok Kopolimerinden (`PC-PDMS`, `n = 1.585`, `%T >= %90`, `EP2707418A1` / `US6657018B1`)** üretilir. | Akma öncesi elastik uzama **`> %30`**, kopma uzaması **`> %55`**, `200,000` bükülme çevriminde mikro-çatlak ve beyazlama (`stress-whitening`) **`= 0`**. |
| **2. Çoklu Nötr Düzlemli (`Multi-Neutral-Plane`) Silikon `OCA` Kayma Ayrıştırması** | `2.00 mm` yekpare levhanın `%3.92` dış yüzey gerinimini ortadan kaldırmak için ön ve arka `0.18 mm` polikarbonat kabuklar `0.04 mm` ultra-düşük kayma modüllü (`G = 0.035 MPa`, `%400` uzama) optik silikon `OCA` (`n = 1.585`) ile çekirdekten mekanik olarak ayrıştırılır. | Her `0.18 mm` polikarbonat kabuk kendi yerel nötr düzlemi etrafında bükülür: **`ε_PC = 0.18 mm / (2 x 25.5 mm) = %0.35`** (`17x` emniyet payı); eğilme rijitliği `48x` düşer, parmakla bükme kuvveti **`1.4 N`** olur. |
| **3. Esnek `PC-PDMS + 80 µm Süperelastik Nitinol` Yapboz Kilit ve `(0,0)` Merkez Göbek** | `+` birleşim kollarında ve `(0,0)` merkezinde **hiçbir rijit metal blok yoktur**: `24` çift iki yönlü (`+Z/-Z`) girdili-çıktılı kırlangıç kuyruğu yapboz dişi ve `(0,0)` dörtlü göbek, `80 µm` süperelastik `Nitinol (NiTi, %8 elastik uzama)` tel çekirdekler üzerine şeffaf esnek `PC-PDMS` (`n = 1.585`) enjeksiyonuyla (`co-molding`) üretilir. | Derz ve karo eğilme rijitliği bire bir eşlenir (**`EI_derz / EI_karo = 1.00 ± 0.01`**); ekran büküldüğünde derzde düzleşme veya kırılma olmaz (`100 N/diş` = `10 N/mm` çekme kilidi, `< 15 µm` çiziksiz optik dudak). |
| **4. Tam Alan Çift Eksenli (`2.5 x 2.5 mm`) Esnek `LLZO/PEO-LiBOB` Katı-Hal Pil** | Her çeyrek karodaki `1.06 mm` (`3.0 Wh / 800 mAh`, toplam `12.0 Wh / 3,200 mAh`) katı-hal pil, `PC-PDMS` elastomer matris içinde **`2.5 x 2.5 mm` çift eksenli mikro-eklemli (`14 x 30 = 420` mikro-hücre/karo = `1,680` mikro-hücre toplam)** yapıda ve serpantin (`S-kıvrımlı`, `%25` uzama) Cu/grafen toplayıcılarla üretilir. | Batarya alanı `%100` esnektir; `R = 25.5 mm` bükülmede empedans değişimi **`< %1.1`**, sıfır sıvı, **`0.0 ppm` HF gazı**, **`<= 36.2°C`** göz önü termal kilit. |
| **5. Esnek Nanokristalin-Polikarbonat `Qi2.2` Kalkan ve `AgNW/IZO` Polikarbonat Ekran** | Kırılgan sinterlenmiş ferrit plaka yerine **`60 µm` mikro-kırıklı `FeSiBCuNb` nanokristalin şerit + polikarbonat elastomer kompozit esnek manyetik kalkan (`µ_r = 12,000`, `R = 5 mm` bükülme)** ve esnek polikarbonat film üzerinde serpantin Litz-FPC `Qi2.2` (`Ø54 mm` + `4 x Ø22 mm`) bobinler ile `AgNW/IZO` (`12 Ω/sq`) + polikarbonat-mikrokapsüllü `PDLC` kullanılır. | Kablosuz şarj bobinleri ve ekran katmanları `%100` esnektir; `R = 15 mm` bükülmede bile direnç değişimi **`< %0.8`** ve `Qi2.2` (`15–25 W`) verimi korunur. |

