#!/usr/bin/env python3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json

def analyze_with_selenium():
    url = "https://banca.ibercaja.es/"
    
    # Configurar Chrome en modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Inicializar driver
    print("[*] Iniciando Chrome driver...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print(f"[*] Navegando a {url}")
        driver.get(url)
        
        # Esperar a que la página cargue
        print("[*] Esperando que la página cargue completamente...")
        time.sleep(5)  # Dar tiempo para que Angular cargue
        
        # Buscar formularios
        forms = driver.find_elements(By.TAG_NAME, "form")
        print(f"\n[*] Formularios encontrados: {len(forms)}")
        
        # Buscar inputs
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"\n[*] Inputs encontrados: {len(inputs)}")
        for inp in inputs:
            input_type = inp.get_attribute("type") or "text"
            input_name = inp.get_attribute("name") or "N/A"
            input_id = inp.get_attribute("id") or "N/A"
            input_placeholder = inp.get_attribute("placeholder") or ""
            input_class = inp.get_attribute("class") or ""
            
            if input_type in ['text', 'password', 'email', 'tel'] or any(word in (input_name + input_id + input_placeholder + input_class).lower() for word in ['user', 'pass', 'login', 'usuario', 'contraseña', 'clave']):
                print(f"  - Type: {input_type}, Name: {input_name}, ID: {input_id}, Placeholder: {input_placeholder}")
                print(f"    Class: {input_class[:100]}")
        
        # Buscar botones
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"\n[*] Botones encontrados: {len(buttons)}")
        for btn in buttons[:10]:
            btn_text = btn.text.strip()
            btn_type = btn.get_attribute("type") or "button"
            btn_class = btn.get_attribute("class") or ""
            btn_onclick = btn.get_attribute("onclick") or ""
            
            if any(word in (btn_text + btn_class).lower() for word in ['login', 'entrar', 'acceder', 'acceso', 'iniciar']):
                print(f"  - Text: '{btn_text}', Type: {btn_type}")
                print(f"    Class: {btn_class[:100]}")
        
        # Buscar elementos con texto relacionado a login
        print("\n[*] Buscando elementos con texto de login...")
        elements_with_text = driver.find_elements(By.XPATH, "//*[contains(text(), 'Acceso') or contains(text(), 'acceso') or contains(text(), 'Usuario') or contains(text(), 'usuario') or contains(text(), 'Contraseña') or contains(text(), 'contraseña') or contains(text(), 'Entrar') or contains(text(), 'entrar')]")
        print(f"[*] Elementos con texto relevante: {len(elements_with_text)}")
        for elem in elements_with_text[:5]:
            print(f"  - Tag: {elem.tag_name}, Text: '{elem.text.strip()}'")
        
        # Buscar componentes Angular específicos
        print("\n[*] Buscando componentes Angular...")
        angular_components = driver.find_elements(By.CSS_SELECTOR, "[ng-click], [ng-model], [ng-submit], [(ngModel)], [formControlName], [formGroupName]")
        print(f"[*] Componentes Angular encontrados: {len(angular_components)}")
        
        # Guardar el HTML renderizado
        with open('rendered_page.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("\n[*] HTML renderizado guardado en rendered_page.html")
        
        # Buscar en el código fuente patrones de API
        page_source = driver.page_source
        if 'api' in page_source.lower() or 'login' in page_source.lower():
            print("\n[*] Patrones de API/Login encontrados en el código fuente")
        
        # Intentar encontrar elementos interactivos
        clickable_elements = driver.find_elements(By.CSS_SELECTOR, "a, button, [role='button'], [onclick], [ng-click]")
        print(f"\n[*] Elementos clickeables encontrados: {len(clickable_elements)}")
        
        # Buscar iframes
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"\n[*] iFrames encontrados: {len(iframes)}")
        for iframe in iframes:
            src = iframe.get_attribute("src") or ""
            if src:
                print(f"  - src: {src}")
        
        # Tomar screenshot
        driver.save_screenshot("screenshot.png")
        print("\n[*] Screenshot guardado como screenshot.png")
        
        # Buscar modales o overlays ocultos
        hidden_elements = driver.find_elements(By.CSS_SELECTOR, "[style*='display: none'], [style*='display:none'], .modal, .overlay, .popup")
        print(f"\n[*] Elementos ocultos/modales encontrados: {len(hidden_elements)}")
        
    except Exception as e:
        print(f"\n[!] Error: {str(e)}")
    
    finally:
        driver.quit()
        print("\n[*] Driver cerrado")

if __name__ == "__main__":
    analyze_with_selenium()