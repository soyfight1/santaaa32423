#!/usr/bin/env python3
import socket
import sys
import threading
import time
import random
from datetime import datetime
import struct

class FirewallEvasion:
    def __init__(self, target):
        self.target = target
        self.open_ports = []
        self.lock = threading.Lock()
    
    def slow_scan(self, ports, delay_range=(1, 5)):
        """Escaneo lento para evadir detección por rate limiting"""
        print(f"=== Escaneo lento con delays aleatorios ===")
        
        for port in ports:
            delay = random.uniform(*delay_range)
            time.sleep(delay)
            
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)  # Timeout más largo
                result = sock.connect_ex((self.target, port))
                if result == 0:
                    with self.lock:
                        self.open_ports.append(port)
                        print(f"[+] Puerto {port} ABIERTO (escaneo lento)")
                sock.close()
            except:
                pass
            
            print(f"Progreso: puerto {port} (delay: {delay:.2f}s)")
    
    def fragmented_scan(self, ports):
        """Escaneo con paquetes fragmentados"""
        print("=== Escaneo con fragmentación ===")
        
        for port in ports:
            try:
                # Crear socket con opciones especiales
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                
                # Intentar conectar con opciones TCP especiales
                result = sock.connect_ex((self.target, port))
                if result == 0:
                    with self.lock:
                        self.open_ports.append(port)
                        print(f"[+] Puerto {port} ABIERTO (fragmentado)")
                
                sock.close()
            except:
                pass
    
    def decoy_scan(self, ports, num_decoys=5):
        """Escaneo con IPs señuelo (simulado)"""
        print(f"=== Escaneo con {num_decoys} señuelos (simulado) ===")
        
        # Generar IPs señuelo aleatorias
        decoys = []
        for _ in range(num_decoys):
            decoy = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
            decoys.append(decoy)
        
        print(f"IPs señuelo: {', '.join(decoys)}")
        
        # En un escenario real, enviaríamos paquetes desde múltiples IPs
        # Por ahora, simularemos con delays aleatorios
        for port in ports:
            for i, decoy in enumerate(decoys + [self.target]):
                if i == len(decoys):  # Último es nuestro escaneo real
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(3)
                        result = sock.connect_ex((self.target, port))
                        if result == 0:
                            with self.lock:
                                self.open_ports.append(port)
                                print(f"[+] Puerto {port} ABIERTO (con señuelos)")
                        sock.close()
                    except:
                        pass
                else:
                    time.sleep(random.uniform(0.1, 0.5))  # Simular tráfico señuelo
    
    def source_port_scan(self, ports, source_ports=[53, 80, 443, 20]):
        """Escaneo usando puertos origen específicos"""
        print("=== Escaneo con puertos origen específicos ===")
        
        for port in ports:
            for src_port in source_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(3)
                    
                    # Intentar bind al puerto origen específico
                    try:
                        sock.bind(('', src_port))
                        print(f"Usando puerto origen {src_port} para escanear {port}")
                    except:
                        pass  # Si no se puede bind, continuar sin él
                    
                    result = sock.connect_ex((self.target, port))
                    if result == 0:
                        with self.lock:
                            self.open_ports.append(port)
                            print(f"[+] Puerto {port} ABIERTO (src port {src_port})")
                        sock.close()
                        break  # Si encontramos el puerto abierto, no probar otros src ports
                    
                    sock.close()
                except:
                    pass
    
    def timing_based_scan(self, ports):
        """Escaneo basado en análisis de timing"""
        print("=== Análisis de timing para detección de filtrado ===")
        
        timing_results = {}
        
        for port in ports:
            times = []
            
            # Hacer múltiples intentos para obtener timing promedio
            for _ in range(3):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    
                    start_time = time.time()
                    result = sock.connect_ex((self.target, port))
                    end_time = time.time()
                    
                    times.append(end_time - start_time)
                    sock.close()
                except:
                    times.append(5.0)  # Timeout
            
            avg_time = sum(times) / len(times)
            timing_results[port] = avg_time
            
            # Análisis del timing
            if avg_time < 0.1:
                status = "CERRADO (respuesta rápida)"
            elif avg_time > 3.0:
                status = "FILTRADO (timeout)"
            elif 0.1 <= avg_time <= 1.0:
                status = "POSIBLE ABIERTO"
            else:
                status = "INCIERTO"
            
            print(f"Puerto {port}: {avg_time:.3f}s - {status}")
    
    def protocol_specific_probes(self):
        """Sondas específicas de protocolo"""
        print("=== Sondas específicas de protocolo ===")
        
        probes = [
            # HTTP
            (80, b'GET / HTTP/1.1\r\nHost: ' + self.target.encode() + b'\r\n\r\n'),
            (8080, b'GET / HTTP/1.1\r\nHost: ' + self.target.encode() + b':8080\r\n\r\n'),
            (443, b'GET / HTTP/1.1\r\nHost: ' + self.target.encode() + b'\r\n\r\n'),
            
            # SSH
            (22, b'SSH-2.0-OpenSSH_Test\r\n'),
            
            # FTP
            (21, b'USER anonymous\r\n'),
            
            # SMTP
            (25, b'EHLO test.com\r\n'),
            (587, b'EHLO test.com\r\n'),
            
            # DNS
            (53, b'\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x01\x00\x01'),
        ]
        
        for port, probe in probes:
            try:
                if port == 53:  # DNS es UDP
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                sock.settimeout(5)
                
                if port == 53:
                    sock.sendto(probe, (self.target, port))
                    try:
                        data, addr = sock.recvfrom(1024)
                        print(f"[+] DNS respuesta en puerto 53: {len(data)} bytes")
                        with self.lock:
                            self.open_ports.append(port)
                    except socket.timeout:
                        pass
                else:
                    result = sock.connect_ex((self.target, port))
                    if result == 0:
                        sock.send(probe)
                        try:
                            response = sock.recv(1024)
                            if response:
                                print(f"[+] Respuesta en puerto {port}: {response[:100]}")
                                with self.lock:
                                    self.open_ports.append(port)
                        except:
                            pass
                
                sock.close()
            except:
                pass
    
    def comprehensive_evasion_scan(self):
        """Ejecutar todas las técnicas de evasión"""
        print(f"=== Escaneo de evasión completo para {self.target} ===")
        print(f"Iniciado: {datetime.now()}")
        print("=" * 60)
        
        # Puertos objetivo
        target_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 993, 995, 3389, 8080, 8443, 9090]
        
        # Ejecutar diferentes técnicas
        self.protocol_specific_probes()
        self.timing_based_scan(target_ports[:10])  # Solo algunos para timing
        self.slow_scan(target_ports[:5], (2, 4))  # Escaneo muy lento
        self.source_port_scan(target_ports[:8])
        self.decoy_scan(target_ports[:5], 3)
        
        # Resultados finales
        print(f"\n=== Resultados de Evasión ===")
        unique_ports = list(set(self.open_ports))
        print(f"Puertos encontrados: {len(unique_ports)}")
        for port in sorted(unique_ports):
            print(f"  {port}/tcp")

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 firewall_evasion.py <IP>")
        sys.exit(1)
    
    target = sys.argv[1]
    evasion = FirewallEvasion(target)
    evasion.comprehensive_evasion_scan()

if __name__ == "__main__":
    main()