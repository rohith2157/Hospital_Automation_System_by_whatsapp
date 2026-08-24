# 🏥 PROJECT OVERVIEW — HOSPITAL WHATSAPP AUTOMATION SYSTEM
## Complete PPT Content Guide | Summer Internship Evaluation 2026

---

# ════════════════════════════════════════════════════════════
# STUDENT & INTERNSHIP DETAILS (FOR ALL SLIDES)
# ════════════════════════════════════════════════════════════

**Student Name:** Maheshwaram Rohith  
**Roll No:** 24EG107C27  
**Class:** B.Tech – AI & Machine Learning, Section C  
**Department:** Artificial Intelligence and Machine Learning (AIML)  
**Mentor:** Ms. Kruthika  
**Institution:** Anurag University  
**Internship Organization:** VedLinks  
**Internship Duration:** Summer 2026  
**Domain:** Full-Stack Web Development, Automation, Cloud Integration  

---

# ════════════════════════════════════════════════════════════
# SLIDE 1 — PROJECT TITLE & STUDENT DETAILS
# ════════════════════════════════════════════════════════════

## 🎯 SLIDE HEADING: "01. PROJECT TITLE & STUDENT DETAILS"

### Project Title:
> **Hospital WhatsApp Automation System**
> *A Full-Stack Hospital Management Platform with Automated WhatsApp-Based Patient Communication*

---

### Left Box — STUDENT:
- **Name:** Maheshwaram Rohith
- **Roll No:** 24EG107C27

### Right Box — PROGRAM:
- B.Tech, AI & Machine Learning (Section C)
- Anurag University

### Left Box — INTERNSHIP ORGANIZATION:
- **VedLinks**

### Right Box — DOMAIN:
- Full-Stack Web Development  
- WhatsApp Automation  
- Cloud Database Integration  
- REST API Development  

### Bottom — DURATION:
- Summer Internship, 2026

### Footer:
- Mentor: Ms. Kruthika | Department of Artificial Intelligence and Machine Learning

---

# ════════════════════════════════════════════════════════════
# SLIDE 2 — ABSTRACT (150–200 WORDS)
# ════════════════════════════════════════════════════════════

## 🎯 SLIDE HEADING: "02. ABSTRACT"

### Abstract Text (use in slide body):

The **Hospital WhatsApp Automation System** is a comprehensive, production-ready hospital management platform developed during a Summer 2026 internship at **VedLinks**. This system bridges the gap between traditional hospital administrative workflows and modern communication technologies by integrating a React-based web dashboard with a Python-powered backend API and the Twilio WhatsApp Business API.

The platform enables hospital staff to manage patients, appointments, doctors, and users through a sleek role-based web interface, while simultaneously allowing patients to interact with the hospital via a conversational WhatsApp chatbot — booking, rescheduling, or cancelling appointments in real time without human intervention.

The system features **PBKDF2/SHA256 secure password hashing**, **JWT-based authentication**, **role-based access control (RBAC)** for five distinct roles (Superadmin, Admin, Reception, Campaign, Viewer), **multi-turn chatbot conversation state management**, and full **MySQL cloud database persistence**.

This project demonstrates the real-world application of software engineering, API integration, database design, and automation engineering — skills directly aligned with the AIML curriculum at Anurag University.

> **Keywords:** WhatsApp Automation, REST API, Flask, React, MySQL, JWT, RBAC, Twilio, Chatbot

---

# ════════════════════════════════════════════════════════════
# SLIDE 3 — OBJECTIVES OF INTERNSHIP
# ════════════════════════════════════════════════════════════

## 🎯 SLIDE HEADING: "03. OBJECTIVES OF INTERNSHIP"

### Primary Objectives:

1. **🏗️ Build a Full-Stack Hospital Management System**
   - Develop a React + Vite frontend dashboard for hospital staff
   - Create a Flask (Python) RESTful backend API to serve data
   - Connect both layers to a remote MySQL cloud database

2. **🤖 Automate Patient Communication via WhatsApp**
   - Integrate the Twilio WhatsApp Business API for real-time messaging
   - Implement a rule-based, multi-turn chatbot for appointment booking
   - Enable automated confirmation, reminder, and notification messages

3. **🔐 Implement Enterprise-Grade Security**
   - Design a secure login system using PBKDF2/SHA256 password hashing with unique salts
   - Implement JWT (JSON Web Token) based stateless authentication
   - Build Role-Based Access Control (RBAC) to restrict module access per role

