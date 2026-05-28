# README_EN.md

# 📱 AndroidHierarchyViewer

Modern visual Android UI Hierarchy Viewer and Inspect Tool powered by `uiautomator2`.

Inspired by Chrome DevTools Inspect System.

---

# 🚀 Features

* ✅ Live Android UI XML hierarchy dump
* ✅ Automatic screenshot capture
* ✅ Visual XML Tree Structure
* ✅ Real-time UI bounds overlay rendering
* ✅ Live hover inspect system
* ✅ Click-to-select inspect system
* ✅ XML ↔ Visual synchronization
* ✅ Raw XML viewer
* ✅ Automatic XML dump saving
* ✅ Modern Dark/Metro UI
* ✅ Professional PyQt6 interface
* ✅ Bounds parsing engine
* ✅ Clipboard XML copy
* ✅ Scrollable device preview
* ✅ Live refresh mode

---

# 🧠 Inspect System

This tool works similarly to Chrome DevTools.

You can:

* Hover elements
* Inspect live UI components
* Select elements visually
* Sync XML nodes with screen overlays
* Highlight elements in raw XML

---

# 🖱️ Hover Inspect

When hovering over an element:

* Green highlight box appears
* Tooltip displays:

  * Class
  * Text
  * Resource ID
  * Clickable state
  * Enabled state
  * Bounds

---

# 🎯 Element Selection

When clicking an element:

* Red highlight appears
* Related XML node is selected automatically
* TreeView scrolls to the element
* Raw XML highlights the bounds

---

# 📡 Live Refresh Mode

Supports real-time UI inspection.

Features:

* Automatic XML refresh
* Automatic screenshot refresh
* Dynamic UI monitoring
* Real-time hierarchy analysis

---

# 🖼️ Screenshot Overlay Engine

The application renders:

* Real Android screenshots
* XML bounds rectangles
* Live overlay rendering system

Powered by:

* QGraphicsScene
* QGraphicsRectItem
* QGraphicsPixmapItem

---

# 📦 Technologies

| Technology      | Description          |
| --------------- | -------------------- |
| Python          | Core language        |
| PyQt6           | Modern GUI framework |
| uiautomator2    | Android automation   |
| XML ElementTree | XML parsing          |
| QPainter        | Overlay rendering    |

---

# ⚙️ Requirements

## Python

Python 3.10+

## Android

* USB Debugging enabled
* ADB installed

---

# 📦 Installation

## Clone Repository

```bash
git clone https://github.com/ebubekirbastama/Android_GU-_Hierarchy_Viewer.git
cd Android_GU-_Hierarchy_Viewer
```

---

## Install Requirements

```bash
pip install -r requirements.txt
```

---

# 📜 requirements.txt

```txt
PyQt6>=6.6.0
uiautomator2>=3.1.0
```

Optional:

```bash
pip install adbutils lxml pillow
```

---

# ▶️ Run

```bash
python AndroidHierarchyViewer.py
```

---

# 🧪 Tested Platforms

| Platform   | Status |
| ---------- | ------ |
| Windows 10 | ✅      |
| Windows 11 | ✅      |

---

# 🔥 Planned Features

* XPath Generator
* CSS Selector Generator
* Multi-device support
* AI selector generation
* OCR analysis
* Element screenshot crop
* Auto tap inspector
* Search system

---

# 🔬 Use Cases

* Android Automation
* Reverse Engineering
* Mobile Testing
* UI Analysis
* Accessibility Testing
* Bot Development
* Mobile Scraping
* Dynamic Selector Extraction

---

# 📄 License

Apache License 2.0

---

# ❤️ Developer Note

This project aims to provide:

* Modern UI
* Real-time inspect system
* Advanced overlay rendering
* Chrome DevTools-like experience

for Android UI analysis and automation.
