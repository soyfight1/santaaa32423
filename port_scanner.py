#!/usr/bin/env python3
import socket
import sys
import threading
from datetime import datetime

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"
            print(f"Puerto {port}/tcp ABIERTO - {service}")
            
            # Intentar banner grabbing
            try:
                sock.send(b'GET / HTTP/1.1\r\nHost: ' + target.encode() + b'\r\n\r\n')
                banner = sock.recv(1024).decode('utf-8', errors='ignore')
                if banner.strip():
                    print(f"  Banner: {banner[:100]}...")
            except:
                pass
                
        sock.close()
    except:
        pass

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 port_scanner.py <IP>")
        sys.exit(1)
    
    target = sys.argv[1]
    print(f"Escaneando {target}...")
    print(f"Iniciado: {datetime.now()}")
    print("-" * 50)
    
    # Puertos comunes a escanear
    common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995, 1723, 3306, 3389, 5432, 5900, 8080, 8443, 8888, 9090]
    
    # Top 1000 ports
    top_ports = list(range(1, 1025))
    all_ports = sorted(set(common_ports + top_ports))
    
    threads = []
    for port in all_ports:
        t = threading.Thread(target=scan_port, args=(target, port))
        t.start()
        threads.append(t)
        
        # Limitar threads concurrentes
        if len(threads) >= 100:
            for thread in threads:
                thread.join()
            threads = []
    
    # Esperar threads restantes
    for thread in threads:
        thread.join()
    
    print("-" * 50)
    print(f"Escaneo completado: {datetime.now()}")

if __name__ == "__main__":
    main()