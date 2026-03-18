from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                               QLineEdit, QPushButton, QFrame, QStackedWidget,
                               QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from app.services.auth_service import register_user, authenticate_user
import sqlite3


class LoginPage(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success

        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignCenter)
        root.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget()
        self.stack.setFixedWidth(460)

        self.page_signin = self._build_signin()
        self.page_signup = self._build_signup()

        self.stack.addWidget(self.page_signin)
        self.stack.addWidget(self.page_signup)

        root.addWidget(self.stack, alignment=Qt.AlignCenter)

    # ------------------------------------------------------------------
    # Construction des pages
    # ------------------------------------------------------------------

    def _build_signin(self):
        container, layout = self._card("Connexion", "Connecte-toi a ton espace de veille IA")

        self.in_email = self._input("Adresse email")
        self.in_password = self._input("Mot de passe", password=True)

        self.lbl_err_in = QLabel("")
        self.lbl_err_in.setObjectName("ErrorLabel")
        self.lbl_err_in.setWordWrap(True)
        self.lbl_err_in.setAlignment(Qt.AlignCenter)
        self.lbl_err_in.hide()

        btn_login = QPushButton("Se connecter")
        btn_login.setObjectName("PrimaryButton")
        btn_login.setMinimumHeight(44)
        btn_login.setCursor(Qt.PointingHandCursor)
        btn_login.clicked.connect(self.handle_login)

        btn_switch = QPushButton("Pas encore de compte ? S'inscrire")
        btn_switch.setObjectName("SecondaryButton")
        btn_switch.setMinimumHeight(44)
        btn_switch.setCursor(Qt.PointingHandCursor)
        btn_switch.clicked.connect(lambda: self._switch(1))

        layout.addWidget(self.in_email)
        layout.addWidget(self.in_password)
        layout.addWidget(self.lbl_err_in)
        layout.addSpacing(4)
        layout.addWidget(btn_login)
        layout.addWidget(btn_switch)

        return container

    def _build_signup(self):
        container, layout = self._card("Creer un compte", "Rejoins l'application et commence ta veille")

        self.up_email = self._input("Adresse email")
        self.up_password = self._input("Mot de passe (min. 6 caracteres)", password=True)

        self.lbl_err_up = QLabel("")
        self.lbl_err_up.setObjectName("ErrorLabel")
        self.lbl_err_up.setWordWrap(True)
        self.lbl_err_up.setAlignment(Qt.AlignCenter)
        self.lbl_err_up.hide()

        btn_register = QPushButton("Creer mon compte")
        btn_register.setObjectName("PrimaryButton")
        btn_register.setMinimumHeight(44)
        btn_register.setCursor(Qt.PointingHandCursor)
        btn_register.clicked.connect(self.handle_register)

        btn_switch = QPushButton("Deja un compte ? Se connecter")
        btn_switch.setObjectName("SecondaryButton")
        btn_switch.setMinimumHeight(44)
        btn_switch.setCursor(Qt.PointingHandCursor)
        btn_switch.clicked.connect(lambda: self._switch(0))

        layout.addWidget(self.up_email)
        layout.addWidget(self.up_password)
        layout.addWidget(self.lbl_err_up)
        layout.addSpacing(4)
        layout.addWidget(btn_register)
        layout.addWidget(btn_switch)

        return container

    # ------------------------------------------------------------------
    # Helpers visuels
    # ------------------------------------------------------------------

    def _card(self, title_text, subtitle_text):
        """Cree une carte de formulaire avec titre + sous-titre + ombre portee."""
        container = QFrame()
        container.setObjectName("Card")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 25))
        container.setGraphicsEffect(shadow)

        layout = QVBoxLayout(container)
        layout.setSpacing(16)
        layout.setContentsMargins(36, 40, 36, 36)

        title = QLabel(title_text)
        title.setObjectName("PageTitle")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel(subtitle_text)
        subtitle.setObjectName("PageSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(8)

        return container, layout

    def _input(self, placeholder, password=False):
        """Cree un QLineEdit style premium."""
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setMinimumHeight(44)
        if password:
            field.setEchoMode(QLineEdit.Password)
        return field

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def _switch(self, index):
        self.lbl_err_in.hide()
        self.lbl_err_up.hide()
        self.in_email.clear()
        self.in_password.clear()
        self.up_email.clear()
        self.up_password.clear()
        self.stack.setCurrentIndex(index)
        if index == 0:
            self.in_email.setFocus()
        else:
            self.up_email.setFocus()

    # ------------------------------------------------------------------
    # Logique metier
    # ------------------------------------------------------------------

    def handle_login(self):
        email = self.in_email.text().strip()
        pwd = self.in_password.text().strip()

        if not email or not pwd:
            self._show_error(self.lbl_err_in, "Email et mot de passe obligatoires.")
            return

        if authenticate_user(email, pwd):
            self.lbl_err_in.hide()
            self.in_password.clear()
            self.on_login_success(email)
        else:
            self._show_error(self.lbl_err_in, "Email ou mot de passe incorrect.")

    def handle_register(self):
        email = self.up_email.text().strip()
        pwd = self.up_password.text().strip()

        if not email or not pwd:
            self._show_error(self.lbl_err_up, "Email et mot de passe obligatoires.")
            return

        if len(pwd) < 6:
            self._show_error(self.lbl_err_up, "Le mot de passe doit faire au moins 6 caracteres.")
            return

        try:
            register_user(email, pwd)
            self.lbl_err_up.hide()
            self._switch(0)
            self.in_email.setText(email)
            self._show_success(self.lbl_err_in, "Compte cree ! Connecte-toi maintenant.")
        except sqlite3.IntegrityError:
            self._show_error(self.lbl_err_up, "Cet email existe deja.")

    # ------------------------------------------------------------------
    # Affichage messages
    # ------------------------------------------------------------------

    def _show_error(self, label, message):
        label.setText(message)
        label.setObjectName("ErrorLabel")
        label.style().unpolish(label)
        label.style().polish(label)
        label.show()

    def _show_success(self, label, message):
        label.setText(message)
        label.setObjectName("SuccessLabel")
        label.style().unpolish(label)
        label.style().polish(label)
        label.show()