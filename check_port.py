#!/usr/bin/env python3
import socket
import sys

host = "hackme1.vulnmachines.com"
port = 7500

print(f"[*] Checking port {port} on {host}...")

try:
    # Try socket connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    result = s.connect_ex((host, port))
    s.close()
    
    if result == 0:
        print(f"[+] Port {port} is OPEN!")
        print("[*] Trying HTTP request...")
        
        import requests
        try:
            response = requests.get(f"http://{host}:{port}/", timeout=10)
            print(f"[+] HTTP Response: {response.status_code}")
            print(f"[+] Content length: {len(response.content)} bytes")
            if len(response.content) < 1000:
                print(f"[*] Content preview:\n{response.text[:500]}")
        except Exception as e:
            print(f"[-] HTTP request failed: {e}")
    else:
        print(f"[-] Port {port} is CLOSED or FILTERED (error code: {result})")
        print("[*] Common error codes:")
        print("    111 = Connection refused (port closed)")
        print("    110 = Connection timed out (filtered/no response)")
        
except socket.gaierror:
    print(f"[-] Hostname {host} could not be resolved")
except Exception as e:
    print(f"[-] Error: {e}")

print("\n[*] Checking alternative ports...")
alt_ports = [80, 443, 8080, 8000, 8888, 3000, 5000, 9000]
open_ports = []

for p in alt_ports:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((host, p))
    s.close()
    if result == 0:
        open_ports.append(p)
        print(f"[+] Port {p} is OPEN")

if open_ports:
    print(f"\n[*] Open ports found: {open_ports}")
else:
    print("\n[-] No alternative ports found open")