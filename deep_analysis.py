#!/usr/bin/env python3
import requests
import json
import re
from urllib.parse import urljoin

def deep_analysis():
    # Endpoints encontrados
    endpoints = [
        "https://identidad.ibercaja.es/soporte/plataforma/identidad/api/v1/",
        "https://sgv.ibercaja.es/auth/",
        "https://sgv.ibercaja.es/auth_logout",
        "https://banca.ibercaja.es/configuration/config.json",
        "https://banca.ibercaja.es/setting/SettingsJs"
    ]
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        'Origin': 'https://banca.ibercaja.es',
        'Referer': 'https://banca.ibercaja.es/'
    })
    
    print("[*] Análisis profundo de endpoints...")
    
    # Analizar cada endpoint
    for endpoint in endpoints:
        print(f"\n[*] Analizando: {endpoint}")
        
        try:
            # GET request
            response = session.get(endpoint, allow_redirects=False)
            print(f"  - Status Code: {response.status_code}")
            print(f"  - Headers: {dict(response.headers)}")
            
            if response.status_code == 302 or response.status_code == 301:
                print(f"  - Redirección a: {response.headers.get('Location', 'N/A')}")
            
            # Analizar contenido
            if response.text:
                if response.headers.get('Content-Type', '').startswith('application/json'):
                    try:
                        data = response.json()
                        print(f"  - JSON Response: {json.dumps(data, indent=2)[:500]}...")
                    except:
                        print(f"  - Contenido: {response.text[:200]}...")
                else:
                    print(f"  - Contenido: {response.text[:200]}...")
            
            # OPTIONS request para CORS
            options_response = session.options(endpoint)
            if options_response.status_code == 200:
                print(f"  - CORS Headers:")
                for header in ['Access-Control-Allow-Origin', 'Access-Control-Allow-Methods', 
                             'Access-Control-Allow-Headers', 'Access-Control-Allow-Credentials']:
                    if header in options_response.headers:
                        print(f"    - {header}: {options_response.headers[header]}")
            
        except Exception as e:
            print(f"  - Error: {str(e)}")
    
    # Buscar endpoints de login específicos
    print("\n[*] Buscando endpoints de login...")
    login_endpoints = [
        "https://identidad.ibercaja.es/soporte/plataforma/identidad/api/v1/login",
        "https://identidad.ibercaja.es/soporte/plataforma/identidad/api/v1/authenticate",
        "https://identidad.ibercaja.es/soporte/plataforma/identidad/api/v1/auth/login",
        "https://sgv.ibercaja.es/auth/login",
        "https://banca.ibercaja.es/api/login",
        "https://banca.ibercaja.es/api/auth/login"
    ]
    
    for endpoint in login_endpoints:
        try:
            response = session.post(endpoint, json={}, allow_redirects=False)
            if response.status_code != 404:
                print(f"\n[!] Endpoint activo: {endpoint}")
                print(f"  - Status Code: {response.status_code}")
                print(f"  - Response: {response.text[:200]}...")
        except:
            pass
    
    # Analizar el archivo de configuración principal
    print("\n[*] Analizando archivo principal main.js...")
    try:
        main_js_url = "https://banca.ibercaja.es/main.c672c30c80c6e6c8.js"
        response = session.get(main_js_url)
        
        # Buscar patrones de configuración
        patterns = [
            r'loginUrl["\']?\s*[:=]\s*["\'](.*?)["\']',
            r'authUrl["\']?\s*[:=]\s*["\'](.*?)["\']',
            r'apiUrl["\']?\s*[:=]\s*["\'](.*?)["\']',
            r'baseUrl["\']?\s*[:=]\s*["\'](.*?)["\']',
            r'identidad["\']?\s*[:=]\s*["\'](.*?)["\']'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, response.text, re.IGNORECASE)
            if matches:
                print(f"\n[*] Patrón encontrado: {pattern}")
                for match in matches[:5]:
                    print(f"  - {match}")
        
        # Buscar campos de formulario
        form_fields = re.findall(r'(usuario|password|contraseña|user|pass|login)["\']?\s*[:=]', response.text, re.IGNORECASE)
        if form_fields:
            print(f"\n[*] Campos de formulario encontrados: {set(form_fields)}")
        
    except Exception as e:
        print(f"  - Error: {str(e)}")
    
    # Guardar resultados
    with open('deep_analysis_results.txt', 'w') as f:
        f.write("=== ANÁLISIS PROFUNDO DE ENDPOINTS ===\n\n")
        f.write("Endpoints principales:\n")
        f.write("- API Identidad: https://identidad.ibercaja.es/soporte/plataforma/identidad/api/v1/\n")
        f.write("- Auth SGV: https://sgv.ibercaja.es/auth/\n")
        f.write("\nPosibles endpoints de login:\n")
        for endpoint in login_endpoints:
            f.write(f"- {endpoint}\n")
    
    print("\n[*] Resultados guardados en deep_analysis_results.txt")

if __name__ == "__main__":
    deep_analysis()