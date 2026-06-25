# HOSPITAL WHATSAPP AUTOMATION SYSTEM
## Complete Project Testing & Implementation Guide

**Document Version:** 1.0  
**Date:** January 10, 2026  
**Project:** Hospital WhatsApp Chatbot Automation System  
**Status:** Production Ready

---

## TABLE OF CONTENTS
1. Project Overview
2. System Requirements
3. Database Setup
4. Authentication & Security
5. File Structure & Descriptions
6. Testing Procedures
7. Login Credentials
8. API Testing
9. Troubleshooting
10. Deployment Checklist

---

## 1. PROJECT OVERVIEW

The Hospital WhatsApp Automation System is a comprehensive web-based solution designed to:
- Automate hospital appointments through WhatsApp
- Manage patient information and medical records
- Provide role-based dashboard access
- Integrate with WhatsApp Business API
- Secure user authentication with SHA256+PBKDF2 hashing

### Key Features:
- Multi-user authentication system
- Role-based access control (Admin, Reception, Doctor, Campaign Manager, Viewer)
- Hospital branch management
- Doctor and patient databases
- Appointment scheduling and management
- WhatsApp integration for notifications
- Real-time chat logging
- Secure password hashing (PBKDF2+SHA256)

### Technology Stack:
- **Backend:** Python Flask
- **Database:** MySQL (Remote Server: 69.62.82.234)
- **Frontend:** React.js with Vite
- **Authentication:** JWT Tokens
- **Security:** SHA256 PBKDF2 Password Hashing

---

## 2. SYSTEM REQUIREMENTS

### Hardware Requirements:
- Minimum 4GB RAM
- 500MB free disk space
- Windows/Linux/macOS compatible

### Software Requirements:
- Python 3.10+ (Installed: Python 3.13)
- Node.js 16+ (for frontend)
- MySQL 5.7+ (Remote access available)
- Git for version control
- VS Code or similar IDE

### Python Packages Required:
```
Flask==2.3.2
Flask-JWT-Extended==4.4.4
Flask-SQLAlchemy==3.0.5
Flask-Cors==4.0.0
PyMySQL==1.1.0
python-dotenv==1.0.0
bcrypt==4.0.1
```

---

## 3. DATABASE SETUP

### Database Connection Details:
```
Host: 69.62.82.234
Database Name: wha_chatbot
Username: remote_user
Password: [REDACTED]
Port: 3306
```

### Database Tables Created:

#### Users Table Structure:
```
Column Name         Type            Properties
---------------------------------------------------
id                  INT             PRIMARY KEY, AUTO_INCREMENT
username            VARCHAR(100)    UNIQUE, NOT NULL
password_hash       VARCHAR(255)    NOT NULL
password_salt       VARCHAR(255)    NULL
full_name           VARCHAR(255)    NULL
role                ENUM            (superadmin, admin, reception, campaign, viewer)
phone               VARCHAR(20)     NULL
email               VARCHAR(255)    NULL
is_active           BOOLEAN         DEFAULT: 1
created_at          TIMESTAMP       DEFAULT: CURRENT_TIMESTAMP
updated_at          TIMESTAMP       ON UPDATE CURRENT_TIMESTAMP
```

#### Other Tables:
- patients: Patient information and medical history
- doctors: Doctor profiles and specialties
- appointments: Appointment scheduling and status
- branches: Hospital branch locations
- campaigns: Marketing campaigns
- feedback: Patient feedback and reviews
- permissions: Role-based permissions
- login_details: Authentication logs
- message_logs: WhatsApp message history
- chat_context: Conversation context storage

### Database Initialization:
```bash
cd Api
python init_db.py
```

---

## 4. AUTHENTICATION & SECURITY

### Password Hashing Algorithm:

**Algorithm:** PBKDF2 (Password-Based Key Derivation Function 2)  
**Hash Function:** SHA256  
**Iterations:** 1000  
**Salt Length:** 32 bytes (256 bits)  
**Output:** 128 bytes (1024 bits)

