# BUDLUM LEAF · NEREDE NE VAR · 2026-10-12 · REVİZYON L.5.0 (`2.00 MM` `R=6.35 MM` `+` YAPBOZ KİLİTLİ 4-KADRANLI EKRAN-BATARYA GÖVDESİ, QI2.2 KABLOSUZ ŞARJ, GÖZ-GÜVENLİ KATI-HAL PİL VE BOŞLUKTAN 90° BÜKÜLEN `1.00 MM` YATAY ÇUBUKLU `b` MODÜLÜ · 84 İÇ PARÇA)

> **Revizyon L.6.0 (2026-10-12)**. `FINAL/21-stretch-stem-and-projection.md` bu haritadaki eski bilgilerin önüne geçer. Gövde artık esner (mümkün olan en yüksek değer, yaklaşık `%13`, `1.7 Wh`). B çubuğu `8.0 x 32.0 x 1.00 mm` LCP-GF40, menteşesiz ve metalsiz. USB-C halka kenarına taşındı. Kamera `50 MP`: sensör halkada yatık, ışık iki prizmayla katlanıyor. Yüzey baştan sona polikarbonat; adaların arasında yılankavi PC şeritler esniyor. Yansıtma: validatörler Leaf'i Budlum'u çalıştırdıkları gibi çalıştırır, Leaf gösterir. Paftalar, STL modelleri ve renderlar henüz L.5.0'ı gösteriyor.

Bu dosya çalışma alanının tam haritasıdır. `AUDIT/ARENA-MULTI-AGENT-QUAD-PLUS-AND-BENT-B-REPORT.md` (5-Ajanlı Canlı Arena API Mühendislik Araştırma ve İç Parça Raporu) doğrultusunda **kaba duran dış alt batarya modülü tamamen iptal edilmiştir**. Ekran gövdesi (`80.0 x 160.0 x 2.00 mm`, `2 milim`, `68.0 g`, dış köşe radyusu `uploads/Group 911.png` ile bire bir **`R = 6.35 mm` (`IoU = 0.999987`)**), merkezden **`+` (artı) şeklinde 4 eşit tak-çıkar polikarbonat ekran-batarya karosuna (`4 x 40.0 x 80.0 x 2.00 mm`, her biri `17.0 g`)** bölünmüştür. Ekranın içinde iki taraftan da (`+Z` veya `-Z`) birbirinin içine takılabilen **esnek girdili-çıktılı yapboz kilit dişleri (`24` süperelastik `Nitinol/Ti-PEEK` kırlangıç kuyruğu kilit çifti, `100 N/diş` = `10 N/mm` çekme direnci)** yer alır; böylece `2.00 mm` ekran **`R = 25.5 mm`** yarıçapında esnetildiğinde ayrılmaz ve dış yüzeyde **`< 15 µm` (`n = 1.585`) sıfır çizikli optik derz** korunur. Her karonun içinde gözlük/göz, el ve cep kullanımına tam uygun **yanmaz `LLZO/PEO-LiBOB` katı-hal pil (`4 x 3.0 Wh = 12.0 Wh` / `3 200 mAh`, `<= 36.2 °C`, `ISO 10993`, `EU 2023/1542` Madde 11)** ve **evrensel `Qi2.2` kablosuz şarj bobinleri** yer alır. Ekran gövdesinde **hiçbir USB Type-C portu veya buton yoktur**; **USB Type-C sadece orijinal `uploads/b.png` tasarımının (`40.0 x 32.0 mm`, `IoU = 0.9995`, ek menteşe parçası eklenmeden) ters çevrilip çubuk ile yuvarlak arasındaki doğal boşluktan `90°` dik açıyla büküldüğü `b` kamera modülünün (`20.0 g`, toplam `88.0 g`) yukarıda yatay olarak duran `1.00 mm` (`bir milim`) çubuk kısmındadır**. Çubuk alanı hariç kalan yuvarlak kısım (`Ø32.0 / Ø24.0 mm`) ise ekranın ön (`+Z`) veya arka (`-Z`) yüzeyinde **bize doğru bakarak durur**. Toplam **84 iç alt parçanın tamamı** 3B CAD, STL, render, pafta ve belgelerde modellenmiştir.

