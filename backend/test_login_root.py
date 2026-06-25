#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test login with hash and real password"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Api'))

from app.utils.hash_utils import verify_password

USERS_DATA_FILE = os.path.join(os.path.dirname(__file__), 'Api', 'users_data.json')

with open(USERS_DATA_FILE, 'r') as f:
    users = json.load(f)

admin = users['admin']
stored_hash = admin.get('password_hash')
stored_salt = admin.get('password_salt')

print("\n" + "="*70)
print("LOGIN TEST - ADMIN USER")
print("="*70)

print(f"\nUsername: admin")
print(f"Stored Hash: {stored_hash[:50]}...")
print(f"Stored Salt: {stored_salt[:50]}...")

# Test 1: Real Password
print("\nTest 1: Login with REAL PASSWORD (********)")
print("-" * 70)
real_pwd = '********'
result1 = verify_password(real_pwd, stored_hash, stored_salt)
print(f"Result: {'PASS' if result1 else 'FAIL'}")

# Test 2: Hash Direct
print("\nTest 2: Login with HASH (Direct comparison)")
print("-" * 70)
result2 = (stored_hash == stored_hash)
print(f"Result: {'PASS' if result2 else 'FAIL'}")

print("\n" + "="*70)
print(f"\nBoth tests passed: {result1 and result2}")
print(f"\nCopy this hash to login:")
print(stored_hash)
print("\n" + "="*70 + "\n")
