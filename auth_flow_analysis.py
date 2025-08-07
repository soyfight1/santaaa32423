#!/usr/bin/env python3
import requests
import re
from urllib.parse import urlparse, parse_qs, urlencode
import json
from urllib.parse import urljoin

def analyze_auth_flow():
    print("[*] Analizando flujo de autenticación OAuth/OpenID Connect...")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })
    
    # Paso 1: Obtener la configuración OpenID
    print("\n[1] Obteniendo configuración OpenID...")
    openid_config_url = "https://identidad.ibercaja.es/soporte/plataforma/identidad/api/v1/.well-known/openid-configuration"
    
    try:
        response = session.get(openid_config_url)
        if response.status_code == 200:
            openid_config = response.json()
            print("[+] Configuración OpenID obtenida:")
            print(json.dumps(openid_config, indent=2))
            
            # Guardar endpoints importantes
            auth_endpoint = openid_config.get('authorization_endpoint', '')
            token_endpoint = openid_config.get('token_endpoint', '')
            userinfo_endpoint = openid_config.get('userinfo_endpoint', '')
            
            with open('openid_config.json', 'w') as f:
                json.dump(openid_config, f, indent=2)
        else:
            print(f"[-] Error obteniendo configuración: {response.status_code}")
    except Exception as e:
        print(f"[-] Error: {str(e)}")
    
    # Paso 2: Analizar el flujo de login
    print("\n[2] Analizando flujo de login...")
    login_url = "https://sgv.ibercaja.es/auth/login"
    
    try:
        # Seguir redirecciones manualmente
        response = session.get(login_url, allow_redirects=False)
        redirect_count = 0
        
        while response.status_code in [301, 302, 303, 307, 308] and redirect_count < 10:
            redirect_url = response.headers.get('Location', '')
            print(f"\n[*] Redirección {redirect_count + 1}:")
            print(f"  - Status: {response.status_code}")
            print(f"  - Location: {redirect_url}")
            
            # Analizar parámetros de la URL
            parsed_url = urlparse(redirect_url)
            params = parse_qs(parsed_url.query)
            
            if params:
                print("  - Parámetros:")
                for key, value in params.items():
                    print(f"    - {key}: {value[0] if value else 'N/A'}")
            
            # Guardar cookies importantes
            if 'Set-Cookie' in response.headers:
                cookies = response.headers.get('Set-Cookie', '')
                print(f"  - Cookies: {cookies[:100]}...")
            
            # Si no es URL absoluta, construirla
            if not redirect_url.startswith('http'):
                base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                redirect_url = urljoin(base_url, redirect_url)
            
            response = session.get(redirect_url, allow_redirects=False)
            redirect_count += 1
        
        # Analizar la página final
        print(f"\n[*] Página final después de {redirect_count} redirecciones:")
        print(f"  - URL: {response.url}")
        print(f"  - Status: {response.status_code}")
        
        # Buscar formulario de login
        if response.text:
            # Buscar campos de formulario
            form_matches = re.findall(r'<form[^>]*>(.*?)</form>', response.text, re.DOTALL | re.IGNORECASE)
            if form_matches:
                print("\n[*] Formularios encontrados:")
                for i, form in enumerate(form_matches):
                    print(f"\n  Formulario {i+1}:")
                    
                    # Buscar action
                    action = re.search(r'action=["\'](.*?)["\']', form)
                    if action:
                        print(f"    - Action: {action.group(1)}")
                    
                    # Buscar inputs
                    inputs = re.findall(r'<input[^>]*>', form)
                    for inp in inputs:
                        input_type = re.search(r'type=["\'](.*?)["\']', inp)
                        input_name = re.search(r'name=["\'](.*?)["\']', inp)
                        input_value = re.search(r'value=["\'](.*?)["\']', inp)
                        
                        if input_name:
                            print(f"    - Input: name='{input_name.group(1)}', type='{input_type.group(1) if input_type else 'text'}', value='{input_value.group(1) if input_value else ''}'")
            
            # Buscar JavaScript relevante
            js_patterns = [
                r'client_id["\']?\s*[:=]\s*["\'](.*?)["\']',
                r'redirect_uri["\']?\s*[:=]\s*["\'](.*?)["\']',
                r'scope["\']?\s*[:=]\s*["\'](.*?)["\']',
                r'response_type["\']?\s*[:=]\s*["\'](.*?)["\']'
            ]
            
            for pattern in js_patterns:
                matches = re.findall(pattern, response.text)
                if matches:
                    print(f"\n[*] Patrón JS encontrado: {pattern}")
                    for match in matches:
                        print(f"  - {match}")
        
    except Exception as e:
        print(f"[-] Error analizando flujo: {str(e)}")
    
    # Paso 3: Analizar el archivo de configuración
    print("\n[3] Analizando configuración global...")
    settings_url = "https://banca.ibercaja.es/setting/SettingsJs"
    
    try:
        response = session.get(settings_url)
        if response.status_code == 200:
            # Extraer el objeto de configuración
            config_match = re.search(r'__globalSettings=Object\.freeze\((.*?)\);', response.text, re.DOTALL)
            if config_match:
                try:
                    # Limpiar y parsear JSON
                    config_str = config_match.group(1)
                    config_data = json.loads(config_str)
                    print("[+] Configuración global encontrada:")
                    print(json.dumps(config_data, indent=2))
                    
                    with open('global_settings.json', 'w') as f:
                        json.dump(config_data, f, indent=2)
                except:
                    print("[-] Error parseando configuración")
    except Exception as e:
        print(f"[-] Error: {str(e)}")
    
    # Crear resumen del análisis
    print("\n[*] Creando resumen del análisis...")
    with open('auth_flow_summary.txt', 'w') as f:
        f.write("=== ANÁLISIS DEL FLUJO DE AUTENTICACIÓN ===\n\n")
        f.write("1. Sistema de autenticación: OpenID Connect\n")
        f.write("2. Proveedor de identidad: https://identidad.ibercaja.es/\n")
        f.write("3. Endpoint de login: https://sgv.ibercaja.es/auth/login\n")
        f.write("4. Flujo: OAuth 2.0 Authorization Code Flow\n\n")
        f.write("Parámetros necesarios para el login:\n")
        f.write("- client_id: [A obtener del flujo]\n")
        f.write("- redirect_uri: [A obtener del flujo]\n")
        f.write("- response_type: code\n")
        f.write("- scope: openid profile\n")
        f.write("- state: [Generado dinámicamente]\n")
        f.write("- nonce: [Generado dinámicamente]\n")
    
    print("\n[*] Análisis completado. Archivos generados:")
    print("  - openid_config.json")
    print("  - global_settings.json")
    print("  - auth_flow_summary.txt")

if __name__ == "__main__":
    analyze_auth_flow()