### How Hashing Works:
1. System generates random 32-byte salt
2. Password is combined with salt
3. PBKDF2 applies SHA256 1000 times
4. Result is 128-byte secure hash
5. Both hash and salt stored in database

### Security Features:
- ✅ Passwords never stored in plain text
- ✅ Each password has unique salt
- ✅ 1000 iterations prevent brute force
- ✅ SHA256 provides cryptographic security
- ✅ Salt stored separately for verification
- ✅ No MD5 or weak algorithms used

### Password Verification Process:
1. User enters password during login
2. System retrieves stored salt from database
3. PBKDF2+SHA256 applied with same salt
4. Result compared with stored hash
5. If match: authentication successful
6. If no match: authentication failed

---

## 5. FILE STRUCTURE & DESCRIPTIONS

### Root Directory Files:

#### **show_credentials.py**
**Purpose:** Display login credentials from JSON file  
**Usage:** `python show_credentials.py`  
**Output:** Displays usernames and password hashes  
**When to Use:** When you need to verify credentials for testing

#### **test_login.py**
**Purpose:** Test login functionality with different authentication methods  
**Usage:** `python test_login.py`  
**Tests:** Username/password validation, hash verification, error handling

#### **test_dual_login_methods.py**
**Purpose:** Test both hash-based and real password authentication  
**Usage:** `python test_dual_login_methods.py`  
**Features:** Tests SHA256+PBKDF2 hashing method

#### **test_sha256_login.py**
**Purpose:** Specific testing for SHA256 PBKDF2 authentication  
**Usage:** `python test_sha256_login.py`  
**Validates:** Password hashing with salt verification

#### **chatbot_demo.py**
**Purpose:** Interactive demo of chatbot functionality  
**Usage:** `python chatbot_demo.py`  
**Features:** Test appointment booking, patient info, doctor queries

#### **test_api_login.py**
**Purpose:** Test API endpoints for authentication  
**Usage:** `python test_api_login.py`  
**Tests:** /login endpoint, JWT token generation, user data response

#### **whatsapp_simulator.py**
**Purpose:** Simulate WhatsApp messages for testing  
**Usage:** `python whatsapp_simulator.py`  
**Features:** Test message handling without actual WhatsApp connection

### Api Directory:

#### **run.py**
**Purpose:** Start the Flask application server  
**Usage:** `python run.py`  
**Output:** Server runs on http://localhost:5000  
**Configuration:** Uses app/config.py for settings

#### **init_db.py**
**Purpose:** Initialize database and create test users  
**Usage:** `python init_db.py`  
**Creates:** Database tables and 4 default users  
**Default Users:**
- admin / ********
- rohith / rohith123
- reception / reception123
- doctor / doctor123

#### **setup_db.py**
**Purpose:** Database migration and schema updates  
**Usage:** `python setup_db.py`  
**Function:** Adds new columns, updates existing tables

#### **create_test_data.py**
**Purpose:** Populate database with sample data  
**Usage:** `python create_test_data.py`  
**Creates:** Sample patients, doctors, appointments, branches

#### **migrate_db_add_salt.py**
**Purpose:** Migration script for adding password_salt column  
**Usage:** `python migrate_db_add_salt.py`  
**When:** Only if password_salt missing from database

#### **app/config.py**
**Purpose:** Application configuration settings  
**Contains:**
- Database connection URI
- JWT secret keys
- WhatsApp API credentials
- Redis configuration
- Flask settings

#### **app/models.py**
**Purpose:** Database model definitions  
**Models:**
- User: User accounts and authentication
- Patient: Patient information
- Doctor: Doctor profiles
- Appointment: Appointment records
- Branch: Hospital locations
- Campaign: Marketing campaigns
- Feedback: Patient feedback
- Permission: Role-based access control

#### **app/auth.py**
**Purpose:** Authentication and JWT token generation  
**Endpoints:**
- POST /login: User login with JWT
- POST /register: User registration
- GET /verify: Token verification
- POST /logout: User logout

