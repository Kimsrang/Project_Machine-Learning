
import requests

# Your credentials (from your RTE developer portal)
CLIENT_ID = "4ddabe8a-645e-4306-9054-c5651b2f2aed"
CLIENT_SECRET = "bda97d6e-62b0-486a-a44b-fca1437b28f1"

# Token endpoint (RTE official)
TOKEN_URL = "https://digital.iservices.rte-france.com/token/oauth/"

print("🔐 Requesting a new RTE access token...")

# Make request for token
response = requests.post(
    TOKEN_URL,
    auth=(CLIENT_ID, CLIENT_SECRET),
    data={"grant_type": "client_credentials"}
)

if response.status_code == 200:
    data = response.json()
    
    print("✅ Token successfully obtained!\n")
    print(data)
else:
    print(f"❌ Error {response.status_code}")
    print(response.text)
