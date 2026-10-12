# BUDLUM LEAF · REVİZYON L.4.1 · ÇOKLU-AJAN (ARENA API) İÇ PARÇA VE MİMARİ DENETİM RAPORU

**Tarih:** 2026-10-12 · **Yöntem:** Arena API Gateway (`https://api.preview.arena.ai/v1/chat/completions`) üzerinden 4 paralel uzman ajan denetimi.
**Güvenlik Notu:** API anahtarı hiçbir dosyaya kaydedilmemiştir; yalnızca çalışma anında bellekten kullanılmıştır.

---
## 1_POLYCARBONATE_AND_FLEX_BODY_AGENT (Arena Modeli: `claude-sonnet-5-5`)

**Budlum Leaf 160 Rev L.4.1 – Bare gövde (80×160×1.10 mm, 20.0 g)**

Not: Bu ölçülerin bir kısmı tasarım hedefi veya varsayımdır. Prototipte doğrulanmaları gerekir.

**Katman dizilimi (dıştan merkeze, simetrik):** PC 0.22 → OCA 0.06 → T-OLED 0.16 → AgNW/ITO 0.04 → PDLC 0.14 (merkez) → ayna simetri. Toplam 0.44 + 0.12 + 0.32 + 0.08 + 0.14 = **1.10 mm**. Nötr düzlem z = 0.55 mm.

1. **PC kabuk (2×0.22 mm):** Optik kalite polikarbonat, lazer/ultrasonik kaynaklı, 80×160 mm. Görevi darbe ve burulma taşımak ve hava ile nem bariyeri olmaktır.
2. **SiO₂ sert kaplama (~2–3 µm, dış yüzler):** Çizilmeye karşı yüzey sertliği sağlar. Gerinim sınırı ~%0.5 civarında olduğundan R=25.5 mm'de sınırda çalışır. Çatlak testi gerekir.
3. **Kenar mikro-iskelet (castellated flex-rib omurga, 1.0 mm geniş × 0.50 mm yüksek, çevre boyunca):** Ti/PC hibrit, 2 mm adımlı dişli yapıdır. Kenarlarda eğilme rijitliğini ve burulma direncini artırır. Diş boşlukları bükülmeye izin verir.
4. **Silikon elastomer OCA kayma katmanları (2×0.06 mm):** Düşük modüllü (~0.1 MPa) optik berrak silikon. Katmanları mekanik olarak ayırır ve kaymaya izin verir.
   - Ayrık kabuk için gerinim: 0.11/25.5 = %0.43.
   - Verilen %0.51 değeri, kalan kayma bağlaşımı ve kaplama payı olarak ~0.02 mm ekler.
   - Katmanlar tam yapışık olsaydı gerinim 0.55/25.5 = %2.16 olurdu. OCA ayrıştırması bu yüzden şarttır.
5. **Çift yüz T-OLED (2×0.16 mm):** İnce film kapsüllü şeffaf OLED, her yüze bir panel. Ekran emisyonu sağlar.
6. **GIP kenar sürücü şeritleri (~1.5 mm geniş × 0.16 mm, panel kenarında):** Satır sürücüsünü panele entegre eder. Ayrı sürücü çipi ihtiyacını ve kenar kalınlığını azaltır.
7. **PDLC gizlilik filmi (0.14 mm, merkez nötr düzlem):** Gizlilik filmi, gerinimin en düşük olduğu yere yerleştirilmiştir. Gerilim verilince şeffaf, verilmeyince saydam değildir.
8. **Yan elektrot baraları (~0.8 mm × 0.03 mm Ag/Cu, uzun kenarlarda):** PDLC filmini yanlardan homojen sürer.
9. **Görünmez AgNW/ITO ağları (2×0.04 mm):**
   - Güç, MIPI veri hatları ve 240 Hz dokunmatik/kalem sensör matrisini taşır.
   - AgNW esnek yönde, ITO ise düşük bükülme bölgelerinde kullanılır.
   - Katmanlar OLED ile PDLC arasında simetrik yer alır.
