import sys
import re
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QComboBox, QPushButton, QMessageBox, QGridLayout,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout,
    QTabWidget, QHeaderView, QMainWindow, QDockWidget, QFrame,
    QSplitter, QScrollArea
)
from PyQt6.QtGui import QKeySequence, QShortcut, QIcon
from PyQt6.QtCore import Qt, QTimer


class DatabaseManager:
    def __init__(self, db_name="user_profiles.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Initialize the database and create the users table if it doesn't exist"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    age INTEGER NOT NULL,
                    phone TEXT NOT NULL,
                    address TEXT NOT NULL,
                    gender TEXT NOT NULL,
                    education TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def save_user(self, name, email, age, phone, address, gender, education):
        """Save a new user to the database"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (name, email, age, phone, address, gender, education)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (name, email, age, phone, address, gender, education))
                conn.commit()
                return True, "User saved successfully!"
        except sqlite3.IntegrityError:
            return False, "Email already exists in the database!"
        except Exception as e:
            return False, f"Database error: {str(e)}"
    
    def get_all_users(self):
        """Retrieve all users from the database"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
                return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving users: {str(e)}")
            return []
    
    def delete_user(self, user_id):
        """Delete a user by ID"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting user: {str(e)}")
            return False
    
    def update_user(self, user_id, name, email, age, phone, address, gender, education):
        """Update an existing user"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users 
                    SET name=?, email=?, age=?, phone=?, address=?, gender=?, education=?
                    WHERE id=?
                ''', (name, email, age, phone, address, gender, education, user_id))
                conn.commit()
                return cursor.rowcount > 0, "User updated successfully!"
        except sqlite3.IntegrityError:
            return False, "Email already exists in the database!"
        except Exception as e:
            return False, f"Database error: {str(e)}"

    def search_users(self, search_term):
        """Search users by name or email"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM users 
                    WHERE name LIKE ? OR email LIKE ?
                    ORDER BY created_at DESC
                ''', (f'%{search_term}%', f'%{search_term}%'))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error searching users: {str(e)}")
            return []


class SearchDockWidget(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Search Panel", parent)
        self.parent_window = parent
        self.setup_ui()
        
    def setup_ui(self):
        # Create main widget for the dock
        dock_widget = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("🔍 Search Users")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        layout.addWidget(title_label)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name or email...")
        self.search_input.textChanged.connect(self.on_search_text_changed)
        layout.addWidget(self.search_input)
        
        # Search button
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.perform_search)
        layout.addWidget(search_btn)
        
        # Clear search button
        clear_btn = QPushButton("Clear Search")
        clear_btn.clicked.connect(self.clear_search)
        layout.addWidget(clear_btn)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        # Developer
        help_label = QLabel("🤖 Muhammad Nune Huria Sakti")
        help_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        layout.addWidget(help_label)
        
        help_text = QLabel("""
• F1D022075
• Visual Programming C - Assignment 11
        """)
        help_text.setWordWrap(True)
        help_text.setStyleSheet("font-size: 11px; color: #666; padding: 5px;")
        layout.addWidget(help_text)
        
        layout.addStretch()
        dock_widget.setLayout(layout)
        self.setWidget(dock_widget)
        
        # Set minimum width
        self.setMinimumWidth(250)
    
    def on_search_text_changed(self, text):
        """Auto-search as user types (with delay)"""
        if hasattr(self, 'search_timer'):
            self.search_timer.stop()
        
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(lambda: self.perform_search(text))
        self.search_timer.start(500)  # 500ms delay
    
    def perform_search(self, search_term=None):
        """Perform search and update users table"""
        if search_term is None:
            search_term = self.search_input.text().strip()
        
        if self.parent_window and hasattr(self.parent_window, 'central_widget'):
            users_tab = self.parent_window.central_widget.users_tab
            if search_term:
                users = self.parent_window.central_widget.db_manager.search_users(search_term)
                users_tab.display_users(users)
            else:
                users_tab.load_users()
    
    def clear_search(self):
        """Clear search and show all users"""
        self.search_input.clear()
        if self.parent_window and hasattr(self.parent_window, 'central_widget'):
            self.parent_window.central_widget.users_tab.load_users()


