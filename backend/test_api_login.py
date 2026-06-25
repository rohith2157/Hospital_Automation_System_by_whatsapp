#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test login via API"""
import requests
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Api'))

from app.utils.hash_utils import verify_password

USERS_DATA_FILE = os.path.join(os.path.dirname(__file__), 'Api', 'users_data.json')

# Load users
with open(USERS_DATA_FILE, 'r') as f:
    users = json.load(f)

admin = users['admin']
stored_hash = admin.get('password_hash')

print("\n" + "="*70)
print("LOGIN CREDENTIALS FOR TESTING")
print("="*70)
print(f"\nUsername: admin")
print(f"Password (Method 1 - Real): admin123")
print(f"\nPassword (Method 2 - Hash): {stored_hash}")
print(f"\nHash length: {len(stored_hash)} characters")
print("\n" + "="*70)

# Test API URL
BASE_URL = "http://localhost:5000"
LOGIN_URL = f"{BASE_URL}/api/login"

print("\nTesting API Login...")
print("="*70)

# Test 1: Real password
print("\nTest 1: Login with real password")
try:
    response = requests.post(LOGIN_URL, json={"username": "admin", "password": "admin123"})
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Result: SUCCESS - You can login with real password!")
    else:
        print(f"Result: FAILED - {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Hash password
print("\nTest 2: Login with hash password")
try:
    response = requests.post(LOGIN_URL, json={"username": "admin", "password": stored_hash})
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Result: SUCCESS - You can login with hash password!")
    else:
        print(f"Result: FAILED - {response.json()}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*70 + "\n")
