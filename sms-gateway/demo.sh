#!/bin/bash

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

clear

echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}     SMS GATEWAY - DEMOSTRACIÓN COMPLETA${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""

# Función para pausar
pause() {
    echo ""
    echo -e "${YELLOW}Presiona ENTER para continuar...${NC}"
    read
}

# 1. Verificar servicios
echo -e "${GREEN}1. VERIFICANDO SERVICIOS${NC}"
echo "   Comprobando API..."
if curl -s http://localhost:5000/ > /dev/null 2>&1; then
    echo -e "   ${GREEN}✓${NC} API funcionando en http://localhost:5000"
else
    echo -e "   ${RED}✗${NC} API no responde"
fi

echo "   Comprobando Web UI..."
if curl -s http://localhost:8080/ > /dev/null 2>&1; then
    echo -e "   ${GREEN}✓${NC} Web UI funcionando en http://localhost:8080"
else
    echo -e "   ${RED}✗${NC} Web UI no responde"
fi

pause

# 2. Estadísticas del sistema
echo -e "${GREEN}2. ESTADÍSTICAS DEL SISTEMA${NC}"
curl -s http://localhost:5000/api/stats | python3 -c "
import sys, json
data = json.load(sys.stdin)['stats']
print(f'   Modo: {data.get(\"mode\", \"PRODUCTION\")}')
print(f'   Módems totales: {data[\"modems\"]}')
print(f'   Módems activos: {data[\"active_modems\"]}')
print(f'   SMS enviados: {data[\"messages_sent\"]}')
print(f'   SMS fallidos: {data[\"messages_failed\"]}')
"

pause

# 3. Enviar SMS individual
echo -e "${GREEN}3. ENVIANDO SMS INDIVIDUAL${NC}"
echo "   Enviando SMS con sender ID 'BANCO'..."
echo ""

RESPONSE=$(curl -s -X POST http://localhost:5000/api/send \
  -H 'Content-Type: application/json' \
  -d '{
    "number": "+34600111222",
    "sender_id": "BANCO",
    "message": "Su transferencia de 1000€ ha sido procesada correctamente",
    "method": "pdu"
  }')

echo "$RESPONSE" | python3 -m json.tool

pause

# 4. Envío masivo
echo -e "${GREEN}4. ENVÍO MASIVO (3 números)${NC}"
echo "   Enviando campaña SMS..."
echo ""

curl -s -X POST http://localhost:5000/api/send-bulk \
  -H 'Content-Type: application/json' \
  -d '{
    "numbers": ["+34600222333", "+34600333444", "+34600444555"],
    "sender_id": "OFERTA",
    "message": "50% descuento BLACK FRIDAY solo hoy!",
    "delay": 1
  }' | python3 -m json.tool

echo ""
echo "   Esperando a que termine el envío masivo..."
sleep 5

pause

# 5. Test de sender IDs
echo -e "${GREEN}5. TEST DE SENDER IDS${NC}"
echo "   Probando qué sender IDs funcionan..."
echo ""

curl -s -X POST http://localhost:5000/api/test \
  -H 'Content-Type: application/json' \
  -d '{"number": "+34600555666", "custom_sender": "TESLA"}' \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data['success']:
    for r in data['results']:
        status = '✓' if r['success'] else '✗'
        print(f'   {status} {r[\"sender_id\"]:<12} - {r[\"message\"][:30]}...')
"

pause

# 6. Ver rutas disponibles
echo -e "${GREEN}6. RUTAS DISPONIBLES${NC}"
curl -s http://localhost:5000/api/routes | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'   Total rutas: {data[\"total_routes\"]}')
print(f'   Rutas activas: {data[\"active_routes\"]}')
print('')
print('   Primeras 10 rutas:')
for r in data['routes'][:10]:
    sender = '✓' if r['capabilities']['sender_id'] else '✗'
    print(f'   • {r[\"name\"]:<20} [{r[\"status\"]:<8}] Sender ID: {sender}')
"

pause

# 7. Estadísticas finales
echo -e "${GREEN}7. ESTADÍSTICAS FINALES${NC}"
curl -s http://localhost:5000/api/stats | python3 -c "
import sys, json
data = json.load(sys.stdin)['stats']
print(f'   Total SMS enviados: {data[\"messages_sent\"]}')
print('')
if 'last_messages' in data and data['last_messages']:
    print('   Últimos 3 mensajes:')
    for msg in data['last_messages'][-3:]:
        print(f'   • {msg[\"number\"]} | {msg[\"sender_id\"]} | {msg[\"message\"][:30]}...')
"

echo ""
echo -e "${BLUE}============================================================${NC}"
echo -e "${GREEN}DEMOSTRACIÓN COMPLETADA${NC}"
echo ""
echo "Accesos:"
echo "  • Web UI: http://localhost:8080"
echo "  • API REST: http://localhost:5000"
echo "  • Documentación API: http://localhost:5000/"
echo ""
echo -e "${YELLOW}NOTA: Este es modo SIMULACIÓN. Para usar con módems reales,${NC}"
echo -e "${YELLOW}conecta módems Huawei E3372 y ejecuta con main.py${NC}"
echo -e "${BLUE}============================================================${NC}"