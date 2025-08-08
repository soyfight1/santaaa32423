#!/usr/bin/env python3
import cloudscraper
import requests
from bs4 import BeautifulSoup
import time
import json
import re

def analyze_target():
    target_url = "https://hispachan.in/"
    
    print("[*] Iniciando análisis de", target_url)
    print("[*] Intentando bypasear Cloudflare...")
    
    # Crear instancia de cloudscraper
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'mobile': False
        }
    )
    
    try:
        # Intentar obtener la página
        response = scraper.get(target_url, timeout=30)
        
        if response.status_code == 200:
            print("[+] Bypass exitoso! Status:", response.status_code)
            print("[+] Headers recibidos:")
            for header, value in response.headers.items():
                print(f"    {header}: {value}")
            
            # Analizar el contenido
            soup = BeautifulSoup(response.text, 'html.parser')
            
            print("\n[*] Analizando contenido HTML...")
            print(f"[+] Título: {soup.title.string if soup.title else 'No encontrado'}")
            
            # Buscar formularios
            forms = soup.find_all('form')
            print(f"\n[+] Formularios encontrados: {len(forms)}")
            for i, form in enumerate(forms):
                print(f"    Form {i+1}:")
                print(f"      Action: {form.get('action', 'N/A')}")
                print(f"      Method: {form.get('method', 'GET')}")
                inputs = form.find_all(['input', 'textarea'])
                for inp in inputs:
                    print(f"      Input: {inp.get('name', 'unnamed')} - Type: {inp.get('type', 'text')}")
            
            # Buscar scripts
            scripts = soup.find_all('script')
            print(f"\n[+] Scripts encontrados: {len(scripts)}")
            for i, script in enumerate(scripts[:5]):  # Solo los primeros 5
                src = script.get('src', 'inline')
                print(f"    Script {i+1}: {src}")
            
            # Buscar comentarios HTML
            comments = soup.find_all(string=lambda text: isinstance(text, str) and text.strip().startswith('<!--'))
            print(f"\n[+] Comentarios HTML encontrados: {len(comments)}")
            for comment in comments[:3]:  # Solo los primeros 3
                print(f"    {comment.strip()[:100]}...")
            
            # Buscar links
            links = soup.find_all('a', href=True)
            print(f"\n[+] Links encontrados: {len(links)}")
            unique_links = set()
            for link in links:
                href = link['href']
                if href.startswith('http'):
                    unique_links.add(href)
                elif href.startswith('/'):
                    unique_links.add(target_url.rstrip('/') + href)
            
            print(f"[+] Links únicos externos/internos: {len(unique_links)}")
            for link in list(unique_links)[:10]:  # Solo los primeros 10
                print(f"    {link}")
            
            # Guardar el HTML completo
            with open('/workspace/hispachan_content.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("\n[+] HTML guardado en: /workspace/hispachan_content.html")
            
            # Buscar información de tecnologías
            print("\n[*] Analizando tecnologías...")
            
            # Buscar generadores
            generators = soup.find_all('meta', {'name': 'generator'})
            for gen in generators:
                print(f"[+] Generator: {gen.get('content', 'N/A')}")
            
            # Buscar frameworks JS
            if 'angular' in response.text.lower():
                print("[+] Posible uso de AngularJS")
            if 'react' in response.text.lower():
                print("[+] Posible uso de React")
            if 'vue' in response.text.lower():
                print("[+] Posible uso de Vue.js")
            
            return True
            
        else:
            print(f"[-] Error: Status code {response.status_code}")
            print(f"[-] Response: {response.text[:500]}...")
            return False
            
    except Exception as e:
        print(f"[-] Error durante el análisis: {str(e)}")
        return False

if __name__ == "__main__":
    analyze_target()