import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from src.detector import start_monitoring

class DetectorThread(QThread):
    update_signal = pyqtSignal(str)

    def run(self):
        start_monitoring()  # Runs infinite monitoring loop

class MalwareUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-Time Malware Detector")
        self.setGeometry(300, 100, 700, 500)

        self.set_dark_theme()
        self.init_ui()

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(20, 20, 20))
        palette.setColor(QPalette.AlternateBase, QColor(40, 40, 40))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(45, 45, 45))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        self.setPalette(palette)

    def init_ui(self):
        self.label = QLabel("🛡️ Real-Time Malware Protection", self)
        self.label.setFont(QFont("Arial", 18))
        self.label.setAlignment(Qt.AlignCenter)

        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)
        self.log_output.setFont(QFont("Courier", 10))

        self.start_btn = QPushButton("▶ Start Monitoring", self)
        self.start_btn.setFont(QFont("Arial", 12))
        self.start_btn.clicked.connect(self.start_monitoring_thread)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.log_output)
        layout.addWidget(self.start_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_monitoring_thread(self):
        self.log_output.append("[INFO] Monitoring started...\n")
        self.thread = DetectorThread()
        self.thread.update_signal.connect(self.update_log)
        self.thread.start()

    def update_log(self, msg):
        self.log_output.append(msg)

def run_ui():
    app = QApplication(sys.argv)
    window = MalwareUI()
    window.show()
    sys.exit(app.exec_())
