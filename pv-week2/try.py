from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget

import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.label = QLabel()

        self.input = QLineEdit()
        # self.input.textChanged.connect(self.label.setText)
        self.input.editingFinished.connect(self.updateLabel)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

    def updateLabel(self):
        self.label.setText(self.input.text())
        


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()