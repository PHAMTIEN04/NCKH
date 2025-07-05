import pandas as pd
import numpy as np
import pickle
import re
from datetime import datetime
from collections import defaultdict

LOG_FILE = '/var/log/user_data.log'
MODEL_FILE = 'rf_model_full.pkl'
THRESHOLD_TIME = 60

with open(MODEL_FILE, 'rb') as f:
    model = pickle.load(f)

def parse_time(t):
    try:
        return datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None

def extract_payload_features(payload):
    length = len(payload)
    has_script = int(bool(re.search(r'script', payload, re.IGNORECASE)))
    has_sql = int(bool(re.search(r'select|union|--|insert|drop', payload, re.IGNORECASE)))
    has_special = int(bool(re.search(r"[<>'\"]", payload)))
    return [length, has_script, has_sql, has_special]

ip_counter = defaultdict(list)
list_attack= []
check_ip=0
with open(LOG_FILE, encoding='utf-8', errors='replace') as f:
    f.seek(0, 2)
    while True:
        line = f.readline()
        if not line:
            continue
        parts = line.strip().split(';')
        ip = ""
        time_str = ""
        payload = ""
        for part in parts:
            if part.strip().startswith("IP:"):
                ip = part.split("IP:")[1].strip()
            elif part.strip().startswith("Thời gian:"):
                time_str = part.split("Thời gian:")[1].strip()
            elif part.strip().startswith("Dữ liệu:"):
                payload = part.split("Dữ liệu:")[1].strip()
        if not ip or not time_str:
            continue
        if check_ip != ip:
            check_ip = ip
            list_attack=[]
        now = parse_time(time_str)
        if not now:
            print("Bỏ qua dòng không hợp lệ:", time_str)
            continue

        ip_counter[ip].append(now)

        for k in list(ip_counter.keys()):
            ip_counter[k] = [t for t in ip_counter[k] if (now - t).total_seconds() <= THRESHOLD_TIME]
            if not ip_counter[k]:
                del ip_counter[k]

        request_count = len(ip_counter[ip])
        unique_ip_count = len(ip_counter)
        total_request_in_window = sum(len(v) for v in ip_counter.values())

        payload_feature = extract_payload_features(payload)
        feature = np.array([[request_count, unique_ip_count, total_request_in_window] + payload_feature])
        prediction = model.predict(feature)[0]

        if prediction == 0:
            status = "✅ Bình thường"
        elif prediction == 1:
            status = "🚨 DoS"
        elif prediction == 2:
            status = "⚠️ DDoS"
        elif prediction == 3:
            status = "🟡 XSS"
        elif prediction == 4:
            status = "🔴 SQLi"
        else:
            status = "❓ Không xác định"
        if status not in list_attack and status != "✅ Bình thường":
            list_attack.append(status)
        print(f"IP: {ip} | Attack: ")
        for i in list_attack:
            print(i,end=",")
        print()
        print(f"IP: {ip} | Request: {request_count} | Unique IP: {unique_ip_count} | Total: {total_request_in_window} | Payload: {payload[:30]} --> {status}")