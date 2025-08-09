#!/usr/bin/env python3
import socket
import sys
import threading
import time
import random
import subprocess
import json
from datetime import datetime

class AlternativeRecon:
    def __init__(self, target):
        self.target = target
        self.results = {}
    
    def reverse_dns_lookup(self):
        """Lookup DNS reverso"""
        print("=== Lookup DNS Reverso ===")
        try:
            hostname = socket.gethostbyaddr(self.target)[0]
            print(f"[+] Hostname: {hostname}")
            self.results['hostname'] = hostname
            return hostname
        except:
            print("[-] No se encontró hostname")
            return None
    
    def dns_enumeration(self, hostname=None):
        """Enumeración DNS completa"""
        print("=== Enumeración DNS ===")
        
        if not hostname:
            hostname = self.reverse_dns_lookup()
        
        if hostname:
            # Intentar diferentes tipos de registros DNS
            dns_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
            
            for dns_type in dns_types:
                try:
                    result = subprocess.run(['dig', '+short', dns_type, hostname], 
                                          capture_output=True, text=True, timeout=10)
                    if result.stdout.strip():
                        print(f"[+] {dns_type}: {result.stdout.strip()}")
                except:
                    # Si dig no está disponible, usar nslookup o métodos alternativos
                    pass
    
    def subdomain_enumeration(self, domain):
        """Enumeración básica de subdominios"""
        print(f"=== Enumeración de subdominios para {domain} ===")
        
        common_subdomains = [
            'www', 'mail', 'ftp', 'admin', 'administrator', 'test', 'dev', 'staging',
            'api', 'app', 'blog', 'forum', 'shop', 'store', 'secure', 'vpn',
            'remote', 'portal', 'dashboard', 'panel', 'control', 'manager',
            'webmail', 'email', 'smtp', 'pop', 'imap', 'ns1', 'ns2', 'dns',
            'backup', 'old', 'new', 'beta', 'alpha', 'demo', 'preview'
        ]
        
        found_subdomains = []
        
        def check_subdomain(sub):
            try:
                full_domain = f"{sub}.{domain}"
                ip = socket.gethostbyname(full_domain)
                print(f"[+] {full_domain} -> {ip}")
                found_subdomains.append((full_domain, ip))
            except:
                pass
        
        threads = []
        for sub in common_subdomains:
            t = threading.Thread(target=check_subdomain, args=(sub,))
            t.start()
            threads.append(t)
            
            if len(threads) >= 20:
                for thread in threads:
                    thread.join()
                threads = []
        
        for thread in threads:
            thread.join()
        
        self.results['subdomains'] = found_subdomains
        return found_subdomains
    
    def whois_lookup(self):
        """Lookup WHOIS"""
        print("=== Lookup WHOIS ===")
        try:
            result = subprocess.run(['whois', self.target], 
                                  capture_output=True, text=True, timeout=15)
            if result.stdout:
                print(result.stdout[:1000])  # Primeros 1000 caracteres
                self.results['whois'] = result.stdout
        except:
            print("[-] WHOIS no disponible")
    
    def geolocation_lookup(self):
        """Geolocalización básica"""
        print("=== Geolocalización ===")
        
        # Usar servicios públicos de geolocalización
        geo_services = [
            f"http://ip-api.com/json/{self.target}",
            f"http://ipinfo.io/{self.target}/json"
        ]
        
        for service in geo_services:
            try:
                # Simular lookup de geolocalización
                print(f"Consultando: {service}")
                # En un entorno real, haríamos una petición HTTP aquí
                print("[-] Servicio de geolocalización no disponible en este entorno")
            except:
                pass
    
    def shodan_like_banner_grab(self):
        """Banner grabbing estilo Shodan"""
        print("=== Banner Grabbing Avanzado ===")
        
        services = [
            (21, b'', 'FTP'),
            (22, b'SSH-2.0-Test\r\n', 'SSH'),
            (23, b'', 'Telnet'),
            (25, b'EHLO test.com\r\n', 'SMTP'),
            (53, b'\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06test\x03com\x00\x00\x01\x00\x01', 'DNS'),
            (80, b'HEAD / HTTP/1.1\r\nHost: ' + self.target.encode() + b'\r\n\r\n', 'HTTP'),
            (110, b'USER test\r\n', 'POP3'),
            (143, b'A001 CAPABILITY\r\n', 'IMAP'),
            (443, b'GET / HTTP/1.1\r\nHost: ' + self.target.encode() + b'\r\n\r\n', 'HTTPS'),
            (993, b'A001 CAPABILITY\r\n', 'IMAPS'),
            (995, b'USER test\r\n', 'POP3S'),
            (3389, b'\x03\x00\x00\x13\x0e\xe0\x00\x00\x00\x00\x00\x01\x00\x08\x00\x03\x00\x00\x00', 'RDP'),
            (5900, b'RFB 003.008\n', 'VNC'),
            (8080, b'GET / HTTP/1.1\r\nHost: ' + self.target.encode() + b':8080\r\n\r\n', 'HTTP-Alt'),
        ]
        
        banners = {}
        
        for port, probe, service in services:
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
                        if data:
                            print(f"[+] {service} ({port}): Respuesta DNS {len(data)} bytes")
                            banners[port] = f"DNS Response: {len(data)} bytes"
                    except socket.timeout:
                        pass
                else:
                    result = sock.connect_ex((self.target, port))
                    if result == 0:
                        if probe:
                            sock.send(probe)
                        
                        try:
                            banner = sock.recv(2048).decode('utf-8', errors='ignore')
                            if banner.strip():
                                print(f"[+] {service} ({port}): {banner[:200].strip()}")
                                banners[port] = banner.strip()
                        except:
                            print(f"[+] {service} ({port}): Conectado, sin banner")
                            banners[port] = "Connected, no banner"
                
                sock.close()
            except:
                pass
        
        self.results['banners'] = banners
        return banners
    
    def comprehensive_recon(self):
        """Reconocimiento completo alternativo"""
        print(f"=== Reconocimiento alternativo completo para {self.target} ===")
        print(f"Iniciado: {datetime.now()}")
        print("=" * 60)
        
        # Ejecutar todas las técnicas
        hostname = self.reverse_dns_lookup()
        self.dns_enumeration(hostname)
        
        if hostname:
            domain = '.'.join(hostname.split('.')[1:]) if '.' in hostname else hostname
            self.subdomain_enumeration(domain)
        
        self.whois_lookup()
        self.geolocation_lookup()
        banners = self.shodan_like_banner_grab()
        
        # Resumen final
        print(f"\n=== Resumen de Reconocimiento Alternativo ===")
        print(f"Hostname: {self.results.get('hostname', 'N/A')}")
        print(f"Subdominios encontrados: {len(self.results.get('subdomains', []))}")
        print(f"Banners capturados: {len(banners)}")
        
        if banners:
            print("\nServicios identificados:")
            for port, banner in banners.items():
                print(f"  {port}: {banner[:100]}")

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 alternative_recon.py <IP>")
        sys.exit(1)
    
    target = sys.argv[1]
    recon = AlternativeRecon(target)
    recon.comprehensive_recon()

if __name__ == "__main__":
    main()