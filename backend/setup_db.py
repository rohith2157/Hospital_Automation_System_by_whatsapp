import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

print("Starting database initialization...")

try:
    from app.init import create_app, db, bcrypt
    print("✓ Imports successful")
    
    from app.models import User
    print("✓ Models imported")
    
    app = create_app()
    print("✓ App created")
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Tables created")
        
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            hashed_password = bcrypt.generate_password_hash('********').decode('utf-8')
            admin = User(
                username='admin',
                email='admin@hospital.com',
                password=hashed_password,
                role='admin',
                full_name='System Administrator'
            )
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created!")
            print("  Username: admin")
            print("  Password: ********")
        else:
            print("✓ Admin user already exists")
        
        print("\n=== Database initialized successfully! ===")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
