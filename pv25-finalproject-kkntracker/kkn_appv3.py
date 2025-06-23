import sys
import csv
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
    QDateEdit, QTextEdit, QStatusBar, QMessageBox, QFileDialog, QHeaderView,
    QFrame, QScrollArea, QSplitter, QGroupBox, QProgressBar, QSpacerItem,
    QSizePolicy, QTabWidget, QToolBar, QSystemTrayIcon, QMenu, QGraphicsDropShadowEffect, QSpinBox
)
from PyQt6.QtGui import QAction, QIcon, QFont, QPixmap, QPainter, QColor, QPen, QIntValidator
from PyQt6.QtCore import QDate, Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve, pyqtSignal
from supabase import create_client, Client
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# --- PANGGIL KONFIGURASI SUPABASE ---
load_dotenv()

# --- KONFIGURASI SUPABASE ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

NAMA_MAHASISWA = "Muhammad Nune Huria Sakti"
NIM_MAHASISWA = "F1D022075"

class AnimatedButton(QPushButton):
    """Custom animated button with hover effects"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(45)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

class ModernCard(QFrame):
    """Modern card widget with shadow effect"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            ModernCard {
                background-color: white;
                border-radius: 12px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
        """)

class StatsWidget(QWidget):
    """Widget to display statistics"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(20)
        
        # Create stat cards
        self.total_card = self.create_stat_card("Total Kegiatan", "0", "#3498db")
        self.completed_card = self.create_stat_card("Selesai", "0", "#27ae60")
        self.ongoing_card = self.create_stat_card("Berlangsung", "0", "#f39c12")
        self.planned_card = self.create_stat_card("Rencana", "0", "#9b59b6")
        self.total_hours_card = self.create_stat_card("JKEM", "0", "#b65959")
        
        layout.addWidget(self.total_card)
        layout.addWidget(self.completed_card)
        layout.addWidget(self.ongoing_card)
        layout.addWidget(self.planned_card)
        layout.addWidget(self.total_hours_card)
        
    def create_stat_card(self, title, value, color):
        card = ModernCard()
        card.setFixedHeight(100)
        
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setStyleSheet(f"""
            QLabel {{
                font-size: 28px;
                font-weight: bold;
                color: {color};
                margin: 5px;
            }}
        """)
        
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #666;
                font-weight: 500;
            }
        """)
        
        layout.addWidget(value_label)
        layout.addWidget(title_label)
        
        # Store references for updating
        card.value_label = value_label
        card.title_label = title_label
        
        return card
        
    def update_stats(self, total, completed, ongoing, planned, total_hours):
        self.total_card.value_label.setText(str(total))
        self.completed_card.value_label.setText(str(completed))
        self.ongoing_card.value_label.setText(str(ongoing))
        self.planned_card.value_label.setText(str(planned))
        self.total_hours_card.value_label.setText(f"{total_hours} Jam")

class NotificationWidget(QWidget):
    """Enhanced notification widget with improved styling and features"""
    closed = pyqtSignal()
    
    def __init__(self, message, type="info", duration=3000, parent=None):
        super().__init__(parent)
        self.type = type
        self.duration = duration
        self.setFixedHeight(60)
        self.setMinimumWidth(400)
        self.setup_ui(message, type)
        self.setup_auto_close()
        
    def setup_ui(self, message, type):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(12)
        
        # Icon and colors based on type
        icons = {
            "success": "✅",
            "error": "❌", 
            "warning": "⚠️",
            "info": "ℹ️"
        }
        
        colors = {
            "success": {
                "bg": "#d4edda",
                "border": "#c3e6cb",
                "text": "#155724",
                "accent": "#28a745"
            },
            "error": {
                "bg": "#f8d7da", 
                "border": "#f5c6cb",
                "text": "#721c24",
                "accent": "#dc3545"
            },
            "warning": {
                "bg": "#fff3cd",
                "border": "#ffeaa7", 
                "text": "#856404",
                "accent": "#ffc107"
            },
            "info": {
                "bg": "#d1ecf1",
                "border": "#bee5eb",
                "text": "#0c5460", 
                "accent": "#17a2b8"
            }
        }
        
        color_scheme = colors.get(type, colors["info"])
        
        # Apply enhanced styling
        self.setStyleSheet(f"""
            NotificationWidget {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {color_scheme["bg"]}, stop:1 {color_scheme["border"]});
                border: 2px solid {color_scheme["border"]};
                border-left: 4px solid {color_scheme["accent"]};
                border-radius: 12px;
                padding: 5px;
            }}
        """)
        
        # Icon label
        icon_label = QLabel(icons.get(type, "ℹ️"))
        icon_label.setStyleSheet(f"""
            QLabel {{
                font-size: 20px;
                color: {color_scheme["accent"]};
                font-weight: bold;
                border: none;
                background: transparent;
                min-width: 30px;
                max-width: 30px;
            }}
        """)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        # Message label with enhanced styling
        message_label = QLabel(message)
        message_label.setStyleSheet(f"""
            QLabel {{
                color: {color_scheme["text"]};
                font-weight: 600;
                font-size: 13px;
                border: none;
                background: transparent;
                padding: 2px 0px;
            }}
        """)
        message_label.setWordWrap(True)
        layout.addWidget(message_label, 1)
        
        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(24, 24)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: {color_scheme["text"]};
                font-weight: bold;
                font-size: 14px;
                border-radius: 12px;
                padding: 0px;
            }}
            QPushButton:hover {{
                background-color: {color_scheme["accent"]};
                color: white;
            }}
        """)
        close_btn.clicked.connect(self.close_notification)
        layout.addWidget(close_btn)
        
        # Progress bar for duration
        self.progress_widget = QWidget()
        self.progress_widget.setFixedHeight(3)
        self.progress_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {color_scheme["accent"]};
                border-radius: 1px;
            }}
        """)
        
        # Add progress bar to bottom
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        content_widget = QWidget()
        content_widget.setLayout(layout)
        
        main_layout.addWidget(content_widget)
        main_layout.addWidget(self.progress_widget)
        
        self.setLayout(main_layout)
        
        # Enhanced shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)
        
    def setup_auto_close(self):
        """Setup auto-close timer with progress animation"""
        if self.duration > 0:
            # Progress animation
            self.progress_animation = QPropertyAnimation(self.progress_widget, b"geometry")
            self.progress_animation.setDuration(self.duration)
            
            # Start from full width to zero width
            full_rect = QRect(0, 0, self.width(), 3)
            empty_rect = QRect(0, 0, 0, 3)
            
            self.progress_animation.setStartValue(full_rect)
            self.progress_animation.setEndValue(empty_rect)
            self.progress_animation.setEasingCurve(QEasingCurve.Type.Linear)
            
            # Auto close timer
            self.close_timer = QTimer()
            self.close_timer.setSingleShot(True)
            self.close_timer.timeout.connect(self.close_notification)
            self.close_timer.start(self.duration)
            
    def close_notification(self):
        """Close notification and emit signal"""
        if hasattr(self, 'close_timer'):
            self.close_timer.stop()
        if hasattr(self, 'progress_animation'):
            self.progress_animation.stop()
        self.closed.emit()
        
    def enterEvent(self, event):
        """Pause auto-close on hover"""
        if hasattr(self, 'close_timer') and self.close_timer.isActive():
            self.close_timer.stop()
        if hasattr(self, 'progress_animation') and self.progress_animation.state() == QPropertyAnimation.State.Running:
            self.progress_animation.pause()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        """Resume auto-close when mouse leaves"""
        if hasattr(self, 'close_timer'):
            remaining_time = max(500, self.duration // 4)  # Give at least 500ms
            self.close_timer.start(remaining_time)
        if hasattr(self, 'progress_animation'):
            self.progress_animation.resume()
        super().leaveEvent(event)
        
    def resizeEvent(self, event):
        """Update progress bar on resize"""
        super().resizeEvent(event)
        if hasattr(self, 'progress_animation') and self.progress_animation.state() != QPropertyAnimation.State.Running:
            self.progress_widget.setFixedWidth(self.width())

class NotificationManager:
    """Manages multiple notifications with queuing and positioning"""
    
    def __init__(self, parent):
        self.parent = parent
        self.notifications = []
        self.overlay = None
        
    def show_notification(self, message, type="info", duration=3000):
        """Show notification with enhanced features"""
        # Create overlay if needed
        if not self.overlay:
            self.overlay = OverlayWidget(self.parent)
            
        # Create new notification
        notification = NotificationWidget(message, type, duration, self.parent)
        notification.closed.connect(lambda: self.remove_notification(notification))
        
        # Add to list and position
        self.notifications.append(notification)
        self.position_notifications()
        
        # Show overlay and notification
        self.overlay.setGeometry(self.parent.rect())
        self.overlay.show()
        notification.show()
        
        # Animate in
        self.animate_notification_in(notification)
        
        # Start progress animation after slide-in
        QTimer.singleShot(400, lambda: self.start_progress_animation(notification))
        
    def start_progress_animation(self, notification):
        """Start the progress bar animation"""
        if hasattr(notification, 'progress_animation'):
            # Update progress bar size to match notification width
            full_rect = QRect(0, 0, notification.width(), 3)
            empty_rect = QRect(0, 0, 0, 3)
            
            notification.progress_animation.setStartValue(full_rect)
            notification.progress_animation.setEndValue(empty_rect)
            notification.progress_animation.start()
            
    def remove_notification(self, notification):
        """Remove notification with animation"""
        if notification in self.notifications:
            self.animate_notification_out(notification)
            
    def animate_notification_in(self, notification):
        """Animate notification sliding in"""
        notif_rect = notification.geometry()
        start_pos = QRect(notif_rect.x(), -notif_rect.height(), notif_rect.width(), notif_rect.height())
        
        notification.setGeometry(start_pos)
        
        animation = QPropertyAnimation(notification, b"geometry")
        animation.setDuration(500)
        animation.setStartValue(start_pos)
        animation.setEndValue(notif_rect)
        animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        animation.start()
        
        # Store animation reference
        notification.slide_in_animation = animation
        
    def animate_notification_out(self, notification):
        """Animate notification sliding out"""
        current_pos = notification.geometry()
        end_pos = QRect(current_pos.x(), -current_pos.height(), current_pos.width(), current_pos.height())
        
        animation = QPropertyAnimation(notification, b"geometry")
        animation.setDuration(300)
        animation.setStartValue(current_pos)
        animation.setEndValue(end_pos)
        animation.setEasingCurve(QEasingCurve.Type.InCubic)
        
        def cleanup():
            if notification in self.notifications:
                self.notifications.remove(notification)
                notification.hide()
                notification.deleteLater()
                
            # Reposition remaining notifications
            self.position_notifications()
            
            # Hide overlay if no notifications
            if not self.notifications and self.overlay:
                self.overlay.hide()
                
        animation.finished.connect(cleanup)
        animation.start()
        
    def position_notifications(self):
        """Position all notifications vertically"""
        y_offset = 20
        for i, notification in enumerate(self.notifications):
            x_pos = (self.parent.width() - notification.width()) // 2
            notification.setGeometry(x_pos, y_offset, notification.width(), notification.height())
            y_offset += notification.height() + 10
            
    def resize_event(self):
        """Handle parent window resize"""
        if self.overlay:
            self.overlay.setGeometry(self.parent.rect())
        self.position_notifications()

# Enhanced OverlayWidget with blur effect
class OverlayWidget(QWidget):
    """Enhanced overlay widget with subtle blur effect"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(2px);
        """)
        self.hide()

class KKNLogbookApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.init_notification_system()
        self.current_log_id = None
        self.overlay = None
        
        self.setWindowTitle("Logbook Digital - KKN PMD")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 700)

        # Create the main interface
        self.setup_ui()
        self.apply_modern_styles()
        
        # Load initial data
        self.load_data()
        
        # Setup auto-refresh
        self.setup_auto_refresh()

    def setup_ui(self):
        """Setup the main user interface"""
        # Create toolbar
        self.create_toolbar()
        
        # Create status bar
        self.create_status_bar()
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Create splitter for resizable sections
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout = QHBoxLayout(main_widget)
        main_layout.addWidget(splitter)
        
        # Left panel (Form)
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel (Table and Stats)
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([400, 800])
        
        # Notification area
        self.notification_widget = None

    def create_toolbar(self):
        """Create modern toolbar"""
        toolbar = QToolBar()
        toolbar.setStyleSheet("""
            QToolBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border-bottom: 1px solid #e9ecef;
                spacing: 10px;
                padding: 5px;
            }
            QToolBar QToolButton {
                background-color: transparent;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 500;
            }
            QToolBar QToolButton:hover {
                background-color: rgba(0, 123, 255, 0.1);
            }
        """)
        
        # Add actions
        refresh_action = QAction("🔄 Refresh", self)
        refresh_action.triggered.connect(self.load_data)
        toolbar.addAction(refresh_action)
        
        toolbar.addSeparator()
        
        export_action = QAction("📊 Export CSV", self)
        export_action.triggered.connect(self.export_to_csv)
        toolbar.addAction(export_action)
        
        toolbar.addSeparator()
        
        about_action = QAction("ℹ️ About", self)
        about_action.triggered.connect(self.show_about_dialog)
        toolbar.addAction(about_action)
        
        self.addToolBar(toolbar)

    def create_status_bar(self):
        """Create enhanced status bar"""
        status_bar = QStatusBar()
        
        # Student info
        student_info = QLabel(f"👤 {NAMA_MAHASISWA} | 🎓 {NIM_MAHASISWA}")
        student_info.setStyleSheet("""
            QLabel {
                padding: 5px 10px;
                background-color: #e3f2fd;
                border-radius: 4px;
                font-weight: 500;
            }
        """)
        
        # Last updated info
        self.last_updated_label = QLabel("Last updated: Never")
        self.last_updated_label.setStyleSheet("color: #666; font-size: 11px;")
        
        status_bar.addWidget(student_info)
        status_bar.addPermanentWidget(self.last_updated_label)
        
        self.setStatusBar(status_bar)

    def create_left_panel(self):
        """Create the left panel with form"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumWidth(450)
        
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("📝 Form Input Kegiatan")
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border-radius: 8px;
            }
        """)
        layout.addWidget(title)
        
        # Form card
        form_card = ModernCard()
        form_layout = QVBoxLayout(form_card)
        form_layout.setSpacing(15)
        
        # Create form fields
        self.create_form_fields(form_layout)
        
        layout.addWidget(form_card)
        
        # Buttons
        self.create_action_buttons(layout)
        
        # Add stretch to push everything to top
        layout.addStretch()
        
        scroll_area.setWidget(panel)
        return scroll_area

    def create_form_fields(self, layout):
        """Create enhanced form fields"""
        # Title field
        title_group = QGroupBox("Judul Kegiatan")
        title_layout = QVBoxLayout(title_group)
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Masukkan judul kegiatan...")
        title_layout.addWidget(self.title_input)
        layout.addWidget(title_group)
        
        # Date and Category row
        date_jkem_layout = QHBoxLayout()
        
        # Date field
        date_group = QGroupBox("Tanggal")
        date_layout = QVBoxLayout(date_group)
        self.date_input = QDateEdit(calendarPopup=True)
        self.date_input.setDate(QDate.currentDate())
        date_layout.addWidget(self.date_input)
        date_jkem_layout.addWidget(date_group)
        
        # JKEM field
        jkem_group = QGroupBox("JKEM")
        jkem_layout = QVBoxLayout(jkem_group)
        self.jkem_input = QSpinBox()
        self.jkem_input.setRange(1, 24) 
        self.jkem_input.setValue(1) 
        self.jkem_input.setSuffix(" Jam")
        self.jkem_input.setSingleStep(1)
        jkem_layout.addWidget(self.jkem_input)
        date_jkem_layout.addWidget(jkem_group)
        
        layout.addLayout(date_jkem_layout)
        
        # Status field
        status_group = QGroupBox("Status Kegiatan")
        status_layout = QVBoxLayout(status_group)
        self.status_input = QComboBox()
        self.status_input.addItems([
            "📋 Rencana", "⚡ Berlangsung", "✅ Selesai", "❌ Dibatalkan"
        ])
        status_layout.addWidget(self.status_input)
        layout.addWidget(status_group)
        
        # Notes field
        notes_group = QGroupBox("Catatan & Deskripsi")
        notes_layout = QVBoxLayout(notes_group)
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText(
            "Tulis deskripsi detail kegiatan, hasil yang dicapai, "
            "kendala yang dihadapi, dan rencana tindak lanjut..."
        )
        self.notes_input.setMaximumHeight(120)
        notes_layout.addWidget(self.notes_input)
        layout.addWidget(notes_group)

    def create_action_buttons(self, layout):
        """Create action buttons with icons"""
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)
        
        # Primary actions
        primary_layout = QHBoxLayout()
        
        self.add_button = AnimatedButton("➕ Tambah")
        self.add_button.clicked.connect(self.add_log)
        self.add_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #28a745, stop:1 #218838);
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #218838, stop:1 #1e7e34);
            }
        """)
        
        self.update_button = AnimatedButton("✏️ Update")
        self.update_button.clicked.connect(self.update_log)
        self.update_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #007bff, stop:1 #0056b3);
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0056b3, stop:1 #004494);
            }
        """)
        
        primary_layout.addWidget(self.add_button)
        primary_layout.addWidget(self.update_button)
        button_layout.addLayout(primary_layout)
        
        # Secondary actions
        secondary_layout = QHBoxLayout()
        
        self.delete_button = AnimatedButton("🗑️ Hapus")
        self.delete_button.clicked.connect(self.delete_log)
        self.delete_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #dc3545, stop:1 #c82333);
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c82333, stop:1 #bd2130);
            }
        """)
        
        self.clear_button = AnimatedButton("🧹 Bersihkan")
        self.clear_button.clicked.connect(self.clear_form)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6c757d, stop:1 #545b62);
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #545b62, stop:1 #4e555b);
            }
        """)
        
        secondary_layout.addWidget(self.delete_button)
        secondary_layout.addWidget(self.clear_button)
        button_layout.addLayout(secondary_layout)
        
        layout.addLayout(button_layout)

    def create_right_panel(self):
        """Create the right panel with stats and table"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)
        
        # Stats section
        stats_card = ModernCard()
        stats_layout = QVBoxLayout(stats_card)
        
        stats_title = QLabel("📊 Statistik Kegiatan")
        stats_title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
                margin-bottom: 10px;
            }
        """)
        stats_layout.addWidget(stats_title)
        
        self.stats_widget = StatsWidget()
        stats_layout.addWidget(self.stats_widget)
        
        layout.addWidget(stats_card)
        
        # Table section
        table_card = ModernCard()
        table_layout = QVBoxLayout(table_card)
        
        table_title = QLabel("📋 Daftar Kegiatan KKN")
        table_title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
                margin-bottom: 10px;
            }
        """)
        table_layout.addWidget(table_title)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("🔍 Cari:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari berdasarkan judul atau kategori...")
        self.search_input.textChanged.connect(self.filter_table)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        table_layout.addLayout(search_layout)
        
        # Create table
        self.create_table(table_layout)
        
        layout.addWidget(table_card)
        
        return panel

    def create_table(self, parent_layout):
        """Create enhanced table"""
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Judul Kegiatan", "JKEM (Jam)", "Tanggal", "Status", "Catatan"
        ])
        
        # Table styling
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        
        # Header styling
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        
        # Connect selection event
        self.table.itemSelectionChanged.connect(self.populate_form_from_table)
        
        parent_layout.addWidget(self.table)

    def apply_modern_styles(self):
        """Apply modern styling to the application"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            
            QLabel {
                color: #2c3e50;
                font-size: 13px;
            }
            
            QLineEdit, QComboBox, QDateEdit, QTextEdit {
                padding: 10px;
                font-size: 13px;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                background-color: white;
                selection-background-color: #007bff;
            }
            
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTextEdit:focus {
                border-color: #007bff;
                background-color: #fff;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                color: #495057;
                font-size: 12px;
                font-weight: bold;
            }
            
            QTableWidget {
                gridline-color: #e9ecef;
                background-color: white;
                alternate-background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                font-size: 12px;
            }
            
            QTableWidget::item {
                padding: 8px;
                border: none;
            }
            
            QTableWidget::item:selected {
                background-color: #007bff;
                color: white;
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #495057, stop:1 #343a40);
                color: white;
                padding: 8px;
                font-weight: bold;
                font-size: 12px;
                border: none;
                border-right: 1px solid #6c757d;
            }
            
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            
            QScrollBar:vertical {
                background-color: #f8f9fa;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #ced4da;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #adb5bd;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #6c757d;
                margin-right: 5px;
            }
            
            QDateEdit::drop-down {
                border: none;
                width: 30px;
            }
            
            QDateEdit::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #6c757d;
                margin-right: 5px;
            }
        """)

    def setup_auto_refresh(self):
        """Setup auto-refresh timer"""
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.load_data)
        self.refresh_timer.start(300000)  # Refresh every 5 minutes

    def load_data(self):
        """Load data from Supabase with enhanced error handling"""
        try:
            response = self.supabase.table("logbook_kkn").select("*").order("tanggal", desc=True).execute()
            logs = response.data
            
            self.populate_table(logs)
            self.update_statistics(logs)
            
            # Update last updated time
            current_time = datetime.now().strftime("%H:%M:%S")
            self.last_updated_label.setText(f"Last updated: {current_time}")
            
        except Exception as e:
            self.show_notification(f"❌ Gagal memuat data: {str(e)}", "error")

    def populate_table(self, logs):
        """Populate table with data"""
        self.table.setRowCount(len(logs))
        
        for row_idx, log in enumerate(logs):
            # Store ID in first item
            title_item = QTableWidgetItem(log['judul'])
            title_item.setData(Qt.ItemDataRole.UserRole, log['id'])
            self.table.setItem(row_idx, 0, title_item)
            
            # JKEM
            jkem_value = log.get('jkem', 0) # Ambil nilai jkem, default 0 jika tidak ada
            jkem_item = QTableWidgetItem(str(jkem_value))
            jkem_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter) # Pusatkan teks
            self.table.setItem(row_idx, 1, jkem_item)
            
            # Date formatting
            date_str = log['tanggal']
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                formatted_date = date_obj.strftime('%d/%m/%Y')
            except:
                formatted_date = date_str
            self.table.setItem(row_idx, 2, QTableWidgetItem(formatted_date))
            
            # Status 
            status = log['status']
            status_item = QTableWidgetItem(f" {status}") # Beri spasi agar rapi
            if 'Selesai' in status:
                status_item.setBackground(QColor(212, 237, 218))
                status_item.setText("✅" + status_item.text())
            elif 'Berlangsung' in status:
                status_item.setBackground(QColor(255, 243, 205))
                status_item.setText("⚡" + status_item.text())
            elif 'Dibatalkan' in status:
                status_item.setBackground(QColor(248, 215, 218))
                status_item.setText("❌" + status_item.text())
            else: # Rencana
                status_item.setBackground(QColor(209, 236, 241))
                status_item.setText("📋" + status_item.text())
            self.table.setItem(row_idx, 3, status_item)

            # Notes (truncated) (Kolom 4)
            notes = log.get('catatan', '')
            if len(notes) > 50:
                notes = notes[:50] + "..."
            self.table.setItem(row_idx, 4, QTableWidgetItem(notes))

    def update_statistics(self, logs):
        """Update statistics display"""
        total = len(logs)
        completed = sum(1 for log in logs if 'Selesai' in log['status'])
        ongoing = sum(1 for log in logs if 'Berlangsung' in log['status'])
        planned = sum(1 for log in logs if 'Rencana' in log['status'])
        total_hours = sum(log.get('jkem', 0) for log in logs)
        
        self.stats_widget.update_stats(total, completed, ongoing, planned, total_hours)

    def filter_table(self):
        """Filter table based on search input"""
        search_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            title_item = self.table.item(row, 0)
            category_item = self.table.item(row, 1)
            
            # Pastikan item ada sebelum mengambil teksnya
            title_text = title_item.text().lower() if title_item else ""
            category_text = category_item.text().lower() if category_item else ""
            
            # Periksa apakah teks pencarian ada di judul atau kategori
            if search_text in title_text or search_text in category_text:
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)

    def populate_form_from_table(self):
            """Isi formulir dengan data dari baris tabel yang dipilih"""
            selected_rows = self.table.selectionModel().selectedRows()
            if not selected_rows:
                return

            selected_row = selected_rows[0].row()
            
            # Ambil ID log dari data pengguna pada item pertama
            log_id_item = self.table.item(selected_row, 0)
            self.current_log_id = log_id_item.data(Qt.ItemDataRole.UserRole)
            
            # Isi kolom formulir
            title = self.table.item(selected_row, 0).text()
            jkem_str = self.table.item(selected_row, 1).text()
            date_str = self.table.item(selected_row, 2).text()
            status_with_emoji = self.table.item(selected_row, 3).text().strip()
            
            # Ambil catatan lengkap dari database karena tabel hanya menampilkan potongan
            try:
                response = self.supabase.table("logbook_kkn").select("catatan, jkem").eq("id", self.current_log_id).single().execute()
                notes = response.data.get('catatan', '')
                jkem_val = response.data.get('jkem', 1)
            except Exception as e:
                notes = "Gagal mengambil detail."
                jkem_val = 1
                self.show_notification(f"❌ Gagal mengambil detail: {e}", "error")
            
            self.title_input.setText(title)
            
            # Atur tanggal
            self.date_input.setDate(QDate.fromString(date_str, "dd/MM/yyyy"))
            
            # Atur nilai JKEM
            self.jkem_input.setValue(jkem_val)
            
            # Atur status (cocokkan teks tanpa emoji)
            for i in range(self.status_input.count()):
                if self.status_input.itemText(i).endswith(status_with_emoji.split(" ", 1)[-1]):
                    self.status_input.setCurrentIndex(i)
                    break
            
            self.notes_input.setText(notes)

    def add_log(self):
        """Tambahkan entri log baru ke database"""
        title = self.title_input.text().strip()
        if not title:
            self.show_notification("❌ Judul kegiatan tidak boleh kosong!", "error")
            return
            
        # Ambil data dari formulir, hilangkan emoji dari teks combo box
        jkem = self.jkem_input.value()
        date_str = self.date_input.date().toString("yyyy-MM-dd")
        status = self.status_input.currentText().split(" ", 1)[-1]
        notes = self.notes_input.toPlainText().strip()
        
        
        log_data = {
            'judul': title,
            'jkem': jkem,
            'tanggal': date_str,
            'status': status,
            'catatan': notes,
        }
        
        try:
            self.supabase.table("logbook_kkn").insert(log_data).execute()
            self.show_notification("✅ Kegiatan berhasil ditambahkan!", "success")
            self.load_data()
            self.clear_form()
        except Exception as e:
            self.show_notification(f"❌ Gagal menambahkan kegiatan: {e}", "error")

    def update_log(self):
        """Perbarui entri log yang ada"""
        if self.current_log_id is None:
            self.show_notification("ℹ️ Pilih kegiatan dari tabel untuk diupdate.", "info")
            return
            
        title = self.title_input.text().strip()
        if not title:
            self.show_notification("❌ Judul kegiatan tidak boleh kosong!", "error")
            return
            
        # Ambil data yang diperbarui dari formulir
        updated_data = {
            'judul': title,
            'jkem': self.jkem_input.value(),
            'tanggal': self.date_input.date().toString("yyyy-MM-dd"),
            'status': self.status_input.currentText().split(" ", 1)[-1],
            'catatan': self.notes_input.toPlainText().strip()
        }
        
        try:
            self.supabase.table("logbook_kkn").update(updated_data).eq("id", self.current_log_id).execute()
            self.show_notification("✅ Kegiatan berhasil diupdate!", "success")
            self.load_data()
            self.clear_form()
        except Exception as e:
            self.show_notification(f"❌ Gagal mengupdate kegiatan: {e}", "error")

    def delete_log(self):
        """Hapus entri log yang dipilih"""
        if self.current_log_id is None:
            self.show_notification("ℹ️ Pilih kegiatan dari tabel untuk dihapus.", "info")
            return
            
        # Dialog konfirmasi
        reply = QMessageBox.question(self, 'Konfirmasi Hapus',
                                        f"Apakah Anda yakin ingin menghapus kegiatan '{self.title_input.text()}'?",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                        QMessageBox.StandardButton.No)
                                        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.supabase.table("logbook_kkn").delete().eq("id", self.current_log_id).execute()
                self.show_notification("🗑️ Kegiatan berhasil dihapus!", "success")
                self.load_data()
                self.clear_form()
            except Exception as e:
                self.show_notification(f"❌ Gagal menghapus kegiatan: {e}", "error")

    def clear_form(self):
        """Kosongkan semua kolom input dan pilihan saat ini"""
        self.title_input.clear()
        self.date_input.setDate(QDate.currentDate())
        self.jkem_input.setValue(1)
        self.status_input.setCurrentIndex(0)
        self.notes_input.clear()
        self.current_log_id = None
        self.table.clearSelection()
        self.title_input.setFocus()
        self.show_notification("🧹 Formulir dibersihkan.", "info", duration=1500)

    def export_to_csv(self):
        """Ekspor data tabel ke file CSV"""
        if self.table.rowCount() == 0:
            self.show_notification("ℹ️ Tidak ada data untuk diekspor.", "info")
            return
            
        path, _ = QFileDialog.getSaveFileName(self, "Simpan CSV", "logbook_kkn.csv", "CSV Files (*.csv)")
        
        if path:
            try:
                with open(path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Tulis header
                    headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
                    writer.writerow(headers)
                    
                    # Tulis baris data
                    for row in range(self.table.rowCount()):
                        row_data = []
                        for col in range(self.table.columnCount()):
                            item = self.table.item(row, col)
                            row_data.append(item.text() if item else "")
                        writer.writerow(row_data)
                        
                self.show_notification(f"📊 Data berhasil diekspor ke {path}", "success")
            except Exception as e:
                self.show_notification(f"❌ Gagal mengekspor data: {e}", "error")

    def show_about_dialog(self):
        """Tampilkan dialog box 'Tentang Aplikasi'"""
        about_text = f"""
        <b>Logbook Digital KKN-PMD v1.0</b>
        <p>Dibuat sebagai tugas pada mata kuliah Pemrograman Visual 2025</p>
        <p><b>Dikembangkan Oleh:</b><br>
        Nama: {NAMA_MAHASISWA}<br>
        NIM: {NIM_MAHASISWA}</p>
        <p><b>Teknologi:</b><br>
        - Python & PyQt6<br>
        - Supabase (Backend)</p>
        <p>2025</p>
        """
        QMessageBox.about(self, "Tentang Aplikasi", about_text)

    def init_notification_system(self):
        """Initialize the enhanced notification system"""
        self.notification_manager = NotificationManager(self)

    def show_notification(self, message, type="info", duration=3000):
        """Show enhanced notification"""
        self.notification_manager.show_notification(message, type, duration)

    def resizeEvent(self, event):
        """Handle window resize for notifications"""
        super().resizeEvent(event)
        if hasattr(self, 'notification_manager'):
            self.notification_manager.resize_event()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Terapkan font global untuk konsistensi
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    main_window = KKNLogbookApp()
    main_window.show()
    sys.exit(app.exec())