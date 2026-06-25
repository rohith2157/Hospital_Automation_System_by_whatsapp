#!/usr/bin/env python
"""
Migration script to hash all existing plain-text passwords in users_data.json
This converts password fields to password_hash and password_salt fields using SHA256
"""
import json
import os
import sys
import hashlib
import binascii

# Add Api directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Api'))

# Import hash utility
from app.utils.hash_utils import hash_password

# Path to users data file
USERS_DATA_FILE = os.path.join(os.path.dirname(__file__), 'Api', 'users_data.json')

def migrate_passwords():
    """Migrate all plain-text passwords to SHA256 hashes"""
    
    print("🔐 Starting password migration to SHA256 hashing...\n")
    
    if not os.path.exists(USERS_DATA_FILE):
        print(f"❌ File not found: {USERS_DATA_FILE}")
        return False
    
    # Load current users data
    with open(USERS_DATA_FILE, 'r') as f:
        users_data = json.load(f)
    
    migrated_count = 0
    already_hashed = 0
    
    # Process each user
    for username, user_data in users_data.items():
        # Check if already has hashed password
        if 'password_hash' in user_data and 'password_salt' in user_data:
            already_hashed += 1
            print(f"✓ {username}: Already hashed")
            continue
        
        # Check if plain-text password exists
        if 'password' in user_data:
            plain_password = user_data['password']
            
            # Hash the password
            password_hash, password_salt = hash_password(plain_password)
            
            # Update user data
            user_data['password_hash'] = password_hash
            user_data['password_salt'] = password_salt
            
            # Remove plain-text password
            del user_data['password']
            
            migrated_count += 1
            print(f"✓ {username}: Migrated (password: {plain_password})")
            print(f"  Hash: {password_hash[:32]}...")
            print(f"  Salt: {password_salt[:32]}...\n")
    
    # Save updated users data
    with open(USERS_DATA_FILE, 'w') as f:
        json.dump(users_data, f, indent=2)
    
    print("\n✅ Migration complete!")
    print(f"   Migrated: {migrated_count} users")
    print(f"   Already hashed: {already_hashed} users")
    print(f"   Total: {len(users_data)} users")
    print(f"\n📝 Updated file: {USERS_DATA_FILE}")
    print("\n🔒 All passwords are now SHA256 hashed with salt!")
    
    return True

if __name__ == '__main__':
    try:
        success = migrate_passwords()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
