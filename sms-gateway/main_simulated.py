#!/usr/bin/env python3
"""
SMS Gateway - Versión SIMULADA (funciona sin módems físicos)
"""

import os
import sys
import json
import time
import random
from datetime import datetime
from typing import List, Dict, Optional
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('SMSGateway')

class SimulatedModemPool:
    """Pool de módems SIMULADOS para testing"""
    
    def __init__(self):
        self.modems = []
        self.create_virtual_modems()
    
    def create_virtual_modems(self):
        """Crea módems virtuales para simular"""
        logger.info("🔧 Creando módems virtuales...")
        
        # Simular 8 módems conectados
        for i in range(8):
            self.modems.append({
                'port': f'/dev/ttyUSB{i}',
                'status': 'active',
                'messages_sent': random.randint(0, 100),
                'last_used': None,
                'sim_info': {
                    'operator': random.choice(['Movistar', 'Vodafone', 'Orange', 'Lycamobile']),
                    'imsi': f'21401{random.randint(1000000000, 9999999999)}'
                }
            })
        
        logger.info(f"✅ {len(self.modems)} módems virtuales creados")
    
    def get_next_modem(self):
        """Obtiene el siguiente módem disponible"""
        if not self.modems:
            return None
        
        # Buscar módem menos usado
        available = [m for m in self.modems if m['status'] == 'active']
        if not available:
            return None
        
        modem = min(available, key=lambda x: x['messages_sent'])
        modem['last_used'] = datetime.now()
        return modem

class SimulatedSMSSender:
    """Envía SMS SIMULADOS (no reales)"""
    
    def __init__(self, modem_pool):
        self.modem_pool = modem_pool
        self.stats = {
            'sent': 0,
            'failed': 0,
            'pending': 0
        }
        self.sent_messages = []  # Historial de mensajes "enviados"
    
    def send_sms_pdu_mode(self, port, number, sender_id, message):
        """SIMULA envío en modo PDU"""
        # Simular delay de envío
        time.sleep(random.uniform(0.5, 1.5))
        
        # 90% de éxito en la simulación
        success = random.random() < 0.9
        
        if success:
            logger.info(f"📱 [SIMULADO] SMS enviado desde {port}")
            logger.info(f"   → Destino: {number}")
            logger.info(f"   → Sender ID: {sender_id}")
            logger.info(f"   → Mensaje: {message[:50]}...")
            return True, "SMS enviado correctamente (SIMULADO)"
        else:
            return False, "Error simulado al enviar SMS"
    
    def send_sms_text_mode(self, port, number, sender_id, message):
        """SIMULA envío en modo texto"""
        time.sleep(random.uniform(0.3, 0.8))
        
        # 85% de éxito
        success = random.random() < 0.85
        
        if success:
            logger.info(f"📱 [SIMULADO-TEXT] SMS: {number} | {sender_id}")
            return True, "SMS enviado en modo texto (SIMULADO)"
        else:
            return False, "Error simulado en modo texto"
    
    def send_flash_sms(self, port, number, sender_id, message):
        """SIMULA Flash SMS"""
        time.sleep(random.uniform(0.5, 1.0))
        
        # 80% de éxito para flash
        success = random.random() < 0.8
        
        if success:
            logger.info(f"⚡ [SIMULADO-FLASH] SMS Flash: {number} | {sender_id}")
            return True, "Flash SMS enviado (SIMULADO)"
        else:
            return False, "Error simulado en Flash SMS"
    
    def send_with_best_method(self, number, sender_id, message, method='auto'):
        """Envía SMS usando el mejor método disponible"""
        
        modem = self.modem_pool.get_next_modem()
        if not modem:
            return False, "No hay módems disponibles"
        
        port = modem['port']
        
        # Guardar en historial
        self.sent_messages.append({
            'timestamp': datetime.now().isoformat(),
            'number': number,
            'sender_id': sender_id,
            'message': message,
            'modem': port,
            'method': method
        })
        
        # Seleccionar método
        methods = {
            'pdu': self.send_sms_pdu_mode,
            'text': self.send_sms_text_mode,
            'flash': self.send_flash_sms
        }
        
        if method == 'auto':
            # Probar PDU primero (mejor para sender ID)
            method_func = self.send_sms_pdu_mode
            method_name = 'pdu'
        else:
            method_func = methods.get(method, self.send_sms_pdu_mode)
            method_name = method
        
        success, msg = method_func(port, number, sender_id, message)
        
        if success:
            modem['messages_sent'] += 1
            self.stats['sent'] += 1
            logger.info(f"✅ SMS enviado via {method_name}: {number}")
        else:
            self.stats['failed'] += 1
            logger.error(f"❌ Error enviando SMS: {msg}")
        
        return success, msg

