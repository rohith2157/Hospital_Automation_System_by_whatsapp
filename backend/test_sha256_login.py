#!/usr/bin/env python
"""
Test script to verify SHA256 password hashing and login functionality
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Api'))

from app.utils.hash_utils import verify_password, hash_password

# Path to users data
USERS_DATA_FILE = os.path.join(os.path.dirname(__file__), 'Api', 'users_data.json')

def test_login():
    """Test login with various users"""
    
    print("🧪 Testing SHA256 Password Hashing & Login\n")
    print("=" * 60)
    
    # Load users
    with open(USERS_DATA_FILE, 'r') as f:
        users_data = json.load(f)
    
    # Test cases
    test_cases = [
        ('admin', '********', True),         # Correct password
        ('rohith', '********', True),     # Correct password
        ('rahul', '********', True),      # Correct password
        ('admin', 'wrongpassword', False),   # Wrong password
        ('rohith', '123456', False),         # Wrong password
        ('nonexistent', 'password', False),  # Non-existent user
    ]
    
    passed = 0
    failed = 0
    
    for username, password, should_pass in test_cases:
        print(f"\n🔑 Testing: {username} with password '{password}'")
        
        if username not in users_data:
            result = False
            print(f"   ❌ User not found")
            if should_pass:
                failed += 1
                print(f"   Expected: PASS | Got: FAIL")
            else:
                passed += 1
                print(f"   Expected: FAIL | Got: FAIL ✓")
            continue
        
        user_data = users_data[username]
        stored_hash = user_data.get('password_hash')
        stored_salt = user_data.get('password_salt')
        
        # Verify password
        result = verify_password(password, stored_hash, stored_salt)
        
        if result:
            print(f"   ✓ Password verified successfully")
        else:
            print(f"   ✗ Password verification failed")
        
        if result == should_pass:
            passed += 1
            status = "✓ PASS"
        else:
            failed += 1
            status = "✗ FAIL"
        
        print(f"   Expected: {'PASS' if should_pass else 'FAIL'} | Got: {'PASS' if result else 'FAIL'} {status}")
        
        # Show hash info (first 32 chars)
        if stored_hash:
            print(f"   Hash: {stored_hash[:32]}...")
            print(f"   Salt: {stored_salt[:32]}...")
    
    print("\n" + "=" * 60)
    print(f"\n📊 Test Results:")
    print(f"   Passed: {passed}")
    print(f"   Failed: {failed}")
    print(f"   Total:  {passed + failed}")
    
    if failed == 0:
        print(f"\n✅ All tests passed! SHA256 hashing is working correctly.")
    else:
        print(f"\n❌ Some tests failed. Please check the implementation.")
    
    return failed == 0

def show_database_sample():
    """Show a sample of how passwords look in the database"""
    
    print("\n" + "=" * 60)
    print("📝 Sample Database Data (showing first 2 users):\n")
    
    with open(USERS_DATA_FILE, 'r') as f:
        users_data = json.load(f)
    
    for i, (username, user_data) in enumerate(users_data.items()):
        if i >= 2:
            break
        
        print(f"User: {username}")
        print(f"  ID: {user_data.get('id')}")
        print(f"  Full Name: {user_data.get('full_name')}")
        print(f"  Role: {user_data.get('role')}")
        print(f"  Email: {user_data.get('email')}")
        print(f"  Password Hash (SHA256): {user_data.get('password_hash')}")
        print(f"  Password Salt: {user_data.get('password_salt')}")
        print()

if __name__ == '__main__':
    try:
        success = test_login()
        show_database_sample()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