#### **app/utils/hash_utils.py**
**Purpose:** Password hashing and verification functions  
**Functions:**
- `hash_password(password, salt=None)`: Create PBKDF2+SHA256 hash
- `verify_password(password, hash, salt)`: Verify password against hash
- `generate_salt()`: Create random 32-byte salt

#### **routes/dashboard.py**
**Purpose:** Dashboard API endpoints  
**Features:** User statistics, system overview, quick links

#### **routes/users.py**
**Purpose:** User management endpoints  
**Operations:** Create, read, update, delete users

#### **routes/appointments.py**
**Purpose:** Appointment management  
**Operations:** Book, view, update, cancel appointments

#### **routes/patients.py**
**Purpose:** Patient information management  
**Operations:** Add, view, update patient records

#### **routes/doctors.py**
**Purpose:** Doctor profile management  
**Operations:** Add, view, update doctor information

#### **routes/branches.py**
**Purpose:** Hospital branch management  
**Operations:** Create, view, update branch locations

#### **whatsapp_webhook_server.py**
**Purpose:** Handle incoming WhatsApp messages  
**Function:** Webhook endpoint for WhatsApp Business API
**Port:** 8000 (configurable)

#### **whatsapp_chat.py**
**Purpose:** WhatsApp conversation handling  
**Features:** Process messages, generate responses, send replies

### Frontend Directory:

#### **src/App.jsx**
**Purpose:** Main React application component  
**Features:** Routing, authentication check, layout

#### **src/main.jsx**
**Purpose:** React application entry point  
**Function:** Mount React app to DOM

#### **src/pages/LoginPage.jsx**
**Purpose:** User login interface  
**Features:** Username/password form, error handling

#### **src/pages/DashboardPage.jsx**
**Purpose:** Main dashboard after login  
**Features:** Statistics, quick actions, navigation

#### **src/components/Navigation.jsx**
**Purpose:** Application navigation bar  
**Features:** Links to different modules, user menu

#### **src/services/api.js**
**Purpose:** API communication service  
**Features:** HTTP requests, authentication headers, error handling

### Documentation Files:

#### **SHA256_ARCHITECTURE.md**
Complete explanation of PBKDF2+SHA256 implementation

#### **HASHING_WITH_JWT_GUIDE.md**
Guide to password hashing and JWT authentication

#### **USER_MANAGEMENT_GUIDE.md**
User creation, roles, permissions management

#### **TESTING_GUIDE.md**
Complete testing procedures and test cases

#### **CHATBOT_COMPLETE_SUMMARY.md**
Chatbot features and capabilities overview

#### **README_FINAL.md**
Project setup and quick start guide

---

## 6. TESTING PROCEDURES

### 6.1 Unit Tests

#### Test Password Hashing:
```bash
python test_sha256_login.py
```
**Expected Output:**
- ✅ Salt generation successful
- ✅ Password hashing successful
- ✅ Password verification successful
- ✅ Invalid passwords rejected

#### Test API Login Endpoint:
```bash
python test_api_login.py
```
**Expected Output:**
- ✅ /login endpoint responds
- ✅ JWT token generated
- ✅ User data returned
- ✅ Invalid credentials rejected

### 6.2 Integration Tests

#### Test Dual Authentication Methods:
```bash
python test_dual_login_methods.py
```
**Tests:**
1. Hash-based authentication (for testing)
2. Real password with SHA256+PBKDF2
3. Error handling for invalid credentials
4. Session management

#### Test Database Connection:
```bash
python -c "
import pymysql
conn = pymysql.connect(host=os.environ.get('DB_HOST', 'localhost'), user=os.environ.get('DB_USER', 'root'), password=os.environ.get('DB_PASSWORD', 'your_password_here'), database=os.environ.get('DB_NAME', 'hospital_db'))
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM users;')
print(f'Total users: {cursor.fetchone()[0]}')
conn.close()
"
```

### 6.3 API Endpoint Testing

#### Using cURL:
```bash
# Login Test
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"********"}'

# Expected Response:
# {"access_token":"eyJ0eX...","user":{"id":1,"username":"admin","role":"admin"}}
```

