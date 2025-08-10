#!/usr/bin/env python3
import socket
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

host = "hackme1.vulnmachines.com"

# Extended port ranges - common web ports and CTF ports
port_ranges = [
    range(80, 100),      # Around standard HTTP
    range(443, 445),     # Around HTTPS  
    range(1000, 1100),   # Common high ports
    range(3000, 3010),   # Node.js apps
    range(4000, 4010),   # Various apps
    range(5000, 5010),   # Flask/Python apps
    range(6000, 6010),   # X11 and others
    range(7000, 7600),   # Various including your 7500
    range(8000, 8200),   # Alternative HTTP
    range(8080, 8090),   # Proxy/Alternative HTTP
    range(8443, 8445),   # Alternative HTTPS
    range(8880, 8890),   # Various web apps
    range(9000, 9100),   # Various services
    range(10000, 10010), # Webmin and others
    range(31337, 31340), # Elite/Leet ports (CTF favorite)
]

# Flatten the ranges
all_ports = []
for r in port_ranges:
    all_ports.extend(list(r))

def check_port(port):
    # First check if port is open
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((socket.gethostbyname(host), port))
    sock.close()
    
    if result == 0:
        # Port is open, check if it's HTTP
        try:
            url = f"http://{host}:{port}"
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                content = response.text.lower()
                # Check for interesting content
                if any(keyword in content for keyword in ['idor', 'flag', 'vnm', 'challenge', 'login', 'user', 'profile']):
                    if 'apache2 ubuntu default' not in content:
                        return f"[WEB SERVICE WITH KEYWORDS!] Port {port} - {url}"
                elif 'apache2 ubuntu default' not in content and len(response.content) > 100:
                    return f"[WEB SERVICE] Port {port} - {url} - Size: {len(response.content)}"
            elif response.status_code in [301, 302, 401, 403]:
                return f"[WEB SERVICE] Port {port} - Status: {response.status_code}"
        except:
            # Try HTTPS
            try:
                url = f"https://{host}:{port}"
                response = requests.get(url, timeout=2, verify=False)
                if response.status_code in [200, 301, 302, 401, 403]:
                    return f"[HTTPS SERVICE] Port {port} - Status: {response.status_code}"
            except:
                return f"[OPEN] Port {port} - Non-HTTP service"
    
    return None

print(f"[*] Aggressive port scan on {host}")
print(f"[*] Scanning {len(all_ports)} ports for web services...")
print("-" * 60)

found_services = []
interesting_services = []

with ThreadPoolExecutor(max_workers=100) as executor:
    futures = {executor.submit(check_port, port): port for port in all_ports}
    
    for future in as_completed(futures):
        result = future.result()
        if result:
            print(result)
            if "WITH KEYWORDS" in result:
                interesting_services.append(result)
            else:
                found_services.append(result)

print("\n" + "=" * 60)
if interesting_services:
    print("[!!!] INTERESTING WEB SERVICES FOUND:")
    for service in interesting_services:
        print(service)
    print("\n[*] These services contain IDOR/challenge related keywords!")
    
if found_services:
    print("\n[+] Other services found:")
    for service in found_services:
        print(service)

if not interesting_services and not found_services:
    print("[-] No additional web services found on scanned ports")