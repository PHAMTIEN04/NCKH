<?php
// Thiết lập múi giờ Việt Nam (ICT, UTC+7) để đảm bảo thời gian luôn là giờ Việt Nam
date_default_timezone_set('Asia/Ho_Chi_Minh');

// Ghi log khi người dùng truy cập trang
$ip = $_SERVER['REMOTE_ADDR'];
$time = date('Y-m-d H:i:s'); // Thời gian sẽ luôn là giờ Việt Nam
$log_file = '/var/log/user_data.log';

// Hàm ghi log
function ghi_log($data) {
    global $ip, $time, $log_file;
    $data_str = implode('; ', array_map(function($k, $v) { return "$k: $v"; }, array_keys($data), $data));
    $log = "Dữ liệu: $data_str; IP: $ip; Thời gian: $time\n";
    file_put_contents($log_file, $log, FILE_APPEND);
}

// Ghi log cho GET
if ($_SERVER['REQUEST_METHOD'] === 'GET' && !empty($_GET)) {
    ghi_log($_GET);
}

// Ghi log cho POST
if ($_SERVER['REQUEST_METHOD'] === 'POST' && !empty($_POST)) {
    ghi_log($_POST);
}

// Xử lý tìm kiếm
$search_results = [];
if (isset($_GET['book_name']) && !empty($_GET['book_name'])) {
    $book_name = $_GET['book_name'];
    // Danh sách sách mẫu (có thể thay bằng cơ sở dữ liệu)
    $books = [
        'Lập trình PHP cơ bản',
        'Học Python từ đầu',
        'Kỹ thuật lập trình C++',
        'Giải thuật và lập trình',
        'Phát triển web với Flask',
        'Laravel cho người mới bắt đầu'
    ];

    // Tìm kiếm sách theo tên
    foreach ($books as $book) {
        if (stripos($book, $book_name) !== false) {
            $search_results[] = $book;
        }
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Đăng Nhập & Tìm Kiếm Sách</title>
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
        .search-bar {
            margin-bottom: 20px;
        }
        .results {
            margin-top: 15px;
            text-align: left;
        }
        .results p {
            background-color: rgba(255, 255, 255, 0.3);
            padding: 8px;
            margin: 5px 0;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Tìm Kiếm Sách</h2>
        <form method="GET" action="">
            <input type="text" name="book_name" placeholder="Nhập tên sách...">
            <input type="submit" value="Tìm Kiếm">
        </form>
        <div class="results">
            <?php if (!empty($search_results)) {
                echo '<h3>Kết quả tìm kiếm:</h3>';
                foreach ($search_results as $result) {
                    echo '<p>' . htmlspecialchars($result) . '</p>';
                }
            } ?>
        </div>
        <h2><a href="login.php" style="color: #fff; text-decoration: none;">Đăng Nhập</a></h2>
    </div>
</body>
</html>