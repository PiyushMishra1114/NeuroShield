from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QMessageBox, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QColor, QIcon
from PyQt5.QtCore import Qt
from src.detector import start_monitoring

class MalwareDetectorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NeuroShield - AI Malware Detector")
        self.setGeometry(100, 100, 650, 350)
        self.setStyleSheet("background-color: #0d1117; color: #ffffff;")
        self.setWindowIcon(QIcon("assets/icon.png"))  # Optional icon

        layout = QVBoxLayout()

        self.label = QLabel("🔐 NeuroShield")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Consolas", 22, QFont.Bold))
        self.label.setStyleSheet("color: #58a6ff;")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor("#58a6ff"))
        shadow.setOffset(0, 0)
        self.label.setGraphicsEffect(shadow)
        layout.addWidget(self.label)

        self.subtitle = QLabel("Real-time AI-Powered Malware Detection")
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setFont(QFont("Consolas", 12))
        self.subtitle.setStyleSheet("color: #8b949e;")
        layout.addWidget(self.subtitle)

        self.browse_button = QPushButton("🗂️ Select File to Scan")
        self.browse_button.setStyleSheet(
            "QPushButton {"
            "background-color: #21262d;"
            "padding: 14px;"
            "font-size: 14px;"
            "color: #c9d1d9;"
            "border: 2px solid #30363d;"
            "border-radius: 8px;"
            "}"
            "QPushButton:hover {"
            "background-color: #238636;"
            "color: white;"
            "}"
        )
        self.browse_button.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_button)

        self.setLayout(layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select EXE File", "", "Executables (*.exe);;All Files (*)")
        if file_path:
            from src.detector import scan_file  # new function
            result = scan_file(file_path)
            QMessageBox.information(self, "Scan Result", f"Result:\n{result}")

def run_ui():
    app = QApplication([])
    window = MalwareDetectorUI()
    window.show()
    app.exec_()
