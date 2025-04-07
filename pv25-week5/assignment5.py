import sys
import re
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QComboBox, QPushButton, QMessageBox, QGridLayout
)
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtCore import Qt


class FormValidationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assignment 5 - Form Validation")
        self.setup_ui()
        self.setFixedSize(400, 400)

    def setup_ui(self):
        layout = QGridLayout()

        # Input Fields
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.age_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.phone_input.setInputMask("+62 999 9999 9999;_")

        self.address_input = QTextEdit()
        self.gender_input = QComboBox()
        self.gender_input.addItems(["", "Male", "Female"])

        self.education_input = QComboBox()
        self.education_input.addItems(["", "Elementary School", "Junior High School", "Senior High School", "Diploma", "Bachelor's Degree", "Master's Degree", "Doctoral Degree"])

        # Labels
        layout.addWidget(QLabel("Name:"), 0, 0)
        layout.addWidget(self.name_input, 0, 1)

        layout.addWidget(QLabel("Email:"), 1, 0)
        layout.addWidget(self.email_input, 1, 1)

        layout.addWidget(QLabel("Age:"), 2, 0)
        layout.addWidget(self.age_input, 2, 1)

        layout.addWidget(QLabel("Phone Number:"), 3, 0)
        layout.addWidget(self.phone_input, 3, 1)

        layout.addWidget(QLabel("Address:"), 4, 0)
        layout.addWidget(self.address_input, 4, 1)

        layout.addWidget(QLabel("Gender:"), 5, 0)
        layout.addWidget(self.gender_input, 5, 1)

        layout.addWidget(QLabel("Education:"), 6, 0)
        layout.addWidget(self.education_input, 6, 1)

        # Buttons
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_data)
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_fields)

        layout.addWidget(save_btn, 7, 0)
        layout.addWidget(clear_btn, 7, 1)

        # Auth Label
        self.auth_label = QLabel("Muhammad Nune Huria Sakti | F1D022075")
        self.auth_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.auth_label, 8, 0, 1, 2)

        # Shortcut to quit (Q)
        quit_shortcut = QShortcut(QKeySequence("Q"), self)
        quit_shortcut.activated.connect(self.close)

        self.setLayout(layout)

    def save_data(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        age = self.age_input.text().strip()
        phone = self.phone_input.text().strip()
        address = self.address_input.toPlainText().strip()
        gender = self.gender_input.currentText()
        education = self.education_input.currentText()

        # Validations
        if not name:
            self.show_warning("Name is required.")
            return

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email) or not email.endswith(".com"):
            self.show_warning("Invalid email format")
            return

        if not age.isdigit() or not (10 <= int(age) <= 100):
            self.show_warning("Age must be a number between 10 and 100.")
            return

        if len(phone.replace(" ", "").replace("+", "")) != 13:
            self.show_warning("Phone number must be exactly 13 digits.")
            return

        if not address:
            self.show_warning("Address is required.")
            return

        if gender == "":
            self.show_warning("Please select a gender.")
            return

        if education == "":
            self.show_warning("Please select your education.")
            return

        QMessageBox.information(self, "Success", "Profile saved successfully!")
        self.clear_fields()

    def clear_fields(self):
        self.name_input.clear()
        self.email_input.clear()
        self.age_input.clear()
        self.phone_input.clear()
        self.address_input.clear()
        self.gender_input.setCurrentIndex(0)
        self.education_input.setCurrentIndex(0)

    def show_warning(self, message):
        QMessageBox.warning(self, "Error", message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FormValidationApp()
    window.show()
    sys.exit(app.exec())
