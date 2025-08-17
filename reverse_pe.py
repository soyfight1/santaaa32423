#!/usr/bin/env python3
import struct
import sys

def read_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

def find_xor_strings(data):
    """Buscar strings que puedan estar XOR-eados"""
    results = []
    
    # Probar diferentes claves XOR
    for key in range(1, 256):
        decoded = []
        for byte in data:
            decoded_byte = byte ^ key
            if 0x20 <= decoded_byte <= 0x7E:
                decoded.append(chr(decoded_byte))
            else:
                if len(decoded) >= 8:
                    s = ''.join(decoded)
                    if 'password' in s.lower() or 'flag' in s.lower() or 'correct' in s.lower():
                        results.append((key, s))
                decoded = []
    
    return results

def find_all_strings(data, min_len=4):
    """Encontrar todos los strings ASCII y Unicode"""
    ascii_strings = []
    unicode_strings = []
    
    # ASCII strings
    current = []
    for byte in data:
        if 0x20 <= byte <= 0x7E:
            current.append(chr(byte))
        else:
            if len(current) >= min_len:
                ascii_strings.append(''.join(current))
            current = []
    
    # Unicode strings (little-endian)
    current = []
    for i in range(0, len(data)-1, 2):
        if data[i+1] == 0 and 0x20 <= data[i] <= 0x7E:
            current.append(chr(data[i]))
        else:
            if len(current) >= min_len:
                unicode_strings.append(''.join(current))
            current = []
    
    return ascii_strings, unicode_strings

def main():
    data = read_file("FirstStepsOnWindows.exe")
    
    print("=== Analizando el ejecutable ===\n")
    
    # Buscar el offset del código principal
    dos_header = data[:2]
    if dos_header == b'MZ':
        pe_offset = struct.unpack('<I', data[0x3C:0x40])[0]
        print(f"PE header offset: 0x{pe_offset:X}")
        
        # Buscar la sección .text
        num_sections = struct.unpack('<H', data[pe_offset+6:pe_offset+8])[0]
        optional_header_size = struct.unpack('<H', data[pe_offset+20:pe_offset+22])[0]
        section_table_offset = pe_offset + 24 + optional_header_size
        
        print(f"Número de secciones: {num_sections}")
        
        for i in range(num_sections):
            section_offset = section_table_offset + (i * 40)
            section_name = data[section_offset:section_offset+8].rstrip(b'\x00').decode('ascii', errors='ignore')
            virtual_size = struct.unpack('<I', data[section_offset+8:section_offset+12])[0]
            virtual_address = struct.unpack('<I', data[section_offset+12:section_offset+16])[0]
            raw_size = struct.unpack('<I', data[section_offset+16:section_offset+20])[0]
            raw_offset = struct.unpack('<I', data[section_offset+20:section_offset+24])[0]
            
            print(f"Sección {section_name}: VA=0x{virtual_address:X}, Size=0x{virtual_size:X}, Offset=0x{raw_offset:X}")
            
            if section_name == '.text':
                text_section = data[raw_offset:raw_offset+raw_size]
                print(f"\nAnalizando sección .text (tamaño: {len(text_section)} bytes)")
                
                # Buscar patrones de comparación de strings
                for i in range(len(text_section) - 10):
                    # Buscar instrucciones CMP o TEST seguidas de JE/JNE
                    if text_section[i] in [0x3C, 0x3D, 0x80, 0x81, 0x83, 0x38, 0x39, 0x84, 0x85]:
                        if i + 2 < len(text_section) and text_section[i+2] in [0x74, 0x75, 0x0F]:
                            print(f"Posible comparación en offset 0x{raw_offset+i:X}")
    
    print("\n=== Strings encontrados ===")
    ascii_strings, unicode_strings = find_all_strings(data, 5)
    
    # Filtrar strings interesantes
    interesting = []
    for s in ascii_strings:
        if len(s) >= 8 and len(s) <= 50:
            # Buscar strings que parezcan contraseñas
            has_upper = any(c.isupper() for c in s)
            has_lower = any(c.islower() for c in s)
            has_digit = any(c.isdigit() for c in s)
            has_special = any(c in '!@#$%^&*()-_=+[]{}|;:,.<>?' for c in s)
            
            # Si tiene mezcla de caracteres, podría ser una contraseña
            if (has_upper and has_lower) or (has_digit and (has_upper or has_lower)) or has_special:
                if not any(word in s.lower() for word in ['kernel32', 'user32', 'msvcrt', 'windows', 'microsoft']):
                    interesting.append(s)
    
    print("\nPosibles contraseñas (ASCII):")
    for s in interesting[:20]:
        print(f"  - {s}")
    
    # Buscar en strings Unicode
    interesting_unicode = []
    for s in unicode_strings:
        if len(s) >= 8 and len(s) <= 50:
            if not s.startswith('\\') and not s.endswith('.dll'):
                interesting_unicode.append(s)
    
    if interesting_unicode:
        print("\nPosibles contraseñas (Unicode):")
        for s in interesting_unicode[:10]:
            print(f"  - {s}")
    
    # Buscar strings XOR
    print("\n=== Buscando strings XOR-eados ===")
    xor_results = find_xor_strings(data[:10000])  # Solo los primeros 10KB para velocidad
    if xor_results:
        for key, s in xor_results[:5]:
            print(f"  XOR key {key}: {s}")

if __name__ == "__main__":
    main()