---

## 1 · Direktif, doğrulama ve çoklu-ajan (Multi-Agent) optimizasyon araçları

| Kalem | Dosya | Durum |
|---|---|---|
| **5-Ajanlı Revizyon L.5.0 Mühendislik Raporu (`84` iç parça)** | `AUDIT/ARENA-MULTI-AGENT-QUAD-PLUS-AND-BENT-B-REPORT.md` | 4-kadranlı (`+`) sıfır çizikli optik derz (`<15 µm`, `n=1.585`), göz-güvenli `LLZO` katı-hal pil (`<=36.2 °C`, `ISO 10993`), portsuz `Qi2.2` kablosuz şarj ve `90°` dik bükümlü `b` modülü raporu |
| 21 bölümlük direktif dizisi | `FINAL/00` … `FINAL/20` | Revizyon L.5.0 4-kadranlı (`+`) gövde ve `90°` dik bükümlü `b` modülüyle güncellendi |
| Tek cilt birleşik direktif | `BUDLUM-LEAF-FINAL-DIRECTIVE-v5.md` | 20 ana bölüm, **251 doğrulama kapısı** |
| Sayaçların tek kaynağı | `tools/canon.json` | 251 kapı (218 cihaz/ağ + 16 program + 17 araştırma), 39 açık kalem |
| Doğrulama araçları | `tools/assemble.py`, `tools/check_crossrefs.py`, `tools/check_prose.py` | PRG-16, PRG-15 ve PRG-12 denetimleri (`0` hata) |
| **Çoklu-Ajan (Multi-Agent) Arena API Optimizasyon Sistemi** | `tools/multi_agent_optimize.py` | `ARENA_API_KEY` ortam değişkeniyle CAD, Pafta, Donanım ve Denetim ajanlarını paralel çalıştıran orkestratör |
| Durum ve revizyon kaydı | `MASTER/STATE.md`, `MASTER/00` … `MASTER/18` | Revizyon L.5.0 güncel durum |

---

## 2 · Donanım cildi (`HARDWARE/00` … `HARDWARE/20`)

