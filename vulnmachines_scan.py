#!/usr/bin/env python3
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

target = "http://hackme1.vulnmachines.com"

# VulnMachines specific paths and patterns
paths = [
    # Common VulnMachines patterns
    "vnm", "VNM", "vulnmachines", "VulnMachines", "VULNMACHINES",
    "vm", "VM", "machines", "machine", "vulnerable",
    
    # Challenge patterns
    "challenges", "challenge", "labs", "lab", "exercises", "exercise",
    "missions", "mission", "tasks", "task", "levels", "level",
    "stages", "stage", "problems", "problem", "puzzles", "puzzle",
    
    # Specific vulnerability labs
    "vulnerabilities", "vulnerability", "vulns", "vuln", 
    "exploits", "exploit", "attacks", "attack",
    "web-attacks", "web_attacks", "webattacks",
    
    # IDOR specific combinations
    "idor", "IDOR", "Idor", "idors", "IDORS",
    "idor-lab", "idor_lab", "idorlab", "IDOR-lab", "IDOR_lab", "IDORlab",
    "idor-challenge", "idor_challenge", "idorchallenge",
    "idor-exercise", "idor_exercise", "idorexercise",
    "idor-mission", "idor_mission", "idormission",
    "insecure-direct-object-reference", "insecure_direct_object_reference",
    "direct-object-reference", "direct_object_reference",
    "object-reference", "object_reference",
    
    # Try with extensions
    "idor.php", "IDOR.php", "idor.html", "IDOR.html",
    "idor/index.php", "IDOR/index.php", "idor/index.html", "IDOR/index.html",
    
    # Authentication related
    "auth", "authentication", "login", "signin", "signup", "register",
    "users", "user", "profiles", "profile", "accounts", "account",
    "members", "member", "dashboard", "panel", "console",
    
    # API endpoints
    "api", "API", "api/v1", "api/v2", "api/users", "api/user",
    "api/profile", "api/account", "api/idor", "api/IDOR",
    "rest", "REST", "rest/api", "REST/API",
    "graphql", "GraphQL", "graphql/api",
    
    # Hidden or backup paths
    ".hidden", ".secret", ".backup", ".bak", ".old", ".new",
    "backup", "backups", "bak", "old", "new", "temp", "tmp",
    "private", "secret", "hidden", "internal", "restricted",
    
    # Common CTF paths
    "ctf", "CTF", "capture", "flag", "flags", "FLAG", "FLAGS",
    "ctf/idor", "CTF/IDOR", "ctf/web", "CTF/WEB",
    
    # Try with query parameters
    "index.php?page=idor", "index.php?challenge=idor", "index.php?lab=idor",
    "index.php?vuln=idor", "index.php?type=idor", "index.php?module=idor",
    "main.php?page=idor", "app.php?page=idor", "challenge.php?type=idor",
    
    # User/Profile endpoints with IDs
    "user.php?id=1", "profile.php?id=1", "account.php?id=1",
    "users.php?id=1", "member.php?id=1", "view.php?id=1",
    "show.php?id=1", "display.php?id=1", "get.php?id=1",
    "fetch.php?id=1", "load.php?id=1", "read.php?id=1",
    
    # File/Document access
    "files", "file", "documents", "document", "docs", "doc",
    "downloads", "download", "uploads", "upload", "media",
    "file.php?id=1", "document.php?id=1", "download.php?id=1",
    "view.php?file=1", "get.php?file=1", "fetch.php?doc=1",
    
    # Database related
    "db", "database", "mysql", "phpmyadmin", "adminer", "phpMyAdmin",
    "sql", "SQL", "query", "queries", "data", "DATA",
    
    # Configuration files
    "config", "configuration", "settings", "setup", "install",
    "config.php", "configuration.php", "settings.php", "setup.php",
    ".env", ".config", ".htaccess", ".htpasswd",
    
    # Robots and sitemap
    "robots.txt", "sitemap.xml", "sitemap.txt", "humans.txt",
    
    # Common vulnerable apps
    "dvwa", "DVWA", "bwapp", "BWAPP", "webgoat", "WebGoat",
    "mutillidae", "Mutillidae", "damn", "DAMN"
]

