# Configuración OpenBullet para Ibercaja Banca Digital

## 📋 Descripción

Esta configuración permite realizar pruebas de autenticación en el sistema de banca digital de Ibercaja (entorno de pruebas TryHackMe). La configuración implementa el flujo completo de OAuth 2.0 / OpenID Connect utilizado por el sistema.

## 🔧 Características

- **Flujo OAuth 2.0 completo** con OpenID Connect
- **Manejo de tokens CSRF** y cookies de sesión
- **Detección inteligente** de respuestas (éxito, fallo, ban, retry)
- **Captura de tokens** de acceso y refresh
- **Extracción de información** del usuario autenticado
- **Delays aleatorios** para evitar detección
- **Soporte para 2FA** (detección de verificación adicional)

## 📁 Archivos Incluidos

1. **`ibercaja_openbullet_config.loli`** - Configuración básica
2. **`ibercaja_openbullet_advanced.loli`** - Configuración avanzada con características adicionales
3. **`openid_config.json`** - Configuración del servidor OpenID Connect
4. **`auth_flow_summary.txt`** - Resumen del flujo de autenticación

## 🚀 Cómo Usar

### Requisitos Previos

- OpenBullet 2 o Silverbullet
- Proxies HTTP/HTTPS (recomendado)
- Lista de credenciales en formato `usuario:contraseña`

### Instalación

1. Importar el archivo `.loli` en OpenBullet
2. Configurar los proxies si es necesario
3. Cargar el wordlist con las credenciales
4. Ajustar los threads según necesidad (recomendado: 1-5 para evitar detección)

### Configuración de Proxies

```
Tipo: HTTP/HTTPS
Timeout: 30 segundos
Reintentos: 2
```

## 🔍 Flujo de Autenticación

1. **Inicialización** → GET a `/auth/login`
2. **Autorización OAuth** → Redirección al servidor de identidad
3. **Formulario de Login** → Captura de tokens CSRF
4. **Envío de Credenciales** → POST con usuario/contraseña
5. **Intercambio de Código** → Obtención de access token
6. **Información de Usuario** → GET a `/userinfo`

## 📊 Tipos de Respuesta

### ✅ Success (Éxito)
- Redirección con código de autorización
- Status code 302 con `code=` en Location
- Captura de tokens de acceso

### ❌ Failure (Fallo)
- "Usuario o contraseña incorrectos"
- "Credenciales no válidas"
- Status codes 401, 403

### 🚫 Ban (Cuenta Bloqueada)
- "Cuenta bloqueada"
- "Too many failed attempts"
- "Suspendido"

### 🔄 Retry (Reintentar)
- Status code 429 (Rate limit)
- Status code 503 (Servicio no disponible)
- "Try again"

### ⚠️ Custom (2FA/Verificación Adicional)
- "Verificación adicional requerida"
- "Código SMS"
- "2FA"

## 🛡️ Mecanismos de Seguridad Detectados

1. **Imperva/Incapsula WAF** - Cookies de sesión especiales
2. **Tokens CSRF** - `__RequestVerificationToken`
3. **Campo Data encriptado** - Datos de sesión cifrados
4. **Rate Limiting** - Límite de intentos por IP
5. **Device Fingerprinting** - Headers específicos requeridos

## ⚙️ Personalización

### Variables Modificables

```loli
SET VAR "USER_AGENT" "Tu User Agent"
SET VAR "DELAY" "1000-3000"  # Delay en ms
```

### Headers Adicionales

Puedes agregar headers adicionales según necesidad:

```loli
HEADER "X-Forwarded-For: <PROXY_IP>"
HEADER "X-Real-IP: <PROXY_IP>"
```

## 📈 Optimización

### Para Mayor Velocidad
- Reducir delays
- Aumentar threads
- Usar proxies rápidos

### Para Mayor Stealth
- Aumentar delays aleatorios
- Rotar User Agents
- Limitar threads a 1-3
- Usar proxies residenciales

## ⚠️ Notas Importantes

1. **Solo para uso educativo** en entornos autorizados
2. **Respetar rate limits** para evitar bloqueos
3. **Usar proxies de calidad** para mejores resultados
4. **Monitorear respuestas** para ajustar configuración

## 🐛 Solución de Problemas

### Error: "Cannot find Chrome binary"
- No es necesario navegador, la config usa requests HTTP directos

### Error: Token CSRF no encontrado
- Verificar que el sitio no haya cambiado estructura
- Revisar cookies de sesión

### Muchos Retries
- Reducir velocidad/threads
- Cambiar proxies
- Agregar delays más largos

## 📝 Capturas Disponibles

Al obtener un hit exitoso, se capturan:

- `ACCESS_TOKEN` - Token de acceso OAuth
- `REFRESH_TOKEN` - Token para renovar acceso
- `USER_ID` - ID único del usuario
- `FULL_NAME` - Nombre completo
- `EMAIL` - Correo electrónico

## 🔄 Actualizaciones

- **v1.0** - Configuración básica
- **v2.0** - Añadido manejo avanzado de errores, soporte 2FA, delays aleatorios

## 📞 Soporte

Para problemas o mejoras, revisar:
- Logs de OpenBullet
- Respuestas HTTP en debugger
- Configuración de proxies

---

**Disclaimer**: Esta configuración es solo para propósitos educativos y pruebas en entornos autorizados. No usar para actividades no autorizadas.