import os
import pymysql

# Connect and fix appointments table
try:
    connection = pymysql.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', 'your_password_here'),
        database=os.environ.get('DB_NAME', 'hospital_db')
    )
    
    cursor = connection.cursor()
    
    print("Fixing appointments table id column...")
    cursor.execute("ALTER TABLE appointments MODIFY COLUMN id INT AUTO_INCREMENT PRIMARY KEY")
    connection.commit()
    print("✓ Fixed appointments table")
    
    cursor.close()
    connection.close()
    
    print("\n✅ All done! You can now create appointments.")
    
except Exception as e:
    print(f"Error: {e}")
