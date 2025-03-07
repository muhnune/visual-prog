import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QGroupBox, 
    QVBoxLayout, 
    QHBoxLayout, 
    QFormLayout,
    QLabel, 
    QPushButton,
    QLineEdit,
    QRadioButton,
    QButtonGroup,
    QComboBox
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.identity_group = self.create_identity_group()
        self.navigation_group = self.create_navigation_group()
        self.form_group = self.create_form_group()
        self.actions_group = self.create_actions_group()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.identity_group)
        main_layout.addWidget(self.navigation_group)
        main_layout.addWidget(self.form_group)
        main_layout.addWidget(self.actions_group)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        self.setWindowTitle("Week 2 : Layout - User Registration Form")
        self.setGeometry(600, 400, 400, 200)


    def create_identity_group(self):
        identity_group = QGroupBox("Identity")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Nama   : Muhammad Nune Huria Sakti"))
        layout.addWidget(QLabel("NIM    : F1D022075"))
        layout.addWidget(QLabel("Kelas  : Pemrograman Visual - C"))

        identity_group.setLayout(layout)
        return identity_group

    def create_navigation_group(self):
        navigation_group = QGroupBox("Navigation")

        layout = QHBoxLayout()
        layout.addWidget(QPushButton("Home"))
        layout.addWidget(QPushButton("About"))
        layout.addWidget(QPushButton("Contact"))

        navigation_group.setLayout(layout)
        return navigation_group
    
    def create_form_group(self):
        form_group = QGroupBox("User Registration Form")

        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        nameForm = QLineEdit()
        layout.addRow("Full name :", nameForm)

        emailForm = QLineEdit()
        layout.addRow("Email :", emailForm)

        phoneForm = QLineEdit()
        layout.addRow("Phone :", phoneForm)

        gender_layout = QHBoxLayout() 
        gender_group = QButtonGroup()

        male_radio = QRadioButton("Male")
        female_radio = QRadioButton("Female")

        gender_group.addButton(male_radio)
        gender_group.addButton(female_radio)

        gender_layout.addWidget(male_radio)
        gender_layout.addWidget(female_radio)

        layout.addRow("Gender :", gender_layout) 

        countryForm = QComboBox()
        countryForm.addItems(["Indonesia", "Korea", "Japan", "China", "USA", "UK"])
        layout.addRow("Country :", countryForm)

        form_group.setLayout(layout)
        return form_group
    
    def create_actions_group(self):
        actions_group = QGroupBox("Actions")

        layout = QHBoxLayout()
        layout.addWidget(QPushButton("Submit"))
        layout.addWidget(QPushButton("Cancel"))

        actions_group.setLayout(layout)
        return actions_group
    

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())