10. **Alt 15.0 mm geçiş bölgesi (y = −80…−65, 80 mm genişlik):**
    - Dereceli Ti (Gr.5) / CFRP tarak mikro-iskelet (comb fingers), ~0.20–0.30 mm kalınlıkta, ~1.0 mm parmak genişliği ve 0.5 mm aralık.
    - Esnek gövdeden rijit bölgeye gerilim yoğunlaşmasını yumuşatır.
    - Üst uçta CFRP, alt uçta Ti ağırlıklıdır (kademeli).
11. **Enerji ve güç elektroniği (alt bölge):**
    - 3× katı-hal ince film süperkapasitör hücresi (2.2 F, ~18×10×0.45 mm). Hot-swap sırasında ~15 s enerji köprüsü sağlar.
    - LDO/Boost IC (~2.0×2.0×0.4 mm): Gerilimi ayarlar.
    - Dead-Pad FET (~1.6×1.6×0.3 mm): Boş pad durumunda enerji kaçağını keser ve ters akımı engeller.
12. **Arayüz:**
    - 12 altın pad (~2.0×1.2×0.05 mm, Ni/Au kaplı): Güç, veri ve algılama kontaklarıdır.
    - 8 N52H mıknatıs yuvası (Ø3.0×0.6 mm cep, mıknatıs Ø3×0.5 mm): Hizalama ve tutma sağlar.
    - Yuvalar rijit bölgede yer alır ve bükülme alanına taşmaz.

**Riskler:**
- SiO₂ sert kaplama gerinim sınırına yakın.
- Alt bölgede 1.10 mm içine süperkapasitör (0.45 mm) ve mıknatıs (0.6 mm) sığdırmak için katman yerel olarak inceltilmelidir.
- Ağırlık bütçesi (20.0 g) Ti/CFRP ve mıknatıslarla birlikte doğrulanmalıdır.

---
## 2_BOTTOM_BATTERY_STRENGTH_AND_POWER_AGENT (Arena Modeli: `gpt-6-sol`)

**Budlum Leaf 160 L.4.1 — alt batarya modülü, 10 maddelik tasarım raporu**

**Önce kritik sınır:** Verilen iki hücrenin toplam hacmi **4,41 mL**’dir. **700–950 Wh/L** yoğunlukta bu hacim **3,1–4,2 Wh** sağlar; **38,5 Wh / ~10.000 mAh** sağlamaz. Hatta 38,5 Wh, bütün **80,0 × 36,0 × 4,00 mm** modül hacminde **3.342 Wh/L** gerektirir. Bu nedenle 46,0 g hedefi ve parça kütleleri, hücre kapasitesi düzeltilmeden doğrulanmış bir ürün spesifikasyonu sayılamaz.

1. **Dış yapı:** **80,0 × 36,0 × 4,00 mm**, hedef **46,0 g**. Rijit çevre çerçevesi ve kontrollü oturma yüzeyleri eğilmeyi ve hücreye noktasal basıyı sınırlar.
2. **İç şasi:** **6061-T6 CNC H-kiriş**; yaklaşık **0,6–1,0 mm** et kalınlığı, tahmini **4–7 g**. Yükü hücrelere değil kenetlenme noktalarına taşır.
3. **Kenetlenme köprüsü:** **y = −80 mm** çenesinde **0,35 mm Grade-5 titanyum**, boyuna bağlı yaklaşık **0,2–0,5 g**. Lazer kaynağı **Ti–Ti** bağlantıda kullanılmalı; titanyumu 6061 alüminyuma doğrudan kaynaklama varsayılmamalıdır.
4. **Twin-Pouch Si-C hücreler:** Sol ve sağda **2 × 34,0 × 24,0 × 2,70 mm**; hücre kütlesi üretici verisiyle belirlenir. Bu ölçülerle savunulabilir enerji **toplam 3,1–4,2 Wh**’dir, 38,5 Wh değil.
5. **Akım bağlantıları:** Kaynaklı nikel bara sekmeleri ve yalıtılmış geçişler; sekme kalınlığı tasarım hedefi **0,10–0,20 mm**, kütlesi yerleşime göre ölçülmelidir. Çekme yükünü kaynaklardan uzaklaştıran sabitleme gerekir.
6. **Isıl yapı:** Her hücre için **NTC** ve **0,15 mm pirolitik grafit**; aerojel kalkanın kalınlığı ile gramajı 4,00 mm toplam zarf içinde ayrıca bütçelenmelidir. Grafit ısıyı yayar; aerojel sıcak bölgelerden yalıtır.
7. **Şarj katı:** **40 W USB-PD 3.1** için ayrı PD denetleyicisi ve uygun şarj mimarisi gerekir. **BQ25980 sınıfı parça tek başına Buck-Boost değildir**; kart alanı, mm yüksekliği ve gramajı seçilen entegreyle doğrulanmalıdır.
8. **Güç pasifleri:** **2 × 2,2 µH** ekranlı indüktör ve MLCC dizisi; **4,00 mm** zarfına sığma, toplam **g** ve 40 W’taki sıcaklık artışı gerçek parça seçimiyle doğrulanmalıdır. Yerel ısı, hücrelerden uzak tutulmalıdır.
9. **Hot-Swap:** Kesintisiz **15 saniye** için modül dışında yeterli enerji tamponu şarttır: **40 W yükte 600 J**. Sadece anahtarlama protokolü bu enerjiyi sağlayamaz; tamponun mm/g bütçesi ayrıca tanımlanmalıdır.
10. **Ölü pin koruması:** Temasta enerjisiz pinler, karşılıklı **çift MOSFET**, ön şarj ve kimlik doğrulama kullanılmalı. **3 ms** hedefi pinleri güvenli duruma alma için tanımlanabilir; kriptografik doğrulamanın 3 ms’de biteceği ölçülmeden garanti edilmemelidir. Koruma kartının mm/g değeri prototipte ölçülmelidir.

