#!/usr/bin/env python3
import socket
import sys
import threading
import time
import random
import struct
import subprocess
from datetime import datetime

class InnovativeScanner:
    def __init__(self, target):
        self.target = target
        self.discoveries = []
        self.lock = threading.Lock()
    
    def icmp_timestamp_probe(self):
        """Sonda ICMP timestamp (tipo 13)"""
        print("=== Sonda ICMP Timestamp ===")
        try:
            # Crear socket raw ICMP (requiere privilegios)
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            
            # Construir paquete ICMP timestamp
            icmp_type = 13  # Timestamp request
            icmp_code = 0
            icmp_checksum = 0
            icmp_id = random.randint(1, 65535)
            icmp_seq = 1
            
            # Timestamp actual (millisegundos desde medianoche UTC)
            timestamp = int(time.time() * 1000) % (24 * 60 * 60 * 1000)
            
            # Construir header ICMP
            icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)
            icmp_data = struct.pack('!III', timestamp, 0, 0)
            
            # Calcular checksum
            packet = icmp_header + icmp_data
            checksum = self.calculate_checksum(packet)
            icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, checksum, icmp_id, icmp_seq)
            packet = icmp_header + icmp_data
            
            sock.sendto(packet, (self.target, 0))
            sock.settimeout(5)
            
            try:
                data, addr = sock.recvfrom(1024)
                print(f"[+] ICMP Timestamp respuesta de {addr[0]}")
                with self.lock:
                    self.discoveries.append(f"ICMP Timestamp response from {addr[0]}")
            except socket.timeout:
                print("[-] Sin respuesta ICMP Timestamp")
            
            sock.close()
            
        except PermissionError:
            print("[-] Sin privilegios para socket ICMP raw")
        except Exception as e:
            print(f"[-] Error ICMP Timestamp: {e}")
    
    def calculate_checksum(self, data):
        """Calcular checksum para ICMP"""
        checksum = 0
        for i in range(0, len(data), 2):
            if i + 1 < len(data):
                checksum += (data[i] << 8) + data[i + 1]
            else:
                checksum += data[i] << 8
        
        checksum = (checksum >> 16) + (checksum & 0xFFFF)
        checksum += checksum >> 16
        return ~checksum & 0xFFFF
    
    def arp_discovery(self):
        """Descubrimiento ARP (solo funciona en la misma red)"""
        print("=== Descubrimiento ARP ===")
        try:
            result = subprocess.run(['arp', '-n', self.target], 
                                  capture_output=True, text=True, timeout=5)
            if result.stdout and "no entry" not in result.stdout.lower():
                print(f"[+] Entrada ARP encontrada: {result.stdout.strip()}")
                with self.lock:
                    self.discoveries.append(f"ARP entry: {result.stdout.strip()}")
            else:
                print("[-] Sin entrada ARP")
        except:
            print("[-] Error en lookup ARP")
    
    def protocol_tunneling_detection(self):
        """Detección de túneles de protocolo"""
        print("=== Detección de Túneles de Protocolo ===")
        
        # Probar diferentes protocolos que podrían estar tunelizados
        tunnel_tests = [
            # DNS sobre TCP (puerto 53)
            (53, 'tcp', b'\x00\x1c\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x01\x00\x01'),
            
            # HTTP sobre puertos no estándar
            (8080, 'tcp', b'GET / HTTP/1.1\r\nHost: ' + self.target.encode() + b'\r\n\r\n'),
            (8443, 'tcp', b'GET / HTTP/1.1\r\nHost: ' + self.target.encode() + b'\r\n\r\n'),
            (9090, 'tcp', b'GET / HTTP/1.1\r\nHost: ' + self.target.encode() + b'\r\n\r\n'),
            
            # SSH sobre puertos alternativos
            (2222, 'tcp', b'SSH-2.0-Test\r\n'),
            (2200, 'tcp', b'SSH-2.0-Test\r\n'),
            
            # HTTPS sobre puertos alternativos
            (8443, 'tcp', b'GET / HTTP/1.1\r\nHost: ' + self.target.encode() + b'\r\n\r\n'),
        ]
        
        for port, protocol, payload in tunnel_tests:
            try:
                if protocol == 'tcp':
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                sock.settimeout(3)
                
                if protocol == 'tcp':
                    result = sock.connect_ex((self.target, port))
                    if result == 0:
                        sock.send(payload)
                        try:
                            response = sock.recv(1024)
                            if response:
                                print(f"[+] Posible túnel en puerto {port}: {len(response)} bytes")
                                with self.lock:
                                    self.discoveries.append(f"Tunnel detected on port {port}")
                        except:
                            pass
                else:
                    sock.sendto(payload, (self.target, port))
                    try:
                        data, addr = sock.recvfrom(1024)
                        print(f"[+] Respuesta UDP en puerto {port}: {len(data)} bytes")
                        with self.lock:
                            self.discoveries.append(f"UDP response on port {port}")
                    except socket.timeout:
                        pass
                
                sock.close()
            except:
                pass
    
    def covert_channel_detection(self):
        """Detección de canales encubiertos"""
        print("=== Detección de Canales Encubiertos ===")
        
        # Probar diferentes técnicas de canal encubierto
        
        # 1. ICMP Data Channel
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            # Enviar ICMP con datos específicos
            print("Probando canal ICMP encubierto...")
            sock.close()
        except:
            print("[-] Sin privilegios para canal ICMP")
        
        # 2. DNS TXT Records
        print("Probando canal DNS TXT...")
        try:
            result = subprocess.run(['dig', '+short', 'TXT', f"test.{self.target}"], 
                                  capture_output=True, text=True, timeout=5)
            if result.stdout.strip():
                print(f"[+] Posible canal DNS TXT: {result.stdout.strip()}")
        except:
            pass
        
        # 3. HTTP Headers
        print("Probando canales HTTP encubiertos...")
        http_ports = [80, 8080, 8000, 8443]
        for port in http_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                result = sock.connect_ex((self.target, port))
                if result == 0:
                    # Enviar petición HTTP con headers especiales
                    request = f"GET / HTTP/1.1\r\nHost: {self.target}\r\nX-Covert: test\r\n\r\n"
                    sock.send(request.encode())
                    try:
                        response = sock.recv(2048).decode('utf-8', errors='ignore')
                        if 'x-covert' in response.lower():
                            print(f"[+] Posible canal HTTP en puerto {port}")
                            with self.lock:
                                self.discoveries.append(f"HTTP covert channel on port {port}")
                    except:
                        pass
                sock.close()
            except:
                pass
    
    def timing_attack_analysis(self):
        """Análisis de ataques de timing"""
        print("=== Análisis de Timing para Detección de Servicios ===")
        
        # Medir tiempos de respuesta para diferentes tipos de paquetes
        timing_data = {}
        
        test_ports = [22, 80, 443, 21, 25, 53, 3389]
        
        for port in test_ports:
            times = []
            
            # Hacer múltiples mediciones
            for _ in range(5):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    
                    start_time = time.time()
                    result = sock.connect_ex((self.target, port))
                    end_time = time.time()
                    
                    times.append(end_time - start_time)
                    sock.close()
                except:
                    times.append(2.0)
            
            avg_time = sum(times) / len(times)
            std_dev = (sum((t - avg_time) ** 2 for t in times) / len(times)) ** 0.5
            
            timing_data[port] = {
                'avg': avg_time,
                'std_dev': std_dev,
                'times': times
            }
            
            # Análisis del patrón de timing
            if std_dev < 0.01 and avg_time > 1.5:
                status = "FILTRADO (timing consistente)"
            elif std_dev > 0.1:
                status = "POSIBLE SERVICIO (timing variable)"
            elif avg_time < 0.1:
                status = "CERRADO (respuesta rápida)"
            else:
                status = "INCIERTO"
            
            print(f"Puerto {port}: avg={avg_time:.3f}s, std={std_dev:.3f}s - {status}")
    
    def innovative_discovery(self):
        """Ejecutar todas las técnicas innovadoras"""
        print(f"=== Escaneo Innovador para {self.target} ===")
        print(f"Iniciado: {datetime.now()}")
        print("=" * 60)
        
        # Ejecutar técnicas innovadoras
        self.arp_discovery()
        self.icmp_timestamp_probe()
        self.protocol_tunneling_detection()
        self.covert_channel_detection()
        self.timing_attack_analysis()
        
        # Resumen
        print(f"\n=== Resultados Innovadores ===")
        print(f"Descubrimientos: {len(self.discoveries)}")
        for discovery in self.discoveries:
            print(f"  [+] {discovery}")
        
        if not self.discoveries:
            print("[!] No se encontraron vectores alternativos")
            print("[!] El objetivo parece estar completamente aislado o inactivo")

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 innovative_scanner.py <IP>")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = InnovativeScanner(target)
    scanner.innovative_discovery()

if __name__ == "__main__":
    main()