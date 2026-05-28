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
    QGraphicsPixmapItem
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

        self.setWindowTitle("📱 EBS Android XML Inspect Viewer")
        self.setGeometry(80, 60, 1750, 950)

        self.device = None
        self.selected_graphics_item = None
        self.hover_graphics_item = None

        self.live_timer = QTimer()
        self.live_timer.timeout.connect(self.live_refresh)

        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: #ffffff;
                font-family: Segoe UI;
            }

            QPushButton {
                background-color: #0078d7;
                color: white;
                border-radius: 6px;
                padding: 10px;
                font-size: 13px;
            }

            QPushButton:hover {
                background-color: #005a9e;
            }

            QTextEdit {
                background-color: #252535;
                color: #ffffff;
                border-radius: 6px;
                font-family: Consolas;
                font-size: 10pt;
                padding: 8px;
            }

            QTreeWidget {
                background-color: #252535;
                color: #ffffff;
                border-radius: 6px;
                font-family: Consolas;
                font-size: 9pt;
            }

            QTreeWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }

            QLabel {
                font-size: 14pt;
            }

            QGraphicsView {
                background-color: #111111;
                border: 1px solid #444;
                border-radius: 8px;
            }
        """)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        title = QLabel("Android XML Viewer - Chrome Inspect Element Gibi")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        left_panel = QWidget()
        left_layout = QVBoxLayout()
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
        left_layout.addWidget(self.tree)

        left_layout.addWidget(QLabel("Ham XML"))

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        left_layout.addWidget(self.text_area)

        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)

        right_layout.addWidget(QLabel("Canlı Telefon Ekranı - Inspect Modu"))

        self.preview_scene = QGraphicsScene()
        self.preview_view = InspectGraphicsView(self)
        self.preview_view.setScene(self.preview_scene)
        self.preview_view.setMouseTracking(True)

        right_layout.addWidget(self.preview_view)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([1000, 750])

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
            item.setPen(QPen(QColor("#00ff00"), 3))
            item.setBrush(QBrush(Qt.BrushStyle.NoBrush))

            xml_node = item.xml_data

            text = xml_node.attrib.get("text", "")
            resource_id = xml_node.attrib.get("resource-id", "")
            class_name = xml_node.attrib.get("class", "")
            bounds = xml_node.attrib.get("bounds", "")
            clickable = xml_node.attrib.get("clickable", "")
            enabled = xml_node.attrib.get("enabled", "")

            tooltip = (
                f"Class: {class_name}\n"
                f"Text: {text}\n"
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

        graphics_item.setPen(QPen(QColor("#ff0000"), 4))
        graphics_item.setBrush(QBrush(Qt.BrushStyle.NoBrush))
        self.selected_graphics_item = graphics_item

        tree_item = self.find_tree_item_by_node(xml_node)

        if tree_item:
            self.tree.setCurrentItem(tree_item)
            self.tree.scrollToItem(tree_item)
            tree_item.setExpanded(True)

        bounds = xml_node.attrib.get("bounds", "")
        self.find_in_raw_xml(bounds)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = UIDumpGUI()
    gui.show()
    sys.exit(app.exec())
