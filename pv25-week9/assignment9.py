import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QLineEdit, QPushButton, QDialog,
    QDialogButtonBox, QFormLayout
)
from PyQt6.QtCore import Qt

class InputDialog(QDialog):
    def __init__(self, label: str, options=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Input Dialog")
        self.setFixedSize(250, 120)

        self.input_value = None
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        self.input_field = QComboBox(self) if options else QLineEdit(self)

        if options:
            self.input_field.addItems(options)
        form_layout.addRow(label, self.input_field)
        layout.addLayout(form_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_input(self):
        if isinstance(self.input_field, QComboBox):
            return self.input_field.currentText()
        return self.input_field.text()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Input Dialog Demo")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()

        self.combo_label = QLabel("Choose from list:")
        self.combo_input = QLineEdit()
        self.combo_input.setReadOnly(True)
        self.combo_button = QPushButton("Select")
        self.combo_button.clicked.connect(self.set_combo_input)

        combo_layout = QHBoxLayout()
        combo_layout.addWidget(self.combo_input)
        combo_layout.addWidget(self.combo_button)

        self.line1_label = QLabel("Get name:")
        self.line1_input = QLineEdit()
        self.line1_input.setReadOnly(True)
        self.line1_button = QPushButton("Enter")
        self.line1_button.clicked.connect(lambda: self.set_line_input(self.line1_input, "Input your name"))

        line1_layout = QHBoxLayout()
        line1_layout.addWidget(self.line1_input)
        line1_layout.addWidget(self.line1_button)

        self.line2_label = QLabel("Enter an integer:")
        self.line2_input = QLineEdit()
        self.line2_input.setReadOnly(True)
        self.line2_button = QPushButton("Input")
        self.line2_button.clicked.connect(lambda: self.set_line_input(self.line2_input, "Enter an integer"))

        line2_layout = QHBoxLayout()
        line2_layout.addWidget(self.line2_input)
        line2_layout.addWidget(self.line2_button)

        layout.addWidget(self.combo_label)
        layout.addLayout(combo_layout)

        layout.addWidget(self.line1_label)
        layout.addLayout(line1_layout)

        layout.addWidget(self.line2_label)
        layout.addLayout(line2_layout)

        self.setLayout(layout)

    def set_combo_input(self):
        options = ["Python", "Java", "C++"]
        dialog = InputDialog("List of languages:", options, self)
        if dialog.exec():
            self.combo_input.setText(dialog.get_input())

    def set_line_input(self, line_edit: QLineEdit, label: str):
        dialog = InputDialog(label, parent=self)
        if dialog.exec():
            line_edit.setText(dialog.get_input())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

# Muhammad Nune Huria Sakti - F1D022075
# Visual Programming 2025