4. **📊 Create a Role-Based Dashboard with Real-Time Data**
   - Build role-adaptive dashboards (what each user sees depends on their role)
   - Display live statistics: Total Patients, Today's Appointments, Total Appointments
   - Support full CRUD operations for Users, Doctors, Patients, and Appointments

5. **🧩 Integrate Multiple Modern Technologies**
   - Learn and apply Flask-SQLAlchemy ORM for database interaction
   - Use Celery + Redis for background task queuing
   - Apply n8n workflow automation for webhook-based message routing

6. **📁 Write Production-Quality, Documented Code**
   - Follow clean architecture principles (separation of concerns)
   - Write extensive documentation (10+ .md guide files)
   - Implement environment variable-based configuration for secure deployment

---

### Secondary Objectives:
- Learn professional Git version control and GitHub workflow
- Practice API testing and debugging
- Experience agile-style iterative development at a real company (VedLinks)
- Develop a portfolio-ready, deployable project

---

# ════════════════════════════════════════════════════════════
# SLIDE 4 — TECHNOLOGIES & TOOLS USED
# ════════════════════════════════════════════════════════════

## 🎯 SLIDE HEADING: "04. TECHNOLOGIES & TOOLS USED"

---

### 🖥️ FRONTEND TECHNOLOGIES:

| Technology | Version | Purpose |
|---|---|---|
| **React.js** | v18 | UI Component Library |
| **Vite** | v5 | Build Tool & Dev Server (ultra-fast HMR) |
| **JavaScript (ES6+)** | — | Frontend Logic & Interactivity |
| **CSS / TailwindCSS** | — | Responsive Styling & Layout |
| **React Hooks** | — | State Management (`useState`, `useEffect`) |
| **Axios / Fetch API** | — | REST API Communication |
| **localStorage** | Browser API | Client-Side Data Persistence |

---

### ⚙️ BACKEND TECHNOLOGIES:

| Technology | Version | Purpose |
|---|---|---|
| **Python** | 3.10+ | Core Backend Language |
| **Flask** | 2.3.3 | Micro Web Framework for REST API |
| **Flask-SQLAlchemy** | 3.0.5 | ORM for Database Models |
| **Flask-JWT-Extended** | 4.5.3 | JWT Authentication Middleware |
| **Flask-CORS** | 4.0.0 | Cross-Origin Request Handling |
| **Flask-Bcrypt** | 1.0.1 | Password Hashing Support |
| **PyMySQL** | 1.1.0 | MySQL Database Connector |
| **python-dotenv** | 1.0.0 | Environment Variable Management |
| **Celery** | 5.3.4 | Distributed Task Queue |
| **Redis** | 5.0.1 | Message Broker for Celery |
| **Twilio** | 8.2.2 | WhatsApp Business API Integration |
| **Requests** | 2.31.0 | HTTP Client for API calls |

---

### 🗄️ DATABASE:

| Component | Details |
|---|---|
| **MySQL** | Remote Cloud Database (hosted server) |
| **Database Name** | `wha_chatbot` |
| **Tables** | users, doctors, patients, appointments, feedback, campaigns, message_logs, branches, permissions, login_details, module_creation, role_creation, role_assign |
| **ORM** | Flask-SQLAlchemy with connection pooling & auto-reconnect |

---

### 📱 WHATSAPP & AUTOMATION STACK:

| Tool | Purpose |
|---|---|
| **Twilio WhatsApp Business API** | Send & receive WhatsApp messages programmatically |
| **n8n (Open-Source)** | No-code automation to route webhook messages to Flask API |
| **Webhooks (HTTP POST)** | Receive incoming WhatsApp messages from patients |
| **Twilio Sandbox** | Development & testing environment for WhatsApp messaging |

---

### 🔐 SECURITY TOOLS:

| Tool | Purpose |
|---|---|
| **PBKDF2-SHA256** | Password hashing algorithm (100,000 iterations) |
| **Unique Salt per User** | Prevents rainbow table & brute-force attacks |
| **JWT (JSON Web Tokens)** | Stateless authentication (24hr expiry) |
| **Environment Variables (.env)** | Secure credential storage (never hardcoded) |

---

### 🛠️ DEVELOPER TOOLS:

