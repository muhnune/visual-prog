import sys
from PyQt6.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QSpinBox, QDoubleSpinBox, QComboBox, QFormLayout, QGroupBox, QMessageBox, QHeaderView, QSplitter, 
                             QDialog, QDialogButtonBox, QTabWidget, QFileDialog)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QSize, QDate, QDateTime

from db import DatabaseManager

class InventoryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistem Inventori Barang")
        self.setGeometry(100, 100, 1200, 800)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                padding: 6px 12px;
                border-radius: 4px;
                border: 1px solid #bbbbbb;
                background-color: #f0f0f0;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QTableWidget {
                gridline-color: #d0d0d0;
                selection-background-color: #a6c9e2;
                alternate-background-color: #f9f9f9;
            }
            QHeaderView::section {
                background-color: #e6e6e6;
                padding: 4px;
                border: 1px solid #d0d0d0;
                font-weight: bold;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                padding: 4px;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
        """)

        self.db = DatabaseManager()

        # Main widget with splitter for resizable sections
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        # Create UI Components
        self.create_menu()
        self.create_toolbar()
        self.create_main_content()

        # Load initial data
        self.load_data()
        
    def create_menu(self):
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("File")
        
        export_action = QAction("Export Data", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)
        
        import_action = QAction("Import Data", self)
        import_action.setShortcut("Ctrl+I")
        import_action.triggered.connect(self.import_data)
        file_menu.addAction(import_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Keluar", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menu_bar.addMenu("Edit")
        
        clear_action = QAction("Reset Form", self)
        clear_action.setShortcut("Ctrl+R")
        clear_action.triggered.connect(self.clear_form)
        edit_menu.addAction(clear_action)
        
        # View menu
        view_menu = menu_bar.addMenu("Tampilan")
        
        refresh_action = QAction("Refresh Data", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.load_data)
        view_menu.addAction(refresh_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("Bantuan")
        
        about_action = QAction("Tentang Aplikasi", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
        
        help_action = QAction("Panduan Penggunaan", self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

    def create_toolbar(self):
        toolbar = self.addToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(24, 24))
        
        # Export action
        export_action = QAction("Export", self)
        export_action.setToolTip("Export data ke CSV")
        export_action.triggered.connect(self.export_data)
        toolbar.addAction(export_action)
        
        # Import action
        import_action = QAction("Import", self)
        import_action.setToolTip("Import data dari CSV")
        import_action.triggered.connect(self.import_data)
        toolbar.addAction(import_action)

    def add_item_from_dialog(self, dialog, item_code, item_name, quantity, price, category, notes):
        code = item_code.text().strip()
        name = item_name.text().strip()
        qty = quantity.value()
        prc = price.value()
        cat = category.currentText()
        note = notes.text().strip()
        
        if not code or not name:
            QMessageBox.warning(self, "Input Error", "Kode dan Nama harus diisi!")
            return
        
        try:
            self.db.insert_item(code, name, qty, prc, cat, note)
            self.load_data()
            dialog.accept()
            QMessageBox.information(self, "Tambah Berhasil", f"Item '{name}' berhasil ditambahkan")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menambahkan item: {str(e)}")

    def create_main_content(self):
        # Use splitter for resizable areas
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Create content tabs
        tab_widget = QTabWidget()
        
        # Input tab
        input_tab = QWidget()
        input_layout = QVBoxLayout()
        input_tab.setLayout(input_layout)
        
        # Add form and buttons to input tab
        input_layout.addWidget(self.create_input_form())
        
        # Data view tab
        data_tab = QWidget()
        data_layout = QVBoxLayout()
        data_tab.setLayout(data_layout)
        
        # Create table widget
        self.create_table()
        self.create_search_section()
        
        data_layout.addWidget(self.table)
        data_layout.addLayout(self.search_layout)
        
        # Add tabs to tab widget
        tab_widget.addTab(input_tab, "Input dan Edit Data")
        tab_widget.addTab(data_tab, "Tampilan Data")
        
        # Add tab widget and summary to splitter
        splitter.addWidget(tab_widget)
        
        # Summary section
        summary_widget = QWidget()
        summary_layout = QVBoxLayout()
        summary_widget.setLayout(summary_layout)
        
        self.create_summary()
        summary_layout.addLayout(self.summary_layout)
        
        # Identity label
        self.create_identity_label()
        summary_layout.addWidget(self.identity_label)
        
        splitter.addWidget(summary_widget)
        
        # Set initial sizes
        splitter.setSizes([600, 200])
        
        self.main_layout.addWidget(splitter)

    def create_input_form(self):
        group = QGroupBox("Masukkan Data Barang")
        main_layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        # Enhanced input fields with validation and placeholders
        self.item_code = QLineEdit()
        self.item_code.setPlaceholderText("Contoh: QC-001")
        self.item_code.setMaxLength(10)
        
        self.item_name = QLineEdit()
        self.item_name.setPlaceholderText("Masukkan nama barang")
        
        self.quantity = QSpinBox()
        self.quantity.setRange(0, 10000)
        self.quantity.setSingleStep(1)
        
        self.price = QDoubleSpinBox()
        self.price.setRange(0, 1000000000)
        self.price.setPrefix("Rp. ")
        self.price.setGroupSeparatorShown(True)
        self.price.setDecimals(0)
        self.price.setSingleStep(1000)
        
        self.category = QComboBox()
        self.category.addItems(["Elektronik", "Peralatan", "Bahan", "Alat Kantor", "Furniture", "Lainnya"])
        
        self.notes = QLineEdit()
        self.notes.setPlaceholderText("Catatan tambahan (opsional)")
        
        # Add form fields with proper styling
        form_layout.addRow(QLabel("Kode Barang:"), self.item_code)
        form_layout.addRow(QLabel("Nama Barang:"), self.item_name)
        form_layout.addRow(QLabel("Jumlah:"), self.quantity)
        form_layout.addRow(QLabel("Harga Satuan:"), self.price)
        form_layout.addRow(QLabel("Kategori:"), self.category)
        form_layout.addRow(QLabel("Catatan:"), self.notes)
        
        # Buttons with improved layout and styling
        btn_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Tambah")
        self.add_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.add_btn.clicked.connect(self.add_item)
        
        self.update_btn = QPushButton("Update")
        self.update_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        self.update_btn.clicked.connect(self.update_item)
        
        self.delete_btn = QPushButton("Hapus")
        self.delete_btn.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        self.delete_btn.clicked.connect(self.delete_item)
        
        self.clear_btn = QPushButton("Reset")
        self.clear_btn.clicked.connect(self.clear_form)
        
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.clear_btn)
        
        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)
        
        group.setLayout(main_layout)
        return group

    def create_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(6)  # Added column for notes
        self.table.setHorizontalHeaderLabels(["Kode", "Nama", "Stok", "Harga Satuan", "Kategori", "Catatan"])
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # Connect table selection to form update
        self.table.itemSelectionChanged.connect(self.on_table_selection_changed)
        
        # Set columns to resize with table
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)

    def create_search_section(self):
        self.search_layout = QHBoxLayout()
        
        search_label = QLabel("Pencarian:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari barang...")
        self.search_input.returnPressed.connect(self.search_items)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Semua", "Kode", "Nama", "Kategori", "Catatan"])
        
        self.search_btn = QPushButton("Cari")
        self.search_btn.clicked.connect(self.search_items)
        
        clear_search_btn = QPushButton("Reset Pencarian")
        clear_search_btn.clicked.connect(self.reset_search)
        
        self.search_layout.addWidget(search_label)
        self.search_layout.addWidget(self.search_input, 3)
        self.search_layout.addWidget(self.filter_combo, 1)
        self.search_layout.addWidget(self.search_btn)
        self.search_layout.addWidget(clear_search_btn)

    def create_summary(self):
        self.summary_layout = QHBoxLayout()
        
        # Create styled summary labels
        summary_style = "font-weight: bold; font-size: 14px; padding: 5px; background-color: #e6e6e6; border-radius: 3px;"
        
        self.total_items = QLabel("Total Jenis: 0")
        self.total_items.setStyleSheet(summary_style)
        self.total_items.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.total_stock = QLabel("Total Stok: 0")
        self.total_stock.setStyleSheet(summary_style)
        self.total_stock.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.total_value = QLabel("Nilai Inventori: Rp0")
        self.total_value.setStyleSheet(summary_style)
        self.total_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add date and time label
        now = QDateTime.currentDateTime()
        self.date_label = QLabel(f"Terakhir update: {now.toString('dd/MM/yyyy HH:mm')}")
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.date_label.setStyleSheet("color: #666666; font-style: italic;")
        
        self.summary_layout.addWidget(self.total_items)
        self.summary_layout.addWidget(self.total_stock)
        self.summary_layout.addWidget(self.total_value)
        self.summary_layout.addWidget(self.date_label)

    def create_identity_label(self):
        self.identity_label = QLabel("Muhammad Nune Huria Sakti - F1D022075")
        self.identity_label.setStyleSheet("color: gray; font-size: 12px; font-style: italic;")
        self.identity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def show_about_dialog(self):
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("Tentang Aplikasi")
        
        layout = QVBoxLayout()
        
        title_label = QLabel("Sistem Inventori Barang")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        description = QLabel("Mini Project Pemrograman Visual 2025")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        developer = QLabel("Made with 💗 by Muhammad Nune Huria Sakti - F1D022075")
        developer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        version = QLabel("Semester Genap 2025")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(title_label)
        layout.addWidget(description)
        layout.addWidget(developer)
        layout.addWidget(version)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(about_dialog.accept)
        layout.addWidget(buttons)
        
        about_dialog.setLayout(layout)
        about_dialog.exec()

    def show_help(self):
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("Panduan Penggunaan")
        help_dialog.resize(500, 400)
        
        layout = QVBoxLayout()
        
        title = QLabel("Panduan Penggunaan Aplikasi")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        help_text = QLabel(
            "Petunjuk penggunaan aplikasi:\n\n"
            "1. Tambah Barang: Isi form dengan data lengkap lalu klik tombol 'Tambah'\n"
            "2. Update Barang: Pilih barang dari tabel, edit data di form, lalu klik 'Update'\n"
            "3. Hapus Barang: Pilih barang dari tabel lalu klik tombol 'Hapus'\n"
            "4. Pencarian: Masukkan kata kunci di kolom pencarian, pilih filter, lalu klik 'Cari'\n"
            "5. Export Data: Pilih menu File > Export Data untuk menyimpan data ke CSV\n\n"
            "Shortcut:\n"
            "- Ctrl+E : Export data\n"
            "- Ctrl+I : Import data\n"
            "- Ctrl+R : Reset form\n"
            "- F5 : Refresh data"
        )
        help_text.setWordWrap(True)
        
        layout.addWidget(title)
        layout.addWidget(help_text)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(help_dialog.accept)
        layout.addWidget(buttons)
        
        help_dialog.setLayout(layout)
        help_dialog.exec()

    def load_data(self):
        self.table.setRowCount(0)
        items = self.db.fetch_all()
        
        for row_data in items:
            row_number = self.table.rowCount()
            self.table.insertRow(row_number)
            
            # Assume db returns kode, nama, qty, price, category, notes
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                
                # Format price column with currency format
                if column_number == 3:  # Price column
                    item = QTableWidgetItem(f"Rp {int(data):,}")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                
                self.table.setItem(row_number, column_number, item)
        
        self.update_summary()
        
        # Update date/time label
        now = QDateTime.currentDateTime()
        self.date_label.setText(f"Terakhir update: {now.toString('dd/MM/yyyy HH:mm')}")

    def on_table_selection_changed(self):
        selected_rows = self.table.selectedItems()
        if selected_rows:
            row = selected_rows[0].row()
            self.item_code.setText(self.table.item(row, 0).text())
            self.item_name.setText(self.table.item(row, 1).text())
            self.quantity.setValue(int(self.table.item(row, 2).text()))
            
            # Parse price from string like "Rp 5,000"
            price_text = self.table.item(row, 3).text().replace("Rp ", "").replace(",", "")
            self.price.setValue(float(price_text))
            
            # Find category index
            category_text = self.table.item(row, 4).text()
            category_index = self.category.findText(category_text)
            if category_index >= 0:
                self.category.setCurrentIndex(category_index)
                
            # Set notes if available
            if self.table.columnCount() > 5 and self.table.item(row, 5) is not None:
                self.notes.setText(self.table.item(row, 5).text())
            else:
                self.notes.clear()

    def add_item(self):
        code = self.item_code.text().strip()
        name = self.item_name.text().strip()
        quantity = self.quantity.value()
        price = self.price.value()
        category = self.category.currentText()
        notes = self.notes.text().strip()

        if not code or not name:
            QMessageBox.warning(self, "Input Error", "Kode dan Nama harus diisi!")
            return
            
        try:
            self.db.insert_item(code, name, quantity, price, category, notes)
            self.load_data()
            self.clear_form()
            QMessageBox.information(self, "Tambah Berhasil", f"Item '{name}' berhasil ditambahkan")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menambahkan item: {str(e)}")

    def update_item(self):
        code = self.item_code.text().strip()
        name = self.item_name.text().strip()
        quantity = self.quantity.value()
        price = self.price.value()
        category = self.category.currentText()
        notes = self.notes.text().strip()

        if not code:
            QMessageBox.warning(self, "Update Error", "Kode Barang harus diisi untuk update!")
            return     
            
        try:
            self.db.update_item(code, name, quantity, price, category, notes)
            self.load_data()
            self.clear_form()
            QMessageBox.information(self, "Update Berhasil", f"Item '{name}' berhasil diupdate")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal mengupdate item: {str(e)}")

    def delete_item(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Hapus Error", "Pilih item yang ingin dihapus!")
            return

        reply = QMessageBox.question(
            self,
            "Konfirmasi Hapus",
            "Apakah Anda yakin ingin menghapus item yang dipilih?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            for row in selected_rows:
                item_code = self.table.item(row.row(), 0).text()  # Assuming the first column is the item code
                try:
                    self.db.delete_item(item_code)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Gagal menghapus item: {str(e)}")
            self.load_data()
            QMessageBox.information(self, "Hapus Berhasil", "Item berhasil dihapus")

    def load_data(self):
        self.table.setRowCount(0)
        items = self.db.fetch_all()
        
        for row_data in items:
            row_number = self.table.rowCount()
            self.table.insertRow(row_number)
            
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                
                # Format price column with currency format
                if column_number == 3:  # Price column
                    item = QTableWidgetItem(f"Rp {int(data):,}")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                
                self.table.setItem(row_number, column_number, item)
        
        # Resize columns and update summary
        self.table.resizeColumnsToContents()
        self.update_summary()
    
        # Update date/time label
        now = QDateTime.currentDateTime()
        self.date_label.setText(f"Terakhir update: {now.toString('dd/MM/yyyy HH:mm')}")

    def clear_form(self):
        self.item_code.clear()
        self.item_name.clear()
        self.quantity.setValue(0)
        self.price.setValue(0)
        self.category.setCurrentIndex(0)
        self.notes.clear()

    def search_items(self):
        keyword = self.search_input.text().strip()
        filter_by = self.filter_combo.currentText()

        items = self.db.search_items(keyword, filter_by)
        self.table.setRowCount(0)
        
        for row_data in items:
            row_number = self.table.rowCount()
            self.table.insertRow(row_number)
            
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                
                # Format price column
                if column_number == 3:  # Price column
                    item = QTableWidgetItem(f"Rp {int(data):,}")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    
                self.table.setItem(row_number, column_number, item)
        
        self.table.resizeColumnsToContents()
        QMessageBox.information(self, "Pencarian", f"Ditemukan {self.table.rowCount()} item")

    def reset_search(self):
        self.search_input.clear()
        self.filter_combo.setCurrentIndex(0)
        self.load_data()

    def update_summary(self):
        items = self.db.fetch_all()
        total_items = len(items)
        
        # Calculate totals from data
        try:
            total_stock = sum([item[2] for item in items])
            total_value = sum([item[2] * item[3] for item in items])
        except:
            total_stock = 0
            total_value = 0

        self.total_items.setText(f"Total Jenis: {total_items}")
        self.total_stock.setText(f"Total Stok: {total_stock}")
        self.total_value.setText(f"Nilai Inventori: Rp{total_value:,.0f}")

    def export_data(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Export Data",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_name:
            try:
                self.db.export_to_csv(file_name)
                QMessageBox.information(self, "Export Berhasil", f"Data berhasil diekspor ke {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Export Gagal", f"Gagal mengekspor data: {str(e)}")

    def import_data(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Import Data",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_name:
            try:
                count = self.db.import_from_csv(file_name)
                self.load_data()
                QMessageBox.information(self, "Import Berhasil", f"{count} data berhasil diimpor")
            except Exception as e:
                QMessageBox.critical(self, "Import Gagal", f"Gagal mengimpor data: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec())