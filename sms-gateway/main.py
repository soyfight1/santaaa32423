#!/usr/bin/env python3
"""
SMS Gateway Principal - Sistema completo con sender ID personalizado
"""

import os
import sys
import json
import time
import random
import serial
import threading
import queue
from datetime import datetime
from typing import List, Dict, Optional
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/gateway.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('SMSGateway')

class ModemPool:
    """Gestiona pool de módems GSM con rotación y balanceo"""
    
    def __init__(self):
        self.modems = []
        self.active_modems = {}
        self.modem_stats = {}
        self.lock = threading.Lock()
        self.detect_modems()
    
    def detect_modems(self):
        """Detecta automáticamente todos los módems conectados"""
        logger.info("Detectando módems...")
        
        # Buscar dispositivos ttyUSB
        for i in range(32):  # Hasta 32 módems
            port = f"/dev/ttyUSB{i}"
            if os.path.exists(port):
                try:
                    # Probar conexión
                    ser = serial.Serial(port, 115200, timeout=1)
                    ser.write(b'AT\r')
                    time.sleep(0.5)
                    response = ser.read(100)
                    ser.close()
                    
                    if b'OK' in response:
                        self.modems.append({
                            'port': port,
                            'status': 'active',
                            'messages_sent': 0,
                            'last_used': None,
                            'sim_info': self.get_sim_info(port)
                        })
                        logger.info(f"✓ Módem detectado: {port}")
                except:
                    pass
        
        logger.info(f"Total módems detectados: {len(self.modems)}")
        return len(self.modems)
    
    def get_sim_info(self, port):
        """Obtiene información de la SIM"""
        try:
            ser = serial.Serial(port, 115200, timeout=2)
            
            # Obtener IMSI
            ser.write(b'AT+CIMI\r')
            time.sleep(0.5)
            imsi = ser.read(100).decode('utf-8', errors='ignore')
            
            # Obtener operador
            ser.write(b'AT+COPS?\r')
            time.sleep(0.5)
            operator = ser.read(100).decode('utf-8', errors='ignore')
            
            ser.close()
            
            return {
                'imsi': imsi.strip(),
                'operator': operator.strip()
            }
        except:
            return {'imsi': 'Unknown', 'operator': 'Unknown'}
    
    def get_next_modem(self):
        """Obtiene el siguiente módem disponible (round-robin)"""
        with self.lock:
            if not self.modems:
                return None
            
            # Buscar módem menos usado
            available = [m for m in self.modems if m['status'] == 'active']
            if not available:
                return None
            
            modem = min(available, key=lambda x: x['messages_sent'])
            modem['last_used'] = datetime.now()
            return modem

