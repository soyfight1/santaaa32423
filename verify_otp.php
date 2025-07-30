<?php
// Este script permite verificar manualmente un OTP

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
$is_valid = isset($data['is_valid']) ? (bool)$data['is_valid'] : false;

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

// Actualizar el estado de verificación
$session_data['otp_verified'] = $is_valid;
$session_data['manually_verified'] = true;
$session_data['verification_time'] = date('Y-m-d H:i:s');

// Guardar los cambios
file_put_contents($session_file, json_encode($session_data, JSON_PRETTY_PRINT));

// Devolver respuesta exitosa
echo json_encode([
    'success' => true,
    'message' => $is_valid ? 'OTP marcado como válido' : 'OTP marcado como inválido',
    'verification_status' => $is_valid ? 'valid' : 'invalid'
]);
?>