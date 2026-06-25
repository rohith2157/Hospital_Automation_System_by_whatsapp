import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.init import create_app, db, bcrypt
from app.models import User

app = create_app()

with app.app_context():
    # Check all users
    users = User.query.all()
    print(f"\n=== Found {len(users)} users in database ===\n")
    
    for user in users:
        print(f"ID: {user.id}")
        print(f"Username: {user.username}")
        print(f"Full Name: {user.full_name}")
        print(f"Role: {user.role}")
        print(f"Email: {user.email}")
        print(f"Active: {user.is_active}")
        print(f"Password Hash: {user.password[:20]}...")
        print("-" * 50)
    
    # Test password verification for rohith
    rohith = User.query.filter_by(username='rohith').first()
    if rohith:
        print("\n=== Testing rohith login ===")
        test_password = '444444'
        is_valid = bcrypt.check_password_hash(rohith.password, test_password)
        print(f"Password '{test_password}' is valid: {is_valid}")
        
        # Try admin too
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print("\n=== Testing admin login ===")
            test_password = 'admin123'
            is_valid = bcrypt.check_password_hash(admin.password, test_password)
            print(f"Password '{test_password}' is valid: {is_valid}")
