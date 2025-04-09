import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Bước 1: Tải dữ liệu
data = pd.read_csv('info_network.csv')

# Bước 2: Chuẩn bị dữ liệu
X = data.drop('label', axis=1)  # Các đặc trưng
y = data['label']  # Nhãn phân loại

# Bước 3: Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Bước 4: Khởi tạo và huấn luyện mô hình Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Bước 5: Đánh giá mô hình
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Bước 6: Dự đoán dữ liệu đầu vào mới
# Ví dụ dữ liệu đầu vào mới
new_data = [[550, 100, 15800, 0.3]]  # Đầu vào mẫu: [num_packets, session_time, bytes_sent, error_rate]
prediction = model.predict(new_data)
print("Prediction for the new data:", prediction[0])
