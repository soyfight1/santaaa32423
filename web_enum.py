#!/usr/bin/env python3
import requests
import threading
import sys
from urllib.parse import urljoin
import time

class WebEnum:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
        self.found_paths = []
        
    def check_path(self, path):
        try:
            url = urljoin(self.target, path)
            resp = self.session.get(url, timeout=5, allow_redirects=False)
            if resp.status_code in [200, 301, 302, 403]:
                print(f"[{resp.status_code}] {url}")
                self.found_paths.append((url, resp.status_code))
                
                # Detectar tecnologías
                if resp.headers.get('Server'):
                    print(f"  Server: {resp.headers['Server']}")
                if resp.headers.get('X-Powered-By'):
                    print(f"  X-Powered-By: {resp.headers['X-Powered-By']}")
                    
        except Exception as e:
            pass
    
    def directory_bruteforce(self):
        # Wordlist básica
        paths = [
            '', '/', '/admin', '/administrator', '/login', '/wp-admin', '/phpmyadmin',
            '/admin.php', '/login.php', '/index.php', '/config.php', '/wp-config.php',
            '/robots.txt', '/sitemap.xml', '/.htaccess', '/backup', '/test', '/dev',
            '/api', '/api/v1', '/api/v2', '/upload', '/uploads', '/images', '/css', '/js',
            '/tmp', '/temp', '/backup.sql', '/database.sql', '/config', '/includes',
            '/dashboard', '/panel', '/control', '/manager', '/console', '/shell',
            '/cmd', '/terminal', '/webshell', '/c99.php', '/r57.php', '/backdoor.php'
        ]
        
        print(f"Enumerando directorios en {self.target}...")
        threads = []
        
        for path in paths:
            t = threading.Thread(target=self.check_path, args=(path,))
            t.start()
            threads.append(t)
            
            if len(threads) >= 20:
                for thread in threads:
                    thread.join()
                threads = []
        
        for thread in threads:
            thread.join()
    
    def technology_detection(self):
        try:
            resp = self.session.get(self.target, timeout=10)
            content = resp.text.lower()
            
            print("\n=== Detección de Tecnologías ===")
            
            # Detectar CMS
            if 'wordpress' in content or 'wp-content' in content:
                print("[+] WordPress detectado")
            if 'joomla' in content:
                print("[+] Joomla detectado")
            if 'drupal' in content:
                print("[+] Drupal detectado")
            
            # Detectar frameworks
            if 'laravel' in content:
                print("[+] Laravel detectado")
            if 'symfony' in content:
                print("[+] Symfony detectado")
            if 'codeigniter' in content:
                print("[+] CodeIgniter detectado")
            
            # Detectar bases de datos
            if 'mysql' in content:
                print("[+] MySQL mencionado")
            if 'postgresql' in content:
                print("[+] PostgreSQL mencionado")
                
        except Exception as e:
            print(f"Error en detección: {e}")

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 web_enum.py <URL>")
        sys.exit(1)
    
    target = sys.argv[1]
    if not target.startswith('http'):
        target = f"http://{target}"
    
    enum = WebEnum(target)
    enum.directory_bruteforce()
    enum.technology_detection()
    
    print(f"\n=== Resumen ===")
    print(f"Paths encontrados: {len(enum.found_paths)}")

if __name__ == "__main__":
    main()