| Konu | Dosya |
|---|---|
| Donanım dizini ve özet | `HARDWARE/00-HARDWARE-INDEX.md` |
| Sistem mimarisi baştan sona (`4 x 40x80x2.00 mm` `68 g` `+` ekran-pil gövdesi + `90°` dik bükümlü `b` modülü `20 g`) | `HARDWARE/01-SYSTEM-ARCHITECTURE.md` |
| Elektronik bloklar, `64` altın `+` derz kontağı, `Qi2.2` kablosuz şarj ve `90°` `b` modülü Sıfır-CPU elektroniği | `HARDWARE/02-ELECTRONICS-AND-BUSES.md` |
| Parça kataloğu ve kütle dağılımı (`68.0 g` 4-kadranlı gövde + `20.0 g` `90°` `b` modülü = `88.0 g`, `84` iç parça) | `HARDWARE/03-PART-CATALOGUE.md` |
| Portsuz `Qi2.2` kablosuz gövde (gövdede Type-C yok) ve sadece `90°` `b` çubuğunda yer alan tek `USB Type-C` (`40 W`) | `HARDWARE/04-PORT-RAIL.md` |
| **`90°` dik bükümlü `b` modülü (`20.0 g`): sadece çubuk `90°` dik, yuvarlak halka ekran üstünde düz (ön/arka çift yönlü)** | `HARDWARE/05-B-MODULE-CAMERA-AND-PANEL.md` |
| **Form dili: `80.0 x 160.0 x 2.00 mm` (`68 g`) 4-kadranlı (`+`) polikarbonat ekran-pil gövdesi (`<15 µm`, `n=1.585` çiziksiz derz)** | `HARDWARE/06-FORM-LANGUAGE-AND-EDGES.md` |
| 3B modeller (`13` STL) ve render mimarisi (`8` PNG) | `HARDWARE/07-MODELS-AND-3D.md` |
| Bağlantı şartnamesi (`+` merkez derzi `24` N52H + `64` altın yaprak ve 4-kenar tersinir `90°` `b` kenetlenmesi) | `HARDWARE/08-CONNECTION-SPEC.md` |
| Açık doğrulama kalemleri | `HARDWARE/09-OPEN-ITEMS.md` |
| `+` derzi manyetik kilidi (`11.2 N`), 4-kenar `90°` `b` klipsi (`7.2 N`), `3 ms` Dead-Pad ve `IP68` sızdırmazlık | `HARDWARE/10-ANY-PLACE-AND-THE-MAGNETIC-FIELD.md` |
| **4-kadranlı (`+`) göz-güvenli `LLZO/PEO` katı-hal batarya (`4 x 3.0 Wh = 12.0 Wh`, `<=36.2 °C`, `ISO 10993`, `EU 2023/1542`)** | `HARDWARE/11-THE-ENERGY-SHEET.md` |
| **Bükülme kanunu**: `2.00 mm` 11-katmanlı katı-hal polikarbonat laminatın `R25.5 mm`'de `%0.38` gerinimle bükülmesi | `HARDWARE/12-THE-BEND-LAW.md` |
| **`90°` dik bükümlü `b` modülü parça parça (32 iç parça: `±90°` Ti menteşe, çubukta tek Type-C + anten, halkada 50 MP kamera + arka AMOLED)** | `HARDWARE/13-B-MODULE-PART-BY-PART.md` |
| Portsuz `Qi2.2` gövde (`14` parça) ve `90°` `b` çubuğu `USB Type-C` arayüzü (`28` parça = `42` parça) | `HARDWARE/14-PORT-RAIL-PART-BY-PART.md` |
| **4-kadranlı (`+`) `LLZO/PEO` katı-hal batarya ve `Qi2.2` kablosuz şarj sistemi parça parça (25 parça grubu)** | `HARDWARE/15-THE-ENERGY-SHEET-PART-BY-PART.md` |
| **4-kadranlı (`+`) `<15 µm` (`n=1.585`) çiziksiz T-OLED + PDLC + AgNW/ITO ekran parça parça (`79.6 x 159.6 mm`)** | `HARDWARE/16-THE-SCREEN-PART-BY-PART.md` |
| **`2.00 mm` (`68.0 g`) 4-kadranlı gövde ve `20.0 g` `90°` `b` modülü parça parça (14 grup, toplam `88.0 g`, `84` iç parça)** | `HARDWARE/17-BODY-AND-SANDWICH-PART-BY-PART.md` |
| Masaüstü `Qi2.2` + altın kontaklı dock ve stand parça parça (27 parça) | `HARDWARE/18-THE-DOCK-PART-BY-PART.md` |
| **Radyo ve antenler: `90°` dik `b` çubuğunda 3-bant LCP + `1x4` `60 GHz` dizi (`SAR = 0.054 W/kg`) ve `U2` Sıfır-CPU SiP** | `HARDWARE/19-THE-RADIO-AND-ANTENNAS-PART-BY-PART.md` |
| **`90°` dik bükümlü Budlum `b` modülü (`20.0 g`, `uploads/b.png` 1:1, sadece çubuk `90°` dik, halka ekran üstünde düz)** | `HARDWARE/20-THE-BUDLUM-MONOGRAM.md` |

---

## 3 · Paftalar (`pafta/E01`…`E03`, `pafta/P01`…`P22` · toplam 25 temiz SVG pafta + `BUDLUM-LEAF-STACK.svg`)

