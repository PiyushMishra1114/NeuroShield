import os
import pandas as pd
from feature_extractor import extract_features
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

def load_data_from_folder(folder_path, label):
    data = []
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if file_path.endswith(".exe"):
            features = extract_features(file_path)
            if features:
                features["Label"] = label
                features["Filename"] = file
                data.append(features)
    return data

def main():
    malware_path = os.path.join("dataset", "malware")
    benign_path = os.path.join("dataset", "benign")

    print("[INFO] Extracting features from malware samples...")
    malware_data = load_data_from_folder(malware_path, 1)

    print("[INFO] Extracting features from benign samples...")
    benign_data = load_data_from_folder(benign_path, 0)

    all_data = malware_data + benign_data
    df = pd.DataFrame(all_data).drop(columns=["Filename"])  # Keep clean data

    X = df.drop("Label", axis=1)
    y = df["Label"]

    print("[INFO] Training Random Forest Classifier...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print("\n[RESULT] Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    os.makedirs("model", exist_ok=True)
    joblib.dump(clf, "model/classifier.pkl")
    print("[INFO] Model saved to model/classifier.pkl")

if __name__ == "__main__":
    main()
