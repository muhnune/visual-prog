import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QSlider, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPalette

class FontColorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assignment 6 - Adjuster")
        self.setFixedSize(600, 400)

        # Label utama (NIM)
        self.label = QLabel("F1D022075")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont("Arial", 40))
        self.label.setAutoFillBackground(True)
        self.label.setFixedSize(575, 150)

        # Label Nama & NIM untuk otentikasi
        self.auth_label = QLabel("Muhammad Nune Huria Sakti | F1D022075")
        self.auth_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.auth_label.setStyleSheet("color: gray; font-size: 12px;")

        # Slider ukuran font
        self.font_slider = QSlider(Qt.Orientation.Horizontal)
        self.font_slider.setMinimum(20)
        self.font_slider.setMaximum(60)
        self.font_slider.setValue(40)
        self.font_slider.valueChanged.connect(self.update_font_size)

        # Slider warna latar
        self.bg_slider = QSlider(Qt.Orientation.Horizontal)
        self.bg_slider.setMinimum(0)
        self.bg_slider.setMaximum(255)
        self.bg_slider.setValue(255)
        self.bg_slider.valueChanged.connect(self.update_background_color)

        # Slider warna teks
        self.font_color_slider = QSlider(Qt.Orientation.Horizontal)
        self.font_color_slider.setMinimum(0)
        self.font_color_slider.setMaximum(255)
        self.font_color_slider.setValue(0)
        self.font_color_slider.valueChanged.connect(self.update_font_color)

        # Label judul slider
        font_label = QLabel("Font Size")
        bg_label = QLabel("Background Color")
        font_color_label = QLabel("Font Color")

        # Layout slider dengan label
        def slider_layout(label_widget, slider_widget):
            layout = QVBoxLayout()
            layout.addWidget(label_widget)
            layout.addWidget(slider_widget)
            return layout

        # Layout utama
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addLayout(slider_layout(font_label, self.font_slider))
        main_layout.addLayout(slider_layout(bg_label, self.bg_slider))
        main_layout.addLayout(slider_layout(font_color_label, self.font_color_slider))
        main_layout.addWidget(self.auth_label)

        self.setLayout(main_layout)
        self.update_colors()

    def update_font_size(self):
        size = self.font_slider.value()
        font = self.label.font()
        font.setPointSize(size)
        self.label.setFont(font)

    def update_background_color(self):
        self.update_colors()

    def update_font_color(self):
        self.update_colors()

    def update_colors(self):
        bg_val = self.bg_slider.value()
        font_val = self.font_color_slider.value()

        palette = self.label.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(bg_val, bg_val, bg_val))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(font_val, font_val, font_val))
        self.label.setPalette(palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FontColorAdjuster()
    window.show()
    sys.exit(app.exec())
