from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QScrollArea, QGridLayout, QMessageBox, QFrame)
from PySide6.QtCore import Qt, QThread, Signal
from app.services.rss_service import fetch_and_store_articles, get_articles
from app.ui.widgets.article_card import ArticleCard


class RssWorker(QThread):
    """
    Worker pour exécuter la récupération RSS en arrière-plan sans bloquer l'UI.
    C'est une excellente pratique technique (BTS SIO) de séparer les tâches lourdes du thread principal.
    """
    finished = Signal()
    error = Signal(str)

    def run(self):
        try:
            fetch_and_store_articles()
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))


class DashboardPage(QWidget):
    def __init__(self, on_logout):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header Row
        header_layout = QHBoxLayout()
        header_text_layout = QVBoxLayout()
        title = QLabel("Dashboard Veille")
        title.setObjectName("PageTitle")
        
        subtitle = QLabel("Tes articles personnalisés, issus des meilleurs flux RSS.")
        subtitle.setObjectName("PageSubtitle")
        subtitle.setStyleSheet("color: palette(text); font-size: 14px; opacity: 0.8;") 
        
        header_text_layout.addWidget(title)
        header_text_layout.addWidget(subtitle)
        
        # Buttons Row
        self.btn_refresh = QPushButton(" 🔄 Actualiser les articles")
        self.btn_refresh.setObjectName("PrimaryButton")
        self.btn_refresh.setCursor(Qt.PointingHandCursor)
        self.btn_refresh.clicked.connect(self.load_articles)
        
        btn_logout = QPushButton("Déconnexion")
        btn_logout.setObjectName("SecondaryButton")
        btn_logout.setCursor(Qt.PointingHandCursor)
        btn_logout.clicked.connect(on_logout)
        
        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.btn_refresh)
        buttons_layout.addWidget(btn_logout)
        
        header_layout.addLayout(header_text_layout)
        header_layout.addStretch()
        header_layout.addLayout(buttons_layout)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: palette(mid);")

        # --- Grid Area for Cards ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)
        self.scroll_area.setStyleSheet("background: transparent;")
        
        self.grid_container = QWidget()
        self.grid_container.setStyleSheet("background: transparent;")
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(20)
        self.grid_layout.setAlignment(Qt.AlignTop)
        
        self.scroll_area.setWidget(self.grid_container)

        layout.addLayout(header_layout)
        layout.addWidget(line)
        layout.addWidget(self.scroll_area)

        # Reference to avoid garbage collection of the thread
        self.worker = None

    def load_articles(self):
        # UI state: loading
        self.btn_refresh.setText("⏳ Chargement...")
        self.btn_refresh.setEnabled(False)
        
        # Lancement de la tâche réseau dans un thread séparé
        self.worker = RssWorker()
        self.worker.finished.connect(self.on_rss_success)
        self.worker.error.connect(self.on_rss_error)
        self.worker.start()
        
    def on_rss_success(self):
        self.display_grid()
        self.reset_button()

    def on_rss_error(self, error_msg):
        QMessageBox.warning(self, "Erreur Réseau", f"Impossible de récupérer les flux RSS.\n{error_msg}")
        # On affiche quand même la grille (potentiellement avec les articles du cache SQLite)
        self.display_grid()
        self.reset_button()
        
    def reset_button(self):
        self.btn_refresh.setText(" 🔄 Actualiser les articles")
        self.btn_refresh.setEnabled(True)
        
    def display_grid(self):
        # Clear existing layout
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        articles = get_articles()
        
        if not articles:
            empty_lbl = QLabel("Aucun article trouvé dans ton flux. Clique sur Actualiser.")
            empty_lbl.setAlignment(Qt.AlignCenter)
            empty_lbl.setStyleSheet("font-size: 16px; color: gray; margin-top: 50px;")
            self.grid_layout.addWidget(empty_lbl, 0, 0)
            return

        cols = 2 # Fixed 2 columns grid
        row = 0
        col = 0
        
        for article in articles:
            try:
                card = ArticleCard(article)
                card.setMinimumHeight(280)
                self.grid_layout.addWidget(card, row, col)
                
                col += 1
                if col >= cols:
                    col = 0
                    row += 1
            except Exception as e:
                # Protection minimale : un article corrompu n'empêche pas l'affichage des autres
                print(f"Erreur lors du rendu d'une carte ignorée : {e}")