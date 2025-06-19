import time
import joblib
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.feature_extractor import extract_features
from src.notifier import show_notification

MODEL_PATH = "model/classifier.pkl"
WATCH_DIR = "C:/Users/Public"  # Change to directory you want to monitor

# ✅ Load the model once at the top
model = joblib.load(MODEL_PATH)

class MalwareMonitor(FileSystemEventHandler):
    def __init__(self, model, log_callback=None):
        self.model = model
        self.log_callback = log_callback

    def log(self, message):
        print(message)
        if self.log_callback:
            self.log_callback(message)

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".exe"):
            self.log(f"[INFO] New file detected: {event.src_path}")
            try:
                features = extract_features(event.src_path)
                if features:
                    X = [list(features.values())]
                    prediction = self.model.predict(X)[0]

                    if prediction == 1:
                        self.log(f"[ALERT] Malware Detected: {event.src_path}")
                        show_notification("Malware Detected!", f"{event.src_path}", event.src_path)
                    else:
                        self.log(f"[SAFE] File is clean: {event.src_path}")
                else:
                    self.log(f"[ERROR] Could not extract features from: {event.src_path}")
            except Exception as e:
                self.log(f"[ERROR] Failed to process {event.src_path}: {e}")

# ✅ Use the global model here
def scan_file(file_path):
    print(f"[INFO] Scanning file: {file_path}")
    features = extract_features(file_path)
    if not features:
        print(f"[RESULT] {file_path} → {'🛑 Malware' if prediction[0] == 1 else '✅ Safe'}")
        # return "❌ Failed to extract features"

    X = [list(features.values())]
    prediction = model.predict(X)
    return "🛑 Malware Detected!" if prediction[0] == 1 else "✅ File is Safe"

# Folder monitoring for automatic detection
def start_monitoring(log_callback=None):
    print("[INFO] Starting folder monitor:", WATCH_DIR)
    event_handler = MalwareMonitor(model, log_callback)
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
