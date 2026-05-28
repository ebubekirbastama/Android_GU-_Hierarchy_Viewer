import sys
import os
import uuid
import re
import xml.etree.ElementTree as ET
import uiautomator2 as u2

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QLabel,
    QMessageBox,
    QTreeWidget,
    QTreeWidgetItem,
    QSplitter,
    QScrollArea
)
from PyQt6.QtGui import QPixmap, QImage, QPainter, QPen, QColor
from PyQt6.QtCore import Qt


class UIDumpGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("📱 EBS UIAutomator2 Dump Viewer")
        self.setGeometry(100, 100, 1500, 850)

        self.dump_text = ""
        self.screenshot_path = ""

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

            QTreeWidget::item {
                padding: 4px;
            }

            QTreeWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }

            QLabel {
                font-size: 14pt;
            }

            QScrollArea {
                background-color: #11111d;
                border-radius: 6px;
            }
        """)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        title = QLabel("Android UI Hierarchy Dump + Telefon Ekranı Görüntüsü")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)

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
        self.tree.setColumnWidth(0, 110)
        self.tree.setColumnWidth(1, 200)
        self.tree.setColumnWidth(2, 240)
        self.tree.setColumnWidth(3, 230)

        left_layout.addWidget(QLabel("XML Ağaç Yapısı"))
        left_layout.addWidget(self.tree)

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)

        left_layout.addWidget(QLabel("Ham XML"))
        left_layout.addWidget(self.text_area)

        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)

        right_layout.addWidget(QLabel("Telefon Ekranı Görünümü"))

        self.screen_label = QLabel()
        self.screen_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.screen_label.setStyleSheet("""
            QLabel {
                background-color: #000000;
                border: 1px solid #444;
                border-radius: 8px;
            }
        """)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.screen_label)

        right_layout.addWidget(self.scroll_area)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([900, 600])

        button_layout = QHBoxLayout()

        self.dump_button = QPushButton("📥 Dump Al + Ekran Görüntüsü")
        self.dump_button.clicked.connect(self.dump_ui)
        button_layout.addWidget(self.dump_button)

        self.copy_button = QPushButton("📋 XML Kopyala")
        self.copy_button.clicked.connect(self.copy_text)
        button_layout.addWidget(self.copy_button)

        self.clear_button = QPushButton("🧹 Temizle")
        self.clear_button.clicked.connect(self.clear_screen)
        button_layout.addWidget(self.clear_button)

        main_layout.addLayout(button_layout)

    def dump_ui(self):
        try:
            d = u2.connect()

            self.dump_text = d.dump_hierarchy()
            self.text_area.setPlainText(self.dump_text)

            txt_path = self.save_dump_to_txt(self.dump_text)

            self.screenshot_path = self.save_screenshot(d)

            self.tree.clear()

            root = ET.fromstring(self.dump_text)
            self.add_node_to_tree(root)

            self.tree.expandAll()

            self.show_phone_screen_with_boxes(self.screenshot_path, root)

            QMessageBox.information(
                self,
                "Başarılı",
                f"Dump alındı.\n\nXML kayıt:\n{txt_path}\n\nEkran görüntüsü:\n{self.screenshot_path}"
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Hata",
                f"Bağlantı, dump veya ekran görüntüsü alınamadı:\n{e}"
            )

    def save_dump_to_txt(self, dump_text):
        random_name = f"dump_{uuid.uuid4().hex[:10]}.txt"
        save_path = os.path.join(os.getcwd(), random_name)

        with open(save_path, "w", encoding="utf-8") as file:
            file.write(dump_text)

        return save_path

    def save_screenshot(self, device):
        random_name = f"screenshot_{uuid.uuid4().hex[:10]}.png"
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

        item.setToolTip(0, tag)
        item.setToolTip(1, text)
        item.setToolTip(2, resource_id)
        item.setToolTip(3, class_name)
        item.setToolTip(4, clickable)
        item.setToolTip(5, enabled)
        item.setToolTip(6, bounds)

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

    def show_phone_screen_with_boxes(self, screenshot_path, root):
        pixmap = QPixmap(screenshot_path)

        if pixmap.isNull():
            QMessageBox.warning(self, "Uyarı", "Ekran görüntüsü yüklenemedi.")
            return

        painted_pixmap = QPixmap(pixmap)
        painter = QPainter(painted_pixmap)

        pen = QPen(QColor(255, 0, 0))
        pen.setWidth(3)
        painter.setPen(pen)

        def draw_bounds(xml_node):
            bounds = xml_node.attrib.get("bounds", "")
            parsed = self.parse_bounds(bounds)

            if parsed:
                x1, y1, x2, y2 = parsed
                width = x2 - x1
                height = y2 - y1

                if width > 5 and height > 5:
                    painter.drawRect(x1, y1, width, height)

            for child in xml_node:
                draw_bounds(child)

        draw_bounds(root)

        painter.end()

        max_width = 520
        scaled_pixmap = painted_pixmap.scaledToWidth(
            max_width,
            Qt.TransformationMode.SmoothTransformation
        )

        self.screen_label.setPixmap(scaled_pixmap)
        self.screen_label.resize(scaled_pixmap.size())

    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_area.toPlainText())

        QMessageBox.information(
            self,
            "Kopyalandı",
            "XML dump clipboard'a kopyalandı."
        )

    def clear_screen(self):
        self.text_area.clear()
        self.tree.clear()
        self.screen_label.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = UIDumpGUI()
    gui.show()
    sys.exit(app.exec())
