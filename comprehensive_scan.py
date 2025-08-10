#!/usr/bin/env python3
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

target = "http://hackme1.vulnmachines.com"

# Extended search patterns
paths = [
    # IDOR specific patterns with various extensions
    "idor", "IDOR", "Idor",
    "idor.php", "IDOR.php", "idor.html", "IDOR.html", "idor.asp", "idor.aspx",
    "idor/", "IDOR/", "idor/index.php", "IDOR/index.php", "idor/index.html",
    
    # With numbers (common in CTF)
    "idor1", "idor2", "idor3", "IDOR1", "IDOR2", "IDOR3",
    "idor1.php", "idor2.php", "idor3.php",
    "idor1/", "idor2/", "idor3/",
    
    # Challenge variations
    "challenge", "challenges", "challenge/idor", "challenges/idor",
    "challenge1", "challenge2", "challenge3",
    "lab", "labs", "lab/idor", "labs/idor",
    "lab1", "lab2", "lab3",
    "exercise", "exercises", "exercise/idor",
    "task", "tasks", "task/idor",
    "mission", "missions", "mission/idor",
    "level", "levels", "level/idor",
    "stage", "stages", "stage/idor",
    
    # Web application specific
    "webapp", "webapp/idor", "webapps", "webapps/idor",
    "app", "apps", "app/idor", "apps/idor",
    "application", "applications",
    "site", "sites", "website", "websites",
    "portal", "portals", "system", "systems",
    
    # Authentication/User management
    "login", "login.php", "signin", "signin.php", "auth", "auth.php",
    "register", "register.php", "signup", "signup.php",
    "user", "users", "user.php", "users.php",
    "profile", "profiles", "profile.php", "profiles.php",
    "account", "accounts", "account.php", "accounts.php",
    "member", "members", "member.php", "members.php",
    "dashboard", "dashboard.php", "panel", "panel.php",
    "admin", "admin.php", "administrator", "manage",
    
    # File management
    "files", "file", "files.php", "file.php",
    "documents", "document", "documents.php", "document.php",
    "downloads", "download", "downloads.php", "download.php",
    "uploads", "upload", "uploads.php", "upload.php",
    "media", "media.php", "resources", "resource.php",
    "pdfs", "pdf", "pdfs.php", "pdf.php",
    
    # API and services
    "api", "api/", "api/v1", "api/v2", "api.php",
    "service", "services", "service.php", "services.php",
    "rest", "rest/", "graphql", "graphql/",
    "endpoint", "endpoints",
    
    # Database related
    "db", "database", "data", "data.php",
    "query", "query.php", "search", "search.php",
    
    # Common vulnerable apps
    "dvwa", "DVWA", "bwapp", "bWAPP", "mutillidae", "webgoat",
    
    # VulnMachines specific
    "vnm", "VNM", "vulnmachines", "VulnMachines",
    "vm", "VM", "machine", "machines",
    "vulnerable", "vuln", "vulnerability",
    
    # Try with different cases and separators
    "insecure-direct-object-reference",
    "insecure_direct_object_reference",
    "InsecureDirectObjectReference",
    "direct-object-reference",
    "direct_object_reference",
    "DirectObjectReference",
    "object-reference",
    "object_reference",
    "ObjectReference"
]

