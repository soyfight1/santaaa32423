#!/usr/bin/env python3
import socket
import sys
import threading
import time
import requests
from datetime import datetime

class SubdomainAnalyzer:
    def __init__(self):
        self.results = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
        
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
                response = self.session.get(url, timeout=10, verify=False, allow_redirects=True)
                
                if protocol == 'http':
                    result['http_status'] = response.status_code
                else:
                    result['https_status'] = response.status_code
                
                print(f"[+] {protocol.upper()}: {response.status_code}")
                
                # Analizar headers
                interesting_headers = ['server', 'x-powered-by', 'x-frame-options', 'set-cookie']
                for header in interesting_headers:
                    if header in response.headers:
                        result['headers'][header] = response.headers[header]
                        print(f"  {header}: {response.headers[header]}")
                
                # Detectar tecnologías
                content = response.text.lower()
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
                
            except requests.exceptions.SSLError:
                print(f"[-] {protocol.upper()}: Error SSL")
            except requests.exceptions.ConnectionError:
                print(f"[-] {protocol.upper()}: No se puede conectar")
            except requests.exceptions.Timeout:
                print(f"[-] {protocol.upper()}: Timeout")
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
    
    def directory_enumeration(self, domain):
        """Enumeración de directorios web"""
        print(f"\n=== Enumeración de directorios para {domain} ===")
        
        common_paths = [
            '/admin', '/administrator', '/login', '/wp-admin', '/phpmyadmin',
            '/admin.php', '/login.php', '/dashboard', '/panel', '/control',
            '/manager', '/console', '/api', '/backup', '/config', '/test',
            '/dev', '/staging', '/beta', '/demo', '/old', '/new'
        ]
        
        found_paths = []
        
        for protocol in ['http', 'https']:
            base_url = f"{protocol}://{domain}"
            
            for path in common_paths:
                try:
                    url = base_url + path
                    response = self.session.get(url, timeout=5, verify=False, allow_redirects=False)
                    
                    if response.status_code in [200, 301, 302, 401, 403]:
                        print(f"[{response.status_code}] {url}")
                        found_paths.append((url, response.status_code))
                        
                        # Análisis adicional para códigos interesantes
                        if response.status_code == 401:
                            print(f"  [!] Requiere autenticación")
                        elif response.status_code == 403:
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
        
        for domain, data in self.results.items():
            if data['http_status'] and data['http_status'] < 400:
                accessible_http.append(domain)
            if data['https_status'] and data['https_status'] < 400:
                accessible_https.append(domain)
            
            if data['open_ports']:
                interesting_findings.append(f"{domain}: puertos {data['open_ports']}")
            
            if data['technologies']:
                interesting_findings.append(f"{domain}: {', '.join(data['technologies'])}")
        
        print(f"Subdominios accesibles HTTP: {len(accessible_http)}")
        for domain in accessible_http:
            print(f"  - http://{domain}")
        
        print(f"\nSubdominios accesibles HTTPS: {len(accessible_https)}")
        for domain in accessible_https:
            print(f"  - https://{domain}")
        
        print(f"\nHallazgos interesantes:")
        for finding in interesting_findings:
            print(f"  - {finding}")
        
        # Identificar objetivos prioritarios
        priority_targets = []
        for domain, data in self.results.items():
            if any(x in domain for x in ['admin', 'control', 'webmail', 'vpn']):
                priority_targets.append(domain)
            elif data['open_ports'] and any(port in [22, 3389, 5900] for port in data['open_ports']):
                priority_targets.append(domain)
        
        if priority_targets:
            print(f"\n[!] OBJETIVOS PRIORITARIOS para acceso:")
            for target in priority_targets:
                print(f"  - {target}")

def main():
    analyzer = SubdomainAnalyzer()
    analyzer.comprehensive_analysis()

if __name__ == "__main__":
    main()