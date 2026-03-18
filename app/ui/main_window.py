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

        self.theme = ThemeManager()

        # --- Central widget ---
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Top bar ---
        top_bar_widget = QWidget()
        top_bar_widget.setObjectName("TopBar")
        top_bar_widget.setFixedHeight(56)
        top_bar = QHBoxLayout(top_bar_widget)
        top_bar.setContentsMargins(20, 0, 20, 0)
        top_bar.setSpacing(12)

        self.lbl_title = QLabel("Veille IA")
        self.lbl_title.setObjectName("TopTitle")

        self.btn_toggle_theme = QPushButton("Clair")
        self.btn_toggle_theme.setObjectName("ThemeToggle")
        self.btn_toggle_theme.setCursor(Qt.PointingHandCursor)
        self.btn_toggle_theme.clicked.connect(self.toggle_theme)

        top_bar.addWidget(self.lbl_title)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_toggle_theme)
        main_layout.addWidget(top_bar_widget)

        # --- Pages ---
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        self.page_login = LoginPage(on_login_success=self.on_login_success)
        self.stack.addWidget(self.page_login)

        self.page_dashboard = DashboardPage(on_logout=self.logout)
        self.stack.addWidget(self.page_dashboard)

        self.apply_theme()

    def apply_theme(self):
        qss = self.theme.current_qss()
        self.setStyleSheet(qss)
        self.btn_toggle_theme.setText("Clair" if self.theme.is_dark else "Sombre")

    def toggle_theme(self):
        self.theme.toggle()
        self.apply_theme()

    def on_login_success(self, email: str):
        Session.current_user_email = email
        self.lbl_title.setText(f"Veille IA - {email}")
        self.stack.setCurrentWidget(self.page_dashboard)

    def logout(self):
        Session.current_user_email = None
        self.lbl_title.setText("Veille IA")
        self.stack.setCurrentWidget(self.page_login)
