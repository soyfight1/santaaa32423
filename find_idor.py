#!/usr/bin/env python3
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

# Try different hosts/ports combinations
targets = [
    "http://hackme1.vulnmachines.com",
    "http://hackme1.vulnmachines.com:80",
    "http://hackme1.vulnmachines.com:8080",
    "http://hackme1.vulnmachines.com:8000",
    "http://hackme1.vulnmachines.com:3000",
    "http://hackme1.vulnmachines.com:5000"
]

# Different file combinations
files = [
    "", "index.php", "index.html", "main.php", "app.php", 
    "idor.php", "IDOR.php", "challenge.php", "lab.php",
    "vulnerable.php", "vuln.php", "test.php", "demo.php"
]

# Parameter combinations
params = [
    "?page=idor", "?lab=idor", "?challenge=idor", "?vuln=idor",
    "?id=1", "?user=1", "?uid=1", "?userid=1", "?user_id=1",
    "?profile=1", "?account=1", "?customer=1", "?member=1",
    "?file=idor", "?action=idor", "?module=idor", "?section=idor"
]

# Also try direct IDOR paths
direct_paths = [
    "/idor", "/IDOR", "/idor/", "/IDOR/",
    "/idor/index.php", "/IDOR/index.php",
    "/idor/main.php", "/IDOR/main.php",
    "/challenges/idor", "/labs/idor", "/vulns/idor",
    "/exercises/idor", "/practice/idor", "/lessons/idor"
]

def test_url(url):
    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
        if response.status_code == 200:
            content = response.text.lower()
            
            # Check for IDOR-specific content
            if any(keyword in content for keyword in ['idor', 'insecure direct object', 'object reference']):
                # Make sure it's not the Apache default page
                if 'apache2 ubuntu default' not in content:
                    # Look for forms, user profiles, or challenge indicators
                    if any(indicator in content for indicator in ['form', 'login', 'user', 'profile', 'submit', 'flag', 'vnm', 'challenge', 'mission']):
                        return f"[IDOR FOUND!] {url} - Active IDOR challenge page"
                    else:
                        return f"[Possible] {url} - Contains IDOR keywords"
            
            # Check for login/user pages that might be part of IDOR
            elif any(keyword in content for keyword in ['login', 'signin', 'user profile', 'account', 'dashboard']):
                if 'apache2 ubuntu default' not in content:
                    return f"[Related] {url} - User/Login page (might be IDOR related)"
                    
        elif response.status_code in [301, 302, 303, 307, 308]:
            location = response.headers.get('Location', '')
            if location:
                return f"[Redirect] {url} -> {location}"
                
    except requests.exceptions.ConnectTimeout:
        pass
    except requests.exceptions.ConnectionError:
        pass
    except Exception as e:
        pass
    
    return None

print("[*] Comprehensive IDOR search across multiple ports and paths...")
print("-" * 70)

all_urls = []

# Generate all URL combinations
for target in targets:
    # Direct paths
    for path in direct_paths:
        all_urls.append(f"{target}{path}")
    
    # Files with parameters
    for file in files:
        for param in params:
            if file:
                all_urls.append(f"{target}/{file}{param}")
            else:
                all_urls.append(f"{target}{param}")

# Remove duplicates
all_urls = list(set(all_urls))
print(f"[*] Testing {len(all_urls)} unique URLs...")
print("-" * 70)

results = {
    'idor': [],
    'possible': [],
    'related': [],
    'redirect': []
}

with ThreadPoolExecutor(max_workers=50) as executor:
    futures = {executor.submit(test_url, url): url for url in all_urls}
    
    for future in as_completed(futures):
        result = future.result()
        if result:
            print(result)
            if "IDOR FOUND" in result:
                results['idor'].append(result)
            elif "Possible" in result:
                results['possible'].append(result)
            elif "Related" in result:
                results['related'].append(result)
            elif "Redirect" in result:
                results['redirect'].append(result)

print("\n" + "=" * 70)
print("[*] SCAN COMPLETE - Summary:")
print("=" * 70)

if results['idor']:
    print("\n[!!!] CONFIRMED IDOR CHALLENGES:")
    for item in results['idor']:
        print(item)
    print("\n[ACTION] Focus on these URLs for immediate exploitation!")
    
if results['possible']:
    print("\n[+] Possible IDOR locations:")
    for item in results['possible']:
        print(item)
        
if results['related']:
    print("\n[*] Related pages (might lead to IDOR):")
    for item in results['related']:
        print(item)
        
if results['redirect']:
    print("\n[>] Redirects found:")
    for item in results['redirect']:
        print(item)

if not any(results.values()):
    print("\n[-] No IDOR challenge found on common ports/paths")
    print("[*] The challenge might be on a non-standard port or require special access")