**Sonuç:** Mekanik güç için yük taşıyan şasi ve güvenli çene; elektriksel güç için yalıtılmış bağlantılar, ısıl sınırlama ve enerjisiz temaslar doğru yaklaşımdır. Ancak belirtilen **hücre boyutu, 10.000 mAh ve 38,5 Wh** aynı tasarımda fiziksel olarak uyuşmaz.


---
## 3_ZERO_CPU_AND_B_MODULE_INTERNAL_PARTS_AGENT (Arena Modeli: `claude-sonnet-5-5`)

**Budlum Leaf 160 Rev. L.4.1: Sıfır-CPU I/O ve dik b modülü iç parçaları**

**A) Alt modül PCBA (74.0×9.5×0.60 mm, 8-katman HDI)**
1. **T-OLED sürücü ASIC:** TCON + PDLC sürücü, 6.5×6.5×0.55 mm.
2. **UWB + 60 GHz mmWave SiP:** 11.0×4.5×0.85 mm. 1×4 faz-dizili yama anten dizisi eşlik eder (anten ölçüsü belirtilmedi).
3. **Hi-Fi ses DAC/amfi:** 32-bit/384 kHz, 4.0×4.0 mm (kalınlık belirtilmedi).
4. **USB Type-C gövdesi:** IP68 iç O-ring contalı, 9.0×7.5×3.2 mm.
5. **3.5 mm TRRS jak tüpü:** IP68 sızdırmaz, 6.0×14.5×3.3 mm.
6. **Manyetik ve bağlantı seti:** 8 adet N52H Halbach mıknatıs, 2 konik çelik kılavuz pim, 12 yaylı altın pogo-pin ve 0.40 mm FKM IP68 conta (tek tek ölçüler belirtilmedi).

**B) Dik b modülü (40×32×4 mm, 21.0 g)**
7. **Dikey çubuk (32 mm):** 3-bant LCP anten (Wi-Fi 7, BT 5.4, UWB) ve koaksiyel besleme.
8. **Kamera halkası (Ø32/Ø24 mm):** 5P katlanmış optik kamera.
9. **Görüntü sensörü:** 50MP, 12.8×9.6 mm.
10. **OIS aktüatör:** Kamera modülüne entegre (ölçü belirtilmedi).
11. **Halka PCB:** Ø32/Ø24 mm halka geometrisinde (kalınlık belirtilmedi).
12. **Mikrofonlar:** 2× MEMS mikrofon (ölçü belirtilmedi).
13. **Mikro-hoparlör akustik kutusu:** 9.0×3.2 mm.
14. **LED flaş ve arka ekran:** Flaş (ölçü belirtilmedi) ve arkada Ø22.4 mm yuvarlak LTPO AMOLED ekran.

