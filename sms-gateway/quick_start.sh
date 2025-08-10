#!/bin/bash

echo "=========================================="
echo "   SMS GATEWAY - INICIO RÁPIDO"
echo "=========================================="

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Crear directorios necesarios
mkdir -p logs

# Instalar dependencias Python si no existen
echo "📦 Instalando dependencias Python..."
pip3 install pyserial flask flask-cors 2>/dev/null

# Detectar módems
echo ""
echo "🔍 Detectando módems USB..."
MODEMS=$(ls /dev/ttyUSB* 2>/dev/null | wc -l)

if [ $MODEMS -eq 0 ]; then
    echo -e "${RED}⚠️  No se detectaron módems USB${NC}"
    echo ""
    echo "Conecta tus módems Huawei E3372 o similares y vuelve a ejecutar"
    echo ""
    echo "Si tienes módems conectados, ejecuta:"
    echo "  sudo chmod 666 /dev/ttyUSB*"
    echo ""
else
    echo -e "${GREEN}✓ Detectados $MODEMS módems:${NC}"
    ls /dev/ttyUSB*
    
    # Dar permisos
    sudo chmod 666 /dev/ttyUSB* 2>/dev/null
fi

echo ""
echo "🚀 Iniciando servicios..."

# Iniciar API en background
echo "  - API REST en puerto 5000..."
cd api && python3 server.py > ../logs/api.log 2>&1 &
API_PID=$!

# Iniciar servidor web simple para la UI
echo "  - Web UI en puerto 8080..."
cd ../web && python3 -m http.server 8080 > ../logs/web.log 2>&1 &
WEB_PID=$!

sleep 2

echo ""
echo "=========================================="
echo -e "${GREEN}✓ GATEWAY INICIADO CON ÉXITO${NC}"
echo "=========================================="
echo ""
echo "📱 Accesos:"
echo "  • Web UI: http://localhost:8080"
echo "  • API REST: http://localhost:5000"
echo ""
echo "📝 Ejemplos de uso:"
echo ""
echo "1. Enviar SMS desde terminal:"
echo "   python3 main.py +34600000000 BANCO 'Tu código es 1234'"
echo ""
echo "2. Enviar SMS via API:"
echo "   curl -X POST http://localhost:5000/api/send \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"number\":\"+34600000000\",\"sender_id\":\"AMAZON\",\"message\":\"Tu paquete llegó\"}'"
echo ""
echo "3. Ver estadísticas:"
echo "   curl http://localhost:5000/api/stats"
echo ""
echo "⚠️  Para detener el gateway:"
echo "   kill $API_PID $WEB_PID"
echo ""
echo "Logs en: logs/"
echo ""