class FormTab(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__()
        self.db_manager = db_manager
        self.parent = parent
        self.editing_user_id = None
        self.setup_ui()

    def setup_ui(self):
        layout = QGridLayout()

        # Input Fields
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.age_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.phone_input.setInputMask("+62 999 9999 9999;_")

        self.address_input = QTextEdit()
        self.address_input.setMaximumHeight(80)
        
        self.gender_input = QComboBox()
        self.gender_input.addItems(["", "Male", "Female"])

        self.education_input = QComboBox()
        self.education_input.addItems([
            "", "Elementary School", "Junior High School", "Senior High School", 
            "Diploma", "Bachelor's Degree", "Master's Degree", "Doctoral Degree"
        ])

        # Labels and input fields layout
        layout.addWidget(QLabel("Name:"), 0, 0)
        
        # Name input with clipboard button
        name_layout = QHBoxLayout()
        name_layout.addWidget(self.name_input)
        paste_name_btn = QPushButton("📋")
        paste_name_btn.setToolTip("Paste from clipboard")
        paste_name_btn.setMaximumWidth(30)
        paste_name_btn.clicked.connect(lambda: self.paste_from_clipboard(self.name_input))
        name_layout.addWidget(paste_name_btn)
        name_widget = QWidget()
        name_widget.setLayout(name_layout)
        layout.addWidget(name_widget, 0, 1)

        layout.addWidget(QLabel("Email:"), 1, 0)
        
        # Email input with clipboard button
        email_layout = QHBoxLayout()
        email_layout.addWidget(self.email_input)
        paste_email_btn = QPushButton("📋")
        paste_email_btn.setToolTip("Paste from clipboard")
        paste_email_btn.setMaximumWidth(30)
        paste_email_btn.clicked.connect(lambda: self.paste_from_clipboard(self.email_input))
        email_layout.addWidget(paste_email_btn)
        email_widget = QWidget()
        email_widget.setLayout(email_layout)
        layout.addWidget(email_widget, 1, 1)

        layout.addWidget(QLabel("Age:"), 2, 0)
        layout.addWidget(self.age_input, 2, 1)

        layout.addWidget(QLabel("Phone Number:"), 3, 0)
        
        # Phone input with clipboard button
        phone_layout = QHBoxLayout()
        phone_layout.addWidget(self.phone_input)
        paste_phone_btn = QPushButton("📋")
        paste_phone_btn.setToolTip("Paste from clipboard")
        paste_phone_btn.setMaximumWidth(30)
        paste_phone_btn.clicked.connect(lambda: self.paste_from_clipboard(self.phone_input))
        phone_layout.addWidget(paste_phone_btn)
        phone_widget = QWidget()
        phone_widget.setLayout(phone_layout)
        layout.addWidget(phone_widget, 3, 1)

        layout.addWidget(QLabel("Address:"), 4, 0)
        
        # Address input with clipboard button
        address_layout = QHBoxLayout()
        address_layout.addWidget(self.address_input)
        
        address_btn_layout = QVBoxLayout()
        paste_address_btn = QPushButton("📋")
        paste_address_btn.setToolTip("Paste from clipboard")
        paste_address_btn.setMaximumWidth(30)
        paste_address_btn.clicked.connect(lambda: self.paste_from_clipboard(self.address_input))
        address_btn_layout.addWidget(paste_address_btn)
        address_btn_layout.addStretch()
        
        address_layout.addLayout(address_btn_layout)
        address_widget = QWidget()
        address_widget.setLayout(address_layout)
        layout.addWidget(address_widget, 4, 1)

        layout.addWidget(QLabel("Gender:"), 5, 0)
        layout.addWidget(self.gender_input, 5, 1)

        layout.addWidget(QLabel("Education:"), 6, 0)
        layout.addWidget(self.education_input, 6, 1)

        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_data)
        
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_fields)
        
        self.cancel_btn = QPushButton("Cancel Edit")
        self.cancel_btn.clicked.connect(self.cancel_edit)
        self.cancel_btn.hide()

        # Copy all data button
        copy_all_btn = QPushButton("Copy All Data")
        copy_all_btn.setToolTip("Copy all form data to clipboard")
        copy_all_btn.clicked.connect(self.copy_all_to_clipboard)

        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(copy_all_btn)

        layout.addLayout(button_layout, 7, 0, 1, 2)

        self.setLayout(layout)

    def paste_from_clipboard(self, target_widget):
        """Paste text from clipboard to the target widget"""
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        
        if text:
            if isinstance(target_widget, QLineEdit):
                target_widget.setText(text.strip())
            elif isinstance(target_widget, QTextEdit):
                target_widget.setPlainText(text.strip())
            
            # Show confirmation message
            self.show_info(f"Pasted from clipboard: {text[:50]}{'...' if len(text) > 50 else ''}")
        else:
            self.show_warning("Clipboard is empty!")

    def copy_all_to_clipboard(self):
        """Copy all form data to clipboard"""
        data = {
            "Name": self.name_input.text(),
            "Email": self.email_input.text(),
            "Age": self.age_input.text(),
            "Phone": self.phone_input.text(),
            "Address": self.address_input.toPlainText(),
            "Gender": self.gender_input.currentText(),
            "Education": self.education_input.currentText()
        }
        
        text_data = "\n".join([f"{key}: {value}" for key, value in data.items() if value])
        
        if text_data:
            clipboard = QApplication.clipboard()
            clipboard.setText(text_data)
            self.show_info("All form data copied to clipboard!")
        else:
            self.show_warning("No data to copy!")

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

        # Save to database
        if self.editing_user_id:
            success, message = self.db_manager.update_user(
                self.editing_user_id, name, email, int(age), phone, address, gender, education
            )
        else:
            success, message = self.db_manager.save_user(
                name, email, int(age), phone, address, gender, education
            )

        if success:
            QMessageBox.information(self, "Success", message)
            self.clear_fields()
            self.cancel_edit()
            if self.parent:
                self.parent.refresh_user_list()
        else:
            self.show_warning(message)

    def clear_fields(self):
        self.name_input.clear()
        self.email_input.clear()
        self.age_input.clear()
        self.phone_input.clear()
        self.address_input.clear()
        self.gender_input.setCurrentIndex(0)
        self.education_input.setCurrentIndex(0)

    def load_user_data(self, user_data):
        """Load user data into the form for editing"""
        self.editing_user_id = user_data[0]
        self.name_input.setText(user_data[1])
        self.email_input.setText(user_data[2])
        self.age_input.setText(str(user_data[3]))
        self.phone_input.setText(user_data[4])
        self.address_input.setPlainText(user_data[5])
        self.gender_input.setCurrentText(user_data[6])
        self.education_input.setCurrentText(user_data[7])
        
        self.save_btn.setText("Update")
        self.cancel_btn.show()

    def cancel_edit(self):
        """Cancel editing mode"""
        self.editing_user_id = None
        self.save_btn.setText("Save")
        self.cancel_btn.hide()
        self.clear_fields()

    def show_warning(self, message):
        QMessageBox.warning(self, "Error", message)

    def show_info(self, message):
        QMessageBox.information(self, "Info", message)


