import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow
from app.services.db import init_db

def test_app():
    print("TEST STARTING")
    init_db()
    # Need to pass an empty list if using instance, or create
    app = QApplication.instance() or QApplication(sys.argv)
    window = MainWindow()
    
    print("TEST: Window created")
    assert window.stack.currentWidget() == window.page_login, "Should start on Login"
    
    # Simulate empty login
    window.page_login.btn_login.click()
    assert window.page_login.lbl_error.text() == "Email et mot de passe obligatoires.", "Empty login validation failed"
    print("TEST: Empty login validation OK")
    
    # Simulate register
    window.page_login.input_email.setText("bts@test.com")
    window.page_login.input_password.setText("sio2024")
    window.page_login.btn_register.click()
    print("TEST: Register response:", window.page_login.lbl_error.text())
    
    # Simulate login
    window.page_login.btn_login.click()
    assert window.stack.currentWidget() == window.page_dashboard, "Login failed, not on dashboard"
    print("TEST: Login successful, on dashboard")
    
    # Simulate refresh articles
    window.page_dashboard.btn_refresh.click()
    count = window.page_dashboard.list_articles.count()
    print(f"TEST: Found {count} articles after refresh")
    
    # Check open_article bug
    print("TEST: Note - no double click connection found for list_articles.")
    
    print("ALL TESTS PASSED")

if __name__ == "__main__":
    test_app()
