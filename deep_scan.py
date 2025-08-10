#!/usr/bin/env python3
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import itertools

target = "http://hackme1.vulnmachines.com"

# Different levels and combinations
base_paths = ["", "labs", "challenges", "vulns", "exercises", "practice", "test", "demo", "learn", "tutorial"]
vuln_types = ["idor", "IDOR", "insecure", "direct", "object", "reference", "access", "authorization"]
extensions = ["", ".php", ".html", "/", "/index.php", "/index.html", "/main.php", "/app.php"]

# Generate combinations
paths_to_test = []

# Direct paths
for vuln in vuln_types:
    for ext in extensions:
        paths_to_test.append(f"{vuln}{ext}")

# Subdirectory combinations
for base in base_paths:
    for vuln in vuln_types:
        if base:
            paths_to_test.append(f"{base}/{vuln}")
            paths_to_test.append(f"{base}/{vuln}/")
            paths_to_test.append(f"{base}/{vuln}/index.php")
            paths_to_test.append(f"{base}/{vuln}.php")

# Try numbered variations
for i in range(1, 11):
    paths_to_test.extend([
        f"lab{i}", f"lab{i}/idor", f"challenge{i}", f"challenge{i}/idor",
        f"level{i}", f"level{i}/idor", f"task{i}", f"task{i}/idor",
        f"idor{i}", f"idor{i}.php", f"idor-{i}", f"idor_{i}"
    ])

# Common parameter patterns
param_paths = [
    "index.php?page=idor", "index.php?lab=idor", "index.php?challenge=idor",
    "index.php?vuln=idor", "index.php?type=idor", "index.php?lesson=idor",
    "main.php?page=idor", "app.php?page=idor", "view.php?page=idor",
    "?page=idor", "?lab=idor", "?challenge=idor"
]
paths_to_test.extend(param_paths)

# Remove duplicates
paths_to_test = list(set(paths_to_test))

def check_path(path):
    try:
        url = f"{target}/{path}" if path else target
        response = requests.get(url, timeout=3, allow_redirects=True)
        
        if response.status_code == 200:
            content = response.text.lower()
            # Look for IDOR-related keywords
            idor_keywords = ['idor', 'insecure direct object', 'object reference', 
                           'user profile', 'view profile', 'user details', 'account details',
                           'userid', 'user_id', 'uid', 'id=', 'vnm{', 'flag', 'challenge']
            
            if any(keyword in content for keyword in idor_keywords):
                # Extra check for actual content (not error pages)
                if 'not found' not in content and '404' not in content:
                    return f"[FOUND IDOR!] {url} - Contains IDOR keywords"
            
            # Check if it's a different page than Apache default
            if len(response.content) not in [10918, 0] and response.status_code == 200:
                if 'apache' not in content and 'ubuntu' not in content:
                    return f"[Interesting] {url} - Size: {len(response.content)}"
                    
        elif response.status_code in [301, 302]:
            return f"[Redirect] {url} -> {response.headers.get('Location', 'unknown')}"
            
    except Exception as e:
        pass
    return None

print("[*] Deep scanning for IDOR challenge...")
print(f"[*] Testing {len(paths_to_test)} paths")
print("-" * 60)

results = []
idor_found = []

with ThreadPoolExecutor(max_workers=30) as executor:
    futures = {executor.submit(check_path, path): path for path in paths_to_test}
    
    for future in as_completed(futures):
        result = future.result()
        if result:
            print(result)
            if "FOUND IDOR" in result:
                idor_found.append(result)
            else:
                results.append(result)

print("\n" + "=" * 60)
if idor_found:
    print("[!!!] IDOR CHALLENGE FOUND:")
    for item in idor_found:
        print(item)
    print("\n[*] Focus on these URLs for the IDOR exploitation!")
elif results:
    print("[+] Interesting paths found (may need further investigation):")
    for item in results:
        print(item)
else:
    print("[-] No IDOR-specific paths found in common locations")