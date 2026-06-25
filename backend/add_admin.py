#!/usr/bin/env python
"""Add admin user using direct SQL"""
import sys
import os
from urllib.parse import unquote
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.init import create_app, db, bcrypt
from app.models import User
from app.utils.hash_utils import hash_password
import time

print("Connecting to database...")
app = create_app()

try:
    with app.app_context():
        print("Connected! Checking for admin user...")
        
        # Try to query users with timeout
        try:
            admin = User.query.filter_by(username='admin').first()
            
            if admin:
                print("✅ Admin user already exists!")
                print(f"   Username: {admin.username}")
                print(f"   Role: {admin.role}")
                print(f"   Email: {admin.email}")
            else:
                print("Creating admin user with SHA256 hashing...")
                password = '********'
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
                print("✅ Admin user created!")
                print(f"   Username: admin")
                print(f"   Password: ********")
                print(f"   Role: superadmin")
                
        except Exception as e:
            print(f"⚠️  Error checking user: {e}")
            print("Trying to create admin anyway...")
            
            try:
                hashed = bcrypt.generate_password_hash('********').decode('utf-8')
                admin = User(
                    username='admin',
                    password_hash=hashed,
                    full_name='System Administrator',
                    role='superadmin',
                    email='admin@hospital.com',
                    phone='9999999999',
                    is_active=True
                )
                db.session.add(admin)
                db.session.commit()
                print("✅ Admin user created!")
            except Exception as e2:
                print(f"❌ Failed to create admin: {e2}")

except KeyboardInterrupt:
    print("\n⚠️  Cancelled by user")
except Exception as e:
    print(f"❌ Error: {e}")
