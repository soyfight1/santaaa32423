<?php
// Este script devuelve las notificaciones no leídas

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Directorio de notificaciones
$notifications_dir = __DIR__ . '/notifications';
if (!is_dir($notifications_dir)) {
    mkdir($notifications_dir, 0755, true);
    echo json_encode(['success' => true, 'notifications' => []]);
    exit();
}

// Obtener todas las notificaciones
$notifications = [];
$files = glob($notifications_dir . '/*.json');

foreach ($files as $file) {
    $data = json_decode(file_get_contents($file), true);
    if ($data) {
        $notifications[] = $data;
    }
}

// Ordenar por timestamp (más reciente primero)
usort($notifications, function($a, $b) {
    $time_a = strtotime($a['created_at'] ?? 0);
    $time_b = strtotime($b['created_at'] ?? 0);
    return $time_b - $time_a;
});

// Marcar como leídas si se solicita
if (isset($_GET['mark_read']) && $_GET['mark_read'] === 'true') {
    foreach ($notifications as $notification) {
        $notification_file = $notifications_dir . '/' . $notification['id'] . '.json';
        $notification['read'] = true;
        file_put_contents($notification_file, json_encode($notification, JSON_PRETTY_PRINT));
    }
}

// Devolver las notificaciones
echo json_encode([
    'success' => true,
    'notifications' => $notifications
]);
?>