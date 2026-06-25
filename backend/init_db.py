import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.init import create_app, db, bcrypt
from app.models import User, Patient, Doctor, Branch, Appointment, Feedback, Campaign

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    
    # Check if admin already exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin = User(
            username='admin',
            email='admin@hospital.com',
            password=hashed_password,
            role='admin',
            full_name='System Administrator'
        )
        db.session.add(admin)
        db.session.commit()
        print("✓ Database initialized successfully!")
        print("✓ Admin user created: username='admin', password='admin123'")
    else:
        print("✓ Database already initialized")
