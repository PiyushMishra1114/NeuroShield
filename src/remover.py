import os

def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"[DELETED] File removed: {file_path}")
        else:
            print(f"[ERROR] File not found: {file_path}")
    except PermissionError:
        print(f"[ERROR] Permission denied to delete: {file_path}")
    except Exception as e:
        print(f"[ERROR] Could not delete {file_path}: {e}")


# If a file can't be deleted due to admin rights :
# import subprocess
# subprocess.run(["powershell", "Remove-Item", file_path, "-Force"])
