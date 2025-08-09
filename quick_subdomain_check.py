#!/usr/bin/env python3
import socket
import sys
import threading
import time
import urllib.request
import urllib.error
import ssl
from datetime import datetime

def quick_check_subdomain(domain, ip):
    """Verificación rápida de un subdominio"""
    print(f"\n=== {domain} ({ip}) ===")
    
    results = {
        'domain': domain,
        'ip': ip,
        'accessible': False,
        'ports': [],
        'web_status': None
    }
    
    # Verificación web rápida
    for protocol in ['http', 'https']:
        try:
            url = f"{protocol}://{domain}"
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (compatible)')
            
            if protocol == 'https':
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                response = urllib.request.urlopen(req, timeout=5, context=ctx)
            else:
                response = urllib.request.urlopen(req, timeout=5)
            
            status = response.getcode()
            print(f"[+] {protocol.upper()}: {status}")
            results['web_status'] = status
            results['accessible'] = True
            
            # Leer un poco del contenido para detectar tecnologías básicas
            try:
                content = response.read(2048).decode('utf-8', errors='ignore').lower()
                if 'login' in content:
                    print(f"  [!] Posible login detectado")
                if 'admin' in content:
                    print(f"  [!] Panel admin detectado")
                if 'wordpress' in content:
                    print(f"  [!] WordPress detectado")
            except:
                pass
            break
            
        except urllib.error.HTTPError as e:
            if e.code in [401, 403]:
                print(f"[+] {protocol.upper()}: {e.code} (protegido)")
                results['accessible'] = True
                results['web_status'] = e.code
        except:
            pass
    
    # Escaneo rápido de puertos críticos
    critical_ports = [22, 80, 443, 3389, 5900]
    if 'mail' in domain or 'smtp' in domain:
        critical_ports.extend([25, 465, 587])
    if 'vpn' in domain:
        critical_ports.extend([1723, 1194])
    
    open_ports = []
    for port in critical_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
                print(f"[+] Puerto {port} abierto")
            sock.close()
        except:
            pass
    
    results['ports'] = open_ports
    return results

def main():
    print("=== Verificación rápida de subdominios digimobil.es ===")
    print(f"Iniciado: {datetime.now()}")
    print("=" * 50)
    
    # Subdominios prioritarios
    priority_subdomains = [
        ('www.digimobil.es', '79.117.254.155'),
        ('webmail.digimobil.es', '10.199.235.130'),
        ('control.digimobil.es', '217.76.128.183'),
        ('vpn.digimobil.es', '91.232.81.250'),
        ('blog.digimobil.es', '79.117.254.155'),
    ]
    
    all_results = []
    
    for domain, ip in priority_subdomains:
        result = quick_check_subdomain(domain, ip)
        all_results.append(result)
    
    # Resumen
    print(f"\n=== RESUMEN ===")
    accessible = [r for r in all_results if r['accessible']]
    with_ports = [r for r in all_results if r['ports']]
    
    print(f"Subdominios accesibles: {len(accessible)}")
    for r in accessible:
        print(f"  - {r['domain']} (status: {r['web_status']})")
    
    print(f"\nSubdominios con puertos abiertos: {len(with_ports)}")
    for r in with_ports:
        print(f"  - {r['domain']}: {r['ports']}")
    
    # Identificar vectores de acceso
    print(f"\n[!] VECTORES DE ACCESO:")
    for r in all_results:
        if r['accessible'] or r['ports']:
            vectors = []
            if r['accessible']:
                vectors.append(f"Web ({r['web_status']})")
            if 22 in r['ports']:
                vectors.append("SSH")
            if 3389 in r['ports']:
                vectors.append("RDP")
            if any(p in [25, 465, 587] for p in r['ports']):
                vectors.append("SMTP")
            
            if vectors:
                print(f"  - {r['domain']}: {', '.join(vectors)}")

if __name__ == "__main__":
    main()