def check_path(path):
    try:
        url = f"{target}/{path}"
        response = requests.get(url, timeout=3, allow_redirects=False)
        
        if response.status_code == 200:
            content = response.text.lower()
            content_length = len(response.content)
            
            # Skip Apache default page
            if 'apache2 ubuntu default' in content or content_length == 10918:
                return None
            
            # High priority: IDOR specific content
            if any(keyword in content for keyword in ['idor', 'insecure direct object', 'object reference']):
                if any(indicator in content for indicator in ['form', 'input', 'submit', 'login', 'user', 'profile', 'flag', 'vnm']):
                    return f"[IDOR CHALLENGE!] {url} - Active IDOR page with forms/inputs"
                else:
                    return f"[IDOR Related] {url} - Contains IDOR keywords"
            
            # VulnMachines specific
            elif any(keyword in content for keyword in ['vulnmachines', 'vnm{', 'flag', 'capture the flag']):
                return f"[VulnMachines] {url} - VulnMachines challenge page"
            
            # User/Profile pages (potential IDOR)
            elif any(keyword in content for keyword in ['user profile', 'account details', 'member area', 'dashboard']):
                return f"[User System] {url} - Potential IDOR target"
            
            # Login/Auth pages
            elif any(keyword in content for keyword in ['login', 'sign in', 'username', 'password']):
                return f"[Auth Page] {url} - Authentication system"
            
            # Any other non-default content
            elif content_length > 500:
                return f"[Content] {url} - Size: {content_length}"
                
        elif response.status_code in [301, 302]:
            location = response.headers.get('Location', 'unknown')
            return f"[Redirect] {url} -> {location}"
            
        elif response.status_code in [401, 403]:
            return f"[Restricted] {url} - Status: {response.status_code}"
            
    except Exception:
        pass
    
    return None

print("[*] VulnMachines-specific deep scan...")
print(f"[*] Testing {len(paths)} paths for IDOR challenge")
print("-" * 70)

results = {
    'idor': [],
    'vulnmachines': [],
    'user': [],
    'auth': [],
    'redirect': [],
    'restricted': [],
    'content': []
}

with ThreadPoolExecutor(max_workers=50) as executor:
    futures = {executor.submit(check_path, path): path for path in paths}
    
    for future in as_completed(futures):
        result = future.result()
        if result:
            print(result)
            if "IDOR CHALLENGE" in result or "IDOR Related" in result:
                results['idor'].append(result)
            elif "VulnMachines" in result:
                results['vulnmachines'].append(result)
            elif "User System" in result:
                results['user'].append(result)
            elif "Auth Page" in result:
                results['auth'].append(result)
            elif "Redirect" in result:
                results['redirect'].append(result)
            elif "Restricted" in result:
                results['restricted'].append(result)
            elif "Content" in result:
                results['content'].append(result)

print("\n" + "=" * 70)
print("[*] SCAN RESULTS:")
print("=" * 70)

if results['idor']:
    print("\n[!!!] IDOR SPECIFIC FINDINGS:")
    for item in results['idor']:
        print(item)
    print("\n[ACTION] These are your primary targets for IDOR exploitation!")

if results['vulnmachines']:
    print("\n[!] VulnMachines Challenge Pages:")
    for item in results['vulnmachines']:
        print(item)

if results['user']:
    print("\n[+] User/Profile Systems (potential IDOR):")
    for item in results['user']:
        print(item)

if results['auth']:
    print("\n[*] Authentication Pages:")
    for item in results['auth']:
        print(item)

if results['redirect']:
    print("\n[>] Redirects:")
    for item in results['redirect'][:5]:  # Limit output
        print(item)

if results['restricted']:
    print("\n[X] Restricted Access:")
    for item in results['restricted']:
        print(item)

if not any(results.values()):
    print("\n[-] No IDOR challenge found with standard paths")
    print("[*] The challenge might require:")
    print("    - Special headers or cookies")
    print("    - Authentication first")
    print("    - Non-standard port (confirm 7500 is really down)")
    print("    - Subdomain or virtual host")