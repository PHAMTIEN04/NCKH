import pandas as pd
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from collections import defaultdict
from datetime import datetime

# File cấu hình
LOG_FILE = '/var/log/user_data.log'
DATASET_FILE = 'dataset.csv'
MODEL_FILE = 'rf_model.pkl'
THRESHOLD_TIME = 60  # giây

# Hàm parse timestamp
def parse_time(t):
    return datetime.strptime(t, '%Y-%m-%d %H:%M:%S')

# Huấn luyện hoặc load mô hình
if os.path.exists(MODEL_FILE):
    with open(MODEL_FILE, 'rb') as f:
        model = pickle.load(f)
    print("✅ Mô hình đã được load từ file.")
else:
    print("⚙️ Huấn luyện mô hình mới...")
    df = pd.read_csv(DATASET_FILE)
    X = df[['request_count', 'unique_ip_count', 'total_request_in_window']]
    y = df['label']
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(model, f)
    print("✅ Huấn luyện xong và lưu mô hình.")

# Đếm request và IP
ip_counter = defaultdict(list)

# Mở log realtime
with open(LOG_FILE) as f:
    f.seek(0, 2)
    while True:
        line = f.readline()
        if not line:
            continue
        parts = line.strip().split(';')
        ip = ""
        time_str = ""
        for part in parts:
            if part.strip().startswith("IP:"):
                ip = part.split("IP:")[1].strip()
            elif part.strip().startswith("Thời gian:"):
                time_str = part.split("Thời gian:")[1].strip()
        if not ip or not time_str:
            continue

        now = parse_time(time_str)

        # Lưu lịch sử
        ip_counter[ip].append(now)

        # Lọc chỉ lấy trong THRESHOLD_TIME giây
        for k in list(ip_counter.keys()):
            ip_counter[k] = [t for t in ip_counter[k] if (now - t).total_seconds() <= THRESHOLD_TIME]
            if not ip_counter[k]:
                del ip_counter[k]

        request_count = len(ip_counter[ip])
        unique_ip_count = len(ip_counter)
        total_request_in_window = sum(len(v) for v in ip_counter.values())

        # Tạo feature
        feature = np.array([[request_count, unique_ip_count, total_request_in_window]])
        prediction = model.predict(feature)[0]

        if prediction == 0:
            status = "✅ Bình thường"
        elif prediction == 1:
            status = "🚨 DoS"
        else:
            status = "⚠️ DDoS"

        print(f"IP: {ip} | Request: {request_count} | Unique IP: {unique_ip_count} | Total: {total_request_in_window} --> {status}")
