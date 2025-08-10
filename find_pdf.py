#!/usr/bin/env python3
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

target = "http://hackme1.vulnmachines.com"

# Common PDF locations and naming patterns
pdf_paths = [
    # Direct PDF files
    "file.pdf", "document.pdf", "download.pdf", "pdf.pdf",
    "idor.pdf", "IDOR.pdf", "challenge.pdf", "hint.pdf",
    "flag.pdf", "vnm.pdf", "vulnmachines.pdf", "vm.pdf",
    "user.pdf", "users.pdf", "profile.pdf", "profiles.pdf",
    "account.pdf", "accounts.pdf", "data.pdf", "info.pdf",
    "manual.pdf", "guide.pdf", "instructions.pdf", "readme.pdf",
    "report.pdf", "test.pdf", "demo.pdf", "example.pdf",
    
    # Numbered PDFs
    "1.pdf", "2.pdf", "3.pdf", "file1.pdf", "file2.pdf", 
    "document1.pdf", "document2.pdf", "user1.pdf", "user2.pdf",
    "pdf1.pdf", "pdf2.pdf", "download1.pdf", "download2.pdf",
    
    # In common directories
    "files/file.pdf", "files/document.pdf", "files/idor.pdf",
    "downloads/file.pdf", "downloads/document.pdf", "downloads/idor.pdf",
    "documents/file.pdf", "documents/document.pdf", "documents/idor.pdf",
    "uploads/file.pdf", "uploads/document.pdf", "uploads/idor.pdf",
    "pdf/file.pdf", "pdf/document.pdf", "pdf/idor.pdf",
    "pdfs/file.pdf", "pdfs/document.pdf", "pdfs/idor.pdf",
    "media/file.pdf", "media/document.pdf", "media/idor.pdf",
    "static/file.pdf", "static/document.pdf", "static/idor.pdf",
    "public/file.pdf", "public/document.pdf", "public/idor.pdf",
    "assets/file.pdf", "assets/document.pdf", "assets/idor.pdf",
    "resources/file.pdf", "resources/document.pdf", "resources/idor.pdf",
    
    # IDOR specific paths
    "idor/file.pdf", "idor/document.pdf", "idor/download.pdf",
    "IDOR/file.pdf", "IDOR/document.pdf", "IDOR/download.pdf",
    "challenge/file.pdf", "challenge/document.pdf", "challenge/idor.pdf",
    "lab/file.pdf", "lab/document.pdf", "lab/idor.pdf",
    "vuln/file.pdf", "vuln/document.pdf", "vuln/idor.pdf",
    
    # With PHP scripts
    "download.php?file=file.pdf", "download.php?file=document.pdf",
    "download.php?file=idor.pdf", "download.php?file=1.pdf",
    "download.php?id=1", "download.php?id=2", "download.php?id=3",
    "file.php?name=file.pdf", "file.php?name=document.pdf",
    "file.php?id=1", "file.php?id=2", "file.php?id=3",
    "get.php?file=file.pdf", "get.php?file=document.pdf",
    "get.php?id=1", "get.php?id=2", "get.php?id=3",
    "view.php?file=file.pdf", "view.php?file=document.pdf",
    "view.php?id=1", "view.php?id=2", "view.php?id=3",
    
    # Parameter variations for IDOR
    "index.php?file=file.pdf", "index.php?document=file.pdf",
    "index.php?pdf=file.pdf", "index.php?download=file.pdf",
    "?file=file.pdf", "?document=file.pdf", "?pdf=file.pdf",
    "?file=1", "?document=1", "?pdf=1", "?id=1",
    
    # Hidden or backup locations
    ".pdf", "..pdf", "backup.pdf", "old.pdf", "new.pdf",
    "temp.pdf", "tmp.pdf", "test.pdf", "hidden.pdf", "secret.pdf",
    ".hidden/file.pdf", ".secret/file.pdf", ".backup/file.pdf",
    "backup/file.pdf", "backups/file.pdf", "bak/file.pdf",
    
    # CTF common patterns
    "flag.pdf", "FLAG.pdf", "ctf.pdf", "CTF.pdf",
    "capture.pdf", "mission.pdf", "task.pdf", "level.pdf",
    "stage.pdf", "challenge1.pdf", "challenge2.pdf",
    
    # VulnMachines specific
    "vnm.pdf", "VNM.pdf", "vulnmachines.pdf", "VulnMachines.pdf",
    "vm.pdf", "VM.pdf", "machine.pdf", "machines.pdf"
]

def check_pdf(path):
    try:
        url = f"{target}/{path}"
        response = requests.get(url, timeout=3, allow_redirects=False)
        
        if response.status_code == 200:
            # Check if it's actually a PDF
            content_type = response.headers.get('Content-Type', '').lower()
            
            if 'pdf' in content_type or response.content[:4] == b'%PDF':
                size = len(response.content)
                return f"[PDF FOUND!] {url} - Size: {size} bytes", url, response.content
            elif 'text/html' not in content_type and len(response.content) > 100:
                # Might be a PDF served with wrong content-type
                if response.content[:4] == b'%PDF':
                    size = len(response.content)
                    return f"[PDF FOUND!] {url} - Size: {size} bytes (wrong content-type)", url, response.content
                    
        elif response.status_code in [301, 302]:
            location = response.headers.get('Location', '')
            if 'pdf' in location.lower():
                return f"[Redirect to PDF] {url} -> {location}", None, None
                
    except Exception:
        pass
    
    return None, None, None

print("[*] Searching for PDF files...")
print(f"[*] Target: {target}")
print(f"[*] Testing {len(pdf_paths)} potential PDF locations")
print("-" * 70)

found_pdfs = []
pdf_data = []

with ThreadPoolExecutor(max_workers=50) as executor:
    futures = {executor.submit(check_pdf, path): path for path in pdf_paths}
    
    for future in as_completed(futures):
        result, url, content = future.result()
        if result:
            print(result)
            found_pdfs.append(result)
            if content:
                pdf_data.append((url, content))

print("\n" + "=" * 70)

if pdf_data:
    print(f"\n[+] Found {len(pdf_data)} PDF file(s)!")
    
    # Download the PDFs
    for i, (url, content) in enumerate(pdf_data, 1):
        filename = f"/workspace/found_pdf_{i}.pdf"
        with open(filename, 'wb') as f:
            f.write(content)
        print(f"[+] Downloaded: {url} -> {filename}")
        print(f"    Size: {len(content)} bytes")
        
        # Check if PDF contains text
        if b'flag' in content.lower() or b'vnm' in content.lower() or b'idor' in content.lower():
            print(f"    [!] This PDF might contain the flag or important information!")
    
    print("\n[*] PDFs downloaded. Analyze them for IDOR vulnerabilities or flags.")
    
elif found_pdfs:
    print("\n[*] Found redirects or references to PDFs:")
    for pdf in found_pdfs:
        print(pdf)
    print("\n[*] Follow the redirects manually to download the PDFs.")
    
else:
    print("\n[-] No PDF files found in common locations")
    print("[*] The PDF might be:")
    print("    - Behind authentication")
    print("    - Using a non-standard name or location")
    print("    - Accessible only through IDOR vulnerability")
    print("    - On a different port or subdomain")