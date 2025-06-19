from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QMessageBox, QGraphicsDropShadowEffect, QTextEdit, QHBoxLayout
)
from PyQt5.QtGui import QFont, QColor, QIcon, QMovie
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from src.detector import start_monitoring, scan_file
import threading

class RealTimeThread(QThread):
    log_signal = pyqtSignal(str)

    def run(self):
        def logger(msg):
            self.log_signal.emit(msg)
        start_monitoring(log_callback=logger)

class MalwareDetectorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NeuroShield - Your Security Companion")
        self.setGeometry(100, 100, 720, 500)
        self.setStyleSheet("background-color: #0d1117; color: #ffffff;")
        self.setWindowIcon(QIcon("assets/icon.png"))

        layout = QVBoxLayout()

        self.label = QLabel("🔐 NeuroShield")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Consolas", 26, QFont.Bold))
        self.label.setStyleSheet("color: #58a6ff;")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor("#58a6ff"))
        shadow.setOffset(0, 0)
        self.label.setGraphicsEffect(shadow)
        layout.addWidget(self.label)

        self.subtitle = QLabel("Real-Time ML-Powered Malware Detection")
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setFont(QFont("Consolas", 13))
        self.subtitle.setStyleSheet("color: #8b949e;")
        layout.addWidget(self.subtitle)

        self.browse_button = QPushButton("🗂️ Select File to Scan")
        self.browse_button.setStyleSheet(self.button_style())
        self.browse_button.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_button)

        self.toggle_button = QPushButton("▶️ Enable Real-Time Detection")
        self.toggle_button.setStyleSheet(self.button_style())
        self.toggle_button.setCheckable(True)
        self.toggle_button.toggled.connect(self.toggle_realtime)
        layout.addWidget(self.toggle_button)

        self.realtime_label = QLabel("")
        self.realtime_label.setAlignment(Qt.AlignCenter)
        self.realtime_label.setFont(QFont("Consolas", 12))
        layout.addWidget(self.realtime_label)

        self.loading_gif = QLabel()
        self.loading_movie = QMovie("assets/loading.gif")
        self.loading_gif.setMovie(self.loading_movie)
        self.loading_gif.setAlignment(Qt.AlignCenter)
        self.loading_gif.setVisible(False)
        layout.addWidget(self.loading_gif)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("background-color: #161b22; color: #c9d1d9; border: 1px solid #30363d; padding: 6px;")
        layout.addWidget(self.log_output)

        self.setLayout(layout)

        self.realtime_thread = None

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select EXE File", "", "Executables (*.exe);;All Files (*)")
        if file_path:
            result = scan_file(file_path)
            QMessageBox.information(self, "Scan Result", f"Result:\n{result}")

    def toggle_realtime(self, checked):
        if checked:
            self.toggle_button.setText("⏸️ Disable Real-Time Detection")
            self.realtime_label.setText("🔄 Real-Time Detection Enabled...")
            self.loading_gif.setVisible(True)
            self.loading_movie.start()

            self.realtime_thread = RealTimeThread()
            self.realtime_thread.log_signal.connect(self.append_log)
            self.realtime_thread.start()
        else:
            self.toggle_button.setText("▶️ Enable Real-Time Detection")
            self.realtime_label.setText("")
            self.loading_gif.setVisible(False)
            self.loading_movie.stop()

            if self.realtime_thread:
                self.realtime_thread.terminate()
                self.realtime_thread.wait()

    def append_log(self, message):
        self.log_output.append(message)

    def button_style(self):
        return (
            "QPushButton {"
            "background-color: #21262d;"
            "padding: 14px;"
            "font-size: 14px;"
            "color: #c9d1d9;"
            "border: 2px solid #30363d;"
            "border-radius: 10px;"
            "}"
            "QPushButton:hover {"
            "background-color: #238636;"
            "color: white;"
            "}"
        )

def run_ui():
    app = QApplication([])
    window = MalwareDetectorUI()
    window.show()
    app.exec_()