# 📱 AndroidHierarchyViewer

Modern ve görsel Android UI Hierarchy Viewer aracı.
`uiautomator2` kullanarak bağlı Android cihazdan canlı XML dump alır, ekran görüntüsü oluşturur ve UI elementlerini görsel olarak işaretler.

---

# 🚀 Özellikler

* ✅ Android cihazdan canlı UI XML dump alma
* ✅ Otomatik ekran görüntüsü alma
* ✅ XML verisini TreeView şeklinde görselleştirme
* ✅ Telefon ekranı üzerinde element sınırlarını çizme
* ✅ Ham XML görüntüleme
* ✅ XML dump'ı otomatik `.txt` olarak kaydetme
* ✅ Modern Dark/Metro UI
* ✅ PyQt6 tabanlı profesyonel arayüz
* ✅ Bounds parsing sistemi
* ✅ XML clipboard kopyalama
* ✅ Scroll destekli telefon ekran önizleme sistemi

---

# 🖼️ Görünüm

## Sol Panel

* XML Tree Structure
* Ham XML görüntüsü

## Sağ Panel

* Gerçek telefon ekranı
* UI element bounding box çizimleri

---

# 📦 Kullanılan Teknolojiler

| Teknoloji       | Açıklama                |
| --------------- | ----------------------- |
| Python          | Ana programlama dili    |
| PyQt6           | Modern masaüstü GUI     |
| uiautomator2    | Android UI dump sistemi |
| XML ElementTree | XML parsing             |
| QPainter        | Bounds çizim sistemi    |

---

# ⚙️ Gereksinimler

## Python

* Python 3.10+

## Android

* USB Debugging açık olmalı
* ADB kurulu olmalı

---

# 🔌 Kurulum

## 1) Repo'yu Klonla

```bash
git clone https://github.com/ebubekirbastama/Android_GU-_Hierarchy_Viewer.git
cd AndroidHierarchyViewer
```

---

## 2) Gereksinimleri Kur

```bash
pip install -r requirements.txt
```

---

## 3) Android Cihazı Bağla

ADB cihazını kontrol et:

```bash
adb devices
```

---

## 4) Uygulamayı Başlat

```bash
python AndroidHierarchyViewer.py
```

---

# 📜 requirements.txt

```txt
PyQt6
uiautomator2
```

---

# 📱 Nasıl Çalışır?

Program:

1. Android cihaza bağlanır
2. XML hierarchy dump alır
3. Telefon ekran görüntüsünü kaydeder
4. XML içindeki bounds değerlerini parse eder
5. Telefon ekranı üzerine kırmızı kutular çizer
6. XML yapısını TreeView içinde gösterir

---

# 🧠 XML Bounds Örneği

```xml
bounds="[0,120][1080,240]"
```

Program bunu otomatik olarak:

```python
x1, y1, x2, y2
```

şeklinde parse ederek ekrana çizer.

---

# 📸 Otomatik Kayıt Sistemi

Her dump işleminde otomatik oluşturulur:

```bash
dump_xxxxx.txt
screenshot_xxxxx.png
```

UUID tabanlı random isim sistemi kullanılır.

---

# 🛠️ Desteklenen Özellikler

| Özellik                  | Durum |
| ------------------------ | ----- |
| XML Dump                 | ✅     |
| Screenshot               | ✅     |
| Bounds Visualization     | ✅     |
| Tree Structure           | ✅     |
| Dark Theme               | ✅     |
| Clipboard Copy           | ✅     |
| Scrollable Phone Preview | ✅     |

---

# 🔥 Gelecek Özellikler

* [ ] Canlı element seçimi
* [ ] Tıklayınca elementi highlight etme
* [ ] XPath generator
* [ ] CSS selector generator
* [ ] Search sistemi
* [ ] Multi-device support
* [ ] Screenshot zoom
* [ ] Element inspector panel
* [ ] Auto-refresh mode

---

# 🧪 Test Edilen Ortamlar

| Sistem     | Durum |
| ---------- | ----- |
| Windows 10 | ✅     |
| Windows 11 | ✅     |

---

# ⚠️ Notlar

* Telefon ekranı açık olmalıdır
* USB debugging aktif olmalıdır
* Bazı üretici ROM'larında ek izin gerekebilir

---

# 👨‍💻 Geliştirici

Developed by Ebubekir Bastama

GitHub:
https://github.com/ebubekirbastama

---

# ⭐ Katkıda Bulun

Pull request gönderebilir veya issue açabilirsiniz.

---

# 📄 Lisans

MIT License

---

# ❤️ Android Automation & Reverse Engineering Tools
