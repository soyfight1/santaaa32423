#!/usr/bin/env python3
import socket
import sys
import threading
import time
from datetime import datetime

class QuickScanner:
    def __init__(self, target):
        self.target = target
        self.open_ports = []
        self.lock = threading.Lock()
    
    def scan_port(self, port, timeout=2):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((self.target, port))
            if result == 0:
                with self.lock:
                    self.open_ports.append(port)
                    print(f"[ABIERTO] Puerto {port}/tcp")
                    
                # Banner grabbing básico
                try:
                    if port in [80, 8080, 8000, 8443]:
                        sock.send(b'GET / HTTP/1.1\r\nHost: ' + self.target.encode() + b'\r\n\r\n')
                    elif port == 22:
                        pass  # SSH banner viene automáticamente
                    elif port == 21:
                        pass  # FTP banner viene automáticamente
                    else:
                        sock.send(b'\r\n')
                    
                    banner = sock.recv(1024).decode('utf-8', errors='ignore')
                    if banner.strip():
                        print(f"  Banner: {banner[:150].strip()}")
                except:
                    pass
            sock.close()
        except:
            pass
    
    def scan_top_ports(self):
        # Top 100 puertos más comunes
        top_ports = [
            21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995,
            1723, 3306, 3389, 5432, 5900, 8080, 8443, 8888, 9090, 445, 993,
            143, 587, 465, 110, 995, 20, 69, 161, 162, 137, 138, 139, 445,
            1433, 1434, 3389, 5985, 5986, 47001, 49152, 49153, 49154, 49155,
            49156, 49157, 2049, 2121, 3690, 5060, 6000, 6001, 6002, 6003,
            6004, 6005, 6006, 6007, 6009, 6025, 6059, 6100, 6101, 6106,
            6112, 6646, 7000, 7001, 7002, 7004, 7007, 7019, 7025, 7070,
            7100, 7103, 7106, 7200, 7201, 7402, 7435, 7443, 7496, 7512,
            7625, 7627, 7676, 7741, 7777, 7778, 7800, 7911, 7920, 7921,
            7937, 7938, 7999, 8000, 8001, 8002, 8007, 8008, 8009, 8010
        ]
        
        print(f"Escaneando top {len(top_ports)} puertos en {self.target}...")
        threads = []
        
        for port in top_ports:
            t = threading.Thread(target=self.scan_port, args=(port,))
            t.start()
            threads.append(t)
            
            # Limitar concurrencia
            if len(threads) >= 50:
                for thread in threads:
                    thread.join()
                threads = []
        
        # Esperar threads restantes
        for thread in threads:
            thread.join()
    
    def scan_range(self, start_port, end_port):
        print(f"Escaneando puertos {start_port}-{end_port}...")
        threads = []
        
        for port in range(start_port, end_port + 1):
            t = threading.Thread(target=self.scan_port, args=(port, 1))
            t.start()
            threads.append(t)
            
            if len(threads) >= 100:
                for thread in threads:
                    thread.join()
                threads = []
                if port % 1000 == 0:
                    print(f"  Progreso: puerto {port}")
        
        for thread in threads:
            thread.join()

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 quick_scanner.py <IP> [full]")
        sys.exit(1)
    
    target = sys.argv[1]
    full_scan = len(sys.argv) > 2 and sys.argv[2] == 'full'
    
    scanner = QuickScanner(target)
    start_time = datetime.now()
    
    print(f"=== Escaneo rápido de {target} ===")
    print(f"Iniciado: {start_time}")
    
    # Escaneo de puertos top
    scanner.scan_top_ports()
    
    if full_scan:
        print("\n=== Escaneo completo (1-65535) ===")
        scanner.scan_range(1, 65535)
    
    end_time = datetime.now()
    
    print(f"\n=== Resultados ===")
    print(f"Puertos abiertos: {len(scanner.open_ports)}")
    for port in sorted(scanner.open_ports):
        print(f"  {port}/tcp")
    print(f"Tiempo: {end_time - start_time}")

if __name__ == "__main__":
    main()