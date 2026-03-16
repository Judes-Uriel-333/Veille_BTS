from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow
from app.services.db import init_db

def main():
    init_db()
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