class UsersTab(QWidget):
    def __init__(self, db_manager, form_tab):
        super().__init__()
        self.db_manager = db_manager
        self.form_tab = form_tab
        self.setup_ui()
        self.load_users()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Table to display users
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(9)
        self.users_table.setHorizontalHeaderLabels([
            "ID", "Name", "Email", "Age", "Phone", "Address", "Gender", "Education", "Created At"
        ])
        
        # Make table read-only
        self.users_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.users_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # Enable double-click to edit
        self.users_table.doubleClicked.connect(self.edit_selected_user)
        
        # Resize columns to content
        header = self.users_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(self.users_table)

        # Buttons
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_users)
        
        edit_btn = QPushButton("Edit Selected")
        edit_btn.clicked.connect(self.edit_selected_user)
        
        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(self.delete_selected_user)

        copy_selected_btn = QPushButton("Copy Selected")
        copy_selected_btn.setToolTip("Copy selected user data to clipboard")
        copy_selected_btn.clicked.connect(self.copy_selected_user)

        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(copy_selected_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_users(self):
        """Load all users from database into the table"""
        users = self.db_manager.get_all_users()
        self.display_users(users)

    def display_users(self, users):
        """Display users in the table"""
        self.users_table.setRowCount(len(users))
        
        for row, user in enumerate(users):
            for col, data in enumerate(user):
                self.users_table.setItem(row, col, QTableWidgetItem(str(data)))

    def copy_selected_user(self):
        """Copy selected user data to clipboard"""
        current_row = self.users_table.currentRow()
        if current_row >= 0:
            user_data = {}
            headers = ["ID", "Name", "Email", "Age", "Phone", "Address", "Gender", "Education", "Created At"]
            
            for col in range(self.users_table.columnCount()):
                item = self.users_table.item(current_row, col)
                if item:
                    user_data[headers[col]] = item.text()
            
            text_data = "\n".join([f"{key}: {value}" for key, value in user_data.items()])
            
            clipboard = QApplication.clipboard()
            clipboard.setText(text_data)
            QMessageBox.information(self, "Success", "User data copied to clipboard!")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a user to copy.")

    def edit_selected_user(self):
        """Edit the selected user"""
        current_row = self.users_table.currentRow()
        if current_row >= 0:
            user_data = []
            for col in range(self.users_table.columnCount() - 1):  # Exclude created_at
                item = self.users_table.item(current_row, col)
                user_data.append(item.text() if item else "")
            
            self.form_tab.load_user_data(user_data)
            # Switch to form tab
            if hasattr(self.parent(), 'setCurrentIndex'):
                self.parent().setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "No Selection", "Please select a user to edit.")

    def delete_selected_user(self):
        """Delete the selected user"""
        current_row = self.users_table.currentRow()
        if current_row >= 0:
            user_id = self.users_table.item(current_row, 0).text()
            user_name = self.users_table.item(current_row, 1).text()
            
            reply = QMessageBox.question(
                self, "Confirm Delete", 
                f"Are you sure you want to delete user '{user_name}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                if self.db_manager.delete_user(int(user_id)):
                    QMessageBox.information(self, "Success", "User deleted successfully!")
                    self.load_users()
                else:
                    QMessageBox.warning(self, "Error", "Failed to delete user!")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a user to delete.")


class CentralWidget(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Create tab widget
        self.tabs = QTabWidget()
        
        # Create form tab
        self.form_tab = FormTab(self.db_manager, self)
        self.tabs.addTab(self.form_tab, "Add/Edit User")
        
        # Create users list tab
        self.users_tab = UsersTab(self.db_manager, self.form_tab)
        self.tabs.addTab(self.users_tab, "View Users")

        layout.addWidget(self.tabs)

        # Auth Label
        auth_label = QLabel("Muhammad Nune Huria Sakti | F1D022075")
        auth_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(auth_label)

        self.setLayout(layout)

    def refresh_user_list(self):
        """Refresh the users list in the users tab"""
        self.users_tab.load_users()


class FormValidationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assignment 11 - Enhanced Form Validation")
        self.db_manager = DatabaseManager()
        self.setup_ui()
        self.setMinimumSize(1024, 768)

    def setup_ui(self):
        # Create central widget
        self.central_widget = CentralWidget(self.db_manager)
        self.setCentralWidget(self.central_widget)
        
        # Create search dock widget
        self.search_dock = SearchDockWidget(self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.search_dock)
        
        # Make dock widget detachable and movable
        self.search_dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | 
            Qt.DockWidgetArea.RightDockWidgetArea |
            Qt.DockWidgetArea.TopDockWidgetArea |
            Qt.DockWidgetArea.BottomDockWidgetArea
        )
        self.search_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable |
            QDockWidget.DockWidgetFeature.DockWidgetClosable
        )
        
        # Shortcut to quit (Q)
        quit_shortcut = QShortcut(QKeySequence("Q"), self)
        quit_shortcut.activated.connect(self.close)
        
        # Shortcut to toggle search dock (F3)
        toggle_search_shortcut = QShortcut(QKeySequence("F3"), self)
        toggle_search_shortcut.activated.connect(self.toggle_search_dock)
    
    def toggle_search_dock(self):
        """Toggle search dock visibility"""
        if self.search_dock.isVisible():
            self.search_dock.hide()
        else:
            self.search_dock.show()

    def refresh_user_list(self):
        """Refresh the users list in the users tab"""
        self.central_widget.refresh_user_list()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FormValidationApp()
    window.show()
    sys.exit(app.exec())