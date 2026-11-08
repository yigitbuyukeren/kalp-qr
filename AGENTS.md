# Kalp QR
- Tek dosyalı Python CLI yapısını ve mevcut iki bağımlılığı koru.
- QR üretiminde `random.Random(1101)`, hata düzeltme H ve taranabilirlik korunmalı; süslemeler QR matrisini kapatmamalı.
- Mevcut CLI çıktılarının uyumluluğunu bozma.
- Kontrol: `python3 -m unittest discover -s tests`.