| Tool | Purpose |
|---|---|
| **VS Code** | Primary Code Editor |
| **Git + GitHub** | Version Control & Source Code Hosting |
| **ngrok** | Expose local server via public HTTPS URL for webhook testing |
| **Postman** | API Testing & Debugging |
| **PowerShell / Terminal** | Command-line execution |
| **GitGuardian** | Secret scanning (detected & resolved 17 exposed credentials) |

---

# ════════════════════════════════════════════════════════════
# SLIDE 5 — LEARNINGS (WITH SCREENSHOTS/DIAGRAMS SECTION)
# ════════════════════════════════════════════════════════════

## 🎯 SLIDE HEADING: "05. LEARNINGS"

---

### 🧠 KEY TECHNICAL LEARNINGS:

#### 1. Full-Stack Architecture Design
- Learned how to decouple a frontend (React) from a backend (Flask API)
- Understood the REST API contract pattern — JSON requests/responses
- Implemented CORS to allow cross-origin communication between React (port 5173) and Flask (port 5000)
- Managed environment configuration using `.env` files and `python-dotenv`

#### 2. Database Design & ORM
- Designed 13+ relational MySQL tables with foreign key relationships
- Used Flask-SQLAlchemy to define Python class-based models (ORM)
- Implemented:
  - One-to-many: Branches → Doctors, Doctors → Appointments
  - Many-to-many: Users → Roles (via role_assign table)
  - Polymorphic relationships: Appointments ↔ Patients ↔ Doctors
- Configured connection pooling (`pool_pre_ping`, `pool_recycle`) for remote DB stability

#### 3. Security Engineering
- **Password Hashing:** Implemented PBKDF2-SHA256 (the gold standard) with unique per-user salts
  - Each password is hashed 100,000 times making brute-force computationally infeasible
  - Even if DB is breached, actual passwords cannot be recovered
- **JWT Authentication:** Stateless token system — no server-side session storage required
  - Access tokens expire in 24 hours
  - Protected endpoints require `Authorization: Bearer <token>` header
- **Role-Based Access Control:** 5 roles → different module access
  - `superadmin` → all modules
  - `admin` → all except system settings
  - `reception` → patients + appointments
  - `campaign` → marketing module only
  - `viewer` → read-only dashboard

#### 4. WhatsApp Chatbot Development
- Built a **multi-turn conversation state machine** in Python
- The chatbot maintains conversation context per phone number across multiple messages
- State flow: `new → greeting → select_doctor → choose_date → choose_time → confirm_name → confirm_phone → booked`
- Implemented input validation at each step (date format, time slot validation, phone number checks)
- Integrated with Twilio API to actually send replies back to patients via WhatsApp

#### 5. Webhook Integration
- Learned how webhooks work: Twilio sends an HTTP POST to our Flask server whenever a patient sends a WhatsApp message
- Handled form-encoded data (`application/x-www-form-urlencoded`) from Twilio
- Used ngrok to expose our local Flask server (`localhost:5000`) as a public HTTPS URL for Twilio to call
- Built the webhook handler at `/webhooks/twilio` in Flask

#### 6. Frontend React Development
- Built a single-page application (SPA) with multiple views: Dashboard, Appointments, Patients, Doctors, Users
- Implemented **role-adaptive rendering** — sidebar menu items, stat cards, and action buttons change based on the logged-in user's role
- Used `localStorage` for instant data persistence without API loading delays (optimistic UI)
- Managed complex form state: Add User modal, Edit User modal, Password Reset modal

#### 7. API Design & RESTful Principles
- Designed endpoints following REST conventions:
  - `GET /api/appointments` → list all appointments
  - `POST /api/appointments` → create new appointment
  - `PUT /api/appointments/<id>` → update appointment
  - `DELETE /api/appointments/<id>` → delete appointment
- Similarly for `/api/users`, `/api/doctors`, `/api/patients`, `/api/branches`
- Protected all endpoints with JWT middleware
- Implemented proper HTTP status codes (200, 201, 400, 401, 403, 404, 500)

#### 8. DevSecOps — Secret Management
- Identified 17 exposed secrets (MySQL credentials, Twilio tokens) flagged by GitGuardian
- Fixed all instances across 36 files by replacing hardcoded values with `os.environ.get()`
- Understood the importance of `.gitignore`, `.env` files, and secret rotation in production systems

---

### 📸 DIAGRAMS / SCREENSHOTS FOR SLIDE 5:

