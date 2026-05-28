# 📱 AndroidHierarchyViewer

`uiautomator2` tabanlı modern Android UI Hierarchy Viewer ve Inspect aracıdır.

Chrome DevTools inspect sistemi mantığıyla geliştirilmiştir.

---

# 🚀 Özellikler

* ✅ Canlı Android XML hierarchy dump
* ✅ Otomatik ekran görüntüsü alma
* ✅ XML Tree yapısı
* ✅ Bounds overlay çizim sistemi
* ✅ Canlı hover inspect sistemi
* ✅ Tıklayarak element seçme
* ✅ XML ↔ Görsel senkronizasyon
* ✅ Ham XML görüntüleme
* ✅ Otomatik dump kaydı
* ✅ Modern Dark/Metro UI
* ✅ PyQt6 profesyonel arayüz
* ✅ Bounds parser sistemi
* ✅ Clipboard XML kopyalama
* ✅ Scroll destekli telefon ekranı
* ✅ Canlı yenileme sistemi

---

# 🧠 Inspect Sistemi

Araç Chrome DevTools mantığıyla çalışır.

Yapabilecekleriniz:

* Element hover inspect
* Canlı UI analizi
* Görsel element seçimi
* XML node senkronizasyonu
* Raw XML highlight sistemi

---

# 🖱️ Hover Inspect

Mouse ile element üzerine gelindiğinde:

* Yeşil highlight oluşur
* Tooltip içinde:

  * Class
  * Text
  * Resource ID
  * Clickable
  * Enabled
  * Bounds

bilgileri gösterilir.

---

# 🎯 Element Seçimi

Elemente tıklanınca:

* Kırmızı outline oluşur
* XML node otomatik seçilir
* TreeView ilgili yere gider
* Raw XML highlight edilir

---

# 📡 Canlı Yenileme Modu

Gerçek zamanlı UI takip sistemi.

Özellikler:

* Otomatik XML yenileme
* Otomatik screenshot alma
* Dinamik ekran analizi
* Gerçek zamanlı hierarchy takibi

---

# 🖼️ Screenshot Overlay Sistemi

Program:

* Gerçek telefon ekranı
* XML bounds rectangle
* Overlay render sistemi

oluşturur.

Kullanılan sistemler:

* QGraphicsScene
* QGraphicsRectItem
* QGraphicsPixmapItem

---

# 📦 Teknolojiler

| Teknoloji       | Açıklama          |
| --------------- | ----------------- |
| Python          | Ana dil           |
| PyQt6           | Modern GUI        |
| uiautomator2    | Android otomasyon |
| XML ElementTree | XML parse         |
| QPainter        | Overlay sistemi   |

---

# ⚙️ Gereksinimler

## Python

Python 3.10+

## Android

* USB Debugging açık olmalı
* ADB kurulu olmalı

---

# 📦 Kurulum

## Repo Klonla

```bash
git clone https://github.com/ebubekirbastama/Android_GU-_Hierarchy_Viewer.git
cd Android_GU-_Hierarchy_Viewer
```

---

## Gereksinimleri Kur

```bash
pip install -r requirements.txt
```

---

# 📜 requirements.txt

```txt
PyQt6>=6.6.0
uiautomator2>=3.1.0
```

Opsiyonel:

```bash
pip install adbutils lxml pillow
```

---

# ▶️ Çalıştır

```bash
python AndroidHierarchyViewer.py
```

---

# 🧪 Test Edilen Platformlar

| Platform   | Durum |
| ---------- | ----- |
| Windows 10 | ✅     |
| Windows 11 | ✅     |

---

# 🔥 Planlanan Özellikler

* XPath Generator
* CSS Selector Generator
* Çoklu cihaz desteği
* AI selector sistemi
* OCR analiz sistemi
* Element crop sistemi
* Auto tap inspector
* Search sistemi

---

# 🔬 Kullanım Alanları

* Android Automation
* Reverse Engineering
* Mobile Testing
* UI Analysis
* Accessibility Testing
* Bot Development
* Mobile Scraping
* Dynamic Selector Extraction

---

# 📄 Lisans

Apache License 2.0

---

# ❤️ Geliştirici Notu

Bu proje:

* Modern UI
* Gerçek zamanlı inspect sistemi
* Profesyonel overlay sistemi
* Chrome DevTools benzeri deneyim

sunmayı hedeflemektedir.
