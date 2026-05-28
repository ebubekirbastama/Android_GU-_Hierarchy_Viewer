import sys
import os
import uuid
import re
import xml.etree.ElementTree as ET
import uiautomator2 as u2

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLabel, QMessageBox,
    QTreeWidget, QTreeWidgetItem, QSplitter,
    QGraphicsView, QGraphicsScene, QGraphicsRectItem,
    QGraphicsPixmapItem, QFrame
)

from PyQt6.QtGui import (
    QPen, QBrush, QColor, QTextCursor, QPixmap
)

from PyQt6.QtCore import Qt, QTimer


class InspectGraphicsView(QGraphicsView):
    def __init__(self, parent_gui):
        super().__init__()
        self.parent_gui = parent_gui
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        scene_pos = self.mapToScene(event.pos())
        items = self.scene().items(scene_pos)

        found_item = None

        for item in items:
            if isinstance(item, QGraphicsRectItem) and hasattr(item, "xml_data"):
                found_item = item
                break

        self.parent_gui.hover_xml_node(found_item)
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        scene_pos = self.mapToScene(event.pos())
        items = self.scene().items(scene_pos)

        for item in items:
            if isinstance(item, QGraphicsRectItem) and hasattr(item, "xml_data"):
                self.parent_gui.select_xml_node(item)
                return

        super().mousePressEvent(event)


class UIDumpGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("📱 EBS Android XML Inspect Viewer + XPath Generator")
        self.setGeometry(60, 40, 1900, 1000)

        self.device = None
        self.selected_graphics_item = None
        self.hover_graphics_item = None
        self.current_root = None
        self.current_xpath_text = ""

        self.live_timer = QTimer()
        self.live_timer.timeout.connect(self.live_refresh)

        self.setStyleSheet("""
            QWidget {
                background-color: #151521;
                color: #ffffff;
                font-family: Segoe UI;
            }

            QLabel {
                font-size: 13pt;
                font-weight: 600;
            }

            QPushButton {
                background-color: #1677ff;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 13px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #0f5fc8;
            }

            QPushButton:pressed {
                background-color: #084a9f;
            }

            QTextEdit {
                background-color: #202033;
                color: #e8e8f0;
                border: 1px solid #34344d;
                border-radius: 10px;
                font-family: Consolas;
                font-size: 10pt;
                padding: 10px;
                selection-background-color: #1677ff;
            }

            QTreeWidget {
                background-color: #202033;
                color: #ffffff;
                border: 1px solid #34344d;
                border-radius: 10px;
                font-family: Consolas;
                font-size: 9pt;
            }

            QTreeWidget::item:selected {
                background-color: #1677ff;
                color: white;
            }

            QHeaderView::section {
                background-color: #292943;
                color: #ffffff;
                padding: 6px;
                border: none;
                font-weight: 700;
            }

            QGraphicsView {
                background-color: #09090f;
                border: 1px solid #3a3a55;
                border-radius: 12px;
            }

            QSplitter::handle {
                background-color: #30304a;
            }

            QFrame#card {
                background-color: #1b1b2b;
                border: 1px solid #34344d;
                border-radius: 14px;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)
        self.setLayout(main_layout)

        title = QLabel("Android XML Viewer - Inspect + uiautomator2 XPath Üretici")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18pt; font-weight: 800; color: #ffffff;")
        main_layout.addWidget(title)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # SOL PANEL
        left_panel = QFrame()
        left_panel.setObjectName("card")
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_panel.setLayout(left_layout)

        left_layout.addWidget(QLabel("XML Ağaç Yapısı"))

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels([
            "Tag",
            "Text",
            "Resource ID",
            "Class",
            "Clickable",
            "Enabled",
            "Bounds"
        ])
        self.tree.setColumnWidth(0, 100)
        self.tree.setColumnWidth(1, 180)
        self.tree.setColumnWidth(2, 260)
        self.tree.setColumnWidth(3, 240)
        left_layout.addWidget(self.tree, 2)

        left_layout.addWidget(QLabel("Ham XML"))

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        left_layout.addWidget(self.text_area, 1)

        # ORTA PANEL
        middle_panel = QFrame()
        middle_panel.setObjectName("card")
        middle_layout = QVBoxLayout()
        middle_layout.setContentsMargins(10, 10, 10, 10)
        middle_panel.setLayout(middle_layout)

        middle_layout.addWidget(QLabel("Canlı Telefon Ekranı - Inspect Modu"))

        self.preview_scene = QGraphicsScene()
        self.preview_view = InspectGraphicsView(self)
        self.preview_view.setScene(self.preview_scene)
        self.preview_view.setMouseTracking(True)
        middle_layout.addWidget(self.preview_view)

        # SAĞ PANEL - XPATH
        right_panel = QFrame()
        right_panel.setObjectName("card")
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_panel.setLayout(right_layout)

        xpath_title = QLabel("⚡ XPath Kombinasyonları")
        xpath_title.setStyleSheet("font-size: 15pt; font-weight: 800; color: #6ee7ff;")
        right_layout.addWidget(xpath_title)

        self.selected_info_area = QTextEdit()
        self.selected_info_area.setReadOnly(True)
        self.selected_info_area.setMaximumHeight(185)
        self.selected_info_area.setPlaceholderText("Bir elemente tıkla; özellikleri burada görünecek.")
        right_layout.addWidget(self.selected_info_area)

        self.xpath_area = QTextEdit()
        self.xpath_area.setReadOnly(True)
        self.xpath_area.setPlaceholderText(
            "Ekrandaki elemente tıkladığında uiautomator2 için kullanılabilecek XPath kombinasyonları burada anlık listelenecek."
        )
        right_layout.addWidget(self.xpath_area, 1)

        xpath_button_layout = QHBoxLayout()

        self.copy_xpath_button = QPushButton("📋 XPath Kopyala")
        self.copy_xpath_button.clicked.connect(self.copy_xpath_text)
        xpath_button_layout.addWidget(self.copy_xpath_button)

        self.clear_xpath_button = QPushButton("🧹 XPath Temizle")
        self.clear_xpath_button.clicked.connect(self.clear_xpath_panel)
        xpath_button_layout.addWidget(self.clear_xpath_button)

        right_layout.addLayout(xpath_button_layout)

        splitter.addWidget(left_panel)
        splitter.addWidget(middle_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([720, 760, 520])

        button_layout = QHBoxLayout()

        self.dump_button = QPushButton("📥 Tek Sefer Dump Al")
        self.dump_button.clicked.connect(self.dump_ui)
        button_layout.addWidget(self.dump_button)

        self.live_button = QPushButton("🔴 Canlı Başlat")
        self.live_button.clicked.connect(self.toggle_live)
        button_layout.addWidget(self.live_button)

        self.copy_button = QPushButton("📋 XML Kopyala")
        self.copy_button.clicked.connect(self.copy_text)
        button_layout.addWidget(self.copy_button)

        self.clear_button = QPushButton("🧹 Temizle")
        self.clear_button.clicked.connect(self.clear_screen)
        button_layout.addWidget(self.clear_button)

        main_layout.addLayout(button_layout)

    def connect_device(self):
        if self.device is None:
            self.device = u2.connect()
        return self.device

    def dump_ui(self):
        try:
            device = self.connect_device()
            self.process_device_state(device, save_files=True, show_message=True)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Hata",
                f"Bağlantı, XML veya ekran görüntüsü hatası:\n{e}"
            )

    def toggle_live(self):
        if self.live_timer.isActive():
            self.live_timer.stop()
            self.live_button.setText("🔴 Canlı Başlat")
            return

        try:
            self.connect_device()
            self.live_timer.start(1000)
            self.live_button.setText("⏹ Canlı Durdur")
        except Exception as e:
            QMessageBox.critical(
                self,
                "Hata",
                f"Cihaza bağlanılamadı:\n{e}"
            )

    def live_refresh(self):
        try:
            device = self.connect_device()
            self.process_device_state(device, save_files=False, show_message=False)

        except Exception as e:
            self.live_timer.stop()
            self.live_button.setText("🔴 Canlı Başlat")
            QMessageBox.critical(
                self,
                "Canlı Hata",
                str(e)
            )

    def process_device_state(self, device, save_files=False, show_message=False):
        dump_text = device.dump_hierarchy()
        root = ET.fromstring(dump_text)
        self.current_root = root

        screenshot_path = self.save_screenshot(device)

        txt_path = None

        if save_files:
            txt_path = self.save_dump_to_txt(dump_text)

        self.text_area.setPlainText(dump_text)

        self.tree.clear()
        self.add_node_to_tree(root)
        self.tree.expandAll()

        self.preview_scene.clear()
        self.selected_graphics_item = None
        self.hover_graphics_item = None

        self.render_real_screen_with_xml_overlay(root, screenshot_path)

        if show_message:
            QMessageBox.information(
                self,
                "Başarılı",
                f"XML ve ekran görüntüsü alındı.\n\nXML:\n{txt_path}\n\nEkran:\n{screenshot_path}"
            )

    def save_dump_to_txt(self, dump_text):
        random_name = f"dump_{uuid.uuid4().hex[:10]}.txt"
        save_path = os.path.join(os.getcwd(), random_name)

        with open(save_path, "w", encoding="utf-8") as file:
            file.write(dump_text)

        return save_path

    def save_screenshot(self, device):
        random_name = f"screen_{uuid.uuid4().hex[:10]}.png"
        save_path = os.path.join(os.getcwd(), random_name)

        device.screenshot(save_path)

        return save_path

    def add_node_to_tree(self, xml_node, parent_item=None):
        tag = xml_node.tag
        text = xml_node.attrib.get("text", "")
        resource_id = xml_node.attrib.get("resource-id", "")
        class_name = xml_node.attrib.get("class", "")
        clickable = xml_node.attrib.get("clickable", "")
        enabled = xml_node.attrib.get("enabled", "")
        bounds = xml_node.attrib.get("bounds", "")

        item = QTreeWidgetItem([
            tag,
            text,
            resource_id,
            class_name,
            clickable,
            enabled,
            bounds
        ])

        item.xml_node = xml_node

        if parent_item:
            parent_item.addChild(item)
        else:
            self.tree.addTopLevelItem(item)

        for child in xml_node:
            self.add_node_to_tree(child, item)

    def parse_bounds(self, bounds_text):
        match = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds_text)

        if not match:
            return None

        x1, y1, x2, y2 = map(int, match.groups())
        return x1, y1, x2, y2

    def render_real_screen_with_xml_overlay(self, root, screenshot_path):
        pixmap = QPixmap(screenshot_path)

        if pixmap.isNull():
            QMessageBox.warning(self, "Uyarı", "Ekran görüntüsü yüklenemedi.")
            return

        screen_width = pixmap.width()
        screen_height = pixmap.height()

        self.preview_scene.setSceneRect(0, 0, screen_width, screen_height)

        bg_item = QGraphicsPixmapItem(pixmap)
        bg_item.setZValue(0)
        self.preview_scene.addItem(bg_item)

        def draw_node(xml_node):
            bounds = xml_node.attrib.get("bounds", "")
            parsed = self.parse_bounds(bounds)

            if parsed:
                x1, y1, x2, y2 = parsed
                w = x2 - x1
                h = y2 - y1

                if w > 3 and h > 3:
                    rect = QGraphicsRectItem(x1, y1, w, h)
                    rect.xml_data = xml_node

                    rect.default_pen = QPen(QColor(255, 255, 255, 0), 1)
                    rect.default_brush = QBrush(Qt.BrushStyle.NoBrush)

                    rect.setPen(rect.default_pen)
                    rect.setBrush(rect.default_brush)

                    rect.setZValue(10)
                    rect.setAcceptHoverEvents(True)

                    self.preview_scene.addItem(rect)

            for child in xml_node:
                draw_node(child)

        draw_node(root)

        self.preview_view.fitInView(
            self.preview_scene.sceneRect(),
            Qt.AspectRatioMode.KeepAspectRatio
        )

    def hover_xml_node(self, item):
        if self.hover_graphics_item and self.hover_graphics_item != self.selected_graphics_item:
            try:
                self.hover_graphics_item.setPen(self.hover_graphics_item.default_pen)
                self.hover_graphics_item.setBrush(self.hover_graphics_item.default_brush)
            except Exception:
                pass

        self.hover_graphics_item = item

        if item and item != self.selected_graphics_item:
            item.setPen(QPen(QColor("#00ff90"), 3))
            item.setBrush(QBrush(Qt.BrushStyle.NoBrush))

            xml_node = item.xml_data

            text = xml_node.attrib.get("text", "")
            resource_id = xml_node.attrib.get("resource-id", "")
            class_name = xml_node.attrib.get("class", "")
            bounds = xml_node.attrib.get("bounds", "")
            clickable = xml_node.attrib.get("clickable", "")
            enabled = xml_node.attrib.get("enabled", "")
            content_desc = xml_node.attrib.get("content-desc", "")

            tooltip = (
                f"Class: {class_name}\n"
                f"Text: {text}\n"
                f"Content Desc: {content_desc}\n"
                f"Resource ID: {resource_id}\n"
                f"Clickable: {clickable}\n"
                f"Enabled: {enabled}\n"
                f"Bounds: {bounds}"
            )

            self.preview_view.setToolTip(tooltip)

    def select_xml_node(self, graphics_item):
        xml_node = graphics_item.xml_data

        if self.selected_graphics_item:
            try:
                self.selected_graphics_item.setPen(self.selected_graphics_item.default_pen)
                self.selected_graphics_item.setBrush(self.selected_graphics_item.default_brush)
            except Exception:
                pass

        graphics_item.setPen(QPen(QColor("#ff4d4f"), 4))
        graphics_item.setBrush(QBrush(Qt.BrushStyle.NoBrush))
        self.selected_graphics_item = graphics_item

        tree_item = self.find_tree_item_by_node(xml_node)

        if tree_item:
            self.tree.setCurrentItem(tree_item)
            self.tree.scrollToItem(tree_item)
            tree_item.setExpanded(True)

        bounds = xml_node.attrib.get("bounds", "")
        self.find_in_raw_xml(bounds)
        self.update_xpath_panel(xml_node)

    def find_tree_item_by_node(self, xml_node):
        def search_item(item):
            if hasattr(item, "xml_node") and item.xml_node is xml_node:
                return item

            for i in range(item.childCount()):
                found = search_item(item.child(i))
                if found:
                    return found

            return None

        for i in range(self.tree.topLevelItemCount()):
            found = search_item(self.tree.topLevelItem(i))
            if found:
                return found

        return None

    def find_in_raw_xml(self, search_text):
        if not search_text:
            return

        document_text = self.text_area.toPlainText()
        index = document_text.find(search_text)

        if index == -1:
            return

        cursor = self.text_area.textCursor()
        cursor.setPosition(index)
        cursor.movePosition(
            QTextCursor.MoveOperation.Right,
            QTextCursor.MoveMode.KeepAnchor,
            len(search_text)
        )

        self.text_area.setTextCursor(cursor)

    # -------------------------
    # XPATH GENERATOR HELPERS
    # -------------------------
    def xpath_quote(self, value):
        """XPath string quote helper. Handles apostrophe/double-quote safely."""
        if value is None:
            return "''"
        value = str(value)
        if "'" not in value:
            return f"'{value}'"
        if '"' not in value:
            return f'"{value}"'

        parts = value.split("'")
        return "concat(" + ", \"'\", ".join([f"'{part}'" for part in parts]) + ")"

    def get_parent_map(self):
        if self.current_root is None:
            return {}
        return {child: parent for parent in self.current_root.iter() for child in parent}

    def get_node_index_among_same_class(self, node, parent_map):
        parent = parent_map.get(node)
        class_name = node.attrib.get("class", "")

        if parent is None:
            return 1

        same = [child for child in list(parent) if child.attrib.get("class", "") == class_name]

        if node in same:
            return same.index(node) + 1

        return 1

    def get_node_index_among_same_tag(self, node, parent_map):
        parent = parent_map.get(node)

        if parent is None:
            return 1

        same = [child for child in list(parent) if child.tag == node.tag]

        if node in same:
            return same.index(node) + 1

        return 1

    def get_absolute_xpath(self, node, use_class=True):
        parent_map = self.get_parent_map()
        parts = []
        current = node

        while current is not None:
            class_name = current.attrib.get("class", "")
            tag_name = current.tag

            if use_class and class_name:
                index = self.get_node_index_among_same_class(current, parent_map)
                parts.append(f"{class_name}[{index}]")
            else:
                index = self.get_node_index_among_same_tag(current, parent_map)
                parts.append(f"{tag_name}[{index}]")

            current = parent_map.get(current)

        parts.reverse()
        return "/" + "/".join(parts)

    def get_short_hierarchy_xpath(self, node):
        """Creates a shorter but still hierarchical XPath using last 3 meaningful class segments."""
        parent_map = self.get_parent_map()
        chain = []
        current = node

        while current is not None:
            class_name = current.attrib.get("class", "")
            if class_name:
                index = self.get_node_index_among_same_class(current, parent_map)
                chain.append(f"{class_name}[{index}]")
            current = parent_map.get(current)

        chain.reverse()
        tail = chain[-3:] if len(chain) >= 3 else chain
        return "//" + "/".join(tail)

    def add_xpath(self, results, title, xpath, priority=""):
        if not xpath:
            return
        key = xpath.strip()
        if not key:
            return
        if key in {item[1] for item in results}:
            return
        label = f"{title}{' - ' + priority if priority else ''}"
        results.append((label, key))

    def generate_xpath_combinations(self, node):
        attr = node.attrib
        results = []

        class_name = attr.get("class", "")
        text = attr.get("text", "")
        resource_id = attr.get("resource-id", "")
        content_desc = attr.get("content-desc", "")
        bounds = attr.get("bounds", "")
        package = attr.get("package", "")
        clickable = attr.get("clickable", "")
        enabled = attr.get("enabled", "")
        selected = attr.get("selected", "")
        checked = attr.get("checked", "")
        index = attr.get("index", "")

        base = f"//{class_name}" if class_name else f"//{node.tag}"
        any_node = "//*"

        # En stabil kombinasyonlar
        if resource_id:
            self.add_xpath(results, "resource-id", f"//*[@resource-id={self.xpath_quote(resource_id)}]", "en stabil")
            if class_name:
                self.add_xpath(results, "class + resource-id", f"//{class_name}[@resource-id={self.xpath_quote(resource_id)}]", "önerilen")

        if content_desc:
            self.add_xpath(results, "content-desc", f"//*[@content-desc={self.xpath_quote(content_desc)}]", "erişilebilirlik")
            if class_name:
                self.add_xpath(results, "class + content-desc", f"//{class_name}[@content-desc={self.xpath_quote(content_desc)}]")

        if text:
            self.add_xpath(results, "text", f"//*[@text={self.xpath_quote(text)}]", "metin birebir")
            self.add_xpath(results, "text contains", f"//*[contains(@text, {self.xpath_quote(text[:25])})]")
            if class_name:
                self.add_xpath(results, "class + text", f"//{class_name}[@text={self.xpath_quote(text)}]")
                self.add_xpath(results, "class + text contains", f"//{class_name}[contains(@text, {self.xpath_quote(text[:25])})]")

        # Kombine güçlü seçenekler
        if resource_id and text:
            self.add_xpath(
                results,
                "resource-id + text",
                f"//*[@resource-id={self.xpath_quote(resource_id)} and @text={self.xpath_quote(text)}]",
                "çok güçlü"
            )

        if resource_id and content_desc:
            self.add_xpath(
                results,
                "resource-id + content-desc",
                f"//*[@resource-id={self.xpath_quote(resource_id)} and @content-desc={self.xpath_quote(content_desc)}]"
            )

        if text and content_desc:
            self.add_xpath(
                results,
                "text + content-desc",
                f"//*[@text={self.xpath_quote(text)} and @content-desc={self.xpath_quote(content_desc)}]"
            )

        if class_name and resource_id and text:
            self.add_xpath(
                results,
                "class + resource-id + text",
                f"//{class_name}[@resource-id={self.xpath_quote(resource_id)} and @text={self.xpath_quote(text)}]",
                "en net"
            )

        # Android XML attribute seçenekleri
        if class_name:
            self.add_xpath(results, "class", f"//{class_name}")

        if package:
            self.add_xpath(results, "package", f"//*[@package={self.xpath_quote(package)}]")
            if class_name:
                self.add_xpath(results, "class + package", f"//{class_name}[@package={self.xpath_quote(package)}]")

        if bounds:
            self.add_xpath(results, "bounds", f"//*[@bounds={self.xpath_quote(bounds)}]", "ekran konumu")
            if class_name:
                self.add_xpath(results, "class + bounds", f"//{class_name}[@bounds={self.xpath_quote(bounds)}]")

        if index != "":
            self.add_xpath(results, "index", f"//*[@index={self.xpath_quote(index)}]")
            if class_name:
                self.add_xpath(results, "class + index", f"//{class_name}[@index={self.xpath_quote(index)}]")

        if clickable:
            self.add_xpath(results, "clickable", f"{base}[@clickable={self.xpath_quote(clickable)}]")

        if enabled:
            self.add_xpath(results, "enabled", f"{base}[@enabled={self.xpath_quote(enabled)}]")

        if selected:
            self.add_xpath(results, "selected", f"{base}[@selected={self.xpath_quote(selected)}]")

        if checked:
            self.add_xpath(results, "checked", f"{base}[@checked={self.xpath_quote(checked)}]")

        # Parent/child hiyerarşi XPath'leri
        parent_map = self.get_parent_map()
        parent = parent_map.get(node)
        if parent is not None:
            parent_class = parent.attrib.get("class", "")
            parent_rid = parent.attrib.get("resource-id", "")
            parent_text = parent.attrib.get("text", "")
            parent_desc = parent.attrib.get("content-desc", "")

            child_selector = class_name if class_name else node.tag

            if parent_rid:
                self.add_xpath(
                    results,
                    "parent resource-id -> child class",
                    f"//*[@resource-id={self.xpath_quote(parent_rid)}]//{child_selector}",
                    "hiyerarşik"
                )

            if parent_class:
                self.add_xpath(
                    results,
                    "parent class -> child class",
                    f"//{parent_class}//{child_selector}",
                    "hiyerarşik"
                )

            if parent_text:
                self.add_xpath(
                    results,
                    "parent text -> child class",
                    f"//*[@text={self.xpath_quote(parent_text)}]//{child_selector}"
                )

            if parent_desc:
                self.add_xpath(
                    results,
                    "parent content-desc -> child class",
                    f"//*[@content-desc={self.xpath_quote(parent_desc)}]//{child_selector}"
                )

        # Mutlak ve kısa hiyerarşik path
        self.add_xpath(results, "absolute class path", self.get_absolute_xpath(node, use_class=True), "son çare")
        self.add_xpath(results, "absolute tag path", self.get_absolute_xpath(node, use_class=False), "son çare")
        self.add_xpath(results, "short hierarchy path", self.get_short_hierarchy_xpath(node), "pratik")

        # uiautomator2 Python örnekleri
        wrapped = []
        for title, xpath in results:
            wrapped.append((title, xpath))
            wrapped.append((f"uiautomator2 kullanım - {title}", f"d.xpath({self.xpath_quote(xpath)}).click()"))

        return wrapped

    def update_xpath_panel(self, xml_node):
        attr = xml_node.attrib

        info = (
            "SEÇİLEN ELEMENT\n"
            "────────────────────────\n"
            f"Tag          : {xml_node.tag}\n"
            f"Class        : {attr.get('class', '')}\n"
            f"Text         : {attr.get('text', '')}\n"
            f"Content Desc : {attr.get('content-desc', '')}\n"
            f"Resource ID  : {attr.get('resource-id', '')}\n"
            f"Package      : {attr.get('package', '')}\n"
            f"Clickable    : {attr.get('clickable', '')}\n"
            f"Enabled      : {attr.get('enabled', '')}\n"
            f"Index        : {attr.get('index', '')}\n"
            f"Bounds       : {attr.get('bounds', '')}\n"
        )
        self.selected_info_area.setPlainText(info)

        combinations = self.generate_xpath_combinations(xml_node)

        lines = []
        lines.append("UIAUTOMATOR2 XPATH KOMBİNASYONLARI")
        lines.append("Not: Önce resource-id / content-desc / text kombinasyonlarını dene. Bounds ve absolute path son çaredir.")
        lines.append("═" * 72)

        for i, (title, xpath) in enumerate(combinations, start=1):
            lines.append(f"\n{i:02d}) {title}")
            lines.append(xpath)

        self.current_xpath_text = "\n".join(lines)
        self.xpath_area.setPlainText(self.current_xpath_text)

    def copy_xpath_text(self):
        text = self.xpath_area.toPlainText().strip()
        if not text:
            QMessageBox.information(self, "Bilgi", "Kopyalanacak XPath yok. Önce bir elemente tıkla.")
            return

        QApplication.clipboard().setText(text)
        QMessageBox.information(self, "Kopyalandı", "XPath kombinasyonları clipboard'a kopyalandı.")

    def clear_xpath_panel(self):
        self.selected_info_area.clear()
        self.xpath_area.clear()
        self.current_xpath_text = ""

    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_area.toPlainText())

        QMessageBox.information(
            self,
            "Kopyalandı",
            "XML dump clipboard'a kopyalandı."
        )

    def clear_screen(self):
        if self.live_timer.isActive():
            self.live_timer.stop()
            self.live_button.setText("🔴 Canlı Başlat")

        self.text_area.clear()
        self.tree.clear()
        self.preview_scene.clear()
        self.selected_graphics_item = None
        self.hover_graphics_item = None
        self.current_root = None
        self.clear_xpath_panel()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = UIDumpGUI()
    gui.show()
    sys.exit(app.exec())
