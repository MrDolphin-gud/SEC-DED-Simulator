# Hamming SEC-DED Kod Simülatörü

Bu proje, Hamming Kodunun SEC (Single Error Correction - Tek Hata Düzeltme) ve DED (Double Error Detection - Çift Hata Tespiti) modlarını simüle eden bir Python uygulamasıdır.

## Özellikler

- 8, 16 ve 32 bitlik veri girişi desteği
- SEC (Tek Hata Düzeltme) modu
- DED (Çift Hata Tespiti) modu
- Kullanıcı dostu grafiksel arayüz
- Detaylı hata analizi ve raporlama
- Gerçek zamanlı sendrom hesaplama
- Adım adım Hamming kod hesaplama süreci gösterimi

## Gereksinimler

- Python 3.x
- tkinter (Python ile birlikte gelir)

## Kurulum

1. Projeyi bilgisayarınıza klonlayın veya indirin
2. Python'un bilgisayarınızda kurulu olduğundan emin olun
3. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install numpy
   ```

## Kullanım

1. Uygulamayı başlatın:
   ```bash
   python hamming.py
   ```

2. Arayüzde:
   - Veri girişi alanına 8, 16 veya 32 bitlik binary sayı girin (örn: "10101010")
   - İstediğiniz modu seçin (SEC veya DED)
   - Hata simülasyonu için bit pozisyonunu/pozisyonlarını girin
   - "Simüle Et" butonuna tıklayın

## Modlar

### SEC (Single Error Correction) Modu
- Tek bit hatalarını tespit eder ve düzeltir
- Sendrom kelimesi ile hatalı bitin pozisyonunu belirler
- Hata düzeltme işlemini otomatik olarak gerçekleştirir

### DED (Double Error Detection) Modu
- İki bit hatalarını tespit eder
- Çift hataların düzeltilemeyeceğini gösterir
- Sendrom kelimesi ile hata durumunu analiz eder

## Çıktılar

Program aşağıdaki bilgileri gösterir:
- Orijinal veri
- Hamming kodu
- Parite bitlerinin hesaplanması
- Hata simülasyonu sonuçları
- Sendrom kelimesi
- Hata analizi ve yorumu

## Örnek Kullanım

1. SEC Modu için:
   - Veri: "10101010" (8 bit)
   - Hata pozisyonu: 3
   - Program hatalı biti tespit edip düzeltecektir

2. DED Modu için:
   - Veri: "10101010" (8 bit)
   - Hata pozisyonları: 3 ve 5
   - Program çift hatayı tespit edip düzeltilemeyeceğini gösterecektir

## Teknik Detaylar

### Hamming Kod Hesaplama
- Veri bitleri ve parite bitleri ayrı ayrı hesaplanır
- Parite bitleri 2^n pozisyonlarında yerleştirilir (1,2,4,8,...)
- Her parite biti veri bitinde 1 olan bitlerinin XOR'u ile hesaplanır

### Hata Tespiti
- Sendrom kelimesi, orijinal ve hatalı check bitlerinin XOR'u ile hesaplanır
- SEC modunda sendrom, hatalı bitin pozisyonunu gösterir
- DED modunda sendrom, çift hataların varlığını gösterir