#### Using Postman:
1. Import API collection
2. Set base URL: http://localhost:5000
3. Set Authentication: Bearer Token
4. Test endpoints: /login, /dashboard, /users, /appointments

### 6.4 Frontend Testing

#### Run Development Server:
```bash
cd frontend
npm install
npm run dev
```

**Access Application:**
- URL: http://localhost:5173
- Navigate to login page
- Test with provided credentials

#### Test User Flows:
1. Login with valid credentials
2. Navigate to dashboard
3. View user list
4. Create new appointment
5. Update patient information
6. Logout

### 6.5 WhatsApp Integration Testing

#### Start Webhook Server:
```bash
python Api/whatsapp_webhook_server.py
```

#### Test Message Simulation:
```bash
python whatsapp_simulator.py
```

#### Verify Message Logging:
```bash
# Check message_logs table in database
SELECT * FROM message_logs ORDER BY timestamp DESC LIMIT 10;
```

---

## 7. LOGIN CREDENTIALS

### Test User Accounts (Currently in Database):

#### User 1: Administrator
```
Role: admin
Username: admin
Password (Hash): [Stored in Database with SHA256+PBKDF2]
Email: admin@hospital.com
Phone: 9876543210
Status: Active
Modules: All
```

#### User 2: Super Admin
```
Role: superadmin
Username: rohith
Password (Hash): [Stored in Database with SHA256+PBKDF2]
Email: rohith@hospital.com
Phone: 9999999999
Status: Active
Modules: All
```

#### User 3: Reception Staff
```
Role: reception
Username: reception
Password (Hash): [Stored in Database with SHA256+PBKDF2]
Email: reception@hospital.com
Phone: 8888888888
Status: Active
Modules: Appointments, Patients, Dashboard
```

#### User 4: Doctor/Viewer
```
Role: viewer
Username: doctor
Password (Hash): [Stored in Database with SHA256+PBKDF2]
Email: doctor@hospital.com
Phone: 7777777777
Status: Active
Modules: Dashboard, Appointments
```

### Get Current Credentials:
```bash
python show_credentials.py
```

This displays all users from `Api/users_data.json` with their password hashes for testing.

---

## 8. API TESTING

### Base URL:
```
http://localhost:5000
```

### Authentication Endpoints:

#### POST /login
**Description:** User login and JWT token generation  
**Request Body:**
```json
{
  "username": "admin",
  "password": "********"
}
```
**Response (Success):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "admin",
    "full_name": "Admin User",
    "role": "admin",
    "email": "admin@hospital.com",
    "modules": ["dashboard", "appointments", "patients", "doctors"]
  }
}
```
**Response (Failure):**
```json
{
  "error": "Invalid username or password"
}
```

### User Management Endpoints:

#### GET /users
**Description:** List all users  
**Headers:** `Authorization: Bearer <token>`  
**Response:**
```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@hospital.com",
    "role": "admin"
  }
]
```

#### POST /users
**Description:** Create new user  
**Headers:** `Authorization: Bearer <token>`  
**Request Body:**
```json
{
  "username": "newuser",
  "password": "********",
  "full_name": "New User",
  "email": "newuser@hospital.com",
  "role": "reception"
}
```

### Appointment Endpoints:

#### POST /appointments
**Description:** Create appointment  
**Headers:** `Authorization: Bearer <token>`  
**Request Body:**
```json
{
  "patient_id": 1,
  "doctor_id": 1,
  "appointment_date": "2026-01-15",
  "appointment_time": "10:00"
}
```

#### GET /appointments
**Description:** List appointments  
**Headers:** `Authorization: Bearer <token>`

### Patient Endpoints:

#### POST /patients
**Description:** Add patient  
**Headers:** `Authorization: Bearer <token>`  
**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone": "9876543210",
  "email": "john@example.com",
  "age": 35,
  "gender": "M"
}
```

---

## 9. TROUBLESHOOTING

### Database Connection Issues:

