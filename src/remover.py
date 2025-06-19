import os
import subprocess
import psutil
import time

def delete_file(file_path):
    try:
        # Step 1: Kill any process using the file
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                if proc.info['exe'] and os.path.samefile(proc.info['exe'], file_path):
                    print(f"[INFO] Killing process: {proc.info['name']} (PID: {proc.info['pid']})")
                    proc.kill()
                    proc.wait(timeout=3)  # wait to release lock
            except (psutil.NoSuchProcess, psutil.AccessDenied, FileNotFoundError):
                continue

        time.sleep(1)  # short delay to ensure process lock is cleared

        # Step 2: Try normal deletion
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"[DELETED] File removed: {file_path}")
            except PermissionError:
                print(f"[WARN] Permission denied using os.remove(), retrying with PowerShell...")
                subprocess.run(
                    ["powershell", "-Command", f"Remove-Item -Path '{file_path}' -Force"],
                    check=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                print(f"[DELETED] File removed using PowerShell: {file_path}")
        else:
            print(f"[ERROR] File not found: {file_path}")
    except Exception as e:
        print(f"[ERROR] Could not delete {file_path}: {e}")
