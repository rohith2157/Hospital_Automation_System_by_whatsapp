#!/usr/bin/env python
"""Create admin user in database"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.init import create_app, db, bcrypt
from app.models import User
from app.utils.hash_utils import hash_password

app = create_app()
with app.app_context():
    # Check if admin already exists
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        print("✅ Admin user already exists!")
    else:
        # Create admin user with SHA256 hashing
        password = 'admin123'
        password_hash, password_salt = hash_password(password)
        
        admin = User(
            username='admin',
            password_hash=password_hash,
            full_name='System Administrator',
            role='superadmin',
            email='admin@hospital.com',
            phone='9999999999',
            is_active=True
        )
        
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created successfully with SHA256 hashing!")
        print(f"   Username: admin")
        print(f"   Password: admin123")
        print(f"   Role: superadmin")
        print(f"   Email: admin@hospital.com")
        print(f"\n📝 Database stored:")
        print(f"   Password Hash (SHA256): {password_hash[:32]}...")
        print(f"   Password Salt: {password_salt[:32]}...")

