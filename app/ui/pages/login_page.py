from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QFrame, QStackedWidget)
from PySide6.QtCore import Qt
from app.services.auth_service import register_user, authenticate_user
import sqlite3

class LoginPage(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        
        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignCenter)
        
        self.stack = QStackedWidget()
        self.stack.setFixedWidth(450) # Centered box size
        
        self.page_signin = self.build_signin_page()
        self.page_signup = self.build_signup_page()
        
        self.stack.addWidget(self.page_signin)
        self.stack.addWidget(self.page_signup)
        
        root.addWidget(self.stack)

    def _create_form_container(self, title_text, subtitle_text):
        container = QFrame()
        container.setObjectName("Card")
        # Inline styling fallback, although dark.qss should take over
        layout = QVBoxLayout(container)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel(title_text)
        title.setObjectName("PageTitle")
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel(subtitle_text)
        subtitle.setObjectName("PageSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        return container, layout

    def build_signin_page(self):
        container, layout = self._create_form_container("Connexion", "Accède à ton espace de veille IA.")
        
        self.in_email = QLineEdit()
        self.in_email.setPlaceholderText("Email")
        self.in_password = QLineEdit()
        self.in_password.setPlaceholderText("Mot de passe")
        self.in_password.setEchoMode(QLineEdit.Password)
        
        self.lbl_err_in = QLabel("")
        self.lbl_err_in.setObjectName("ErrorLabel")
        self.lbl_err_in.setWordWrap(True)
        self.lbl_err_in.hide()
        
        btn_login = QPushButton("Se connecter")
        btn_login.setObjectName("PrimaryButton")
        btn_login.clicked.connect(self.handle_login)
        btn_login.setCursor(Qt.PointingHandCursor)
        
        btn_switch = QPushButton("Pas encore de compte ? S'inscrire")
        btn_switch.setObjectName("SecondaryButton")
        btn_switch.clicked.connect(lambda: self.switch_page(1))
        btn_switch.setCursor(Qt.PointingHandCursor)
        
        layout.addWidget(self.in_email)
        layout.addWidget(self.in_password)
        layout.addWidget(self.lbl_err_in)
        layout.addWidget(btn_login)
        layout.addWidget(btn_switch)
        
        return container

    def build_signup_page(self):
        container, layout = self._create_form_container("Créer un compte", "Rejoins l'application pour suivre ta veille.")
        
        self.up_email = QLineEdit()
        self.up_email.setPlaceholderText("Email")
        self.up_password = QLineEdit()
        self.up_password.setPlaceholderText("Mot de passe")
        self.up_password.setEchoMode(QLineEdit.Password)
        
        self.lbl_err_up = QLabel("")
        self.lbl_err_up.setObjectName("ErrorLabel")
        self.lbl_err_up.setWordWrap(True)
        self.lbl_err_up.hide()
        
        btn_register = QPushButton("Créer mon compte")
        btn_register.setObjectName("PrimaryButton")
        btn_register.clicked.connect(self.handle_register)
        btn_register.setCursor(Qt.PointingHandCursor)
        
        btn_switch = QPushButton("Déjà un compte ? Se connecter")
        btn_switch.setObjectName("SecondaryButton")
        btn_switch.clicked.connect(lambda: self.switch_page(0))
        btn_switch.setCursor(Qt.PointingHandCursor)
        
        layout.addWidget(self.up_email)
        layout.addWidget(self.up_password)
        layout.addWidget(self.lbl_err_up)
        layout.addWidget(btn_register)
        layout.addWidget(btn_switch)
        
        return container

    def switch_page(self, index):
        self.lbl_err_in.hide()
        self.lbl_err_up.hide()
        self.in_email.clear()
        self.in_password.clear()
        self.up_email.clear()
        self.up_password.clear()
        self.stack.setCurrentIndex(index)

    def handle_login(self):
        email = self.in_email.text().strip()
        pwd = self.in_password.text().strip()

        if not email or not pwd:
            self.lbl_err_in.setText("Email et mot de passe obligatoires.")
            self.lbl_err_in.setStyleSheet("color: #F44336;")
            self.lbl_err_in.show()
            return

        if authenticate_user(email, pwd):
            self.lbl_err_in.hide()
            self.in_password.clear() # clear pwd on success
            self.on_login_success(email)
        else:
            self.lbl_err_in.setText("Email ou mot de passe incorrect.")
            self.lbl_err_in.setStyleSheet("color: #F44336;")
            self.lbl_err_in.show()

    def handle_register(self):
        email = self.up_email.text().strip()
        pwd = self.up_password.text().strip()

        if not email or not pwd:
            self.lbl_err_up.setText("Email et mot de passe obligatoires.")
            self.lbl_err_up.setStyleSheet("color: #F44336;")
            self.lbl_err_up.show()
            return
            
        if len(pwd) < 6:
            self.lbl_err_up.setText("Le mot de passe doit faire au moins 6 caractères.")
            self.lbl_err_up.setStyleSheet("color: #F44336;")
            self.lbl_err_up.show()
            return

        try:
            register_user(email, pwd)
            self.lbl_err_up.hide()
            # auto-switch to login and pre-fill email
            self.switch_page(0)
            self.in_email.setText(email)
            self.lbl_err_in.setText("Compte créé avec succès ! Connecte-toi.")
            self.lbl_err_in.setStyleSheet("color: #4CAF50; font-weight: bold;") # Green success
            self.lbl_err_in.show()
        except sqlite3.IntegrityError:
            self.lbl_err_up.setText("Cet email existe déjà.")
            self.lbl_err_up.setStyleSheet("color: #F44336;")
            self.lbl_err_up.show()