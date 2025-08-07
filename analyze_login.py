#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import re

def analyze_website():
    url = "https://banca.ibercaja.es/"
    
    # Headers para parecer un navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    # Obtener la página principal
    print("[*] Analizando:", url)
    response = requests.get(url, headers=headers)
    print(f"[*] Status Code: {response.status_code}")
    
    # Parsear HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Buscar formularios
    forms = soup.find_all('form')
    print(f"\n[*] Formularios encontrados: {len(forms)}")
    
    # Buscar inputs
    inputs = soup.find_all('input')
    print(f"\n[*] Inputs encontrados: {len(inputs)}")
    for inp in inputs:
        input_type = inp.get('type', 'text')
        input_name = inp.get('name', 'N/A')
        input_id = inp.get('id', 'N/A')
        input_placeholder = inp.get('placeholder', '')
        
        if input_type in ['text', 'password', 'email', 'tel'] or 'user' in str(inp).lower() or 'pass' in str(inp).lower():
            print(f"  - Type: {input_type}, Name: {input_name}, ID: {input_id}, Placeholder: {input_placeholder}")
    
    # Buscar botones
    buttons = soup.find_all(['button', 'input'], type=['submit', 'button'])
    print(f"\n[*] Botones encontrados: {len(buttons)}")
    for btn in buttons[:5]:
        btn_text = btn.get('value', btn.text.strip() if hasattr(btn, 'text') else '')
        btn_type = btn.get('type', 'button')
        btn_onclick = btn.get('onclick', '')
        if 'login' in str(btn).lower() or 'entrar' in str(btn).lower() or 'acceder' in str(btn).lower():
            print(f"  - Text: {btn_text}, Type: {btn_type}, OnClick: {btn_onclick[:50]}...")
    
    # Buscar scripts JavaScript que puedan contener lógica de login
    scripts = soup.find_all('script')
    print(f"\n[*] Scripts encontrados: {len(scripts)}")
    
    login_patterns = ['login', 'authenticate', 'usuario', 'password', 'contraseña', 'acceder', 'entrar']
    for script in scripts:
        if script.string:
            for pattern in login_patterns:
                if pattern in script.string.lower():
                    print(f"  - Script contiene patrón '{pattern}'")
                    break
    
    # Buscar enlaces relacionados con login
    links = soup.find_all('a')
    print(f"\n[*] Enlaces encontrados: {len(links)}")
    for link in links:
        href = link.get('href', '')
        text = link.text.strip()
        if any(word in href.lower() + text.lower() for word in ['login', 'acceso', 'entrar', 'usuario']):
            print(f"  - Texto: {text}, Href: {href}")
    
    # Buscar iframes que puedan contener el formulario
    iframes = soup.find_all('iframe')
    print(f"\n[*] iFrames encontrados: {len(iframes)}")
    for iframe in iframes:
        src = iframe.get('src', '')
        if src:
            print(f"  - src: {src}")
    
    # Guardar el HTML para análisis posterior
    with open('index_full.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("\n[*] HTML completo guardado en index_full.html")
    
    # Buscar patrones de API endpoints en el HTML
    api_patterns = re.findall(r'["\']([^"\']*(?:api|login|auth|usuario|acceso)[^"\']*)["\']', response.text, re.IGNORECASE)
    if api_patterns:
        print("\n[*] Posibles endpoints encontrados:")
        unique_patterns = list(set(api_patterns))
        for pattern in unique_patterns[:10]:
            if len(pattern) < 100:  # Filtrar strings muy largos
                print(f"  - {pattern}")

if __name__ == "__main__":
    analyze_website()