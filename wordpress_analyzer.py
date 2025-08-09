#!/usr/bin/env python3
import socket
import sys
import urllib.request
import urllib.error
import urllib.parse
import ssl
import re
import json
from datetime import datetime

class WordPressAnalyzer:
    def __init__(self, target_url):
        self.target = target_url.rstrip('/')
        self.findings = []
        self.vulnerabilities = []
        
    def make_request(self, path, method='GET', data=None):
        """Hacer petición HTTP con manejo de errores"""
        try:
            url = self.target + path
            
            if method == 'POST' and data:
                data = urllib.parse.urlencode(data).encode('utf-8')
                req = urllib.request.Request(url, data=data)
            else:
                req = urllib.request.Request(url)
            
            req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')
            
            # Manejar HTTPS
            if url.startswith('https'):
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                response = urllib.request.urlopen(req, timeout=10, context=ctx)
            else:
                response = urllib.request.urlopen(req, timeout=10)
            
            return response.read().decode('utf-8', errors='ignore'), response.getcode()
            
        except urllib.error.HTTPError as e:
            return None, e.code
        except Exception as e:
            return None, None
    
    def detect_wordpress_version(self):
        """Detectar versión de WordPress"""
        print("=== Detección de versión de WordPress ===")
        
        # Método 1: readme.html
        content, status = self.make_request('/readme.html')
        if content and status == 200:
            version_match = re.search(r'Version (\d+\.\d+(?:\.\d+)?)', content)
            if version_match:
                version = version_match.group(1)
                print(f"[+] Versión encontrada en readme.html: {version}")
                self.findings.append(f"WordPress version: {version}")
                return version
        
        # Método 2: wp-includes/version.php
        content, status = self.make_request('/wp-includes/version.php')
        if content and status == 200:
            version_match = re.search(r"\$wp_version = '([^']+)'", content)
            if version_match:
                version = version_match.group(1)
                print(f"[+] Versión encontrada en version.php: {version}")
                self.findings.append(f"WordPress version: {version}")
                return version
        
        # Método 3: Meta generator
        content, status = self.make_request('/')
        if content:
            version_match = re.search(r'<meta name="generator" content="WordPress ([^"]+)"', content)
            if version_match:
                version = version_match.group(1)
                print(f"[+] Versión encontrada en meta generator: {version}")
                self.findings.append(f"WordPress version: {version}")
                return version
        
        print("[-] No se pudo determinar la versión")
        return None
    
    def enumerate_users(self):
        """Enumerar usuarios de WordPress"""
        print("\n=== Enumeración de usuarios ===")
        
        users = []
        
        # Método 1: wp-json/wp/v2/users
        content, status = self.make_request('/wp-json/wp/v2/users')
        if content and status == 200:
            try:
                users_data = json.loads(content)
                for user in users_data:
                    username = user.get('slug', user.get('name', 'unknown'))
                    user_id = user.get('id', 'unknown')
                    print(f"[+] Usuario encontrado: {username} (ID: {user_id})")
                    users.append(username)
            except:
                pass
        
        # Método 2: Author enumeration via ?author=
        if not users:
            for user_id in range(1, 11):
                content, status = self.make_request(f'/?author={user_id}')
                if content and status == 200:
                    # Buscar en la URL de redirección o en el contenido
                    author_match = re.search(r'/author/([^/]+)/', content)
                    if author_match:
                        username = author_match.group(1)
                        if username not in users:
                            print(f"[+] Usuario encontrado: {username}")
                            users.append(username)
        
        # Método 3: wp-login.php error messages
        test_users = ['admin', 'administrator', 'user', 'test', 'digimobil']
        for username in test_users:
            data = {'log': username, 'pwd': 'invalid_password'}
            content, status = self.make_request('/wp-login.php', 'POST', data)
            if content:
                if 'incorrect password' in content.lower():
                    if username not in users:
                        print(f"[+] Usuario válido encontrado: {username}")
                        users.append(username)
                elif 'invalid username' in content.lower():
                    print(f"[-] Usuario inválido: {username}")
        
        self.findings.append(f"Found users: {users}")
        return users
    
    def check_common_vulnerabilities(self):
        """Verificar vulnerabilidades comunes"""
        print("\n=== Verificación de vulnerabilidades comunes ===")
        
        # 1. wp-config.php backup
        backup_files = [
            '/wp-config.php.bak',
            '/wp-config.php.backup',
            '/wp-config.php.old',
            '/wp-config.php~',
            '/.wp-config.php.swp'
        ]
        
        for backup in backup_files:
            content, status = self.make_request(backup)
            if content and status == 200 and 'DB_PASSWORD' in content:
                print(f"[!] CRÍTICO: Backup de wp-config.php accesible: {backup}")
                self.vulnerabilities.append(f"wp-config.php backup exposed: {backup}")
        
        # 2. Directory listing
        directories = ['/wp-content/', '/wp-content/uploads/', '/wp-includes/']
        for directory in directories:
            content, status = self.make_request(directory)
            if content and status == 200 and 'Index of' in content:
                print(f"[!] Directory listing habilitado: {directory}")
                self.vulnerabilities.append(f"Directory listing: {directory}")
        
        # 3. wp-admin sin autenticación
        content, status = self.make_request('/wp-admin/')
        if status == 200:
            print(f"[!] wp-admin accesible sin redirección")
            self.vulnerabilities.append("wp-admin accessible without redirect")
        
        # 4. xmlrpc.php
        content, status = self.make_request('/xmlrpc.php')
        if content and status == 200 and 'XML-RPC server' in content:
            print(f"[!] XML-RPC habilitado (posible brute force)")
            self.vulnerabilities.append("XML-RPC enabled")
            
            # Probar métodos XML-RPC
            xmlrpc_data = '''<?xml version="1.0"?>
<methodCall>
<methodName>system.listMethods</methodName>
<params></params>
</methodCall>'''
            
            req = urllib.request.Request(self.target + '/xmlrpc.php', xmlrpc_data.encode())
            req.add_header('Content-Type', 'text/xml')
            try:
                response = urllib.request.urlopen(req, timeout=5)
                methods_content = response.read().decode('utf-8', errors='ignore')
                if 'wp.getUsersBlogs' in methods_content:
                    print(f"  [!] Método wp.getUsersBlogs disponible")
            except:
                pass
    
    def enumerate_plugins(self):
        """Enumerar plugins instalados"""
        print("\n=== Enumeración de plugins ===")
        
        plugins = []
        
        # Método 1: Buscar en el HTML
        content, status = self.make_request('/')
        if content:
            plugin_matches = re.findall(r'/wp-content/plugins/([^/]+)/', content)
            for plugin in set(plugin_matches):
                plugins.append(plugin)
                print(f"[+] Plugin encontrado: {plugin}")
        
        # Método 2: Probar plugins comunes
        common_plugins = [
            'akismet', 'jetpack', 'yoast-seo', 'contact-form-7', 'wordfence',
            'elementor', 'woocommerce', 'wp-super-cache', 'all-in-one-seo-pack',
            'google-analytics', 'mailchimp-for-wp', 'wp-optimize'
        ]
        
        for plugin in common_plugins:
            content, status = self.make_request(f'/wp-content/plugins/{plugin}/')
            if status == 200 or status == 403:
                if plugin not in plugins:
                    plugins.append(plugin)
                    print(f"[+] Plugin encontrado: {plugin}")
        
        self.findings.append(f"Installed plugins: {plugins}")
        return plugins
    
    def enumerate_themes(self):
        """Enumerar temas instalados"""
        print("\n=== Enumeración de temas ===")
        
        themes = []
        
        # Método 1: Buscar en el HTML
        content, status = self.make_request('/')
        if content:
            theme_matches = re.findall(r'/wp-content/themes/([^/]+)/', content)
            for theme in set(theme_matches):
                themes.append(theme)
                print(f"[+] Tema encontrado: {theme}")
        
        # Método 2: Probar temas comunes
        common_themes = [
            'twentytwentyone', 'twentytwenty', 'twentynineteen', 'twentyseventeen',
            'astra', 'oceanwp', 'generatepress', 'neve', 'storefront'
        ]
        
        for theme in common_themes:
            content, status = self.make_request(f'/wp-content/themes/{theme}/')
            if status == 200 or status == 403:
                if theme not in themes:
                    themes.append(theme)
                    print(f"[+] Tema encontrado: {theme}")
        
        self.findings.append(f"Installed themes: {themes}")
        return themes
    
    def check_login_page(self):
        """Analizar página de login"""
        print("\n=== Análisis de página de login ===")
        
        content, status = self.make_request('/wp-login.php')
        if content and status == 200:
            print(f"[+] Página de login accesible")
            
            # Verificar si hay protección contra brute force
            if 'limit' in content.lower() or 'captcha' in content.lower():
                print(f"[+] Posible protección contra brute force detectada")
            else:
                print(f"[!] Sin protección aparente contra brute force")
                self.vulnerabilities.append("No brute force protection on login")
            
            # Buscar campos ocultos o tokens
            if 'wp_nonce' in content or 'csrf' in content:
                print(f"[+] Tokens CSRF detectados")
            else:
                print(f"[!] Sin tokens CSRF visibles")
    
    def comprehensive_analysis(self):
        """Análisis completo de WordPress"""
        print(f"=== Análisis completo de WordPress: {self.target} ===")
        print(f"Iniciado: {datetime.now()}")
        print("=" * 60)
        
        version = self.detect_wordpress_version()
        users = self.enumerate_users()
        plugins = self.enumerate_plugins()
        themes = self.enumerate_themes()
        self.check_common_vulnerabilities()
        self.check_login_page()
        
        # Resumen final
        print(f"\n=== RESUMEN DEL ANÁLISIS ===")
        print(f"Objetivo: {self.target}")
        print(f"Hallazgos totales: {len(self.findings)}")
        print(f"Vulnerabilidades: {len(self.vulnerabilities)}")
        
        if users:
            print(f"\n[!] USUARIOS ENCONTRADOS:")
            for user in users:
                print(f"  - {user}")
        
        if self.vulnerabilities:
            print(f"\n[!] VULNERABILIDADES CRÍTICAS:")
            for vuln in self.vulnerabilities:
                print(f"  - {vuln}")
        
        print(f"\n[!] VECTORES DE ATAQUE POTENCIALES:")
        attack_vectors = []
        
        if users:
            attack_vectors.append("Brute force login con usuarios conocidos")
        if 'XML-RPC enabled' in [v for v in self.vulnerabilities]:
            attack_vectors.append("XML-RPC brute force")
        if plugins:
            attack_vectors.append("Exploits de plugins conocidos")
        if any('wp-config' in v for v in self.vulnerabilities):
            attack_vectors.append("Acceso directo a credenciales de base de datos")
        
        for vector in attack_vectors:
            print(f"  - {vector}")
        
        return {
            'version': version,
            'users': users,
            'plugins': plugins,
            'themes': themes,
            'vulnerabilities': self.vulnerabilities,
            'attack_vectors': attack_vectors
        }

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 wordpress_analyzer.py <URL>")
        sys.exit(1)
    
    target = sys.argv[1]
    if not target.startswith('http'):
        target = f"http://{target}"
    
    analyzer = WordPressAnalyzer(target)
    results = analyzer.comprehensive_analysis()
    
    return results

if __name__ == "__main__":
    main()