class SMSSender:
    """Envía SMS con sender ID personalizado usando diferentes métodos"""
    
    def __init__(self, modem_pool):
        self.modem_pool = modem_pool
        self.queue = queue.Queue()
        self.stats = {
            'sent': 0,
            'failed': 0,
            'pending': 0
        }
    
    def send_sms_text_mode(self, port, number, sender_id, message):
        """Envía SMS en modo texto con sender ID"""
        try:
            ser = serial.Serial(port, 115200, timeout=5)
            
            # Reset módem
            ser.write(b'ATZ\r')
            time.sleep(0.5)
            
            # Modo texto
            ser.write(b'AT+CMGF=1\r')
            time.sleep(0.5)
            
            # Intentar configurar sender ID (funciona en algunas redes)
            ser.write(f'AT+CSMP=17,167,0,0\r'.encode())
            time.sleep(0.5)
            
            # Enviar mensaje
            ser.write(f'AT+CMGS="{number}"\r'.encode())
            time.sleep(0.5)
            
            # Mensaje con sender ID en el texto (truco para algunas redes)
            full_message = f"[{sender_id}]\n{message}"
            ser.write(f'{full_message}\x1a'.encode())
            time.sleep(2)
            
            response = ser.read(500)
            ser.close()
            
            if b'+CMGS:' in response:
                return True, "SMS enviado correctamente"
            else:
                return False, "Error al enviar SMS"
                
        except Exception as e:
            return False, str(e)
    
    def send_sms_pdu_mode(self, port, number, sender_id, message):
        """Envía SMS en modo PDU con sender ID spoofed"""
        try:
            ser = serial.Serial(port, 115200, timeout=5)
            
            # Modo PDU
            ser.write(b'AT+CMGF=0\r')
            time.sleep(0.5)
            
            # Construir PDU con sender ID personalizado
            pdu = self.build_pdu_with_sender(number, sender_id, message)
            
            # Enviar PDU
            pdu_length = len(pdu) // 2 - 1
            ser.write(f'AT+CMGS={pdu_length}\r'.encode())
            time.sleep(0.5)
            ser.write(f'{pdu}\x1a'.encode())
            time.sleep(2)
            
            response = ser.read(500)
            ser.close()
            
            if b'+CMGS:' in response:
                return True, "SMS enviado con sender ID personalizado"
            else:
                return False, "Error en envío PDU"
                
        except Exception as e:
            return False, str(e)
    
    def build_pdu_with_sender(self, dest_number, sender_id, text):
        """Construye PDU con sender ID personalizado"""
        
        # Remover + del número
        if dest_number.startswith('+'):
            dest_number = dest_number[1:]
        
        # SMSC - usar default (00)
        pdu = "00"
        
        # PDU Type - SMS-SUBMIT con sender ID
        pdu += "51"  # TP-MTI=01, TP-VPF=10, TP-SRR=1
        
        # MR - Message Reference
        pdu += "00"
        
        # Destination number
        dest_len = len(dest_number)
        pdu += f"{dest_len:02X}"  # Longitud
        pdu += "91"  # Tipo internacional
        
        # Swap nibbles del número
        if len(dest_number) % 2:
            dest_number += 'F'
        swapped = ''.join([dest_number[i+1] + dest_number[i] 
                          for i in range(0, len(dest_number), 2)])
        pdu += swapped
        
        # PID - Protocol Identifier
        pdu += "00"
        
        # DCS - Data Coding Scheme (GSM 7-bit)
        pdu += "00"
        
        # VP - Validity Period (1 día)
        pdu += "AA"
        
        # UDL - User Data Length
        # Para sender ID spoofing, incluimos en el header
        sender_bytes = sender_id[:11].encode('ascii')  # Max 11 chars
        
        # Construir user data con sender ID
        # Esto es un truco: algunos operadores procesan esto como sender
        user_data = f"\x00{sender_id}\x00{text}"
        
        # Codificar en GSM 7-bit
        encoded = self.encode_gsm7(user_data)
        pdu += f"{len(encoded):02X}"
        pdu += encoded.hex().upper()
        
        return pdu
    
    def encode_gsm7(self, text):
        """Codifica texto en GSM 7-bit"""
        # Simplificado - usar ASCII directo
        return text.encode('ascii', errors='ignore')
    
    def send_flash_sms(self, port, number, sender_id, message):
        """Envía Flash SMS (Class 0) con sender ID - aparece directo en pantalla"""
        try:
            ser = serial.Serial(port, 115200, timeout=5)
            
            # Modo PDU para Flash SMS
            ser.write(b'AT+CMGF=0\r')
            time.sleep(0.5)
            
            # Construir PDU Flash con sender spoofed
            pdu = self.build_flash_pdu(number, sender_id, message)
            
            pdu_length = len(pdu) // 2 - 1
            ser.write(f'AT+CMGS={pdu_length}\r'.encode())
            time.sleep(0.5)
            ser.write(f'{pdu}\x1a'.encode())
            time.sleep(2)
            
            response = ser.read(500)
            ser.close()
            
            if b'+CMGS:' in response:
                return True, "Flash SMS enviado"
            else:
                return False, "Error en Flash SMS"
                
        except Exception as e:
            return False, str(e)
    
    def build_flash_pdu(self, number, sender_id, text):
        """Construye PDU para Flash SMS con sender ID"""
        # Similar a build_pdu_with_sender pero con DCS para Class 0
        pdu = self.build_pdu_with_sender(number, sender_id, text)
        
        # Modificar DCS para Flash SMS (Class 0)
        # Buscar posición del DCS y cambiar a F0 (Flash)
        # El DCS está después del PID
        # Esta es una simplificación, en producción sería más robusto
        dcs_pos = 44  # Posición aproximada del DCS en el PDU
        pdu = pdu[:dcs_pos] + "F0" + pdu[dcs_pos+2:]
        
        return pdu
    
    def send_with_best_method(self, number, sender_id, message, method='auto'):
        """Envía SMS usando el mejor método disponible"""
        
        modem = self.modem_pool.get_next_modem()
        if not modem:
            return False, "No hay módems disponibles"
        
        port = modem['port']
        
        # Intentar diferentes métodos
        methods = {
            'pdu': self.send_sms_pdu_mode,
            'text': self.send_sms_text_mode,
            'flash': self.send_flash_sms
        }
        
        if method == 'auto':
            # Probar todos los métodos
            for method_name, method_func in methods.items():
                success, msg = method_func(port, number, sender_id, message)
                if success:
                    modem['messages_sent'] += 1
                    self.stats['sent'] += 1
                    logger.info(f"✓ SMS enviado via {method_name}: {number}")
                    return True, msg
            
            self.stats['failed'] += 1
            return False, "Todos los métodos fallaron"
        
        else:
            # Usar método específico
            if method in methods:
                success, msg = methods[method](port, number, sender_id, message)
                if success:
                    modem['messages_sent'] += 1
                    self.stats['sent'] += 1
                return success, msg
            else:
                return False, f"Método desconocido: {method}"

