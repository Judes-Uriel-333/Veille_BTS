from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget
from PySide6.QtCore import Qt
from app.ui.pages.login_page import LoginPage
from app.utils.config import ThemeManager
from app.ui.pages.dashboard_page import DashboardPage
from app.services.session import Session



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Veille IA - BTS (Desktop)")
        self.resize(1000, 650)

        # --- Theme manager (light/dark) ---
        self.theme = ThemeManager()

        # --- Central widget ---
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # --- Top bar ---
        top_bar = QHBoxLayout()
        self.lbl_title = QLabel("Veille IA")
        self.lbl_title.setObjectName("TopTitle")

        self.btn_toggle_theme = QPushButton("🌙")
        self.btn_toggle_theme.setObjectName("ThemeToggle")
        self.btn_toggle_theme.setFixedWidth(60)
        self.btn_toggle_theme.clicked.connect(self.toggle_theme)

        top_bar.addWidget(self.lbl_title)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_toggle_theme)
        main_layout.addLayout(top_bar)

        # --- Pages container ---
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # Pages
        self.page_login = LoginPage(on_login_success=self.on_login_success)
        self.stack.addWidget(self.page_login)

        self.page_dashboard = DashboardPage(on_logout=self.logout)
        self.stack.addWidget(self.page_dashboard)

        # Apply initial theme
        self.apply_theme()

    def apply_theme(self):
        qss = self.theme.current_qss()
        self.setStyleSheet(qss)
        # Update button icon
        self.btn_toggle_theme.setText("☀️" if self.theme.is_dark else "🌙")

    def toggle_theme(self):
        self.theme.toggle()
        self.apply_theme()

    def on_login_success(self, email: str):
        Session.current_user_email = email
        self.lbl_title.setText(f"Veille IA — {email}")
        self.stack.setCurrentWidget(self.page_dashboard)
        
    def logout(self):
        Session.current_user_email = None
        self.lbl_title.setText("Veille IA")
        self.stack.setCurrentWidget(self.page_login)
    
    
