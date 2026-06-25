import pymysql

# Database connection - direct from your config
db = pymysql.connect(
    host="69.62.82.234",
    user="remote_user",
    password="@Codevocado#remote%1",
    database="wha_chatbot"
)
cursor = db.cursor()

print("Setting up chatbot tables...")

# 1. Chat Context Table
print("\n1. Creating chat_context table...")
cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_context (
    phone VARCHAR(20),
    context_key VARCHAR(50),
    context_value VARCHAR(255),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (phone, context_key)
)
""")
print("✓ chat_context table created")

# 2. OPD Feedback Table
print("\n2. Creating opd_feedback table...")
cursor.execute("""
CREATE TABLE IF NOT EXISTS opd_feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    appointment_id INT,
    doctor_rating INT,
    waiting_time_rating INT,
    overall_rating INT,
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (appointment_id) REFERENCES appointments(id)
)
""")
print("✓ opd_feedback table created")

# 3. IPD Feedback Table (without foreign key for now)
print("\n3. Creating ipd_feedback table...")
cursor.execute("""
CREATE TABLE IF NOT EXISTS ipd_feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    room_cleanliness INT,
    nursing_care INT,
    doctor_visit INT,
    food_quality INT,
    overall_rating INT,
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
print("✓ ipd_feedback table created")

# 4. Doctor Leave Table
print("\n4. Creating doctor_leave table...")
cursor.execute("""
CREATE TABLE IF NOT EXISTS doctor_leave (
    id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_id INT,
    leave_date DATE,
    reason VARCHAR(255),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
)
""")
print("✓ doctor_leave table created")

# 5. Add columns to doctors table
print("\n5. Adding columns to doctors table...")
try:
    cursor.execute("ALTER TABLE doctors ADD COLUMN slot_duration INT DEFAULT 15")
    print("✓ Added slot_duration column")
except:
    print("✓ slot_duration column already exists")

try:
    cursor.execute("ALTER TABLE doctors ADD COLUMN max_patients INT DEFAULT 4")
    print("✓ Added max_patients column")
except:
    print("✓ max_patients column already exists")

db.commit()
db.close()

print("\n✅ All chatbot tables created successfully!")
print("\nNext steps:")
print("1. Run: python Api/setup_chatbot_tables.py")
print("2. Configure Twilio webhook URL")
print("3. Test booking flow via WhatsApp")
