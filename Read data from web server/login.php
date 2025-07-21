<?php
session_start();

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

$error = '';

// Xử lý đăng nhập
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';

    // Ghi log
    ghi_log(['tài khoản' => $username, 'mật khẩu' => $password]);

    // Giả lập dữ liệu tài khoản
    $accounts = [
        'admin' => '123456'

    ];

    if (isset($accounts[$username]) && $accounts[$username] === $password) {
   
        $_SESSION['is_admin'] = ($username === 'admin');

        if ($_SESSION['is_admin']) {
            header("Location: dashboard.php");
        } 
        exit();
    } else {
        $error = "Tài khoản hoặc mật khẩu không đúng!";
    }
}
?>


<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Đăng Nhập</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-image: linear-gradient(to right, #007bff, #6610f2);
            color: white;
            height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background-color: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            width: 350px;
            text-align: center;
        }
        h2 {
            margin-bottom: 20px;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: none;
            border-radius: 8px;
            outline: none;
        }
        input[type="submit"] {
            width: 100%;
            padding: 12px;
            background-color: #28a745;
            border: none;
            border-radius: 8px;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #218838;
        }
        .error {
            color: yellow;
            margin-top: 10px;
        }
    </style>
</head>
<body>
<div class="container">
    <h2>Đăng Nhập</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Tài Khoản" required>
        <input type="password" name="password" placeholder="Mật Khẩu" required>
        <input type="submit" value="Đăng Nhập">
        <?php if (!empty($error)): ?>
            <p class="error"><?= htmlspecialchars($error) ?></p>
        <?php endif; ?>
    </form>
</div>
</body>
</html>
