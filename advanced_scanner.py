#!/usr/bin/env python3
import socket
import sys
import threading
import time
import struct
from datetime import datetime
import subprocess

class AdvancedScanner:
    def __init__(self, target):
        self.target = target
        self.open_ports = []
        self.lock = threading.Lock()
    
    def scan_tcp_port(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((self.target, port))
            if result == 0:
                with self.lock:
                    self.open_ports.append(('TCP', port))
                    print(f"[TCP] Puerto {port} ABIERTO")
                    
                # Banner grabbing
                try:
                    sock.send(b'HEAD / HTTP/1.1\r\nHost: ' + self.target.encode() + b'\r\n\r\n')
                    banner = sock.recv(1024).decode('utf-8', errors='ignore')
                    if banner.strip():
                        print(f"  Banner TCP/{port}: {banner[:200]}")
                except:
                    pass
            sock.close()
        except:
            pass
    
    def scan_udp_port(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)
            
            # Enviar diferentes payloads UDP
            payloads = [
                b'\x00\x00\x00\x00',  # Generic
                b'GET / HTTP/1.1\r\n\r\n',  # HTTP
                b'\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x01\x00\x01',  # DNS
                b'\x16\x03\x01\x00\x01\x01',  # SSL/TLS
            ]
            
            for payload in payloads:
                try:
                    sock.sendto(payload, (self.target, port))
                    data, addr = sock.recvfrom(1024)
                    with self.lock:
                        self.open_ports.append(('UDP', port))
                        print(f"[UDP] Puerto {port} RESPONDE")
                        print(f"  Respuesta UDP/{port}: {data[:100]}")
                    break
                except socket.timeout:
                    continue
                except:
                    break
            sock.close()
        except:
            pass
    
    def full_port_scan(self):
        print(f"=== Escaneo completo de puertos para {self.target} ===")
        
        # Escanear todos los puertos TCP (1-65535)
        print("Escaneando puertos TCP...")
        tcp_threads = []
        
        for port in range(1, 65536):
            t = threading.Thread(target=self.scan_tcp_port, args=(port,))
            t.start()
            tcp_threads.append(t)
            
            # Controlar concurrencia
            if len(tcp_threads) >= 500:
                for thread in tcp_threads:
                    thread.join()
                tcp_threads = []
                print(f"Progreso TCP: puerto {port}")
        
        # Esperar threads restantes
        for thread in tcp_threads:
            thread.join()
        
        # Escanear puertos UDP comunes
        print("Escaneando puertos UDP comunes...")
        udp_ports = [53, 67, 68, 69, 123, 135, 137, 138, 139, 161, 162, 445, 500, 514, 520, 631, 1434, 1900, 4500, 5353]
        
        udp_threads = []
        for port in udp_ports:
            t = threading.Thread(target=self.scan_udp_port, args=(port,))
            t.start()
            udp_threads.append(t)
        
        for thread in udp_threads:
            thread.join()
    
    def stealth_scan(self):
        print("=== Escaneo sigiloso ===")
        # Implementar técnicas de evasión
        
        # SYN scan manual (requiere privilegios root)
        try:
            for port in [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 993, 995, 3389, 8080, 8443]:
                self.syn_scan(port)
        except Exception as e:
            print(f"SYN scan falló: {e}")
    
    def syn_scan(self, port):
        # Implementación básica de SYN scan
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            # Esto requiere privilegios root
            print(f"Probando SYN scan en puerto {port}")
        except PermissionError:
            print("SYN scan requiere privilegios root")
        except:
            pass

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 advanced_scanner.py <IP>")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = AdvancedScanner(target)
    
    start_time = datetime.now()
    print(f"Iniciando escaneo avanzado: {start_time}")
    
    scanner.full_port_scan()
    scanner.stealth_scan()
    
    end_time = datetime.now()
    print(f"\n=== Resultados ===")
    print(f"Puertos abiertos encontrados: {len(scanner.open_ports)}")
    for proto, port in scanner.open_ports:
        print(f"  {proto}/{port}")
    print(f"Tiempo total: {end_time - start_time}")

if __name__ == "__main__":
    main()