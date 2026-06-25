import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.init import create_app, db, bcrypt
from app.models import User
from app.utils.hash_utils import hash_password

app = create_app()

with app.app_context():
    # Check if user exists
    existing_user = User.query.filter_by(username='rohith').first()
    
    password = '444444'
    password_hash, password_salt = hash_password(password)
    
    if existing_user:
        # Update existing user with SHA256 hashing
        existing_user.password_hash = password_hash
        db.session.commit()
        print("✓ Updated user 'rohith' with new password (SHA256 hashed)")
    else:
        # Create new user with SHA256 hashing
        new_user = User(
            username='rohith',
            email='rohith@hospital.com',
            password_hash=password_hash,
            role='admin',
            full_name='Rohith'
        )
        db.session.add(new_user)
        db.session.commit()
        print("✓ Created new user 'rohith' with SHA256 hashing")
    
    print("\nLogin credentials:")
    print("  Username: rohith")
    print("  Password: 444444")
    print(f"\n📝 Database stored:")
    print(f"   Password Hash (SHA256): {password_hash[:32]}...")

