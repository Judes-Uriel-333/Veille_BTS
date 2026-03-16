import os
from pathlib import Path
from dotenv import load_dotenv

class ThemeManager:
    def __init__(self):
        self.is_dark = True
        self.base_dir = Path(__file__).resolve().parents[1]  # app/
        self.styles_dir = self.base_dir / "ui" / "styles"

    def toggle(self):
        self.is_dark = not self.is_dark

    def current_qss(self) -> str:
        file_name = "dark.qss" if self.is_dark else "light.qss"
        path = self.styles_dir / file_name
        return path.read_text(encoding="utf-8")


load_dotenv(Path(__file__).resolve().parents[2] / ".env")

class AppConfig:
    @staticmethod
    def password_salt() -> str:
        # Mets une valeur dans .env : PASSWORD_SALT=...
        return os.getenv("PASSWORD_SALT", "dev_salt_change_me")