from BrowserApp import BrowserApp
import sys
from PyQt6.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Ordak Browser")
    window = BrowserApp()
    window.show()
    sys.exit(app.exec())
