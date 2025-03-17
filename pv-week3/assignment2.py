import sys
import random

from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt6.QtCore import Qt, QPoint

class EventHandler(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Week 3 - (F1D022075 - Muhammad Nune Huria Sakti)")
        self.setGeometry(100, 100, 600, 400)
        
        self.label = QLabel(self)
        self.label.move(250, 180)
        self.label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.label.setFixedSize(200, 30)
        
        #enable mouse tracking
        self.setMouseTracking(True)

        #enable mouse tracking for label
        self.label.setMouseTracking(True) 

    def mouseMoveEvent(self, event):
        x, y = event.position().toPoint().x(), event.position().toPoint().y()
        self.label.setText(f"x : {x}, y : {y}")

        # Check if the mouse is over the label
        move_label = self.label.geometry()
        if move_label.contains(QPoint(x, y)):
            self.move_label()

    def move_label(self):
        max_x = self.width() - self.label.width()
        max_y = self.height() - self.label.height()
        new_x = random.randint(0, max_x)
        new_y = random.randint(0, max_y)
        self.label.move(new_x, new_y)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EventHandler()
    window.show()
    sys.exit(app.exec())