#!/usr/bin/env python3
import requests
import re
import json
from urllib.parse import urljoin, urlparse

def analyze_network_traffic():
    base_url = "https://banca.ibercaja.es/"
    
    # Headers típicos de un navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1'
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    print("[*] Analizando recursos JavaScript...")
    
    # Obtener la página principal
    response = session.get(base_url)
    
    # Buscar archivos JavaScript
    js_files = re.findall(r'<script[^>]*src=["\'](.*?)["\']', response.text)
    print(f"\n[*] Archivos JavaScript encontrados: {len(js_files)}")
    
    # Buscar patrones de configuración inline
    config_patterns = re.findall(r'window\.(.*?)=\s*({[^}]+})', response.text)
    if config_patterns:
        print("\n[*] Configuraciones inline encontradas:")
        for name, config in config_patterns[:3]:
            print(f"  - window.{name} = {config[:100]}...")
    
    # Analizar cada archivo JavaScript
    api_endpoints = []
    for js_file in js_files:
        if not js_file.startswith('http'):
            js_url = urljoin(base_url, js_file)
        else:
            js_url = js_file
            
        print(f"\n[*] Analizando: {js_url}")
        
        try:
            js_response = session.get(js_url)
            js_content = js_response.text
            
            # Buscar patrones de API
            api_patterns = [
                r'["\'](/api/[^"\']+)["\']',
                r'["\'](https?://[^"\']*api[^"\']+)["\']',
                r'["\']([^"\']*login[^"\']+)["\']',
                r'["\']([^"\']*auth[^"\']+)["\']',
                r'["\']([^"\']*usuario[^"\']+)["\']',
                r'["\']([^"\']*acceso[^"\']+)["\']',
                r'endpoint["\']?\s*[:=]\s*["\'](.*?)["\']',
                r'url["\']?\s*[:=]\s*["\'](.*?)["\']',
                r'baseURL["\']?\s*[:=]\s*["\'](.*?)["\']'
            ]
            
            for pattern in api_patterns:
                matches = re.findall(pattern, js_content, re.IGNORECASE)
                for match in matches:
                    if len(match) < 200 and not match.startswith('data:'):
                        api_endpoints.append(match)
            
            # Buscar configuración de axios o fetch
            if 'axios' in js_content or 'fetch' in js_content:
                print("  - Contiene llamadas axios/fetch")
            
            # Buscar formularios
            form_patterns = re.findall(r'form[^{]*{[^}]+}', js_content, re.IGNORECASE)
            if form_patterns:
                print(f"  - Patrones de formulario encontrados: {len(form_patterns)}")
                
        except Exception as e:
            print(f"  - Error analizando JS: {str(e)}")
    
    # Mostrar endpoints únicos encontrados
    unique_endpoints = list(set(api_endpoints))
    if unique_endpoints:
        print("\n[*] Endpoints únicos encontrados:")
        for endpoint in unique_endpoints[:20]:
            print(f"  - {endpoint}")
    
    # Buscar archivos de manifiesto o configuración
    print("\n[*] Buscando archivos de configuración...")
    config_files = [
        'manifest.json',
        'config.json',
        'assets/config.json',
        'assets/i18n/es.json',
        'environment.json'
    ]
    
    for config_file in config_files:
        config_url = urljoin(base_url, config_file)
        try:
            config_response = session.get(config_url)
            if config_response.status_code == 200:
                print(f"\n[*] Archivo encontrado: {config_file}")
                try:
                    config_data = config_response.json()
                    print(f"  - Contenido: {json.dumps(config_data, indent=2)[:200]}...")
                except:
                    print(f"  - Contenido: {config_response.text[:200]}...")
        except:
            pass
    
    # Intentar encontrar el archivo main.js o app.js
    print("\n[*] Buscando archivos principales de la aplicación...")
    main_patterns = re.findall(r'(main[^"\']*\.js|app[^"\']*\.js|bundle[^"\']*\.js)', response.text)
    if main_patterns:
        print(f"[*] Archivos principales encontrados: {main_patterns[:5]}")
    
    # Guardar información para análisis posterior
    with open('api_endpoints.txt', 'w') as f:
        f.write("=== API ENDPOINTS ENCONTRADOS ===\n")
        for endpoint in unique_endpoints:
            f.write(f"{endpoint}\n")
    
    print("\n[*] Endpoints guardados en api_endpoints.txt")

if __name__ == "__main__":
    analyze_network_traffic()