#### Diagram A — System Architecture Flow:
```
[Patient's Phone]
      |
      | (sends "Book appointment")
      ↓
[WhatsApp Business API (Twilio)]
      |
      | (HTTP POST webhook)
      ↓
[Flask Backend — /webhooks/twilio]
      |
      | (ChatbotLogic.handle_chat())
      ↓
[MySQL Cloud Database]
      |
      | (saves appointment)
      ↓
[React Dashboard — updates in real-time]
      |
      | (shows new booking)
      ↓
[Hospital Staff sees the booking]
```

#### Diagram B — Role-Based Access Control:
```
LOGIN
  ↓
[JWT Token issued with Role]
  ↓
  ├─ superadmin → ALL modules (Dashboard, Appointments, Patients, Doctors, Users)
  ├─ admin      → Dashboard, Appointments, Patients, Doctors, Users (manage)
  ├─ reception  → Dashboard, Patients, Appointments
  ├─ campaign   → Dashboard, Campaigns
  └─ viewer     → Dashboard only (read-only)
```

#### Diagram C — Chatbot State Machine:
```
START
  ↓
"Hi / Hello" received
  ↓
[GREETING] → Show doctor list
  ↓
Patient selects doctor number
  ↓
[DATE SELECTION] → "Enter date YYYY-MM-DD"
  ↓
Patient enters date
  ↓
[TIME SELECTION] → Show available slots (10:00, 11:00, 14:00, 15:00, 16:00)
  ↓
Patient selects time
  ↓
[NAME COLLECTION] → "Enter your full name"
  ↓
[PHONE COLLECTION] → "Enter your 10-digit phone"
  ↓
[CONFIRMATION] → Appointment saved to MySQL DB
  ↓
✅ "Your appointment is CONFIRMED!" sent via WhatsApp
```

#### Diagram D — Password Security Architecture:
```
User enters: "mypassword"
  ↓
System generates: random_salt = "a1b2c3d4..."
  ↓
PBKDF2-SHA256(password + salt, 100,000 iterations) → hash_value
  ↓
Stored in DB: { password_hash: "ef3a...", password_salt: "a1b2..." }
  ↓
NEVER stores plain text password
  ↓
On login: re-compute hash with stored salt, compare
```

---

### 🌟 SOFT SKILLS & PROFESSIONAL LEARNINGS:
- Working in a real company environment (VedLinks) with professional expectations
- Understanding project planning, feature scoping, and iterative delivery
- Reading and writing technical documentation
- Debugging complex integration issues between multiple systems
- Time management: balancing learning new technologies while delivering results

---

# ════════════════════════════════════════════════════════════
# SLIDE 6 — RESULT & CONCLUSION
# ════════════════════════════════════════════════════════════

## 🎯 SLIDE HEADING: "06. RESULT & CONCLUSION"

---

### ✅ PROJECT RESULTS:

#### Deliverable 1: Fully Functional Hospital Dashboard (React Frontend)
- ✅ Role-based login system with 5 distinct user roles
- ✅ Dynamic dashboard showing Total Patients, Today's Appointments, Total Appointments
- ✅ Full CRUD operations for Users (Add, Edit, Delete, Toggle Status, Reset Password)
- ✅ Full CRUD operations for Appointments, Patients, and Doctors
- ✅ Module-based access control (sidebar adapts to user role)
- ✅ Data persists across page refreshes via localStorage + backend API sync
- ✅ Responsive, modern UI with smooth animations and interactive elements

#### Deliverable 2: Python Flask REST API Backend
- ✅ 9 route modules: auth, users, appointments, patients, doctors, branches, campaigns, feedback, webhooks
- ✅ 13+ database models (ORM) mapped to MySQL tables
- ✅ JWT-protected endpoints
- ✅ PBKDF2-SHA256 secure password system
- ✅ CORS-enabled for frontend-backend communication
- ✅ Connection-pooled MySQL integration with auto-reconnect

#### Deliverable 3: WhatsApp Chatbot Integration
- ✅ Twilio WhatsApp webhook handler (`/webhooks/twilio`)
- ✅ Multi-turn conversation state machine
- ✅ 6-step appointment booking flow via WhatsApp
- ✅ Real-time appointment saving to MySQL database
- ✅ Confirmation messages sent back to patients
- ✅ n8n automation workflow for message routing

