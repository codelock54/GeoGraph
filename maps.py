import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Google Maps en PyQt6")
        self.setGeometry(100, 100, 800, 600)

        # Crea el widget QWebEngineView
        self.browser = QWebEngineView()
        # Carga la página de Google Maps
        self.browser.setUrl(QUrl("https://www.google.com/maps"))

        # Configura el diseño
        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
