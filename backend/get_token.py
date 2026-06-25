import requests
import json

# Login to get JWT token
login_url = "http://localhost:5000/api/auth/login"
login_data = {
    "username": "admin",
    "password": "admin123"
}

try:
    response = requests.post(login_url, json=login_data)
    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token')
        print("\n" + "="*60)
        print("✅ JWT TOKEN GENERATED SUCCESSFULLY!")
        print("="*60)
        print("\nCopy this token for n8n:")
        print("-"*60)
        print(token)
        print("-"*60)
        print("\nUse it in n8n like this:")
        print(f"Bearer {token}")
        print("="*60)
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"❌ Error: {e}")
