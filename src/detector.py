import time
import joblib
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from feature_extractor import extract_features
from notifier import show_notification

MODEL_PATH = "model/classifier.pkl"
WATCH_DIR = "C:/Users/Public"  # Change to directory you want to monitor

class MalwareMonitor(FileSystemEventHandler):
    def __init__(self, model):
        self.model = model

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".exe"):
            print(f"[INFO] New file detected: {event.src_path}")
            features = extract_features(event.src_path)
            if features:
                X = [list(features.values())]
                prediction = self.model.predict(X)[0]

                if prediction == 1:
                    print(f"[ALERT] Malware Detected: {event.src_path}")
                    show_notification("Malware Detected!", f"{event.src_path}", event.src_path)
                else:
                    print(f"[SAFE] File is clean: {event.src_path}")

def start_monitoring():
    print("[INFO] Loading model...")
    model = joblib.load(MODEL_PATH)

    print(f"[INFO] Starting folder monitor: {WATCH_DIR}")
    event_handler = MalwareMonitor(model)
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
