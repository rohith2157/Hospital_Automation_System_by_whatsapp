#!/usr/bin/env python
"""Check if admin user exists and their password hash"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.init import create_app, db, bcrypt
from app.models import User

app = create_app()
with app.app_context():
    # Check if admin user exists
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        print(f"✅ Admin user found!")
        print(f"   Username: {admin.username}")
        print(f"   Full Name: {admin.full_name}")
        print(f"   Role: {admin.role}")
        print(f"   Active: {admin.is_active}")
        print(f"   Password Hash: {admin.password_hash[:50]}...")
        
        # Test password
        test_password = "admin123"
        if bcrypt.check_password_hash(admin.password_hash, test_password):
            print(f"\n✅ Password 'admin123' is CORRECT!")
        else:
            print(f"\n❌ Password 'admin123' is WRONG!")
            print(f"   The password might be different. Try: 'password123' or 'admin'")
    else:
        print("❌ No admin user found in database!")
        print("\nAll users in database:")
        all_users = User.query.all()
        for user in all_users:
            print(f"  - {user.username} (role: {user.role}, active: {user.is_active})")
