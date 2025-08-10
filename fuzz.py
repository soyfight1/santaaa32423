#!/usr/bin/env python3
import requests
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

target = "http://hackme1.vulnmachines.com"

# Common directories for web apps and CTF challenges
directories = [
    "admin", "login", "users", "user", "profile", "profiles", "account", "accounts",
    "api", "app", "application", "portal", "dashboard", "panel", "console",
    "idor", "IDOR", "challenge", "lab", "test", "demo", "vulnerable", "vuln",
    "index.php", "index.html", "home", "main", "welcome", "register", "signup",
    "signin", "auth", "authenticate", "session", "data", "files", "download",
    "upload", "view", "edit", "delete", "update", "create", "list", "show",
    "get", "fetch", "retrieve", "access", "private", "public", "secret",
    "hidden", "backup", "old", "new", "temp", "tmp", "cache", "logs", "log",
    "config", "conf", "settings", "setup", "install", "db", "database",
    "mysql", "phpmyadmin", "wp-admin", "wordpress", "joomla", "drupal",
    ".git", ".svn", ".htaccess", ".htpasswd", ".env", ".config", ".bak",
    "flag", "flags", "ctf", "capture", "challenge1", "level1", "stage1",
    "vulnmachines", "vm", "hackme", "hack", "exploit", "vulnerable-app"
]

def check_directory(path):
    try:
        url = f"{target}/{path}"
        response = requests.get(url, timeout=3, allow_redirects=False)
        
        # Check if it's not a 404 and not the default Apache page
        if response.status_code != 404:
            content_length = len(response.content)
            # Default Apache page is around 10918 bytes
            if content_length != 10918:
                return f"[{response.status_code}] {url} - Size: {content_length}"
    except:
        pass
    return None

print(f"[*] Fuzzing directories on {target}")
print("[*] Looking for the IDOR challenge application...")
print("-" * 50)

found = []
with ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(check_directory, dir): dir for dir in directories}
    
    for future in as_completed(futures):
        result = future.result()
        if result:
            print(result)
            found.append(result)

if found:
    print("\n[+] Found potential directories:")
    for item in found:
        print(item)
else:
    print("\n[-] No directories found with basic wordlist")