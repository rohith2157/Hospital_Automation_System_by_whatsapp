import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.init import create_app, db, bcrypt

app = create_app()

with app.app_context():
    # Create admin user with bcrypt hash
    password = '********'
    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    
    # Insert directly into MySQL
    import pymysql
    connection = pymysql.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', 'your_password_here'),
        database=os.environ.get('DB_NAME', 'hospital_db')
    )
    
    cursor = connection.cursor()
    
    # Check if admin exists
    cursor.execute("SELECT id FROM users WHERE username = 'admin'")
    existing = cursor.fetchone()
    
    if existing:
        # Update password
        cursor.execute(
            "UPDATE users SET password_hash = %s WHERE username = 'admin'",
            (hashed,)
        )
        print("✅ Updated admin user password")
    else:
        # Get max id and increment
        cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM users")
        next_id = cursor.fetchone()[0]
        
        # Insert new admin user
        cursor.execute(
            """INSERT INTO users (id, username, password_hash, full_name, role, is_active) 
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (next_id, 'admin', hashed, 'Administrator', 'superadmin', 1)
        )
        print("✅ Created admin user")
    
    connection.commit()
    
    # Verify
    cursor.execute("SELECT id, username, full_name, role FROM users WHERE username = 'admin'")
    admin = cursor.fetchone()
    print(f"\n✅ Admin user ready:")
    print(f"   Username: admin")
    print(f"   Password: ********")
    print(f"   Role: {admin[3]}")
    
    cursor.close()
    connection.close()
