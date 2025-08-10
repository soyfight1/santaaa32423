#!/usr/bin/env python3
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

target = "http://hackme1.vulnmachines.com"

# Extended wordlist focused on IDOR and common CTF paths
directories = [
    # IDOR specific
    "idor", "IDOR", "idor-lab", "idor_lab", "idor-challenge", "idor_challenge",
    "insecure-direct-object-reference", "direct-object-reference", 
    "object-reference", "reference", "refs", "id", "uid", "userid", "user_id",
    
    # VulnMachines specific
    "vulnmachines", "vnm", "vm", "machine", "vulnerable", "vuln", "vulns",
    "lab", "labs", "challenge", "challenges", "ctf", "flag", "flags",
    
    # Common web app paths
    "app", "application", "webapp", "web", "www", "site", "portal", "platform",
    "system", "service", "api", "v1", "v2", "rest", "graphql", "endpoint",
    
    # User management
    "users", "user", "member", "members", "profile", "profiles", "account",
    "accounts", "customer", "customers", "client", "clients", "person", "people",
    
    # Auth/Session
    "login", "signin", "signup", "register", "auth", "authenticate", "oauth",
    "session", "sessions", "token", "tokens", "jwt", "cookie", "cookies",
    
    # Data access
    "data", "info", "information", "details", "view", "show", "display", "get",
    "fetch", "retrieve", "access", "read", "load", "download", "export",
    
    # File/Document management
    "file", "files", "document", "documents", "doc", "docs", "pdf", "pdfs",
    "image", "images", "img", "imgs", "photo", "photos", "pic", "pics",
    "media", "upload", "uploads", "attachment", "attachments",
    
    # Admin/Management
    "admin", "administrator", "manage", "management", "control", "panel",
    "dashboard", "console", "backend", "backoffice", "cp", "controlpanel",
    
    # Testing/Debug
    "test", "testing", "debug", "dev", "development", "demo", "example",
    "sample", "sandbox", "staging", "qa", "uat", "beta", "alpha",
    
    # Database related
    "db", "database", "sql", "mysql", "postgres", "mongodb", "redis",
    "query", "queries", "search", "find", "lookup", "select",
    
    # Common PHP files
    "index.php", "home.php", "main.php", "login.php", "user.php", "users.php",
    "profile.php", "account.php", "view.php", "show.php", "get.php", "data.php",
    "api.php", "service.php", "fetch.php", "download.php", "file.php",
    
    # Common patterns with IDs
    "user.php?id=1", "profile.php?id=1", "view.php?id=1", "show.php?id=1",
    "get.php?id=1", "data.php?id=1", "file.php?id=1", "document.php?id=1",
    "download.php?id=1", "export.php?id=1", "info.php?id=1", "details.php?id=1",
    
    # Try with different parameter names
    "index.php?user=1", "index.php?uid=1", "index.php?userid=1", "index.php?user_id=1",
    "index.php?customer=1", "index.php?client=1", "index.php?member=1",
    
    # Hidden directories
    "hidden", "secret", "private", "internal", "restricted", "confidential",
    "secure", "protected", "backup", "bak", "old", "new", "temp", "tmp",
    
    # Common CTF paths
    "hackme", "hack", "exploit", "pwn", "own", "root", "shell", "rce",
    "sqli", "xss", "csrf", "ssrf", "lfi", "rfi", "xxe", "ssti",
    
    # Try subdirectories of found paths
    "conf/idor", "phpmyadmin/idor", "conf/app", "phpmyadmin/app"
]

def check_directory(path):
    try:
        url = f"{target}/{path}"
        response = requests.get(url, timeout=3, allow_redirects=False)
        
        # Check various success conditions
        if response.status_code in [200, 301, 302, 401, 403]:
            content_length = len(response.content)
            # Ignore default Apache page (10918 bytes)
            if content_length != 10918:
                # Check for interesting content
                content_lower = response.text.lower()
                if any(keyword in content_lower for keyword in ['idor', 'user', 'profile', 'login', 'flag', 'vnm', 'vulnmachine']):
                    return f"[INTERESTING] [{response.status_code}] {url} - Size: {content_length}"
                elif response.status_code != 404:
                    return f"[{response.status_code}] {url} - Size: {content_length}"
    except:
        pass
    return None

print(f"[*] Extended fuzzing on {target}")
print("[*] Searching for IDOR vulnerable application...")
print("-" * 60)

found = []
interesting = []

with ThreadPoolExecutor(max_workers=30) as executor:
    futures = {executor.submit(check_directory, dir): dir for dir in directories}
    
    for future in as_completed(futures):
        result = future.result()
        if result:
            print(result)
            if "[INTERESTING]" in result:
                interesting.append(result)
            else:
                found.append(result)

print("\n" + "=" * 60)
if interesting:
    print("[+] INTERESTING FINDINGS (likely IDOR related):")
    for item in interesting:
        print(item)
    print()

if found:
    print("[+] Other directories found:")
    for item in found:
        print(item)
else:
    print("[-] No additional directories found")