#!/bin/bash

# Script para conectarse a HackTheBox
# Uso: ./connect_htb.sh <archivo.ovpn>

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}[+] HackTheBox VPN Connection Script${NC}"
echo -e "${GREEN}[+] by Cursor AI Assistant${NC}\n"

# Verificar si se proporcionó archivo
if [ $# -eq 0 ]; then
    echo -e "${RED}[!] Error: No se proporcionó archivo .ovpn${NC}"
    echo -e "${YELLOW}[*] Uso: $0 <archivo.ovpn>${NC}"
    
    # Buscar archivos .ovpn en el directorio actual
    echo -e "\n${YELLOW}[*] Buscando archivos .ovpn en el workspace...${NC}"
    OVPN_FILES=$(find /workspace -name "*.ovpn" 2>/dev/null)
    
    if [ -z "$OVPN_FILES" ]; then
        echo -e "${RED}[!] No se encontraron archivos .ovpn${NC}"
        echo -e "${YELLOW}[*] Por favor, sube tu archivo .ovpn de HackTheBox${NC}"
    else
        echo -e "${GREEN}[+] Archivos .ovpn encontrados:${NC}"
        echo "$OVPN_FILES"
        echo -e "\n${YELLOW}[*] Ejecuta: $0 <ruta_del_archivo>${NC}"
    fi
    exit 1
fi

OVPN_FILE=$1

# Verificar que el archivo existe
if [ ! -f "$OVPN_FILE" ]; then
    echo -e "${RED}[!] Error: El archivo $OVPN_FILE no existe${NC}"
    exit 1
fi

echo -e "${GREEN}[+] Archivo VPN: $OVPN_FILE${NC}"

# Verificar OpenVPN
if ! command -v openvpn &> /dev/null; then
    echo -e "${RED}[!] OpenVPN no está instalado${NC}"
    echo -e "${YELLOW}[*] Instalando OpenVPN...${NC}"
    sudo apt-get update && sudo apt-get install -y openvpn
fi

# Verificar dispositivo TUN
if [ ! -c /dev/net/tun ]; then
    echo -e "${YELLOW}[*] Creando dispositivo TUN...${NC}"
    sudo mkdir -p /dev/net
    sudo mknod /dev/net/tun c 10 200
    sudo chmod 666 /dev/net/tun
fi

echo -e "${GREEN}[+] Iniciando conexión VPN...${NC}"
echo -e "${YELLOW}[*] Presiona Ctrl+C para detener la conexión${NC}\n"

# Conectar a VPN
sudo openvpn "$OVPN_FILE"