| Pafta | Konu |
|---|---|
| `pafta/E01-SISTEM-KAMERA-VE-PORT.svg` | Sistem mimarisi: `4 x 40x80x2.00 mm` (`68 g`) `+` ekran-pil gövdesi, `Qi2.2` kablosuz şarj ve ekran üstünde `90°` dik bükümlü `b` modülü (`20 g`) |
| `pafta/E02-B-MODULU-KESIT.svg` | `90°` dik bükümlü `b` modülü kesiti (`32` parça): sadece çubuk (`USB-C` + anten) `90°` dik, yuvarlak halka (`50 MP` kamera + arka AMOLED) ekran üstünde |
| `pafta/E03-PORT-RAY-KESIT.svg` | Portsuz `Qi2.2` (`Ø54 mm` + `4 x Ø22 mm`) kablosuz gövde, `+` derzi (`64` altın yaprak) ve sadece `90°` `b` çubuğundaki tek `USB Type-C` (`40 W`) |
| `pafta/P01` … `P10` | Genel yerleşim (`4 x 40x80x2.00 mm` `+` gövde), enerji (`12.0 Wh` `LLZO` + `<=36.2 °C` göz güvenliği), `<15 µm` (`n=1.585`) çiziksiz derz ve `Qi2.2` şarj |
| `pafta/P11-ENERJI-SANDVICI.svg` | `2.00 mm` 11-katmanlı simetrik `ISO 10993` polikarbonat + `T-OLED` + `LLZO/PEO` katı-hal pil kesiti ve `<15 µm` (`n=1.585`) optik `+` derzi |
| `pafta/P12-BATARYA-TASARIMI.svg` | Gözlük ve insan sağlığına uygun yanmaz `LLZO/PEO` katı-hal batarya (`4 x 3.0 Wh = 12.0 Wh`, `0` HF, `<=36.2 °C`, `<0.08 µT`, `SAR 0.054 W/kg`) |
| `pafta/P13-MIKNATIS-ALANI-VE-ACI.svg` | `+` merkez derzi (`(0,0)` Ti göbek, `24` N52H, `64` altın yaprak) ve `90°` bükümlü `b` modülünün 4 kenar ve ön/arka (`+Z/-Z`) tersinir kenetlenmesi |
| `pafta/P14-B-MODULU-PARCA-PARCA.svg` | `90°` dik bükümlü `b` modülünün `32` iç parçasının patlatılmış kesiti ve tam BOM tablosu |
| `pafta/P15-B-MODULU-OPTIK-VE-PANEL.svg` | Ekran üstüne düz oturan `b` halkasında `50 MP` katlanmış optik (`z=0.90..3.60`), `0.15 mm` kalkan ve arka yuvarlak AMOLED (`z=0.35..0.75`) |
| `pafta/P16-PORT-RAYI-PARCA-PARCA.svg` | Portsuz `Qi2.2` kablosuz gövde (`14` parça) ve `90°` `b` çubuğundaki tek `USB Type-C` (`40 W PD 3.1`) + kenar klipsi (`28` parça) |
| `pafta/P17-ENERJI-LEVHASI-PARCA-PARCA.svg` | 4-kadranlı (`+`) `LLZO/PEO` katı-hal batarya, `Qi2.2` bobinleri, `<=36.2 °C` NTC ve `+` derzi (`25` parça grubu / `52` gövde alt parçası) |
| `pafta/P18-EKRAN-PARCA-PARCA.svg` | `<15 µm` (`n=1.585`) sıfır çizikli optik `+` derzi, Corning kenar-sarmalı iletkenler ve titreşimsiz DC-dimming `T-OLED + PDLC` ekran (`10` grup) |
| `pafta/P19-GOVDE-VE-SANDVIC-PARCA-PARCA.svg` | `80 x 160 x 2.00 mm` (`68 g`) 4-kadranlı gövde ve `20 g` `90°` `b` modülünün 14 ana grubu (`88 g` toplam, `84` modellenmiş iç parça) |
| `pafta/P20-RADYO-VE-ANTENLER.svg` | `90°` dik `b` çubuğunda 3-bant LCP + `1x4` `60 GHz` dizi (`SAR 0.054 W/kg`), `Mu-metal` göz kalkanı ve `U2` Sıfır-CPU `UWB/mmWave` SiP |
| `pafta/P21-BUDLUM-MODULU.svg` | **Ana B modülü paftası**: sadece çubuk (`USB-C` + anten) `90°` dik bükümlü, yuvarlak halka ekran üstünde düz, 4-kenar ön/arka tersinir |
| `pafta/P22-CIHAZ-VE-KENAR-MODULU.svg` | **Ana cihaz paftası**: `4 x 40x80x2.00 mm` (`68 g`) `+` ekran-pil gövdesi, `Qi2.2` kablosuz şarj (gövdede Type-C yok) ve `90°` bükümlü `b` modülü |
| Pafta denetimi | `pafta/check_sheets.py` ve `pafta/check_widths.py`: **tüm 32 SVG dosyasında OVER=0, COVERED=0, COLLIDE=0, taşan satır=0** |