class SimulatedSMSGateway:
    """Gateway principal SIMULADO"""
    
    def __init__(self):
        logger.info("🚀 Iniciando SMS Gateway en MODO SIMULACIÓN...")
        logger.info("⚠️  NOTA: Este es un modo de prueba, no se envían SMS reales")
        self.modem_pool = SimulatedModemPool()
        self.sender = SimulatedSMSSender(self.modem_pool)
        self.running = False
        
    def send_single(self, number, sender_id, message, method='auto'):
        """Envía un único SMS"""
        logger.info(f"\n📤 Procesando envío individual...")
        return self.sender.send_with_best_method(number, sender_id, message, method)
    
    def send_bulk(self, numbers, sender_id, message, method='auto', delay=1):
        """Envía SMS a múltiples números"""
        logger.info(f"\n📨 Procesando envío masivo a {len(numbers)} números...")
        results = []
        
        for i, number in enumerate(numbers, 1):
            logger.info(f"  [{i}/{len(numbers)}] Enviando a {number}...")
            success, msg = self.send_single(number, sender_id, message, method)
            results.append({
                'number': number,
                'success': success,
                'message': msg,
                'timestamp': datetime.now().isoformat()
            })
            
            # Delay entre mensajes
            if i < len(numbers):
                time.sleep(delay)
        
        logger.info(f"✅ Envío masivo completado")
        return results
    
    def get_stats(self):
        """Obtiene estadísticas del gateway"""
        return {
            'mode': 'SIMULATION',
            'modems': len(self.modem_pool.modems),
            'active_modems': len([m for m in self.modem_pool.modems if m['status'] == 'active']),
            'messages_sent': self.sender.stats['sent'],
            'messages_failed': self.sender.stats['failed'],
            'last_messages': self.sender.sent_messages[-10:],  # Últimos 10 mensajes
            'modem_details': self.modem_pool.modems
        }
    
    def get_history(self):
        """Obtiene historial de mensajes enviados"""
        return self.sender.sent_messages

def main():
    """Función principal"""
    print("\n" + "="*60)
    print("   SMS GATEWAY - MODO SIMULACIÓN")
    print("="*60)
    print("⚠️  Funcionando sin módems físicos")
    print("📱 8 módems virtuales creados")
    print("✅ Listo para enviar SMS simulados\n")
    
    gateway = SimulatedSMSGateway()
    
    # Si se pasan argumentos, enviar SMS de prueba
    if len(sys.argv) > 3:
        number = sys.argv[1]
        sender_id = sys.argv[2]
        message = ' '.join(sys.argv[3:])
        
        print(f"\n📤 Enviando SMS simulado...")
        print(f"   Destino: {number}")
        print(f"   Sender ID: {sender_id}")
        print(f"   Mensaje: {message}")
        print("-"*40)
        
        success, msg = gateway.send_single(number, sender_id, message)
        
        if success:
            print(f"✅ {msg}")
        else:
            print(f"❌ {msg}")
        
        # Mostrar estadísticas
        print("\n📊 Estadísticas:")
        stats = gateway.get_stats()
        print(f"   Mensajes enviados: {stats['messages_sent']}")
        print(f"   Mensajes fallidos: {stats['messages_failed']}")
        print(f"   Módems activos: {stats['active_modems']}")
        
    else:
        print("Uso: python3 main_simulated.py <numero> <sender_id> <mensaje>")
        print("Ejemplo: python3 main_simulated.py +34600000000 BANCO 'Tu código es 1234'")
        print("\nEl gateway está listo para recibir peticiones via API")
        
        # Mostrar estadísticas iniciales
        stats = gateway.get_stats()
        print(f"\n📊 Estado inicial:")
        print(f"   Módems virtuales: {stats['modems']}")
        print(f"   Módems activos: {stats['active_modems']}")

if __name__ == "__main__":
    main()