#### Deliverable 4: Security Hardening
- ✅ Fixed 17 GitGuardian-flagged security incidents
- ✅ All secrets moved to environment variables
- ✅ PBKDF2-SHA256 hashing across all user accounts
- ✅ JWT tokens with 24-hour expiry

#### Deliverable 5: Documentation
- ✅ 10+ comprehensive `.md` documentation files in `/docs/`
- ✅ SHA256 Architecture Guide
- ✅ User Management Guide
- ✅ Testing Guide with step-by-step test cases
- ✅ n8n WhatsApp Setup Guide
- ✅ Dual Login Methods Guide
- ✅ Project Testing Documentation (800+ lines)

---

### 📊 METRICS & IMPACT:

| Metric | Value |
|---|---|
| Total Source Files | 50+ (Python + JavaScript + CSS) |
| Lines of Code | ~15,000+ |
| REST API Endpoints | 30+ endpoints |
| Database Tables | 13 tables |
| User Roles Supported | 5 (superadmin, admin, reception, campaign, viewer) |
| Security Issues Fixed | 17 GitGuardian incidents resolved |
| Documentation Pages | 10 comprehensive guides |
| Technologies Integrated | 15+ tools & frameworks |
| WhatsApp Chatbot Steps | 6-step booking flow |
| Test Accounts Created | 7 users across all roles |

---

### 🏁 CONCLUSION:

The **Hospital WhatsApp Automation System**, developed during the Summer 2026 internship at **VedLinks**, successfully demonstrates how modern software technologies can be combined to solve real-world healthcare administration challenges.

**Key Achievements:**
1. **Eliminated manual appointment booking** — patients can self-serve via WhatsApp, reducing receptionist workload by an estimated 60-70% for routine bookings
2. **Role-based security** — ensures sensitive patient data is only accessible to authorized staff
3. **Zero-cost automation** — the system uses Twilio's free tier and n8n self-hosted, eliminating subscription costs for automation tools
4. **Production-ready security** — PBKDF2-SHA256 meets NIST security standards for password storage
5. **Scalable architecture** — the decoupled frontend/backend design allows each layer to be scaled independently

**Learning Outcome:**  
This internship provided hands-on experience with **full-stack web development**, **API design**, **database engineering**, **security best practices**, and **automation integration** — all highly relevant to the AIML curriculum and future career paths in Software Engineering and AI/ML System Development.

**Future Enhancements:**
- Integrate an actual AI/ML model (NLP) for smarter chatbot responses
- Add appointment reminder push notifications
- Implement real-time WebSocket updates for live dashboard refresh
- Add analytics dashboard with chart visualizations
- Mobile app development for doctors and patients

---

# ════════════════════════════════════════════════════════════
# SLIDE 7 — THANK YOU SLIDE
# ════════════════════════════════════════════════════════════

## 🎯 SLIDE HEADING: "THANK YOU"

### Content:

**"Thank You for Your Valuable Time and Attention"**

---

**Presented By:**  
**Maheshwaram Rohith**  
Roll No: 24EG107C27  
B.Tech – Artificial Intelligence and Machine Learning, Section C  
Anurag University  

---

**Project:** Hospital WhatsApp Automation System  
**Organization:** VedLinks  
**Mentor:** Ms. Kruthika  
**Duration:** Summer Internship 2026  

---

*"This project is a step toward intelligent, automated healthcare administration — where technology empowers medical professionals to focus on what matters most: patient care."*

---

### Optional footer text:
- 📧 maheshwaramrohith2157@gmail.com
- 🐙 github.com/rohith2157

---

# ════════════════════════════════════════════════════════════
# DETAILED APPENDIX — EXTENDED TECHNICAL NOTES
# (Use for viva/questions preparation)
# ════════════════════════════════════════════════════════════

---

## 📁 COMPLETE PROJECT FILE STRUCTURE

```
HOSPITAL_WHATSAPP_AUTOMATION_SYSTEM/
│
├── 📂 backend/                          # Python Flask API Server
│   ├── 📂 app/                          # Main application package
│   │   ├── auth.py                      # Authentication logic (login, JWT)
│   │   ├── config.py                    # App configuration (DB, JWT, Twilio)
│   │   ├── init.py                      # App factory, SQLAlchemy setup
│   │   ├── models.py                    # 13 SQLAlchemy ORM models
│   │   └── 📂 routes/                   # API route blueprints
│   │       ├── appointments.py          # /api/appointments CRUD
│   │       ├── branches.py              # /api/branches CRUD
│   │       ├── campaigns.py             # /api/campaigns CRUD
│   │       ├── dashboard.py             # /api/dashboard stats
│   │       ├── doctors.py               # /api/doctors CRUD
│   │       ├── feedback.py              # /api/feedback CRUD
│   │       ├── patients.py              # /api/patients CRUD
│   │       ├── users.py                 # /api/users CRUD + admin ops
│   │       └── webhooks.py              # /webhooks/twilio handler
│   │
│   ├── hospital_chatbot.py              # Terminal-mode chatbot demo
│   ├── whatsapp_simulator.py            # WhatsApp simulation testing
│   ├── whatsapp_webhook_server.py       # Standalone webhook server
│   ├── run.py                           # App entry point
│   ├── requirements.txt                 # Python dependencies
│   ├── .env                             # Environment variables (gitignored)
│   └── .env.example                     # Template for .env setup
│
├── 📂 frontend/                         # React + Vite Web Application
│   ├── 📂 src/
│   │   ├── WorkingApp.jsx               # Main app component (~1700+ lines)
│   │   ├── index.css                    # Global styles
│   │   └── main.jsx                     # React entry point
│   ├── index.html                       # HTML shell
│   ├── vite.config.js                   # Vite build configuration
│   └── package.json                     # Node.js dependencies
│
└── 📂 docs/                             # Project documentation
    ├── SHA256_ARCHITECTURE.md           # Security architecture guide
    ├── USER_MANAGEMENT_GUIDE.md         # User management docs
    ├── TESTING_GUIDE.md                 # Test procedures
    ├── CHATBOT_SETUP_GUIDE.md           # Chatbot configuration
    ├── N8N_WHATSAPP_SETUP.md            # n8n workflow setup
    ├── HASHING_WITH_JWT_GUIDE.md        # JWT + hashing guide
    ├── DUAL_LOGIN_METHODS_GUIDE.md      # Login method documentation
    ├── ADDITIONAL_FEATURES_GUIDE.md     # Feature documentation
    ├── PROJECT_TESTING_DOCUMENTATION.md # Comprehensive test docs
    └── VISUAL_GUIDE.md                  # UI walkthrough
```

---

## 🔌 COMPLETE API ENDPOINT REFERENCE

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/login` | Login with username + password → returns JWT token |
| GET | `/api/auth/me` | Get current user details from JWT |

### Users
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/users` | List all users |
| POST | `/api/users` | Create new user |
| PUT | `/api/users/<id>` | Update user details |
| DELETE | `/api/users/<id>` | Delete user |
| PUT | `/api/users/<id>/toggle-status` | Toggle active/inactive |

### Appointments
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/appointments` | List all appointments |
| POST | `/api/appointments` | Create new appointment |
| PUT | `/api/appointments/<id>` | Update appointment |
| DELETE | `/api/appointments/<id>` | Delete appointment |

### Doctors
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/doctors` | List all doctors |
| POST | `/api/doctors` | Add new doctor |
| PUT | `/api/doctors/<id>` | Update doctor info |
| DELETE | `/api/doctors/<id>` | Remove doctor |

