import pandas as pd
import numpy as np
import re
import pickle
from sklearn.ensemble import RandomForestClassifier

# ===== Model DoS/DDoS =====
df_freq = pd.read_csv("dataset_freq.csv")
X_freq = df_freq[['request_count', 'unique_ip_count', 'total_request_in_window']].values
y_freq = df_freq['label']

model_freq = RandomForestClassifier(n_estimators=100, random_state=42)
model_freq.fit(X_freq, y_freq)

with open("rf_model_freq.pkl", "wb") as f:
    pickle.dump(model_freq, f)

print("✅ Đã huấn luyện model DoS/DDoS.")

# ===== Model XSS/SQLi =====
df_payload = pd.read_csv("dataset_payload.csv")

def extract_payload_features(payload):
    length = len(payload)
    has_script = int(bool(re.search(r'script', payload, re.IGNORECASE)))
    has_sql = int(bool(re.search(r'select|union|--|insert|drop|or', payload, re.IGNORECASE)))
    has_special = int(bool(re.search(r"[<>'\"]", payload)))
    return [length, has_script, has_sql, has_special]

payload_features = df_payload['payload'].fillna('').apply(extract_payload_features)
payload_features = np.array(payload_features.tolist())
y_payload = df_payload['label']

model_payload = RandomForestClassifier(n_estimators=100, random_state=42)
model_payload.fit(payload_features, y_payload)

with open("rf_model_payload.pkl", "wb") as f:
    pickle.dump(model_payload, f)

print("✅ Đã huấn luyện model XSS/SQLi.")