def check_path(path):
    try:
        url = f"{target}/{path}"
        response = requests.get(url, timeout=3, allow_redirects=True)
        
        if response.status_code == 200:
            content = response.text.lower()
            content_length = len(response.content)
            
            # Skip Apache default
            if 'apache2 ubuntu default' in content or content_length == 10918:
                return None
            
            # High priority: Forms and interactive elements
            if '<form' in content or '<input' in content:
                if any(keyword in content for keyword in ['login', 'user', 'password', 'submit', 'file', 'download', 'upload']):
                    return f"[FORM FOUND] {url} - Interactive page with forms"
                    
            # IDOR specific
            if any(keyword in content for keyword in ['idor', 'insecure direct object', 'object reference']):
                return f"[IDOR CONTENT] {url} - Contains IDOR keywords"
            
            # File/Download related
            if any(keyword in content for keyword in ['download', 'file', 'document', 'pdf', 'export']):
                if 'href=' in content or 'action=' in content:
                    return f"[FILE SYSTEM] {url} - File/Download functionality"
            
            # User/Profile system
            if any(keyword in content for keyword in ['profile', 'user', 'account', 'member', 'dashboard']):
                return f"[USER SYSTEM] {url} - User management page"
            
            # Authentication
            if any(keyword in content for keyword in ['login', 'signin', 'authenticate', 'password']):
                return f"[AUTH PAGE] {url} - Authentication system"
            
            # VulnMachines/CTF
            if any(keyword in content for keyword in ['flag', 'vnm{', 'capture', 'challenge', 'vulnmachines']):
                return f"[CTF/VM] {url} - Challenge related content"
            
            # Any non-default content
            if content_length > 500:
                # Check if it has links or forms
                if 'href=' in content or 'form' in content or 'onclick' in content:
                    return f"[ACTIVE PAGE] {url} - Size: {content_length}"
                    
        elif response.status_code in [301, 302]:
            location = response.headers.get('Location', '')
            if any(keyword in location.lower() for keyword in ['idor', 'file', 'download', 'user', 'profile']):
                return f"[REDIRECT] {url} -> {location}"
                
        elif response.status_code in [401, 403]:
            return f"[RESTRICTED] {url} - Requires authentication"
            
    except Exception:
        pass
    
    return None

print("[*] Comprehensive Web Application Scan")
print(f"[*] Target: {target}")
print(f"[*] Testing {len(paths)} paths")
print("-" * 70)

results = {
    'forms': [],
    'idor': [],
    'files': [],
    'users': [],
    'auth': [],
    'ctf': [],
    'active': [],
    'restricted': []
}

with ThreadPoolExecutor(max_workers=50) as executor:
    futures = {executor.submit(check_path, path): path for path in paths}
    
    for future in as_completed(futures):
        result = future.result()
        if result:
            print(result)
            
            if "[FORM FOUND]" in result:
                results['forms'].append(result)
            elif "[IDOR CONTENT]" in result:
                results['idor'].append(result)
            elif "[FILE SYSTEM]" in result:
                results['files'].append(result)
            elif "[USER SYSTEM]" in result:
                results['users'].append(result)
            elif "[AUTH PAGE]" in result:
                results['auth'].append(result)
            elif "[CTF/VM]" in result:
                results['ctf'].append(result)
            elif "[ACTIVE PAGE]" in result:
                results['active'].append(result)
            elif "[RESTRICTED]" in result:
                results['restricted'].append(result)

print("\n" + "=" * 70)
print("[*] SCAN RESULTS SUMMARY")
print("=" * 70)

if results['forms']:
    print("\n[!!!] PAGES WITH FORMS (High Priority):")
    for item in results['forms']:
        print(item)
    print("\n[ACTION] These pages likely have IDOR vulnerabilities!")

if results['idor']:
    print("\n[!!] IDOR SPECIFIC CONTENT:")
    for item in results['idor']:
        print(item)

if results['files']:
    print("\n[!] FILE/DOWNLOAD SYSTEMS:")
    for item in results['files']:
        print(item)

if results['users']:
    print("\n[+] USER/PROFILE SYSTEMS:")
    for item in results['users']:
        print(item)

if results['auth']:
    print("\n[*] AUTHENTICATION PAGES:")
    for item in results['auth']:
        print(item)

if results['ctf']:
    print("\n[*] CTF/VULNMACHINES RELATED:")
    for item in results['ctf']:
        print(item)

if results['restricted']:
    print("\n[X] RESTRICTED ACCESS:")
    for item in results['restricted'][:5]:
        print(item)

if not any(results.values()):
    print("\n[-] No web applications found")
    print("[*] The IDOR challenge might be:")
    print("    - On a different port (recheck 7500)")
    print("    - Behind a specific virtual host")
    print("    - Requiring special headers")
    print("    - In a subdirectory not yet discovered")