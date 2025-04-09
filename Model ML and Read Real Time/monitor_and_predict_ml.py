import os
import time
import re
import pandas as pd
from datetime import datetime
from collections import defaultdict, deque
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

# ==== CẤU HÌNH ====
LOG_FILE = "/var/log/user_data.log"
DATASET_FILE = "/home/tienpro/Documents/dataset.csv"
MODEL_FILE = "rf_model.pkl"
THRESHOLD_TIME = 60  # Giây để tính số lần truy cập
FEATURES = ["request_count"]  # Có thể mở rộng sau

# ==== HỌC MÁY: HUẤN LUYỆN ====
def train_model_if_needed():
    if not os.path.exists(MODEL_FILE):
        print("📚 Huấn luyện mô hình RandomForest từ dataset.csv...")
        df = pd.read_csv(DATASET_FILE)

        X = df[FEATURES]
        y = df["label"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        with open(MODEL_FILE, "wb") as f:
            pickle.dump(model, f)

        print("✅ Huấn luyện xong và lưu vào rf_model.pkl\n")
    else:
        print("✅ Đã có mô hình rf_model.pkl. Bỏ qua bước huấn luyện.\n")

# ==== LOAD MÔ HÌNH ====
def load_model():
    with open(MODEL_FILE, "rb") as f:
        return pickle.load(f)

# ==== PHÂN TÍCH DÒNG LOG ====
def parse_log_line(line):
    ip_match = re.search(r'IP: ([\d\.]+)', line)
    time_match = re.search(r'Thời gian: ([\d\-: ]+)', line)

    if ip_match and time_match:
        ip = ip_match.group(1)
        timestamp = datetime.strptime(time_match.group(1), "%Y-%m-%d %H:%M:%S")
        return ip, timestamp
    return None, None

# ==== GIÁM SÁT LOG + DỰ ĐOÁN ====
def monitor_and_predict(model):
    print("🔍 Bắt đầu giám sát log và dự đoán tấn công real-time...\n")
    ip_logs = defaultdict(deque)

    with open(LOG_FILE, 'r') as f:
        f.seek(0, 2)

        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue

            ip, timestamp = parse_log_line(line)
            if not ip:
                continue

            dq = ip_logs[ip]
            dq.append(timestamp)

            # Xoá truy cập quá cũ khỏi deque
            while dq and (timestamp - dq[0]).total_seconds() > THRESHOLD_TIME:
                dq.popleft()

            request_count = len(dq)
            X_new = pd.DataFrame([[request_count]], columns=FEATURES)
            prediction = model.predict(X_new)[0]

            if prediction == 1:
                print(f"🚨 TẤN CÔNG: IP {ip} ({request_count} lần/{THRESHOLD_TIME}s)")
            else:
                print(f"✅ Bình thường: IP {ip} ({request_count} lần)")

# ==== CHẠY CHƯƠNG TRÌNH ====
if __name__ == "__main__":
    train_model_if_needed()
    model = load_model()
    monitor_and_predict(model)