**Not:** Verilmeyen ölçüleri uydurmadım. Bu parçalar için ayrıca CAD veya BOM verisi gerekir.

---
## 4_CAD_3D_COMPONENT_MODELING_AUDIT_AGENT (Arena Modeli: `gpt-6-sol`)

## Budlum Leaf L.4.1 — 10 maddelik CAD denetim ve uygulama raporu

**Denetimin sınırı:** Paylaşılan bölüm ölçüleri ve tasarım niyetini gösteriyor; aşağıdaki `leaf_v2.py` gövdesi, üretilmiş STL’ler ve PNG’ler verilmediği için bir parçanın *kesinlikle yok* olduğunu ya da *kesinlikle basit kutu* olduğunu doğrulayamam. Aşağıdaki liste, her parça için **ayrı katı geometriyle doğrulanması gerekenleri** ve yalnızca dış kabuk/kutu varsa yapılacak düzeltmeyi belirtir.

1. **Önce parça envanterini denetlenebilir yapın.** Ekran, geçiş bölgesi, alt modül ve `b` modülü için her iç bileşeni adlandırılmış bağımsız mesh olarak üretin; tek bir gövde mesh’inin içine çizilmiş renkli şekilleri «modellenmiş parça» saymayın. Her parça için `part_id`, malzeme, yerleşim, ölçü, STL yolu ve hangi renderda göründüğünü kaydeden bir manifest oluşturun. Böylece «içinde parça yok» şikâyeti, dosya ve görüntü bazında sınanabilir.

2. **Bare gövdeyi dolu levha yerine gerçek katman ve mikro-iskelet olarak kurun.** İki polikarbonat yüzeyi, T-OLED ve PDLC katmanlarını, çevre omurgasını ve **tek tek mikro-iskelet kaburgalarını** ayrı hacimler olarak modelleyin. Kaburgalar için kesit ve aralık tanımlayıp ekrana taşmalarını önleyin; toplam istifi `BARE_Z0=1.45` ile `BARE_Z1=2.55 mm` arasında tutun. Şeffaf yüzey renderı iç yapıyı saklıyorsa kesit ve patlatılmış görünüş ekleyin. Kaynakta yalnızca `rounded_rect` levhalar varsa, istenen kaburga geometrisi henüz karşılanmıyordur.

3. **AgNW/ITO yollarını renk çizgisi değil, izlenebilir 3B ağ yapın.** Veri ve güç hatlarını ayrı güzergâhlar, dallanmalar, temas adaları ve geçiş bölgesine inen bağlantılar olarak süpürülmüş ince kesitli katılarla temsil edin. Gerçek film kalınlığı STL’de görünemeyecekse **görselleştirme için büyütülmüş kalınlık** kullanın ve manifestte gerçek kalınlığı ayrıca belirtin. İzlerin sürücüye ve pogo arayüzüne sürekliliğini kontrol edin; temassız, yalnızca yüzeye boyanmış çizgi yeterli değildir.

4. **Alt 15 mm geçiş bölgesini ve 15 saniyelik tamponu açın.** `y=-80…-65 mm` içinde sert polimer takviyeyi, mikro-iskelet bağlantılarını, **ayrı süperkapasitör elemanlarını**, hücreler arası bağlantıları ve pogo’ya giden yolları modelleyin. Her kapasitörün gövdesi ve terminalleri görünmeli; `1.10 mm` kalınlık sınırında birbirleriyle veya ekran katmanlarıyla çakışmamalıdır. “15 s” geometriyle kanıtlanamaz: yük gücü, kullanılabilir gerilim aralığı ve kapasite hesabını ayrıca verin.

5. **Alt bataryanın içini tek pil kutusu olmaktan çıkarın.** `80×36×4 mm` zarfı içinde kesitli **H-şasi**, birbirinden ayrılmış **iki Si-C hücre**, hücre terminalleri, **nikel baralar**, yalıtım ve sabitleme boşluklarını bağımsız katılar yapın. Hücreleri şasiden patlatarak gösterin; kapalı görünüşte de kesit sağlayın. Kapasite iddiasını düzeltmeden çizimi onaylamayın: tüm modülün brüt hacmi yalnızca **11,52 mL**; 700–950 Wh/L ile, hiçbir başka parçaya yer ayırmadan bile yaklaşık **8,1–10,9 Wh** eder. Bu, 3,85 V varsayımında en çok yaklaşık **2,1–2,8 Ah**’dir; belirtilen **10.000 mAh** hedefi bu zarf ve enerji yoğunluğuyla uyuşmuyor.

