import pandas as pd
import numpy as np
import pickle
import re
from sklearn.ensemble import RandomForestClassifier

# Đọc dữ liệu
df = pd.read_csv('dataset.csv')

# Tạo feature payload
def extract_payload_features(payload):
    length = len(payload)
    has_script = int(bool(re.search(r'script', payload, re.IGNORECASE)))
    has_sql = int(bool(re.search(r'select|union|--|insert|drop', payload, re.IGNORECASE)))
    has_special = int(bool(re.search(r"[<>'\"]", payload)))
    return [length, has_script, has_sql, has_special]

# Tạo feature từ payload
payload_features = df['payload'].fillna('').apply(extract_payload_features)
payload_features = np.array(payload_features.tolist())

# Feature gốc
X_base = df[['request_count', 'unique_ip_count', 'total_request_in_window']].values

# Nối feature payload
X = np.hstack((X_base, payload_features))

y = df['label']

# Huấn luyện
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Lưu model
with open('rf_model_full.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Đã huấn luyện và lưu model.")
