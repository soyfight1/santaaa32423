#!/usr/bin/env python3
import requests

target_ip = "hackme1.vulnmachines.com"
port = 80

# Common subdomains and vhosts for CTF/VulnMachines
vhosts = [
    "idor", "IDOR", "idors",
    "lab", "labs", "challenge", "challenges",
    "ctf", "CTF", "flag", "flags",
    "vnm", "VNM", "vulnmachines", "VulnMachines",
    "vm", "VM", "machine", "machines",
    "web", "webapp", "app", "application",
    "test", "testing", "demo", "dev", "development",
    "stage", "staging", "prod", "production",
    "api", "API", "rest", "graphql",
    "admin", "administrator", "manage", "management",
    "user", "users", "profile", "profiles",
    "login", "auth", "authentication", "signin",
    "portal", "dashboard", "panel", "console",
    "hidden", "secret", "private", "internal",
    "vulnerable", "vuln", "exploit", "hack",
    "insecure", "direct", "object", "reference",
    "www", "mail", "ftp", "ssh", "vpn",
    "hackme1", "hackme2", "hackme"
]

# Also try the original domain with different hosts
full_domains = [
    f"{vhost}.vulnmachines.com" for vhost in vhosts
] + [
    f"{vhost}.hackme1.vulnmachines.com" for vhost in vhosts
]

def check_vhost(vhost, target):
    try:
        headers = {
            'Host': vhost,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        }
        
        response = requests.get(f"http://{target}", headers=headers, timeout=3)
        
        if response.status_code == 200:
            content = response.text.lower()
            content_length = len(response.content)
            
            # Skip default Apache page
            if 'apache2 ubuntu default' in content or content_length == 10918:
                return None
            
            # Check for interesting content
            if any(keyword in content for keyword in ['idor', 'insecure direct object', 'flag', 'vnm', 'challenge']):
                return f"[VHOST FOUND!] {vhost} - Contains IDOR/challenge keywords - Size: {content_length}"
            elif any(keyword in content for keyword in ['login', 'user', 'profile', 'dashboard']):
                return f"[VHOST] {vhost} - User/Auth system - Size: {content_length}"
            elif content_length > 100:
                return f"[VHOST] {vhost} - Different content - Size: {content_length}"
                
        elif response.status_code in [301, 302, 401, 403]:
            return f"[VHOST] {vhost} - Status: {response.status_code}"
            
    except Exception:
        pass
    
    return None

print("[*] Virtual Host Discovery")
print(f"[*] Target: {target_ip}")
print("-" * 60)

# Check vhosts on the IP
print("\n[*] Checking virtual hosts on IP...")
found_vhosts = []

for vhost in vhosts:
    result = check_vhost(vhost, target_ip)
    if result:
        print(result)
        found_vhosts.append(result)

# Check full domains
print("\n[*] Checking full domain variations...")
for domain in full_domains:
    result = check_vhost(domain, target_ip)
    if result:
        print(result)
        found_vhosts.append(result)

# Also try with port 7500 in case it's up but needs special host header
print("\n[*] Trying port 7500 with vhosts...")
for vhost in ["idor", "IDOR", "hackme1", "vulnmachines", "challenge", "lab"]:
    try:
        headers = {'Host': vhost}
        response = requests.get(f"http://{target_ip}:7500", headers=headers, timeout=2)
        if response.status_code == 200:
            print(f"[PORT 7500 ACTIVE!] With Host: {vhost}")
    except:
        pass

if found_vhosts:
    print("\n" + "=" * 60)
    print("[+] Virtual hosts found! Try accessing with custom Host header:")
    print("    curl -H 'Host: <vhost>' http://hackme1.vulnmachines.com/")
else:
    print("\n[-] No virtual hosts discovered with common names")