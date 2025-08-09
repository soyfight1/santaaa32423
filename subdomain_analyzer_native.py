#!/usr/bin/env python3
import socket
import sys
import threading
import time
import urllib.request
import urllib.error
import ssl
from datetime import datetime

class SubdomainAnalyzer:
    def __init__(self):
        self.results = {}
        
        # Subdominios encontrados
        self.subdomains = [
            ('vpn.digimobil.es', '91.232.81.250'),
            ('www.digimobil.es', '79.117.254.155'),
            ('blog.digimobil.es', '79.117.254.155'),
            ('mail.digimobil.es', '212.54.125.6'),
            ('ns2.digimobil.es', '188.26.216.10'),
            ('dns.digimobil.es', '100.100.1.1'),
            ('control.digimobil.es', '217.76.128.183'),
            ('ns1.digimobil.es', '188.26.208.101'),
            ('imap.digimobil.es', '212.54.127.5'),
            ('smtp.digimobil.es', '212.54.125.9'),
            ('webmail.digimobil.es', '10.199.235.130'),
            ('pop.digimobil.es', '212.54.125.6'),
            ('email.digimobil.es', '212.54.125.6'),
        ]
    
    def analyze_subdomain(self, domain, ip):
        """Analizar un subdominio específico"""
        print(f"\n=== Analizando {domain} ({ip}) ===")
        
        result = {
            'domain': domain,
            'ip': ip,
            'http_status': None,
            'https_status': None,
            'headers': {},
            'technologies': [],
            'open_ports': [],
            'services': {}
        }
        
        # Análisis HTTP/HTTPS
        for protocol in ['http', 'https']:
            try:
                url = f"{protocol}://{domain}"
                
                # Crear contexto SSL que ignore certificados
                if protocol == 'https':
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                else:
                    ctx = None
                
                req = urllib.request.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')
                
                if ctx:
                    response = urllib.request.urlopen(req, timeout=10, context=ctx)
                else:
                    response = urllib.request.urlopen(req, timeout=10)
                
                status_code = response.getcode()
                
                if protocol == 'http':
                    result['http_status'] = status_code
                else:
                    result['https_status'] = status_code
                
                print(f"[+] {protocol.upper()}: {status_code}")
                
                # Analizar headers
                headers = response.info()
                interesting_headers = ['server', 'x-powered-by', 'x-frame-options', 'set-cookie']
                for header in interesting_headers:
                    if header in headers:
                        result['headers'][header] = headers[header]
                        print(f"  {header}: {headers[header]}")
                
                # Leer contenido
                try:
                    content = response.read().decode('utf-8', errors='ignore').lower()
                    
                    # Detectar tecnologías
                    techs = []
                    
                    if 'wordpress' in content or 'wp-content' in content:
                        techs.append('WordPress')
                    if 'joomla' in content:
                        techs.append('Joomla')
                    if 'drupal' in content:
                        techs.append('Drupal')
                    if 'laravel' in content:
                        techs.append('Laravel')
                    if 'jquery' in content:
                        techs.append('jQuery')
                    if 'bootstrap' in content:
                        techs.append('Bootstrap')
                    
                    result['technologies'] = techs
                    if techs:
                        print(f"  Tecnologías: {', '.join(techs)}")
                    
                    # Buscar formularios de login
                    if 'login' in content or 'password' in content:
                        print(f"  [!] Posible formulario de login detectado")
                    
                    # Buscar paneles de administración
                    if 'admin' in content or 'dashboard' in content:
                        print(f"  [!] Posible panel de administración")
                        
                    # Buscar información sensible
                    if 'error' in content and ('sql' in content or 'mysql' in content):
                        print(f"  [!] Posible error SQL detectado")
                    
                    if 'phpmyadmin' in content:
                        print(f"  [!] phpMyAdmin detectado")
                        
                except:
                    pass
                
            except urllib.error.HTTPError as e:
                print(f"[-] {protocol.upper()}: HTTP Error {e.code}")
                if protocol == 'http':
                    result['http_status'] = e.code
                else:
                    result['https_status'] = e.code
            except urllib.error.URLError as e:
                print(f"[-] {protocol.upper()}: URL Error - {e.reason}")
            except Exception as e:
                print(f"[-] {protocol.upper()}: Error - {e}")
        
        # Escaneo de puertos específicos según el tipo de subdominio
        if 'mail' in domain or 'smtp' in domain or 'pop' in domain or 'imap' in domain:
            ports_to_scan = [25, 110, 143, 465, 587, 993, 995]
        elif 'vpn' in domain:
            ports_to_scan = [1723, 1194, 443, 500, 4500]
        elif 'control' in domain or 'admin' in domain:
            ports_to_scan = [22, 80, 443, 3389, 5900, 8080, 8443]
        elif 'dns' in domain or 'ns' in domain:
            ports_to_scan = [53, 853]
        else:
            ports_to_scan = [21, 22, 80, 443, 8080, 8443]
        
        open_ports = self.scan_ports(ip, ports_to_scan)
        result['open_ports'] = open_ports
        
        if open_ports:
            print(f"  Puertos abiertos: {open_ports}")
            
            # Banner grabbing para puertos abiertos
            self.banner_grab(ip, open_ports, result)
        
        self.results[domain] = result
        return result
    
    def scan_ports(self, ip, ports):
        """Escanear puertos específicos"""
        open_ports = []
        
        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except:
                pass
        
        threads = []
        for port in ports:
            t = threading.Thread(target=scan_port, args=(port,))
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join()
        
        return sorted(open_ports)
    
    def banner_grab(self, ip, ports, result):
        """Banner grabbing para puertos abiertos"""
        print(f"  === Banner Grabbing ===")
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((ip, port))
                
                # Enviar sondas específicas según el puerto
                if port == 22:
                    # SSH
                    banner = sock.recv(1024).decode('utf-8', errors='ignore')
                    if banner:
                        print(f"    SSH ({port}): {banner.strip()}")
                        result['services'][port] = f"SSH: {banner.strip()}"
                elif port == 21:
                    # FTP
                    banner = sock.recv(1024).decode('utf-8', errors='ignore')
                    if banner:
                        print(f"    FTP ({port}): {banner.strip()}")
                        result['services'][port] = f"FTP: {banner.strip()}"
                elif port in [80, 8080]:
                    # HTTP
                    sock.send(b'HEAD / HTTP/1.1\r\nHost: ' + ip.encode() + b'\r\n\r\n')
                    banner = sock.recv(1024).decode('utf-8', errors='ignore')
                    if banner:
                        print(f"    HTTP ({port}): {banner[:100].strip()}")
                        result['services'][port] = f"HTTP: {banner.strip()}"
                elif port == 25:
                    # SMTP
                    banner = sock.recv(1024).decode('utf-8', errors='ignore')
                    if banner:
                        print(f"    SMTP ({port}): {banner.strip()}")
                        result['services'][port] = f"SMTP: {banner.strip()}"
                elif port in [110, 995]:
                    # POP3
                    banner = sock.recv(1024).decode('utf-8', errors='ignore')
                    if banner:
                        print(f"    POP3 ({port}): {banner.strip()}")
                        result['services'][port] = f"POP3: {banner.strip()}"
                elif port in [143, 993]:
                    # IMAP
                    banner = sock.recv(1024).decode('utf-8', errors='ignore')
                    if banner:
                        print(f"    IMAP ({port}): {banner.strip()}")
                        result['services'][port] = f"IMAP: {banner.strip()}"
                
                sock.close()
            except:
                pass
    
    def directory_enumeration(self, domain):
        """Enumeración de directorios web"""
        print(f"\n=== Enumeración de directorios para {domain} ===")
        
        common_paths = [
            '/admin', '/administrator', '/login', '/wp-admin', '/phpmyadmin',
            '/admin.php', '/login.php', '/dashboard', '/panel', '/control',
            '/manager', '/console', '/api', '/backup', '/config', '/test',
            '/dev', '/staging', '/beta', '/demo', '/old', '/new', '/robots.txt',
            '/sitemap.xml', '/.htaccess', '/upload', '/uploads'
        ]
        
        found_paths = []
        
        for protocol in ['http', 'https']:
            base_url = f"{protocol}://{domain}"
            
            for path in common_paths:
                try:
                    url = base_url + path
                    req = urllib.request.Request(url)
                    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')
                    
                    if protocol == 'https':
                        ctx = ssl.create_default_context()
                        ctx.check_hostname = False
                        ctx.verify_mode = ssl.CERT_NONE
                        response = urllib.request.urlopen(req, timeout=5, context=ctx)
                    else:
                        response = urllib.request.urlopen(req, timeout=5)
                    
                    status_code = response.getcode()
                    print(f"[{status_code}] {url}")
                    found_paths.append((url, status_code))
                    
                except urllib.error.HTTPError as e:
                    if e.code in [401, 403]:
                        print(f"[{e.code}] {url}")
                        found_paths.append((url, e.code))
                        
                        if e.code == 401:
                            print(f"  [!] Requiere autenticación")
                        elif e.code == 403:
                            print(f"  [!] Acceso prohibido (posible directorio válido)")
                except:
                    pass
        
        return found_paths
    
    def comprehensive_analysis(self):
        """Análisis completo de todos los subdominios"""
        print(f"=== Análisis completo de subdominios digimobil.es ===")
        print(f"Iniciado: {datetime.now()}")
        print("=" * 60)
        
        # Analizar cada subdominio
        for domain, ip in self.subdomains:
            self.analyze_subdomain(domain, ip)
            
            # Enumeración de directorios para subdominios web
            if any(x in domain for x in ['www', 'blog', 'webmail', 'control', 'admin']):
                self.directory_enumeration(domain)
        
        # Resumen final
        print(f"\n=== RESUMEN COMPLETO ===")
        
        accessible_http = []
        accessible_https = []
        interesting_findings = []
        priority_targets = []
        
        for domain, data in self.results.items():
            if data['http_status'] and data['http_status'] < 400:
                accessible_http.append(domain)
            if data['https_status'] and data['https_status'] < 400:
                accessible_https.append(domain)
            
            if data['open_ports']:
                interesting_findings.append(f"{domain}: puertos {data['open_ports']}")
            
            if data['technologies']:
                interesting_findings.append(f"{domain}: {', '.join(data['technologies'])}")
            
            if data['services']:
                for port, service in data['services'].items():
                    interesting_findings.append(f"{domain}:{port} - {service}")
            
            # Identificar objetivos prioritarios
            if any(x in domain for x in ['admin', 'control', 'webmail', 'vpn']):
                priority_targets.append(domain)
            elif data['open_ports'] and any(port in [22, 3389, 5900] for port in data['open_ports']):
                priority_targets.append(domain)
        
        print(f"Subdominios accesibles HTTP: {len(accessible_http)}")
        for domain in accessible_http:
            print(f"  - http://{domain}")
        
        print(f"\nSubdominios accesibles HTTPS: {len(accessible_https)}")
        for domain in accessible_https:
            print(f"  - https://{domain}")
        
        print(f"\nHallazgos interesantes:")
        for finding in interesting_findings:
            print(f"  - {finding}")
        
        if priority_targets:
            print(f"\n[!] OBJETIVOS PRIORITARIOS para acceso:")
            for target in priority_targets:
                print(f"  - {target}")
        
        print(f"\n[!] VECTORES DE ACCESO IDENTIFICADOS:")
        access_vectors = []
        
        for domain, data in self.results.items():
            if data['http_status'] and data['http_status'] < 400:
                access_vectors.append(f"HTTP: {domain}")
            if data['https_status'] and data['https_status'] < 400:
                access_vectors.append(f"HTTPS: {domain}")
            if 22 in data['open_ports']:
                access_vectors.append(f"SSH: {domain}:22")
            if 3389 in data['open_ports']:
                access_vectors.append(f"RDP: {domain}:3389")
            if any(port in [80, 8080, 443, 8443] for port in data['open_ports']):
                access_vectors.append(f"Web: {domain}")
        
        for vector in access_vectors:
            print(f"  - {vector}")

def main():
    analyzer = SubdomainAnalyzer()
    analyzer.comprehensive_analysis()

if __name__ == "__main__":
    main()