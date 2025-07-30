<?php
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

$input = json_decode(file_get_contents('php://input'), true);

if (!$input || !isset($input['session_id'])) {
    echo json_encode(['success' => false, 'message' => 'Session ID requerido']);
    exit();
}

$session_id = $input['session_id'];
$email = $input['email'] ?? 'Desconocido';
$timestamp = $input['timestamp'] ?? date('Y-m-d H:i:s');

// Crear directorio de sesiones si no existe
$sessions_dir = __DIR__ . '/sessions';
if (!is_dir($sessions_dir)) {
    mkdir($sessions_dir, 0777, true);
}

// Verificar si ya existe un archivo de sesión
$session_file = $sessions_dir . '/' . $session_id . '.json';

if (file_exists($session_file)) {
    // Actualizar archivo existente
    $session_data = json_decode(file_get_contents($session_file), true);
    if (!$session_data) {
        $session_data = [];
    }
    
    // Actualizar datos
    $session_data['email'] = $email;
    $session_data['updated_at'] = date('Y-m-d H:i:s');
} else {
    // Crear nuevo archivo de sesión
    $session_data = [
        'session_id' => $session_id,
        'email' => $email,
        'created_at' => date('Y-m-d H:i:s'),
        'updated_at' => date('Y-m-d H:i:s'),
        'otp_requested' => false,
        'otp_verified' => false,
        'status' => 'new'
    ];
}

// Guardar archivo de sesión
file_put_contents($session_file, json_encode($session_data));

echo json_encode(['success' => true, 'message' => 'Sesión registrada correctamente']);
?>