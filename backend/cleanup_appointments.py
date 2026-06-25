import os
import pymysql
from datetime import datetime

# Database connection
connection = pymysql.connect(
    host=os.environ.get('DB_HOST', 'localhost'),
    user=os.environ.get('DB_USER', 'root'),
    password=os.environ.get('DB_PASSWORD', 'your_password_here'),
    database=os.environ.get('DB_NAME', 'hospital_db'),
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with connection.cursor() as cursor:
        # Delete appointments with phone 8333035210 and 9876543210 (your test numbers)
        sql = "DELETE FROM appointments WHERE patient_phone IN ('8333035340', '9876543210')"
        cursor.execute(sql)
        connection.commit()
        print(f"Deleted {cursor.rowcount} test appointments")
        
        # Show remaining appointments
        cursor.execute("SELECT id, patient_name, patient_phone, scheduled_at FROM appointments WHERE DATE(scheduled_at) = '2025-11-21'")
        remaining = cursor.fetchall()
        print("\nRemaining appointments for today:")
        for apt in remaining:
            print(f"ID {apt['id']}: {apt['patient_name']} - {apt['patient_phone']} at {apt['scheduled_at']}")
            
finally:
    connection.close()
