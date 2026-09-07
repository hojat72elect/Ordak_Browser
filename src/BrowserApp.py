from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QMainWindow, QToolBar, QLineEdit, QStatusBar, QProgressBar
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QAction

class BrowserApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ordak Browser")
        self.resize(1200, 800)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://hojat72elect.github.io/"))
        self.setCentralWidget(self.browser)

        # Main navigation bar of the browser
        navbar = QToolBar("Navigation")
        navbar.setMovable(False)
        self.addToolBar(navbar)

        self.backButton = QAction("◀", self)
        self.backButton.setStatusTip("Back to previous page")
        self.backButton.triggered.connect(self.browser.back)
        navbar.addAction(self.backButton)

        self.forwardButton = QAction("▶", self)
        self.forwardButton.setStatusTip("Forward to the next page")
        self.forwardButton.triggered.connect(self.browser.forward)
        navbar.addAction(self.forwardButton)

        reloadButton = QAction("🔄", self)
        reloadButton.setStatusTip("Reload page")
        reloadButton.triggered.connect(self.browser.reload)
        navbar.addAction(reloadButton)

        homeButton = QAction("🏠", self)
        homeButton.setStatusTip("Go to homepage")
        homeButton.triggered.connect(self.navigateHome)
        navbar.addAction(homeButton)

        navbar.addSeparator()

        self.urlBar = QLineEdit()
        self.urlBar.setPlaceholderText("Search or enter URL...")
        self.urlBar.returnPressed.connect(self.navigateToUrl)
        self.urlBar.setStyleSheet("""
        QLineEdit {
                padding: 6px 12px;
                border-radius: 15px;
                border: 1px solid #ccc;
                font-size: 14px;
                background-color: #f9f9f9;
            }
            QLineEdit:focus {
                border: 1px solid #0078d4;
                background-color: #ffffff;
            }
        """)
        navbar.addWidget(self.urlBar)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.progressBar = QProgressBar()
        self.progressBar.setMaximumWidth(120)
        self.progressBar.setMaximumHeight(12)
        self.progressBar.setTextVisible(False)
        self.status_bar.addPermanentWidget(self.progressBar)

        self.browser.urlChanged.connect(self.updateUrlBar)
        self.browser.loadProgress.connect(self.progressBar.setValue)
        self.browser.loadFinished.connect(self.onLoadFinished)

    def navigateHome(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigateToUrl(self):
        text = self.urlBar.text().strip()
        if not text:
            return

        if not text.startswith("http://") and not text.startswith("https://"):
            if "." in text and " " not in text:
                text = "https://" + text
            else:
                text = f"https://www.google.com/search?q={text}"

        self.browser.setUrl(QUrl(text))

    def updateUrlBar(self, qurl):
        self.urlBar.setText(qurl.toString())
        self.urlBar.setCursorPosition(0)

    def onLoadFinished(self):
        self.progressBar.setValue(0)
        self.setWindowTitle(f"{self.browser.page().title()} — Ordak Browser")
