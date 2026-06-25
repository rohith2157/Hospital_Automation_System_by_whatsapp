import os
import pymysql

# Connect to MySQL
connection = pymysql.connect(
    host=os.environ.get('DB_HOST', 'localhost'),
    user=os.environ.get('DB_USER', 'root'),
    password=os.environ.get('DB_PASSWORD', 'your_password_here'),
    database=os.environ.get('DB_NAME', 'hospital_db')
)

try:
    with connection.cursor() as cursor:
        # Insert doctors
        doctors = [
            ("John", "Smith", "Cardiology", 1),
            ("Sarah", "Johnson", "Pediatrics", 1),
            ("Michael", "Brown", "Orthopedics", 1),
        ]
        
        sql = "INSERT INTO doctors (first_name, last_name, specialization, branch_id) VALUES (%s, %s, %s, %s)"
        cursor.executemany(sql, doctors)
        connection.commit()
        
        print(f"✅ Added {cursor.rowcount} doctors!")
        
        # Verify
        cursor.execute("SELECT * FROM doctors")
        results = cursor.fetchall()
        for row in results:
            print(f"   - Dr. {row[1]} {row[2]} ({row[3]})")
            
finally:
    connection.close()