6. **Elektronik kartı ve üzerindeki her işlevsel parçayı ayrı modelleyin.** **8 katmanlı PCBA** için kart konturu, istif kalınlığı, montaj delikleri ve görünür kesit temsili oluşturun. Üstüne **Display Driver ASIC**, **UWB/mmWave SiP**, **dört ayrı yama anten**, **iki indüktör**, **PMIC** ve **DAC**’ı ayrı gövde, pad ve yerleşim yönleriyle koyun. Antenlerin birbirine, metal baralara ve mıknatıslara göre açıklıklarını gösterin. İç katmanları her bakışta gerçek boyutlu göstermek mümkün değilse büyütülmüş kart kesitini açıkça şematik olarak etiketleyin; tek dikdörtgen “PCB kutusu” bu denetimi geçmez.

7. **I/O ve manyetik birleşmeyi iki tarafta da tamamlayın.** USB-C’nin yalnız dış deliğini değil **iç gövdesini ve dilini**; 3,5 mm TRRS’nin **iç tüpünü ve kontak bölgelerini** modelleyin. **8+8 N52H mıknatısın** karşılıklı yuvalarını, mıknatıs katılarını, kutup yönlerini ve **12 ayrı altın pogo-pin** ile karşı pedlerini gösterin. Pogo hareket mesafesi, oturma yüzeyi ve conta için çakışma testi yapın. Panelin 1,10 mm kalınlığı içine mıknatıs yuvası gerçekten sığıyor mu ayrıca çözülmeli. IP68 ve 3 ms “dead-pad” güvenliği, yalnızca CAD geometrisinden doğrulanamaz; conta kesiti ve elektriksel doğrulama ayrı çıktılardır.

8. **`b` modülünün anten ve halka elektroniğini açın.** Sol dik çubuk içine **LCP anten şeridini**, besleme noktasını ve halkaya yönlenen bağlantısını; halka içine **ayrı annüler PCB’yi** yerleştirin. Ø32 dış / Ø24 iç halka yalnızca **4 mm radyal alan** bırakır: PCB, yollar ve bağlantılar bu sınırda ölçülendirilmelidir. Anten şeridini yekpare çubukla birleştirmek veya PCB’yi yalnızca renkle belirtmek yerine ayrı STL katıları üretin.

9. **`b` modülünün optik ve akustik istifini parçalayın.** Ön yüzde **50 MP sensör paketi**, **beş ayrı 5P lens elemanı**, lens taşıyıcı, **OIS hareketli çerçevesi ve bobin/mıknatıs temsili**, **iki ayrı MEMS mikrofon**, hoparlör kutusu ve flaşı; arkada **Ø22,4 mm AMOLED panelin katmanlarını** modelleyin. Bunların hepsinin `z=0…4 mm` içinde birbirine çarpmadan yerleştiğini kesitle gösterin. Özellikle lens/OIS ile arka AMOLED’in aynı hacmi istemesi, çözülmesi gereken bir paketleme riskidir; fiziksel olarak sığmayan istifi renderda gizlemeyin.

10. **STL ve dört renderı kabul testine bağlayın.** Her parça için kapalı/pozitif hacimli mesh, birim-mm, doğru normal, kesişim ve zarf testleri çalıştırın. `render-apart.png` bütün alt montajları ve küçük parçaları ayrılmış/etiketli; `render-battery.png` hücre–H-şasi–bara–PCBA–port sırasını; `render-xray.png` ekran kaburgaları, izler, kapasitörler ve her iki modülün içini; `heypcb-post.png` ise kartın **tek tek ASIC, SiP, dört anten, iki indüktör, PMIC ve DAC** yerleşimini okunur göstermeli. STL malzeme/şeffaflık taşımaz: renk, kesit ve etiketleri render/manifest üzerinden sağlayın
