#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Display exact credentials for login"""
import json
import os

USERS_DATA_FILE = os.path.join(os.path.dirname(__file__), 'Api', 'users_data.json')

with open(USERS_DATA_FILE, 'r') as f:
    users = json.load(f)

print("\n" + "="*100)
print("COPY EXACT LOGIN CREDENTIALS FROM HERE")
print("="*100)

# Show ALL users from JSON file dynamically
for i, (username, user) in enumerate(users.items(), 1):
        user_dict = user if isinstance(user, dict) else {}
        hash_pwd = user_dict.get('password_hash', 'N/A')
        
        print(f"\n{i}. {username.upper()}")
        print("-" * 100)
        print(f"   Method 1 - Real Password:")
        print(f"   Username: {username}")
        print(f"   Password: (Auto-hashed - check database)")
        print()
        print(f"   Method 2 - Hash Password (Copy entire hash below):")
        print(f"   Username: {username}")
        print(f"   Password: {hash_pwd}")
        print()

print("="*100)
print("\nNOTE: When using hash password, make sure to copy the ENTIRE hash!")
print("The hash is 128 characters long (64 bytes).")
print("Do not miss any characters at the end!")
print("="*100 + "\n")