---

## 4 · 3B modeller (`cad/models/`) ve yüksek çözünürlüklü renderlar (`teslim/`)

| Çıktı | Dosya | Açıklama |
|---|---|---|
| **3B `90°` dik bükümlü B modülü (`32` parça)** | `cad/models/monogram-module.stl`, `monogram-letter.stl`, `monogram-ring.stl` | `40 x 44 x 6.70 mm` bükümlü zarf (`20.0 g`): sadece çubuk (`USB-C` + anten) `90°` dik, `Ø32/Ø24 mm` halka ekran üstünde düz |
| **3B tam cihaz (`84` iç parça)** | `cad/models/leaf160-device.stl` | `4 x (40x80x2.00 mm)` (`68 g`) `+` ekran-pil karoları + ekran üstünde `90°` dik bükümlü `b` modülü (`20 g`, toplam `88 g`, `155 968` üçgen) |
| **3B 4-kadranlı çerçeve, ekran ve katı-hal pil** | `cad/models/leaf160-frame.stl`, `leaf160-screen.stl`, `leaf160-battery.stl`, `leaf160-battery-bent.stl` | `Q1..Q4` `ISO 10993` PC kabuklar, `<15 µm` `+` derzi, `(0,0)` Ti göbek, `4 x 3.0 Wh` `LLZO` piller, `Ø54 mm` `Qi2.2` + `4 x Ø22 mm` bobinler ve `R25.5` bükülme |
| **3B gövde ailesi (`Leaf 80 / 160 / 480`)** | `cad/models/leaf80-body.stl`, `leaf160-body.stl`, `leaf480-body.stl` | `40x80x2.00 mm` tekil karo/gözlük (`17 g`), `80x160x2.00 mm` 4-kadranlı gövde (`68 g`), `320x480x2.40 mm` çoklu karo gövde |
| **Tam cihaz ve `90°` B modülü 3B renderları** | `teslim/render-whole.png`, `render-face.png`, `render-back.png`, `render-battery.png`, `render-apart.png`, `render-module.png`, `render-module-back.png` | 4-kadranlı (`+`) ekran-pil gövdesi, `Q4` tak-çıkar karo (`EU 2023/1542`), `84` parçalı patlatılmış görünüm ve `90°` dik bükümlü `b` modülü renderları |
| **heypcb.ai/canvas sunum paftası** | `teslim/heypcb-post.png`, `teslim/heypcb-post.txt` | 6 panelli (`2400 x 1950 px`) yüksek çözünürlüklü 3B sunum görseli ve Revizyon L.5.0 teknik açıklama metni |
