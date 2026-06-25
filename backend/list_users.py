import os
import pymysql

try:
    connection = pymysql.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', 'your_password_here'),
        database=os.environ.get('DB_NAME', 'hospital_db')
    )
    
    cursor = connection.cursor()
    cursor.execute("SELECT id, username, full_name, role, is_active FROM users")
    users = cursor.fetchall()
    
    print("\n=== ALL USERS IN DATABASE ===\n")
    if not users:
        print("No users found in database!")
    else:
        for user in users:
            print(f"ID: {user[0]}, Username: {user[1]}, Name: {user[2]}, Role: {user[3]}, Active: {user[4]}")
    
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f"Error: {e}")
