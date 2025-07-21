import numpy as np
import re
import pickle
from datetime import datetime
from collections import defaultdict

LOG_FILE = '/var/log/user_data.log'
THRESHOLD_TIME = 60

with open("rf_model_freq.pkl", "rb") as f:
    model_freq = pickle.load(f)

with open("rf_model_payload.pkl", "rb") as f:
    model_payload = pickle.load(f)

def parse_time(t):
    try:
        return datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None

def extract_payload_features(payload):
    length = len(payload)
    has_script = int(bool(re.search(r'script', payload, re.IGNORECASE)))
    has_sql = int(bool(re.search(r'select|union|--|insert|drop|or', payload, re.IGNORECASE)))
    has_special = int(bool(re.search(r"[<>'\"]", payload)))
    return [length, has_script, has_sql, has_special]

ip_counter = defaultdict(list)

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

        # Lấy toàn bộ đoạn 'Dữ liệu: ...' từ nguyên dòng
        if "Dữ liệu:" in line and "IP:" in line:
            data_str = line.split("Dữ liệu:")[1].split("IP:")[0].strip()
        else:
            data_str = ""

        if data_str:
            key_vals = data_str.split(';')
        for kv in key_vals:
            if ':' in kv:
                value = kv.split(':', 1)[1].strip()
                payload += value + " "
        payload = payload.strip()

        # Tiếp tục parse các field còn lại
        for part in parts:
            if part.strip().startswith("IP:"):
                ip = part.split("IP:")[1].strip()
            elif part.strip().startswith("Thời gian:"):
                time_str = part.split("Thời gian:")[1].strip()
        
        
        if not ip or not time_str:
            continue

        now = parse_time(time_str)
        if not now:
            continue

        # ===== Check DoS/DDoS =====
        ip_counter[ip].append(now)
        for k in list(ip_counter.keys()):
            ip_counter[k] = [t for t in ip_counter[k] if (now - t).total_seconds() <= THRESHOLD_TIME]
            if not ip_counter[k]:
                del ip_counter[k]
        request_count = len(ip_counter[ip])
        unique_ip_count = len(ip_counter)
        total_request_in_window = sum(len(v) for v in ip_counter.values())

        freq_features = np.array([[request_count, unique_ip_count, total_request_in_window]])
        freq_pred = model_freq.predict(freq_features)[0]

        if freq_pred == 0:
            freq_status = "✅ Bình thường"
        elif freq_pred == 1:
            freq_status = "🚨 DoS"
        else:
            freq_status = "⚠️ DDoS"

        # ===== Check SQLi/XSS =====
        
        if payload != "":
            payload_features = np.array([extract_payload_features(payload)])
            payload_pred = model_payload.predict(payload_features)[0]

            if payload_pred == 0:
                payload_status = "✅ Bình thường"
            elif payload_pred == 3:
                payload_status = "🟡 XSS"
            elif payload_pred == 4:
                payload_status = "🔴 SQLi"
            else:
                payload_status = "❓ Không xác định"
        else:
            payload_status ="Payload NULL"
        print(f"IP: {ip} | Payload check: {payload_status} | Freq check: {freq_status} ('req_c':{request_count} 'uni_c':{unique_ip_count} 't_req_c':{total_request_in_window}| Payload (30): {payload[:30]}")
        log_line = f"{datetime.now()}|{ip}|{payload_status}|{freq_status}|{request_count}|{unique_ip_count}|{total_request_in_window}|{payload[:30]}\n"
        with open("/var/www/html/dashboard_output.txt", "a", encoding="utf-8") as out:
            out.write(log_line)