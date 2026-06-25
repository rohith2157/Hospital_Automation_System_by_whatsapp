import os
#!/usr/bin/env python
"""Quick DB Migration - Run in terminal from Api folder"""
import mysql.connector
import json

# Database connection details - update if needed
config = {
    'host': 'localhost',
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': 'hospital_db'
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    
    # Check if column exists first
    cursor.execute("""
        SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME='users' AND COLUMN_NAME='modules'
    """)
    
    if cursor.fetchone():
        print("✅ Column 'modules' already exists!")
    else:
        # Add the column
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN modules JSON DEFAULT '["dashboard"]'
        """)
        conn.commit()
        print("✅ Successfully added 'modules' column to users table!")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure MySQL is running")
    print("2. Check database credentials in this script")
    print("3. Make sure 'hospital_db' database exists")
