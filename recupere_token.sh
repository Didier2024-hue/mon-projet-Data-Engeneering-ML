TOKEN=$(curl -s http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}' \
  | jq -r '.access_token')

echo "$TOKEN" 