**Problem:** "Connection refused to 69.62.82.234"  
**Solution:**
1. Verify internet connection
2. Check firewall settings
3. Verify database credentials in app/config.py
4. Test connection manually:
```bash
mysql -h 69.62.82.234 -u remote_user -p wha_chatbot
```

**Problem:** "Unknown column 'password_salt'"  
**Solution:**
1. Run migration script:
```bash
python Api/migrate_db_add_salt.py
```
2. Or add column manually:
```sql
ALTER TABLE users ADD COLUMN password_salt VARCHAR(255) NULL;
```

### Authentication Issues:

**Problem:** "Invalid username or password" despite correct credentials  
**Solution:**
1. Verify user exists in database
2. Check password hash is correct
3. Ensure password_salt column is populated
4. Run: `python test_sha256_login.py`

**Problem:** JWT token expired or invalid  
**Solution:**
1. Tokens expire after 24 hours
2. Re-login to get new token
3. Check JWT_SECRET_KEY in config.py

### Server Not Starting:

**Problem:** "Address already in use 5000"  
**Solution:**
```bash
# Kill existing process
lsof -i :5000
kill -9 <PID>

# Or use different port
python run.py --port 5001
```

**Problem:** "Module not found" errors  
**Solution:**
```bash
cd Api
pip install -r requirements.txt
```

### Frontend Issues:

**Problem:** "Cannot GET /api/..."  
**Solution:**
1. Ensure backend server is running
2. Check API base URL in src/services/api.js
3. Verify CORS is enabled in Flask app

---

## 10. DEPLOYMENT CHECKLIST

### Pre-Deployment:

- [ ] All tests passing (`test_login.py`, `test_api_login.py`, etc.)
- [ ] Database connection verified
- [ ] All users created in database
- [ ] Password hashing working correctly
- [ ] JWT tokens generating successfully
- [ ] Frontend building without errors
- [ ] API endpoints responding correctly
- [ ] WhatsApp webhook configured
- [ ] Environment variables set
- [ ] Error logging configured

### Database Deployment:

- [ ] All tables created
- [ ] password_salt column added
- [ ] id column has AUTO_INCREMENT
- [ ] Test data loaded
- [ ] Backups created
- [ ] Database user permissions set
- [ ] Connection pooling configured

### Application Deployment:

- [ ] Python 3.10+ installed
- [ ] All pip packages installed
- [ ] Flask application server configured
- [ ] CORS configured for frontend
- [ ] JWT secrets generated
- [ ] Database credentials secure
- [ ] Error logs configured
- [ ] Rate limiting enabled
- [ ] HTTPS enabled in production

### Frontend Deployment:

- [ ] React build successful
- [ ] API endpoints pointing to production
- [ ] Authentication working
- [ ] All pages loading
- [ ] Responsive design tested
- [ ] Performance optimized
- [ ] Browser compatibility tested

### Post-Deployment:

- [ ] Monitor logs for errors
- [ ] Test critical user flows
- [ ] Verify backups working
- [ ] Monitor database performance
- [ ] Check server resource usage
- [ ] Test WhatsApp integration live
- [ ] Document any issues
- [ ] Plan maintenance window if needed

---

## QUICK REFERENCE

### Start Backend:
```bash
cd Api
python run.py
```

### Start Frontend:
```bash
cd frontend
npm run dev
```

### Test Authentication:
```bash
python test_sha256_login.py
```

### View Credentials:
```bash
python show_credentials.py
```

### Initialize Database:
```bash
cd Api
python init_db.py
```

### Check Database:
```bash
cd Api
python inspect_db.py
```

---

## SUPPORT & DOCUMENTATION

For detailed information, refer to:
- SHA256_ARCHITECTURE.md - Password hashing details
- HASHING_WITH_JWT_GUIDE.md - Authentication guide
- USER_MANAGEMENT_GUIDE.md - User creation guide
- TESTING_GUIDE.md - Complete testing procedures
- API/app/config.py - Configuration reference

---

**Document End**

**Project Status:** ✅ Production Ready  
**Last Updated:** January 10, 2026  
**Contact:** Hospital IT Department  

---