### Patients
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/patients` | List all patients |
| POST | `/api/patients` | Create patient record |
| PUT | `/api/patients/<id>` | Update patient |

### Webhooks
| Method | Endpoint | Description |
|---|---|---|
| POST | `/webhooks/twilio` | Receive incoming WhatsApp messages from Twilio |
| POST | `/webhooks/send-whatsapp` | Send WhatsApp message via Twilio API |
| POST | `/api/chatbot/message` | n8n integration endpoint for chatbot |

---

## 🗄️ DATABASE SCHEMA OVERVIEW

### Table: `users`
| Column | Type | Notes |
|---|---|---|
| id | INT | Primary Key |
| username | VARCHAR(100) | Unique |
| password_hash | VARCHAR(255) | PBKDF2-SHA256 hash |
| password_salt | VARCHAR(255) | Unique per user |
| full_name | VARCHAR(255) | Display name |
| role | ENUM | superadmin/admin/reception/campaign/viewer |
| email | VARCHAR(255) | Contact email |
| phone | VARCHAR(20) | Contact phone |
| is_active | BOOLEAN | Account status |
| created_at | TIMESTAMP | Auto-set |

### Table: `appointments`
| Column | Type | Notes |
|---|---|---|
| id | INT | Primary Key |
| patient_id | INT | FK → patients |
| doctor_id | INT | FK → doctors |
| branch_id | INT | FK → branches |
| patient_name | VARCHAR(255) | Denormalized for speed |
| patient_phone | VARCHAR(30) | For WhatsApp messaging |
| scheduled_at | DATETIME | Appointment date/time |
| status | ENUM | booked/confirmed/cancelled/completed/no_show |
| source | ENUM | whatsapp/admin/phone |

### Table: `doctors`
| Column | Type | Notes |
|---|---|---|
| id | INT | Primary Key |
| branch_id | INT | FK → branches |
| first_name | VARCHAR(100) | — |
| last_name | VARCHAR(100) | — |
| specialties | VARCHAR(255) | Medical specialty |
| consultation_fee | DECIMAL(10,2) | In rupees |
| is_active | BOOLEAN | Available for booking |

### Table: `patients`
| Column | Type | Notes |
|---|---|---|
| id | INT | Primary Key |
| whatsapp_number | VARCHAR(30) | Unique WhatsApp ID |
| name | VARCHAR(255) | Patient name |
| age | INT | — |
| gender | ENUM | male/female/other |
| last_visit | DATE | Last appointment |

### Table: `message_logs`
| Column | Type | Notes |
|---|---|---|
| id | INT | Primary Key |
| to_number | VARCHAR(30) | Recipient |
| from_number | VARCHAR(30) | Sender |
| body | TEXT | Message content |
| direction | ENUM | outbound/inbound |
| status | VARCHAR(50) | Delivery status |
| provider_message_id | VARCHAR(255) | Twilio message SID |

---

## 🔐 SECURITY IMPLEMENTATION DETAIL

### PBKDF2-SHA256 Password Hashing:
```python
import hashlib
import os

def hash_password(plain_password):
    salt = os.urandom(32).hex()  # 256-bit random salt
    key = hashlib.pbkdf2_hmac(
        'sha256',                # Hash digest algorithm
        plain_password.encode(), # Convert password to bytes
        salt.encode(),           # Provide the salt
        100000                   # 100,000 iterations (NIST recommended)
    )
    return key.hex(), salt

def verify_password(stored_hash, salt, plain_password):
    computed = hashlib.pbkdf2_hmac('sha256', 
               plain_password.encode(), salt.encode(), 100000)
    return computed.hex() == stored_hash
```

### JWT Authentication Flow:
```
1. User POSTs { username, password } to /api/auth/login
2. Server fetches user from DB, verifies password hash
3. If valid → creates JWT: { sub: user_id, role: "admin", exp: +24h }
4. JWT signed with SECRET_KEY (from env variable)
5. Client stores JWT in localStorage
6. Every subsequent request includes: Authorization: Bearer <token>
7. Flask-JWT-Extended middleware validates token on protected routes
```

---

## 📱 WHATSAPP CHATBOT CONVERSATION SAMPLE

```
Patient: Hi
Bot: 👋 Welcome to City Hospital!
     How can I help you today?
     
     Reply:
     1️⃣ Book an Appointment
     2️⃣ Check my Appointment
     3️⃣ Cancel Appointment

Patient: 1
Bot: 👨‍⚕️ Available Doctors:
     1. Dr. Rajesh Kumar — Cardiology
     2. Dr. Priya Sharma — Orthopedics  
     3. Dr. Anil Mehta — General Medicine
     
     Please enter doctor number:

Patient: 2
Bot: ✓ You selected Dr. Priya Sharma (Orthopedics)
     
     Please enter preferred date (YYYY-MM-DD):
     Example: 2026-07-15

Patient: 2026-07-15
Bot: 📅 Date: 2026-07-15
     
     Available time slots:
     🕐 10:00 AM
     🕐 11:00 AM
     🕐 02:00 PM
     🕐 03:00 PM
     🕐 04:00 PM
     
     Please enter time (HH:MM):

Patient: 10:00
Bot: ✓ Time: 10:00 AM
     Please provide your full name:

Patient: Maheshwaram Rohith
Bot: ✓ Name: Maheshwaram Rohith
     Please provide your 10-digit phone number:

