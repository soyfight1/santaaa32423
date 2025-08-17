#!/usr/bin/env python3
import struct
import sys

def read_pe_file(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    return data

def find_strings(data, min_length=4):
    strings = []
    current = []
    
    for byte in data:
        if 0x20 <= byte <= 0x7E:  # printable ASCII
            current.append(chr(byte))
        else:
            if len(current) >= min_length:
                strings.append(''.join(current))
            current = []
    
    if len(current) >= min_length:
        strings.append(''.join(current))
    
    return strings

def analyze_exe(filename):
    data = read_pe_file(filename)
    
    # Buscar strings interesantes
    strings = find_strings(data, 4)
    
    print("=== Análisis de strings ===")
    keywords = ['password', 'flag', 'key', 'secret', 'correct', 'invalid', 'enter', 'w3ch']
    
    for s in strings:
        for keyword in keywords:
            if keyword.lower() in s.lower():
                print(f"Found: {s}")
                break
    
    print("\n=== Buscando posibles contraseñas ===")
    # Buscar strings que parezcan contraseñas (longitud específica, caracteres especiales)
    for s in strings:
        if 8 <= len(s) <= 50:
            # Filtrar strings que parezcan contraseñas
            if any(c in s for c in ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+']) or \
               (any(c.isupper() for c in s) and any(c.islower() for c in s) and any(c.isdigit() for c in s)):
                print(f"Posible contraseña: {s}")
    
    print("\n=== Strings únicos de longitud 10-30 ===")
    seen = set()
    for s in strings:
        if 10 <= len(s) <= 30 and s not in seen and not s.startswith('!'):
            seen.add(s)
            # Filtrar strings que no sean solo ruido
            if not all(c in '0123456789ABCDEFabcdef' for c in s):  # No solo hex
                if s.count(' ') < len(s) / 3:  # No demasiados espacios
                    print(s)

if __name__ == "__main__":
    analyze_exe("FirstStepsOnWindows.exe")