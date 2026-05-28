# 📱 AndroidHierarchyViewer

### 🌍 Languages

- 🇸🇦 العربية
- 🇺🇸 [English](README_EN.md)
- 🇹🇷 [Türkçe](README_TR.md)

# 📱 AndroidHierarchyViewer

أداة حديثة لعرض وتحليل Android UI Hierarchy باستخدام `uiautomator2`.

مستوحاة من نظام Chrome DevTools Inspect.

---

# 🚀 المميزات

* ✅ استخراج XML مباشر من جهاز Android
* ✅ التقاط Screenshot تلقائي
* ✅ عرض XML Tree بشكل مرئي
* ✅ رسم حدود العناصر فوق الشاشة
* ✅ نظام Hover Inspect مباشر
* ✅ اختيار العناصر بالضغط
* ✅ مزامنة XML مع العرض المرئي
* ✅ عرض Raw XML
* ✅ حفظ XML تلقائياً
* ✅ واجهة Dark / Metro حديثة
* ✅ واجهة احترافية باستخدام PyQt6
* ✅ نظام Bounds Parsing
* ✅ نسخ XML إلى Clipboard
* ✅ معاينة شاشة الهاتف مع Scroll
* ✅ وضع التحديث المباشر Live Refresh

---

# 🧠 نظام Inspect

الأداة تعمل بطريقة مشابهة لـ Chrome DevTools.

يمكنك:

* فحص العناصر مباشرة
* تحليل واجهات Android
* اختيار العناصر بصرياً
* مزامنة XML مع الشاشة
* تمييز العناصر داخل Raw XML

---

# 🖱️ Hover Inspect

عند تمرير الماوس فوق العنصر:

* يظهر إطار أخضر
* يتم عرض:

  * Class
  * Text
  * Resource ID
  * Clickable
  * Enabled
  * Bounds

---

# 🎯 اختيار العناصر

عند الضغط على عنصر:

* يظهر إطار أحمر
* يتم تحديد XML Node تلقائياً
* يتم الانتقال داخل TreeView
* يتم تمييز العنصر داخل Raw XML

---

# 📡 وضع التحديث المباشر

يدعم مراقبة UI بشكل مباشر.

المميزات:

* تحديث XML تلقائي
* تحديث Screenshot تلقائي
* تحليل UI لحظي
* مراقبة hierarchy مباشرة

---

# 🖼️ نظام Overlay للشاشة

يقوم البرنامج بعرض:

* Screenshot حقيقي للهاتف
* حدود العناصر
* Overlay rendering system

باستخدام:

* QGraphicsScene
* QGraphicsRectItem
* QGraphicsPixmapItem

---

# 📦 التقنيات المستخدمة

| التقنية         | الوصف              |
| --------------- | ------------------ |
| Python          | اللغة الأساسية     |
| PyQt6           | واجهة رسومية حديثة |
| uiautomator2    | Android Automation |
| XML ElementTree | XML Parsing        |
| QPainter        | Overlay Rendering  |

---

# ⚙️ المتطلبات

## Python

Python 3.10+

## Android

* تفعيل USB Debugging
* تثبيت ADB

---

# 📦 التثبيت

## Clone Repository

```bash
git clone https://github.com/ebubekirbastama/Android_GU-_Hierarchy_Viewer.git
cd Android_GU-_Hierarchy_Viewer
```

---

## تثبيت المتطلبات

```bash
pip install -r requirements.txt
```

---

# 📜 requirements.txt

```txt
PyQt6>=6.6.0
uiautomator2>=3.1.0
```

اختياري:

```bash
pip install adbutils lxml pillow
```

---

# ▶️ التشغيل

```bash
python AndroidHierarchyViewer.py
```

---

# 🧪 الأنظمة المجربة

| النظام     | الحالة |
| ---------- | ------ |
| Windows 10 | ✅      |
| Windows 11 | ✅      |

---

# 🔥 مميزات مستقبلية

* XPath Generator
* CSS Selector Generator
* دعم عدة أجهزة
* AI Selector Generator
* OCR Analysis
* Element Screenshot Crop
* Live Tap Inspector
* Search System

---

# 🔬 مجالات الاستخدام

* Android Automation
* Reverse Engineering
* UI Analysis
* Mobile Testing
* Accessibility Testing
* Bot Development
* Mobile Scraping
* Dynamic Selector Extraction

---

# 📄 الترخيص

Apache License 2.0

---

# ❤️ ملاحظة المطور

يهدف هذا المشروع إلى توفير:

* واجهة حديثة
* نظام Inspect مباشر
* Overlay Rendering احترافي
* تجربة مشابهة لـ Chrome DevTools

لتحليل واجهات Android وأتمتتها.

