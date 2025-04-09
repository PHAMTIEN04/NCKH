from scapy.all import sniff
import pandas as pd
import time

# Danh sách lưu trữ thông tin gói tin
packets_info = []

# Hàm xử lý gói tin
def packet_handler(packet):
    # Lấy thông tin từ gói tin (ví dụ, số lượng byte và thời gian)
    num_bytes = len(packet)
    timestamp = time.time()
    
    # Trích xuất thêm thông tin cần thiết từ gói tin nếu có thể
    # Ví dụ: nếu gói tin là TCP
    if packet.haslayer('TCP'):
        src_port = packet['TCP'].sport
        dst_port = packet['TCP'].dport
        packets_info.append({
            'num_bytes': num_bytes,
            'src_port': src_port,
            'dst_port': dst_port,
            'timestamp': timestamp
        })
    # Bạn có thể thêm nhiều thông tin khác từ các lớp gói tin nếu cần

# Bắt gói tin (ví dụ, trong 10 giây)
print("Bắt gói tin trong 10 giây...")
sniff(timeout=10, prn=packet_handler)

# Chuyển đổi danh sách gói tin thành DataFrame
df = pd.DataFrame(packets_info)

# In ra dữ liệu đã thu thập
print("Dữ liệu gói tin đã thu thập:\n", df)

# Giả sử bạn có nhãn cho dữ liệu này, bạn có thể thêm nhãn vào DataFrame
# df['label'] = ...

# Lưu dữ liệu vào CSV nếu cần
df.to_csv('captured_packets.csv', index=False)
