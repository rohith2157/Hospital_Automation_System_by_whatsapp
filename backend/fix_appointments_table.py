import pymysql

# Connect and fix appointments table
try:
    connection = pymysql.connect(
        host='69.62.82.234',
        user='remote_user',
        password='@Codevocado#remote%1',
        database='wha_chatbot'
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
