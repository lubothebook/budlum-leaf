# Revizyon L.4.1: "Bare" Gövde ve Modüler Alt Batarya Mimarisi

Bu doküman, cihazın "Bare" (Çıplak) gövde konseptine uygun olarak yenilenen donanım ve mühendislik planlarını içermektedir. Sürekli esnek batarya tabakası iptal edilmiş olup, enerji ve giriş/çıkış birimleri alt modüle taşınmıştır.

## 1. Gövde ve Ekran Mimarisi
*   **"Bare" (Saf) Ekran Yapısı:** Batarya, iki ekran arasından çıkarılmıştır. Gövde, birbirine kaynaklanmış iki polikarbonat yüzey ve ortasındaki taşıyıcı iskeletten (spine) oluşmaktadır.
*   **Fiziksel Özellikler:** CPU, RAM veya soğutucu blok içermeyen bu yapı sayesinde gövde kalınlığı 1.02 ile 1.20 mm arasına, ağırlığı ise 20 gram seviyesine indirilmiştir. Ekran tamamen esnek, şeffaf ve kağıt inceliğindedir.
*   **Görüntü ve Gizlilik (T-OLED ve PDLC Film):**
    *   *Esnek Şeffaf OLED (T-OLED):* Çift taraflı görüntü verebilen veya sırt sırta yapıştırılmış iki ultra ince, esnek şeffaf ekran katmanı uygulanacaktır.
    *   *PDLC (Polimer Dağıtılmış Likit Kristal) Film:* Ekran katmanları arasına veya dış yüzeyine gizlilik kilidi olarak entegre edilecektir. Düşük voltaj uygulandığında cam matlaşarak arka tarafın görünürlüğünü tamamen kesecek, voltaj kesildiğinde ise tekrar şeffaf yapıya dönecektir.

## 2. İletim Teknolojisi
*   **Görünmez Ağlar (Elektrik ve Veri İletimi):** Polikarbonat gövdenin iletken olmaması nedeniyle, bataryadan ekrana güç ve veri taşıma işlemi için polikarbonat katmanlar arasına Gümüş Nanotel (Silver Nanowires - AgNW) veya Şeffaf İletken Oksit (ITO) katmanları entegre edilmiştir.
*   Bu materyaller çıplak gözle görünmez yapıda olup, cihazın şeffaf cam formunu korumasını sağlar.

## 3. Alt Batarya Modülü ve Kenetlenme Sistemi
*   **Hibrit Kenetleme Sistemi ve Geçiş Bölgesi:** 
    *   Esnek polikarbonat ekranın en alt 1-2 santimetrelik kısmı, esnekliği azaltılmış daha sert bir polimer ve görünmez bir mikro-iskelet ile desteklenerek sertleştirilmiş geçiş bölgesi oluşturulmuştur.
    *   Alt batarya tabakası, ekranın en altına 8+8 N52H mıknatıslar (6.5 N tutunma gücü) ile fiziksel olarak kenetlenen manyetik pogo-pin rayı üzerinden cihaza oturmaktadır.
*   **Güç Aktarımı:** İletim, cihazın alt sınırına yerleştirilmiş ve polikarbonatla hizalanmış 12 adet altın temas noktası (gold pad) üzerinden sağlanmaktadır.
*   **"Ölü Pin" (Dead-Pad) Güvenliği:** Altın pinlerde kısa devreyi önlemek amacıyla donanımsal güvenlik katmanı mevcuttur. Modül yerine tam oturup kriptografik çip üzerinden 3 milisaniyelik kimlik doğrulaması (handshake) yapılana kadar pinlere elektrik akımı verilmeyecektir. Bağlantı noktaları IP68 suya ve toza dayanıklılık standartlarındadır.

## 4. Enerji Kapasitesi ve Kesintisiz Çalışma
*   **Kapasite Dengesi:** Harici, esnek olmayan (rigid) alt modül form faktörü sayesinde litre başına 700 ila 950 Wh enerji yoğunluğuna ulaşan yüksek verimli piller kullanılacaktır (~10.000 mAh hedef kapasite).
*   **Giriş/Çıkış (I/O) Portları:** Bu alt tabaka aynı zamanda Type-C, kulaklık jakı gibi girişleri barındırarak yapısal bir tutma bariyeri (chin/grip) işlevi görecektir.
*   **Hot-Swap (Kesintisiz Değişim) Özelliği:** Kullanıcının batarya modülünü değiştirmesi veya şarja bağlaması sırasında cihazın kapanmasını önlemek için sisteme bir tampon kapasitör (buffer capacitor) eklenmiştir. Bu mekanizma, değişim sırasında (yaklaşık 15 saniye boyunca) donanımı aktif tutacaktır.

## 5. "Sıfır CPU" Mimarisi ve İletişim
*   Cihaz Thin-Client (İnce İstemci) olarak tasarlandığı için alt modülde işlemci (CPU) veya RAM bulunmamaktadır. Ağır işlemler ağdaki onaylayıcı (validator) düğümlerde veya harici hub donanımlarında gerçekleştirilecektir.
*   **Alt Modül Donanımları:** Batarya ünitesi ve I/O portları dışında modül sadece iki ana bileşeni barındırır:
    1.  *Ekran Sürücüsü (Display Driver):* Panel piksellerini yönetecek kontrolcü çip.
    2.  *UWB (Ultra Geniş Bant) / mmWave Alıcı:* Harici işlem gücü donanımıyla (hub veya bulut) gecikmesiz (0 latency) iletişim kurmak, görüntü verisini almak ve dokunmatik geri bildirimleri iletmek için gereken yüksek bant genişliğini sağlayan kablosuz modül.