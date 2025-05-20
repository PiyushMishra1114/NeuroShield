from plyer import notification
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
import sys
from src.remover import delete_file

def show_notification(title, message, file_path):
    # System Tray Notification (quick alert)
    notification.notify(
        title=title,
        message=message,
        timeout=5,
        app_icon=None  # Optionally set to 'icon.ico'
    )

    # GUI Popup with delete option
    app = QApplication(sys.argv)
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("Malware Alert")
    msg.setText("Malware Detected!")
    msg.setInformativeText(f"File: {file_path}")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.button(QMessageBox.Ok).setText("Delete File")
    msg.button(QMessageBox.Cancel).setText("Ignore")

    result = msg.exec_()
    if result == QMessageBox.Ok:
        delete_file(file_path)
    sys.exit(app.exec_())
