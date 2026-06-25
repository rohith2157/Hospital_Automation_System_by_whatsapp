import os
import pymysql

# Connect directly to MySQL to inspect table structure
try:
    connection = pymysql.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', 'your_password_here'),
        database=os.environ.get('DB_NAME', 'hospital_db')
    )
    
    cursor = connection.cursor()
    
    # Show doctors table structure
    cursor.execute("DESCRIBE doctors")
    columns = cursor.fetchall()
    
    print("\n=== DOCTORS TABLE STRUCTURE ===\n")
    for col in columns:
        print(f"Column: {col[0]}, Type: {col[1]}, Null: {col[2]}, Key: {col[3]}, Default: {col[4]}, Extra: {col[5]}")
    
    # Show current doctors data
    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()
    
    print("\n=== CURRENT DOCTORS DATA ===\n")
    if doctors:
        for doctor in doctors:
            print(doctor)
    else:
        print("No doctors found")
    
    # Fix the id column to be auto_increment
    print("\n=== FIXING DOCTORS TABLE ===\n")
    try:
        cursor.execute("ALTER TABLE doctors MODIFY COLUMN id INT AUTO_INCREMENT PRIMARY KEY")
        connection.commit()
        print("✓ Fixed id column to auto_increment")
    except Exception as alter_error:
        print(f"Note: {alter_error}")
    
    # Insert test doctors based on actual table structure
    print("\n=== INSERTING TEST DOCTORS ===\n")
    
    # Prepare test data - match columns: branch_id, first_name, last_name, specialties, consultation_fee, is_active
    test_doctors = [
        (1, "John", "Smith", "Cardiology", 500.00, 1),
        (1, "Sarah", "Johnson", "Pediatrics", 450.00, 1),
        (1, "Michael", "Brown", "Orthopedics", 600.00, 1),
    ]
    
    # Insert query without id column
    insert_query = "INSERT INTO doctors (branch_id, first_name, last_name, specialties, consultation_fee, is_active) VALUES (%s, %s, %s, %s, %s, %s)"
    print(f"Insert query: {insert_query}")
    
    # Try to insert each doctor
    for doctor_data in test_doctors:
        try:
            cursor.execute(insert_query, doctor_data)
            connection.commit()
            print(f"✓ Inserted doctor: Dr. {doctor_data[1]} {doctor_data[2]} - {doctor_data[3]}")
        except Exception as insert_error:
            print(f"✗ Failed to insert Dr. {doctor_data[1]} {doctor_data[2]}: {insert_error}")
    
    # Show updated doctors data
    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()
    
    print("\n=== UPDATED DOCTORS DATA ===\n")
    for doctor in doctors:
        print(doctor)
    
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f"Error: {e}")
