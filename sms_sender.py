#!/usr/bin/env python3
import serial
import time
import random

# Tus módems
MODEMS = [
    "/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2", "/dev/ttyUSB3",
    "/dev/ttyUSB4", "/dev/ttyUSB5", "/dev/ttyUSB6", "/dev/ttyUSB7"
]

def send_sms_spoofed(port, number, sender_id, message):
    """Envía SMS con sender ID falso"""
    ser = serial.Serial(port, 115200, timeout=2)
    
    # Modo texto extendido
    ser.write(b'AT+CMGF=1\r')
    time.sleep(0.2)
    
    # Intentar setear sender (funciona en algunas redes)
    ser.write(f'AT+CSCA="{sender_id}"\r'.encode())
    time.sleep(0.2)
    
    # Enviar mensaje
    ser.write(f'AT+CMGS="{number}"\r'.encode())
    time.sleep(0.5)
    ser.write(f'{message}\x1a'.encode())
    time.sleep(1)
    
    ser.close()
    return True

def send_bulk(numbers, sender_id, message):
    """Envía a múltiples números rotando módems"""
    for i, number in enumerate(numbers):
        modem = MODEMS[i % len(MODEMS)]  # Rotar módems
        send_sms_spoofed(modem, number, sender_id, message)
        time.sleep(random.uniform(1, 3))  # Random delay

# Usar
numbers = ["+34600000000", "+34600000001"]  
send_bulk(numbers, "BANCO", "Tu código es 1234")