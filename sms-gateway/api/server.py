#!/usr/bin/env python3
"""
API REST para SMS Gateway
Endpoints para enviar SMS con sender ID personalizado
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import json
import threading
import time
from datetime import datetime

# Añadir path del proyecto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import SMSGateway

app = Flask(__name__)
CORS(app)

# Gateway global
gateway = None
gateway_lock = threading.Lock()

def init_gateway():
    """Inicializa el gateway"""
    global gateway
    with gateway_lock:
        if gateway is None:
            gateway = SMSGateway()
    return gateway

@app.route('/', methods=['GET'])
def index():
    """Endpoint principal - info del sistema"""
    return jsonify({
        'service': 'SMS Gateway',
        'version': '2.0',
        'status': 'running',
        'endpoints': {
            'send_sms': '/api/send',
            'send_bulk': '/api/send-bulk',
            'stats': '/api/stats',
            'modems': '/api/modems',
            'test': '/api/test'
        }
    })

@app.route('/api/send', methods=['POST'])
def send_sms():
    """Envía un único SMS"""
    try:
        data = request.json
        
        # Validar datos
        required = ['number', 'message']
        for field in required:
            if field not in data:
                return jsonify({'error': f'Campo requerido: {field}'}), 400
        
        number = data['number']
        message = data['message']
        sender_id = data.get('sender_id', 'SMS')
        method = data.get('method', 'auto')  # auto, pdu, text, flash
        
        # Enviar SMS
        gw = init_gateway()
        success, msg = gw.send_single(number, sender_id, message, method)
        
        return jsonify({
            'success': success,
            'message': msg,
            'details': {
                'number': number,
                'sender_id': sender_id,
                'method': method,
                'timestamp': datetime.now().isoformat()
            }
        }), 200 if success else 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/send-bulk', methods=['POST'])
def send_bulk():
    """Envía SMS a múltiples números"""
    try:
        data = request.json
        
        # Validar datos
        required = ['numbers', 'message']
        for field in required:
            if field not in data:
                return jsonify({'error': f'Campo requerido: {field}'}), 400
        
        numbers = data['numbers']
        message = data['message']
        sender_id = data.get('sender_id', 'SMS')
        method = data.get('method', 'auto')
        delay = data.get('delay', 1)
        
        # Validar números
        if not isinstance(numbers, list):
            return jsonify({'error': 'numbers debe ser una lista'}), 400
        
        # Enviar en thread para no bloquear
        def send_async():
            gw = init_gateway()
            results = gw.send_bulk(numbers, sender_id, message, method, delay)
            # Aquí podrías guardar results en DB o cache
        
        thread = threading.Thread(target=send_async)
        thread.start()
        
        return jsonify({
            'success': True,
            'message': f'Enviando SMS a {len(numbers)} números',
            'job_id': datetime.now().timestamp()
        }), 202
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Obtiene estadísticas del gateway"""
    try:
        gw = init_gateway()
        stats = gw.get_stats()
        
        return jsonify({
            'success': True,
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modems', methods=['GET'])
def get_modems():
    """Lista todos los módems detectados"""
    try:
        gw = init_gateway()
        modems = gw.modem_pool.modems
        
        return jsonify({
            'success': True,
            'total': len(modems),
            'modems': modems
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test', methods=['POST'])
def test_sender_id():
    """Prueba diferentes sender IDs para ver cuáles funcionan"""
    try:
        data = request.json
        number = data.get('number')
        
        if not number:
            return jsonify({'error': 'Número requerido'}), 400
        
        # Probar diferentes sender IDs
        test_senders = [
            'BANCO',
            'AMAZON',
            'GOOGLE',
            'PAYPAL',
            '12345',
            'INFO',
            'ALERT',
            data.get('custom_sender', 'TEST')
        ]
        
        results = []
        gw = init_gateway()
        
        for sender in test_senders:
            success, msg = gw.send_single(
                number, 
                sender, 
                f'Test sender ID: {sender}',
                'pdu'  # PDU mode funciona mejor para sender ID
            )
            results.append({
                'sender_id': sender,
                'success': success,
                'message': msg
            })
            time.sleep(2)  # Esperar entre pruebas
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/routes', methods=['GET'])
def get_routes():
    """Simula tener múltiples rutas (para compatibilidad)"""
    # Esto es para simular que tienes "1000 rutas" como querías
    routes = []
    
    gw = init_gateway()
    for i, modem in enumerate(gw.modem_pool.modems):
        routes.append({
            'id': f'route_{i+1}',
            'name': f'Route {modem["port"]}',
            'type': 'GSM',
            'status': modem['status'],
            'capabilities': {
                'sender_id': True,
                'flash_sms': True,
                'unicode': False,
                'long_sms': True
            },
            'stats': {
                'sent': modem['messages_sent'],
                'failed': 0
            }
        })
    
    # Añadir rutas "virtuales" para aparentar más capacidad
    for i in range(len(routes), 50):  # Simular 50 rutas
        routes.append({
            'id': f'virtual_route_{i+1}',
            'name': f'Virtual Route {i+1}',
            'type': 'SMPP',
            'status': 'standby',
            'capabilities': {
                'sender_id': True,
                'flash_sms': False,
                'unicode': True,
                'long_sms': True
            }
        })
    
    return jsonify({
        'success': True,
        'total_routes': len(routes),
        'active_routes': len([r for r in routes if r['status'] == 'active']),
        'routes': routes
    })

if __name__ == '__main__':
    # Inicializar gateway al arrancar
    init_gateway()
    
    # Ejecutar servidor
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )