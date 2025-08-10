#!/usr/bin/env python3
import serial
import time

def send_pdu_spoofed(port, number, sender, text):
    """PDU mode - funciona mejor para sender falso"""
    
    ser = serial.Serial(port, 115200, timeout=2)
    
    # Modo PDU
    ser.write(b'AT+CMGF=0\r')
    time.sleep(0.2)
    
    # Construir PDU con sender falso
    sender_bytes = sender.encode('utf-16-be').hex()
    text_bytes = text.encode('utf-16-be').hex()
    
    # PDU header con sender spoofed
    pdu = "0051000B91" + swap_nibbles(number[1:]) + "F00008" + sender_bytes + text_bytes
    
    # Enviar
    ser.write(f'AT+CMGS={len(pdu)//2-1}\r'.encode())
    time.sleep(0.5)
    ser.write(f'{pdu}\x1a'.encode())
    
    ser.close()

def swap_nibbles(number):
    """Helper para formato número"""
    if len(number) % 2:
        number += 'F'
    return ''.join([number[i+1] + number[i] for i in range(0, len(number), 2)])

# Usar
send_pdu_spoofed("/dev/ttyUSB0", "+34600000000", "AMAZON", "Tu paquete llegó")