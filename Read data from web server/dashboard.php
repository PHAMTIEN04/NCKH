<?php
session_start();

// Kiểm tra quyền truy cập
if (!isset($_SESSION['is_admin']) || $_SESSION['is_admin'] !== true) {
    header("Location: login.php");
    exit();
}
error_reporting(E_ALL);
ini_set('display_errors', 1);

$log_file = "dashboard_output.txt";
$lines = file($log_file, FILE_IGNORE_NEW_LINES);

$data_rows = [];
$attack_types = [];
$freq_anomalies = [];

foreach ($lines as $line) {
    $parts = explode("|", $line);
    if (count($parts) == 7) {
        list($ip, $payload_check, $freq_check, $payload_count, $freq_count, $total, $payload) = $parts;
        $data_rows[] = [
            'ip' => $ip,
            'payload_check' => $payload_check,
            'freq_check' => $freq_check,
            'payload_count' => $payload_count,
            'freq_count' => $freq_count,
            'total' => $total,
            'payload' => $payload
        ];

        if (strpos($payload_check, 'Bình thường') === false) {
            $attack_types[$payload_check] = ($attack_types[$payload_check] ?? 0) + 1;
        }

        if (strpos($freq_check, 'Bình thường') === false) {
            $freq_anomalies[$freq_check] = ($freq_anomalies[$freq_check] ?? 0) + 1;
        }
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Dashboard Giám sát An ninh</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { background: #f4f6f9; padding: 20px; }
        h2 { font-weight: bold; }
        .table th, .table td { vertical-align: middle; }
        .status { font-size: 1.2rem; }
        .refresh-note { font-size: 0.9rem; color: gray; }
    </style>
</head>
<body>

<div class="container">
    <h2 class="text-center mb-4">📊 Dashboard Giám sát Tấn công Mạng</h2>
    <p class="text-center refresh-note">Tự động làm mới mỗi 10 giây</p>

    <!-- Biểu đồ -->
    <div class="row mb-5">
        <div class="col-md-6">
            <h5 class="text-center">📌 Loại tấn công (Payload)</h5>
            <canvas id="attackChart"></canvas>
        </div>
        <div class="col-md-6">
            <h5 class="text-center">📈 Tần suất bất thường</h5>
            <canvas id="freqChart"></canvas>
        </div>
    </div>

    <!-- Bảng dữ liệu -->
    <table class="table table-bordered table-hover bg-white shadow-sm">
        <thead class="table-dark">
            <tr>
                <th>IP</th>
                <th>Phân tích Payload</th>
                <th>Phân tích Tần suất</th>
                <th>Số lần Payload</th>
                <th>Số lần Tần suất</th>
                <th>Tổng</th>
                <th>Payload gửi</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($data_rows as $row): ?>
            <tr>
                <td><?= htmlspecialchars($row['ip']) ?></td>
                <td class="status"><?= htmlspecialchars($row['payload_check']) ?></td>
                <td class="status"><?= htmlspecialchars($row['freq_check']) ?></td>
                <td><?= $row['payload_count'] ?></td>
                <td><?= $row['freq_count'] ?></td>
                <td><?= $row['total'] ?></td>
                <td><code><?= htmlspecialchars($row['payload']) ?></code></td>
            </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
</div>

<!-- Chart Script -->
<script>
const attackLabels = <?= json_encode(array_keys($attack_types)) ?>;
const attackData = <?= json_encode(array_values($attack_types)) ?>;

const freqLabels = <?= json_encode(array_keys($freq_anomalies)) ?>;
const freqData = <?= json_encode(array_values($freq_anomalies)) ?>;

new Chart(document.getElementById('attackChart'), {
    type: 'bar',
    data: {
        labels: attackLabels,
        datasets: [{
            label: 'Số lần phát hiện',
            data: attackData,
            backgroundColor: 'rgba(255, 99, 132, 0.6)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: { beginAtZero: true }
        }
    }
});

new Chart(document.getElementById('freqChart'), {
    type: 'bar',
    data: {
        labels: freqLabels,
        datasets: [{
            label: 'Số lần bất thường',
            data: freqData,
            backgroundColor: 'rgba(54, 162, 235, 0.6)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: { beginAtZero: true }
        }
    }
});

// Tự động reload sau 10 giây
setTimeout(() => location.reload(), 10000);
</script>

</body>
</html>
