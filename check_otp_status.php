<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Registrar todas las solicitudes para depuración
file_put_contents('otp_status_debug.log', date('Y-m-d H:i:s') . " - " . file_get_contents('php://input') . "\n", FILE_APPEND);

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
$action = $input['action'] ?? 'check_status';
$sessions_dir = __DIR__ . '/sessions';

// Crear directorio de sesiones si no existe
if (!is_dir($sessions_dir)) {
    mkdir($sessions_dir, 0777, true);
}

$session_file = $sessions_dir . '/' . $session_id . '.json';

// Si es una acción para marcar como solicitado
if ($action === 'mark_requested') {
    if (file_exists($session_file)) {
        // Actualizar archivo existente
        $session_data = json_decode(file_get_contents($session_file), true);
        if (!$session_data) {
            $session_data = [];
        }
    } else {
        // Crear nuevo archivo
        $session_data = [
            'session_id' => $session_id,
            'created_at' => date('Y-m-d H:i:s')
        ];
    }
    
    // Marcar como solicitado
    $session_data['otp_requested'] = true;
    $session_data['status'] = 'requested';
    $session_data['otp_timestamp'] = time();
    $session_data['updated_at'] = date('Y-m-d H:i:s');
    
    file_put_contents($session_file, json_encode($session_data));
    
    echo json_encode([
        'success' => true,
        'message' => 'OTP marcado como solicitado',
        'session_id' => $session_id
    ]);
    exit();
}

// Verificar estado
if (!file_exists($session_file)) {
    echo json_encode([
        'success' => false, 
        'message' => 'Sesión no encontrada',
        'session_id' => $session_id,
        'file_path' => $session_file
    ]);
    exit();
}

$session_data = json_decode(file_get_contents($session_file), true);

if (!$session_data) {
    echo json_encode(['success' => false, 'message' => 'Error al leer sesión']);
    exit();
}

// Verificar si se ha solicitado OTP
$otp_requested = (isset($session_data['otp_requested']) && $session_data['otp_requested'] === true) || 
                 (isset($session_data['status']) && $session_data['status'] === 'requested');

// Verificar si el OTP ha sido enviado y verificado
$otp_submitted = isset($session_data['otp_submitted']) && $session_data['otp_submitted'] === true;
$manually_verified = isset($session_data['manually_verified']) && $session_data['manually_verified'] === true;
$otp_verified = isset($session_data['otp_verified']) && $session_data['otp_verified'] === true && $manually_verified;
$otp_invalid = isset($session_data['otp_verified']) && $session_data['otp_verified'] === false && $manually_verified;

// Determinar el estado de verificación
$verification_status = 'pending';
if ($otp_verified && $manually_verified) {
    $verification_status = 'valid';
} elseif ($otp_invalid && $manually_verified) {
    $verification_status = 'invalid';
} elseif ($otp_submitted && !$manually_verified) {
    // Si se ha enviado un OTP pero no ha sido verificado manualmente, mostrar como "waiting"
    $verification_status = 'waiting';
}

echo json_encode([
    'success' => true,
    'otp_requested' => $otp_requested,
    'otp_submitted' => $otp_submitted,
    'otp_verified' => $otp_verified,
    'verification_status' => $verification_status,
    'session_id' => $session_id,
    'session_data' => $session_data,
    'timestamp' => time()
]);
?>