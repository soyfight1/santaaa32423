#!/usr/bin/env python3
import socket
import sys
import subprocess
import threading
import time
from datetime import datetime
import struct

class NetworkDiscovery:
    def __init__(self, target):
        self.target = target
        self.results = {}
    
    def icmp_ping(self):
        """Intentar ping ICMP usando diferentes métodos"""
        print("=== Pruebas de conectividad ICMP ===")
        
        # Método 1: ping tradicional (puede fallar sin privilegios)
        try:
            result = subprocess.run(['ping', '-c', '1', '-W', '3', self.target], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"[+] ICMP ping exitoso: {self.target}")
                return True
        except:
            pass
        
        # Método 2: ping sin privilegios usando socket raw (fallará sin root)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            print(f"[+] Socket ICMP raw creado exitosamente")
            sock.close()
        except PermissionError:
            print("[-] Sin privilegios para ICMP raw socket")
        except:
            print("[-] Error creando ICMP socket")
        
        return False
    
    def tcp_ping(self, ports=[80, 443, 22, 21, 25, 53, 8080, 8443]):
        """TCP ping a puertos comunes"""
        print("=== TCP Ping ===")
        responsive_ports = []
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                result = sock.connect_ex((self.target, port))
                if result == 0:
                    print(f"[+] TCP ping exitoso en puerto {port}")
                    responsive_ports.append(port)
                sock.close()
            except:
                pass
        
        if responsive_ports:
            print(f"[+] Puertos que responden: {responsive_ports}")
            return True
        else:
            print("[-] Ningún puerto TCP responde")
            return False
    
    def udp_discovery(self):
        """Descubrimiento UDP"""
        print("=== Descubrimiento UDP ===")
        
        udp_tests = [
            (53, b'\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x01\x00\x01'),  # DNS
            (123, b'\x1b\x00\x00\x00\x00\x00\x00\x00'),  # NTP
            (161, b'\x30\x26\x02\x01\x01\x04\x06\x70\x75\x62\x6c\x69\x63'),  # SNMP
            (69, b'\x00\x01test.txt\x00netascii\x00'),  # TFTP
        ]
        
        responsive_udp = []
        
        for port, payload in udp_tests:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(3)
                sock.sendto(payload, (self.target, port))
                
                try:
                    data, addr = sock.recvfrom(1024)
                    print(f"[+] UDP respuesta en puerto {port}: {len(data)} bytes")
                    responsive_udp.append(port)
                except socket.timeout:
                    pass
                
                sock.close()
            except:
                pass
        
        if responsive_udp:
            print(f"[+] Puertos UDP que responden: {responsive_udp}")
            return True
        else:
            print("[-] Ningún puerto UDP responde")
            return False
    
    def check_firewall_filtering(self):
        """Detectar filtrado de firewall"""
        print("=== Detección de Firewall ===")
        
        # Probar puertos comúnmente filtrados vs abiertos
        test_ports = [21, 22, 23, 25, 53, 80, 135, 139, 443, 445, 993, 995, 3389, 8080]
        
        filtered_count = 0
        closed_count = 0
        
        for port in test_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)  # Timeout corto para detectar filtrado
                start_time = time.time()
                result = sock.connect_ex((self.target, port))
                end_time = time.time()
                
                if result != 0:
                    if end_time - start_time > 0.5:  # Timeout largo = filtrado
                        filtered_count += 1
                    else:  # Respuesta rápida = cerrado
                        closed_count += 1
                
                sock.close()
            except:
                filtered_count += 1
        
        if filtered_count > closed_count:
            print(f"[!] Posible firewall detectado (filtrados: {filtered_count}, cerrados: {closed_count})")
        else:
            print(f"[*] Sin indicios de firewall (filtrados: {filtered_count}, cerrados: {closed_count})")
    
    def traceroute_basic(self):
        """Traceroute básico"""
        print("=== Traceroute básico ===")
        
        try:
            result = subprocess.run(['traceroute', '-m', '10', self.target], 
                                  capture_output=True, text=True, timeout=30)
            if result.stdout:
                print(result.stdout)
        except:
            print("[-] Traceroute no disponible o falló")
    
    def comprehensive_discovery(self):
        """Ejecutar todas las pruebas de descubrimiento"""
        print(f"=== Descubrimiento completo de {self.target} ===")
        print(f"Iniciado: {datetime.now()}")
        print("=" * 50)
        
        # Ejecutar todas las pruebas
        icmp_result = self.icmp_ping()
        tcp_result = self.tcp_ping()
        udp_result = self.udp_discovery()
        self.check_firewall_filtering()
        self.traceroute_basic()
        
        print("\n=== Resumen ===")
        print(f"ICMP responde: {'Sí' if icmp_result else 'No'}")
        print(f"TCP responde: {'Sí' if tcp_result else 'No'}")
        print(f"UDP responde: {'Sí' if udp_result else 'No'}")
        
        if not any([icmp_result, tcp_result, udp_result]):
            print("\n[!] El objetivo no responde a ninguna prueba básica")
            print("[!] Posibles causas:")
            print("    - Host inactivo")
            print("    - Firewall bloqueando todo el tráfico")
            print("    - IP incorrecta")
            print("    - Filtrado por ISP/red")

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 network_discovery.py <IP>")
        sys.exit(1)
    
    target = sys.argv[1]
    discovery = NetworkDiscovery(target)
    discovery.comprehensive_discovery()

if __name__ == "__main__":
    main()