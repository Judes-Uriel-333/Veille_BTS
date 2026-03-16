from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor
import webbrowser

class ArticleCard(QFrame):
    def __init__(self, article_data):
        super().__init__()
        # FIX (Audit) : On convertit la ligne sqlite3.Row en dict standard
        # pour éviter l'erreur TypeError sur la méthode .get()
        self.article = dict(article_data) if article_data else {}
        
        self.setObjectName("ArticleCard")
        
        # Adding a layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 1. Image placeholder / colored top banner to simulate image presence
        image_banner = QLabel()
        image_banner.setFixedHeight(140)
        image_banner.setStyleSheet("background-color: #3f51b5; border-top-left-radius: 8px; border-top-right-radius: 8px;")
        
        # 2. Content container
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(16, 12, 16, 16)
        content_layout.setSpacing(8)
        
        # Source & Date
        meta_layout = QHBoxLayout()
        source_lbl = QLabel(self.article.get("source", "Source inconnue"))
        source_lbl.setStyleSheet("color: #d32f2f; font-weight: bold; font-size: 11px;")
        
        date_str = self.article.get("published", "")
        # truncate date string if too long
        if len(date_str) > 20: date_str = date_str[:16]
        date_lbl = QLabel(date_str)
        date_lbl.setStyleSheet("color: palette(text); font-size: 11px; opacity: 0.6;")
        
        meta_layout.addWidget(source_lbl)
        meta_layout.addStretch()
        meta_layout.addWidget(date_lbl)
        
        # Title
        title_text = self.article.get("title", "")
        title_lbl = QLabel(title_text)
        title_font = QFont()
        title_font.setPointSize(13)
        title_font.setBold(True)
        title_lbl.setFont(title_font)
        title_lbl.setWordWrap(True)
        title_lbl.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        # Bottom Actions
        actions_layout = QHBoxLayout()
        actions_layout.addStretch()
        btn_open = QPushButton("Lire l'article ↗")
        btn_open.setCursor(Qt.PointingHandCursor)
        btn_open.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #1976D2;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                text-decoration: underline;
                color: #1565C0;
            }
        """)
        btn_open.clicked.connect(self.open_link)
        actions_layout.addWidget(btn_open)
        
        content_layout.addLayout(meta_layout)
        content_layout.addWidget(title_lbl)
        content_layout.addStretch() # Push actions to bottom
        content_layout.addLayout(actions_layout)
        
        layout.addWidget(image_banner)
        layout.addWidget(content)
        
        # Apply Card Stylesheet adaptable to light/dark
        self.setStyleSheet("""
            QFrame#ArticleCard {
                border-radius: 8px;
                border: 1px solid palette(mid);
                background-color: palette(base);
            }
            QFrame#ArticleCard:hover {
                border: 1px solid palette(highlight);
            }
        """)
        
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.open_link()
            
    def open_link(self):
        link = self.article.get("link")
        if link:
            webbrowser.open(link)