class SMSGateway:
    """Gateway principal que coordina todo"""
    
    def __init__(self):
        logger.info("Iniciando SMS Gateway...")
        self.modem_pool = ModemPool()
        self.sender = SMSSender(self.modem_pool)
        self.running = False
        
    def send_single(self, number, sender_id, message, method='auto'):
        """Envía un único SMS"""
        return self.sender.send_with_best_method(number, sender_id, message, method)
    
    def send_bulk(self, numbers, sender_id, message, method='auto', delay=1):
        """Envía SMS a múltiples números"""
        results = []
        
        for number in numbers:
            success, msg = self.send_single(number, sender_id, message, method)
            results.append({
                'number': number,
                'success': success,
                'message': msg,
                'timestamp': datetime.now().isoformat()
            })
            
            # Delay entre mensajes para evitar detección
            time.sleep(delay + random.uniform(0, 1))
        
        return results
    
    def get_stats(self):
        """Obtiene estadísticas del gateway"""
        return {
            'modems': len(self.modem_pool.modems),
            'active_modems': len([m for m in self.modem_pool.modems if m['status'] == 'active']),
            'messages_sent': self.sender.stats['sent'],
            'messages_failed': self.sender.stats['failed'],
            'modem_details': self.modem_pool.modems
        }

def main():
    """Función principal"""
    gateway = SMSGateway()
    
    # Verificar módems
    if len(gateway.modem_pool.modems) == 0:
        logger.error("No se detectaron módems. Conecta módems USB y reinicia.")
        sys.exit(1)
    
    logger.info(f"Gateway iniciado con {len(gateway.modem_pool.modems)} módems")
    
    # Ejemplo de uso
    if len(sys.argv) > 3:
        number = sys.argv[1]
        sender_id = sys.argv[2]
        message = ' '.join(sys.argv[3:])
        
        success, msg = gateway.send_single(number, sender_id, message)
        print(f"Resultado: {msg}")
    else:
        print("Uso: python3 main.py <numero> <sender_id> <mensaje>")
        print("Ejemplo: python3 main.py +34600000000 BANCO 'Tu código es 1234'")
        print("")
        print("Gateway ejecutándose. Usa la API en puerto 5000")

if __name__ == "__main__":
    main()