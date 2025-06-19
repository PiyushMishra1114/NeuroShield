from plyer import notification
import os
from src.remover import delete_file

def show_notification(title, message, file_path):
    # ✅ Native System Notification
    try:
        notification.notify(
            title=title,
            message=message,
            timeout=10,
            app_icon=None  # You can use 'assets/icon.ico' here if available
        )
        print("[INFO] System notification sent.")
    except Exception as e:
        print(f"[ERROR] Notification failed: {e}")

    # ✅ Terminal prompt (use only if running from terminal)
    print("\n\033[93mMalware Detected!\033[0m")
    print(f"File: {file_path}")
    try:
        # Only prompt if running interactively
        if os.isatty(0):  # stdin is a terminal
            user_input = input("Do you want to delete the file? (y/n): ").strip().lower()
            if user_input == 'y':
                delete_file(file_path)
            else:
                print("File not deleted.")
        else:
            print("[INFO] Skipping delete prompt (not in terminal mode).")
    except Exception as e:
        print(f"[WARNING] Delete confirmation error: {e}")
