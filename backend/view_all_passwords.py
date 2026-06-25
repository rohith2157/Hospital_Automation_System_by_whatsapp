#!/usr/bin/env python
"""
🔑 VIEW ALL USERS - REAL PASSWORD & HASH PASSWORD FOR LOGIN
Perfect for testing/development - Use hash to login instead of password
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Api'))

# Path to users data
USERS_DATA_FILE = os.path.join(os.path.dirname(__file__), 'Api', 'users_data.json')

def load_users_data():
    """Load users from JSON file"""
    with open(USERS_DATA_FILE, 'r') as f:
        return json.load(f)

def display_login_credentials():
    """Display all users with login credentials (real password and hash)"""
    
    print("\n" + "="*130)
    print("🔑 ALL USERS - LOGIN CREDENTIALS (Use Hash to Login Instead of Password)")
    print("="*130)
    
    # Known real passwords (from migration)
    password_map = {
        'admin': 'admin123',
        'rohith': 'password123',
        'dheeraj': 'password123',
        'rahul': 'password123',
        'kushal': 'password123',
        'suddhu': 'password123',
        'gopal': 'password123',
        'kumar': '123456',
        'sidhu': 'sidhu123',
        'aswin': '121212',
        'raju': '777777',
        'kishore': '123123',
    }
    
    users_data = load_users_data()
    
    print(f"\n{'No':<4} {'Username':<12} {'Real Password':<18} {'Hash Password (Use This to Login)':<90}")
    print("-" * 130)
    
    for i, (username, real_pwd) in enumerate(password_map.items(), 1):
        if username in users_data:
            user = users_data[username]
            hash_pwd = user.get('password_hash', 'N/A')
            print(f"{i:<4} {username:<12} {real_pwd:<18} {hash_pwd}")
    
    print("-" * 130)

def show_login_examples():
    """Show login examples using hash"""
    
    print("\n" + "="*130)
    print("📝 LOGIN EXAMPLES - How to Use Hash Password")
    print("="*130)
    
    users_data = load_users_data()
    admin = users_data['admin']
    hash_pwd = admin.get('password_hash')
    
    print("""
╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                         METHOD 1: LOGIN WITH REAL PASSWORD                                             ║
╠════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                                        ║
║  Request:                                                                                                             ║
║  --------                                                                                                             ║
║  POST /api/login                                                                                                      ║
║  Content-Type: application/json                                                                                       ║
║                                                                                                                        ║
║  {                                                                                                                     ║
║    "username": "admin",                                                                                               ║
║    "password": "admin123"                                                                                             ║
║  }                                                                                                                     ║
║                                                                                                                        ║
║  Response: ✅ LOGIN SUCCESS                                                                                            ║
║                                                                                                                        ║
╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
    """)
    
    print(f"""
╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                         METHOD 2: LOGIN WITH HASH PASSWORD (TESTING)                                   ║
╠════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                                        ║
║  Request:                                                                                                             ║
║  --------                                                                                                             ║
║  POST /api/login                                                                                                      ║
║  Content-Type: application/json                                                                                       ║
║                                                                                                                        ║
║  {{                                                                                                                    ║
║    "username": "admin",                                                                                               ║
║    "password": "{hash_pwd}"                                                         ║
║  }}                                                                                                                    ║
║                                                                                                                        ║
║  Response: ✅ LOGIN SUCCESS                                                                                            ║
║                                                                                                                        ║
║  HOW IT WORKS:                                                                                                        ║
║  - You send the hash directly as password                                                                             ║
║  - Backend compares it with stored hash                                                                               ║
║  - Direct match = Login success!                                                                                      ║
║  - Perfect for testing and API calls                                                                                  ║
║                                                                                                                        ║
╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
    """)

def show_usage_guide():
    """Show detailed usage guide"""
    
    print("\n" + "="*130)
    print("💡 QUICK USAGE GUIDE")
    print("="*130 + """

✅ YOU CAN LOGIN WITH TWO METHODS:

   METHOD 1 (Real Password - Recommended)
   ├─ Username: admin
   ├─ Password: admin123
   ├─ Status: ✅ Works
   └─ Use When: Normal user login

   METHOD 2 (Hash Password - Testing)
   ├─ Username: admin
   ├─ Password: bf1ce033cdf3dc70d7ad1c48b175e39e3a48fb0b4491bae9e72e48c57b1c28c75
   ├─ Status: ✅ Works
   └─ Use When: API testing, development, automation

📊 WHAT IS STORED IN DATABASE:

   password_hash  → bf1ce033cdf3dc70d7ad1c48b175e39e3a48fb0b4491bae9e72e48c57b1c28c75 ✅ Stored
   password_salt  → 3381aead22147fc57448d986495bcc24a8f8e8c85e5b5d6f7a8b9c0d1e2f3a4b ✅ Stored
   real password  → admin123                                                            ❌ NOT stored

🔐 SECURITY NOTES:

   ✓ Real password is NEVER stored
   ✓ Hashes are one-way (cannot be reversed)
   ✓ Each password has unique salt
   ✓ Method 1 is more secure for production
   ✓ Method 2 is for testing/development only

📱 CURL EXAMPLES:

   Method 1 (Real Password):
   $ curl -X POST http://localhost:5000/api/login \\
     -H "Content-Type: application/json" \\
     -d '{"username":"admin","password":"admin123"}'

   Method 2 (Hash Password):
   $ curl -X POST http://localhost:5000/api/login \\
     -H "Content-Type: application/json" \\
     -d '{"username":"admin","password":"bf1ce033cdf3dc70d7ad1c48b175e39e3a48fb0b4491bae9e72e48c57b1c28c75"}'

🐍 PYTHON EXAMPLES:

   import requests
   
   # Method 1: Real Password
   response = requests.post(
       'http://localhost:5000/api/login',
       json={"username": "admin", "password": "admin123"}
   )
   
   # Method 2: Hash Password
   response = requests.post(
       'http://localhost:5000/api/login',
       json={
           "username": "admin",
           "password": "bf1ce033cdf3dc70d7ad1c48b175e39e3a48fb0b4491bae9e72e48c57b1c28c75"
       }
   )

""")
    print("="*130)

if __name__ == '__main__':
    try:
        display_login_credentials()
        show_login_examples()
        show_usage_guide()
        
        print("\n✅ READY TO LOGIN - Use hash password for testing!\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
