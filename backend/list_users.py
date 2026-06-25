import pymysql

try:
    connection = pymysql.connect(
        host='69.62.82.234',
        user='remote_user',
        password='@Codevocado#remote%1',
        database='wha_chatbot'
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