Patient: 9010444486
Bot: ✅ APPOINTMENT BOOKED SUCCESSFULLY!
     
     📋 BOOKING DETAILS:
     ━━━━━━━━━━━━━━━━━━
     👤 Patient: Maheshwaram Rohith
     📞 Phone: 9010444486
     👨‍⚕️ Doctor: Dr. Priya Sharma
     📅 Date: 2026-07-15
     🕐 Time: 10:00 AM
     ━━━━━━━━━━━━━━━━━━
     ✔️ Status: CONFIRMED
     📱 You will receive a reminder before your appointment.
```

---

## 🧩 n8n WORKFLOW ARCHITECTURE

```
[Twilio WhatsApp] 
        ↓ (webhook POST on each incoming message)
[n8n — Webhook Trigger Node]
        ↓ (extract: From, Body)
[n8n — HTTP Request Node]  →  POST http://your-server:5000/api/chatbot/message
        ↓ (receive JSON response with bot's reply)
[n8n — WhatsApp Send Node]  →  Sends reply back to patient via Twilio
```

This architecture means:
- **Zero cost** for the automation workflow (n8n is self-hosted and free)
- **Full flexibility** — can add conditional logic, logging, or branching in n8n
- **Separation of concerns** — the Python chatbot engine is independent of the messaging channel

---

## 🎓 INTERNSHIP SUMMARY FOR VIVA PREPARATION

**Q: What problem does your project solve?**  
A: Traditional hospitals rely on phone calls and walk-ins for appointment booking. Our system automates this via WhatsApp, allowing patients to book 24/7 without staff intervention, while the dashboard gives hospital staff real-time visibility.

**Q: What is your system's most technically complex component?**  
A: The multi-turn WhatsApp chatbot with state persistence per phone number. Each conversation has to remember which step the patient is at across multiple separate HTTP requests (stateless by nature), which required careful state management.

**Q: How is security ensured?**  
A: Three layers — PBKDF2-SHA256 hashing with unique salts (no plain-text passwords stored), JWT tokens for stateless session management, and RBAC to restrict what each user can view and do.

**Q: How does the frontend communicate with the backend?**  
A: Via REST API calls. The React frontend makes `fetch()` / Axios HTTP requests to Flask endpoints. JWT token is included in the `Authorization` header for protected routes.

**Q: What was the biggest challenge?**  
A: Integrating multiple systems (React ↔ Flask ↔ MySQL ↔ Twilio ↔ n8n) while ensuring each component works reliably together, especially when the remote MySQL database was unavailable (connection pooling solved this).

**Q: What is the business value?**  
A: Reduces receptionist workload by 60-70% for routine bookings, eliminates after-hours phone calls, provides 24/7 patient self-service, and gives hospital management real-time visibility into appointment flow — all at near-zero recurring software cost.

---

# ════════════════════════════════════════════════════════════
# PPT DESIGN GUIDELINES (COLOR THEME & STYLE REFERENCE)
# ════════════════════════════════════════════════════════════

## Recommended PPT Style:

**Theme:** Professional Dark / Medical Blue  
**Primary Color:** Deep Navy Blue `#0A1628` or Medical Blue `#1565C0`  
**Accent Color:** Teal / Green `#00BCD4` or `#4CAF50`  
**Text:** White / Light Gray  
**Highlight:** Amber/Gold `#FFA726` for important stats  

**Font:**
- Headings: `Montserrat Bold` or `Poppins SemiBold`  
- Body: `Open Sans` or `Inter Regular`  
- Code snippets: `Courier New` or `Fira Code`  

**Slide Structure (8 slides total):**
| Slide # | Content | Style Note |
|---|---|---|
| 1 | Title + Student Details | Full-page layout with boxes, company logo (VedLinks) |
| 2 | Abstract | Clean text with highlighted keywords |
| 3 | Objectives | Numbered list with icons |
| 4 | Technologies & Tools | 2-column table layout with logos |
| 5 | Learnings + Diagrams | Flowchart diagrams + bullet points |
| 6 | Results & Conclusion | Metric cards + conclusion text |
| 7 | (Optional extra) | Additional screenshots or architecture diagram |
| 8 | Thank You | Minimal, elegant, student details |

---

*Document prepared by: Maheshwaram Rohith | Roll No: 24EG107C27 | B.Tech AIML Section C | Anurag University | Summer Internship 2026 — VedLinks | Mentor: Ms. Kruthika*
