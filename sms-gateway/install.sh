#!/bin/bash

echo "🚀 SMS Gateway - Instalación automática completa"
echo "================================================"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Función para logging
log() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Detectar OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
else
    error "Sistema operativo no soportado"
fi

log "Sistema detectado: $OS"

# Actualizar sistema
log "Actualizando sistema..."
if [ "$OS" == "linux" ]; then
    sudo apt-get update -qq
    sudo apt-get upgrade -y -qq
fi

# Instalar dependencias del sistema
log "Instalando dependencias del sistema..."
if [ "$OS" == "linux" ]; then
    sudo apt-get install -y -qq \
        python3 python3-pip python3-dev \
        build-essential libssl-dev libffi-dev \
        libmysqlclient-dev \
        gammu libgammu-dev python3-gammu \
        usb-modeswitch usb-modeswitch-data \
        mysql-server mysql-client \
        redis-server \
        nginx \
        git curl wget \
        screen tmux \
        usbutils
fi

# Instalar Python packages
log "Instalando paquetes Python..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Configurar MySQL
log "Configurando base de datos MySQL..."
sudo systemctl start mysql
sudo mysql -e "CREATE DATABASE IF NOT EXISTS smsgateway;"
sudo mysql -e "CREATE USER IF NOT EXISTS 'smsuser'@'localhost' IDENTIFIED BY 'sms2024pass';"
sudo mysql -e "GRANT ALL PRIVILEGES ON smsgateway.* TO 'smsuser'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# Configurar Redis
log "Configurando Redis..."
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Detectar módems conectados
log "Detectando módems USB..."
MODEMS=$(ls /dev/ttyUSB* 2>/dev/null | wc -l)
if [ $MODEMS -gt 0 ]; then
    echo -e "${GREEN}✓${NC} Detectados $MODEMS módems:"
    ls /dev/ttyUSB*
else
    echo -e "${YELLOW}⚠${NC} No se detectaron módems. Conecta los módems y ejecuta: sudo ./scripts/detect_modems.sh"
fi

# Configurar permisos para módems
log "Configurando permisos para módems..."
sudo usermod -a -G dialout $USER
sudo chmod 666 /dev/ttyUSB* 2>/dev/null || true

# Crear reglas udev para módems
log "Creando reglas udev para módems..."
sudo tee /etc/udev/rules.d/99-usb-modems.rules > /dev/null <<EOF
# Huawei modems
ATTRS{idVendor}=="12d1", ATTRS{idProduct}=="*", MODE="0666", GROUP="dialout"
# ZTE modems  
ATTRS{idVendor}=="19d2", ATTRS{idProduct}=="*", MODE="0666", GROUP="dialout"
# Generic USB serial
KERNEL=="ttyUSB[0-9]*", MODE="0666", GROUP="dialout"
EOF

sudo udevadm control --reload-rules
sudo udevadm trigger

# Crear estructura de directorios
log "Creando estructura de directorios..."
mkdir -p logs database/migrations config/modems

# Configurar servicios systemd
log "Configurando servicios del sistema..."
sudo tee /etc/systemd/system/sms-gateway.service > /dev/null <<EOF
[Unit]
Description=SMS Gateway Service
After=network.target mysql.service redis.service

[Service]
Type=simple
User=$USER
WorkingDirectory=/workspace/sms-gateway
ExecStart=/usr/bin/python3 /workspace/sms-gateway/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload

# Crear archivo de configuración principal
log "Creando configuración principal..."
cat > config/settings.json <<EOF
{
    "database": {
        "host": "localhost",
        "port": 3306,
        "name": "smsgateway",
        "user": "smsuser",
        "password": "sms2024pass"
    },
    "redis": {
        "host": "localhost",
        "port": 6379,
        "db": 0
    },
    "api": {
        "host": "0.0.0.0",
        "port": 5000,
        "debug": false
    },
    "sms": {
        "max_retries": 3,
        "retry_delay": 5,
        "messages_per_minute": 100,
        "rotate_modems": true,
        "sender_id_enabled": true
    },
    "modems": {
        "auto_detect": true,
        "baud_rate": 115200,
        "timeout": 10
    }
}
EOF

# Configurar firewall
log "Configurando firewall..."
sudo ufw allow 5000/tcp comment 'SMS Gateway API' 2>/dev/null || true
sudo ufw allow 8080/tcp comment 'SMS Gateway Web UI' 2>/dev/null || true

# Crear script de inicio rápido
log "Creando scripts de utilidad..."
cat > start.sh <<'EOF'
#!/bin/bash
echo "Iniciando SMS Gateway..."
screen -dmS sms-api python3 api/server.py
screen -dmS sms-worker python3 scripts/worker.py
screen -dmS sms-monitor python3 scripts/monitor.py
echo "Gateway iniciado. Screens activos:"
screen -ls
echo ""
echo "API disponible en: http://localhost:5000"
echo "Web UI disponible en: http://localhost:8080"
EOF
chmod +x start.sh

# Crear script de parada
cat > stop.sh <<'EOF'
#!/bin/bash
echo "Deteniendo SMS Gateway..."
screen -X -S sms-api quit
screen -X -S sms-worker quit
screen -X -S sms-monitor quit
echo "Gateway detenido"
EOF
chmod +x stop.sh

# Mensaje final
echo ""
echo "================================================"
echo -e "${GREEN}✓ Instalación completada con éxito!${NC}"
echo "================================================"
echo ""
echo "Próximos pasos:"
echo "1. Conecta tus módems USB"
echo "2. Ejecuta: ./start.sh"
echo "3. Accede a la API: http://localhost:5000"
echo "4. Web UI: http://localhost:8080"
echo ""
echo "Comandos útiles:"
echo "  ./start.sh    - Iniciar gateway"
echo "  ./stop.sh     - Detener gateway"
echo "  screen -r sms-api    - Ver logs API"
echo "  screen -r sms-worker - Ver logs worker"
echo ""

log "Instalación completada"