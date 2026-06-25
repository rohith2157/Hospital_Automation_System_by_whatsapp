"""
Complete WhatsApp webhook server - handles verification AND messages
No n8n needed! Direct: Meta → This Server → WhatsApp Reply
Saves appointments to database for frontend display!
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import requests
import sys
import os
from datetime import datetime

# Add the app directory to path for chatbot import
sys.path.insert(0, os.path.dirname(__file__))
from app.utils.chatbot_engine import chatbot, set_db_functions

app = Flask(__name__)
CORS(app)

# ========================================
# DATABASE CONFIGURATION (Remote MySQL)
# ========================================
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://remote_user:%40Codevocado%23remote%251@69.62.82.234/wha_chatbot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}
db = SQLAlchemy(app)

# ========================================
# DATABASE MODELS (Simplified)
# ========================================
class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    branch_id = db.Column(db.Integer, default=1)
    doctor_id = db.Column(db.Integer)
    patient_id = db.Column(db.Integer, nullable=True)
    patient_name = db.Column(db.String(255))
    patient_phone = db.Column(db.String(30))
    scheduled_at = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='booked')
    source = db.Column(db.String(20), default='whatsapp')
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    whatsapp_number = db.Column(db.String(30), unique=True)
    name = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    branch_id = db.Column(db.Integer, default=1)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    specialties = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)


# ========================================
# DATABASE HELPER FUNCTIONS
# ========================================
def get_doctors_from_db():
    """Get all active doctors from database"""
    try:
        with app.app_context():
            doctors = Doctor.query.filter_by(is_active=True).all()
            return [
                {
                    'id': doc.id,
                    'name': f"Dr. {doc.first_name} {doc.last_name}".strip(),
                    'specialization': doc.specialties or 'General'
                }
                for doc in doctors
            ]
    except Exception as e:
        print(f"❌ Error getting doctors: {e}")
        # Return default doctors if DB fails
        return [
            {'id': 1, 'name': 'Dr. John Smith', 'specialization': 'Cardiology'},
            {'id': 2, 'name': 'Dr. Sarah Johnson', 'specialization': 'Pediatrics'},
            {'id': 3, 'name': 'Dr. Michael Brown', 'specialization': 'Orthopedics'}
        ]


def save_appointment_to_db(patient_name, patient_phone, doctor_id, scheduled_at, source='whatsapp'):
    """Save appointment to database and return appointment ID"""
    try:
        with app.app_context():
            # Parse scheduled_at if string
            if isinstance(scheduled_at, str):
                scheduled_at = datetime.fromisoformat(scheduled_at)
            
            # Create appointment directly (skip patient creation to avoid ID issue)
            appointment = Appointment(
                branch_id=1,
                doctor_id=doctor_id,
                patient_id=None,  # Skip patient linking for now
                patient_name=patient_name,
                patient_phone=patient_phone,
                scheduled_at=scheduled_at,
                status='booked',
                source=source
            )
            db.session.add(appointment)
            db.session.commit()
            
            print(f"✅ Appointment #{appointment.id} saved to database!")
            return appointment.id
    except Exception as e:
        print(f"❌ Database error: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return None


def get_or_create_patient(phone, name=None):
    """Get or create patient by phone number"""
    try:
        with app.app_context():
            patient = Patient.query.filter_by(whatsapp_number=phone).first()
            if not patient and name:
                patient = Patient(whatsapp_number=phone, name=name)
                db.session.add(patient)
                db.session.commit()
            return patient.id if patient else None
    except Exception as e:
        print(f"❌ Patient error: {e}")
        return None


# Connect DB functions to chatbot
set_db_functions(save_appointment_to_db, get_or_create_patient, get_doctors_from_db)


# ========================================
# YOUR WHATSAPP CREDENTIALS (Meta API)
# ========================================
WHATSAPP_TOKEN = " EAAeAx7HErpUBQDa6ZCr1W6iQhvZCllJRUouZBkt2rofR092ZAZAiRyF82ec99dBlSsZCKIShG1nfVneUtKulHwHUK50IkiggeSxq2oYYvkP3eoQtaSY6VvVZCQSrZAM66vZBJZBl7wU4Vz8uSjTIieCedrTSZALJzVESuF36kMbqn6KnLoi8EPtp0YgQyTK7FLqfhPb68xTZCCYiMrwqMwov7Ho74ZBqOhrbojSZB2aCypQWay8alZAKAHr889Ov5dxOZAkg7ZAdZAPoxNe0BSfCNLSWjZCKYARj1HGjnMEG6OFKwZDZD"
PHONE_NUMBER_ID = "827223013816682"
VERIFY_TOKEN = "hospital_verify_token"

# In-memory patient state storage
patients_state = {}


def send_whatsapp_message(to_phone, message):
    """Send message via WhatsApp Business API (FREE!)"""
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "text": {"body": message}
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        print(f"📤 WhatsApp API Response: {result}")
        return result
    except Exception as e:
        print(f"❌ Error sending WhatsApp message: {e}")
        return {"error": str(e)}


@app.route('/webhook/whatsapp', methods=['GET', 'POST'])
def whatsapp_webhook():
    """Handle Meta WhatsApp webhook verification and messages"""
    
    # ========================================
    # GET: Webhook Verification (Meta calls this)
    # ========================================
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        print(f"\n{'='*60}")
        print("📥 WEBHOOK VERIFICATION REQUEST")
        print(f"{'='*60}")
        print(f"   Mode: {mode}")
        print(f"   Token: {token}")
        print(f"   Challenge: {challenge}")
        
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("✅ Webhook verified successfully!")
            print(f"{'='*60}\n")
            return challenge, 200
        else:
            print("❌ Verification failed - wrong token!")
            print(f"   Expected: {VERIFY_TOKEN}")
            print(f"   Received: {token}")
            print(f"{'='*60}\n")
            return 'Verification failed', 403
    
    # ========================================
    # POST: Incoming WhatsApp Message
    # ========================================
    try:
        data = request.get_json()
        
        print(f"\n{'='*60}")
        print("📨 INCOMING WHATSAPP MESSAGE")
        print(f"{'='*60}")
        
        # Extract message details from WhatsApp format
        if data.get('entry') and data['entry'][0].get('changes'):
            change = data['entry'][0]['changes'][0]
            value = change.get('value', {})
            
            # Check if it's a message (not a status update)
            if value.get('messages'):
                message_data = value['messages'][0]
                from_phone = message_data['from']
                
                # Handle different message types
                if message_data.get('type') == 'text':
                    message_text = message_data.get('text', {}).get('body', '')
                else:
                    message_text = '[Non-text message received]'
                
                print(f"📱 From: {from_phone}")
                print(f"💬 Message: {message_text}")
                
                # Get or create patient state
                if from_phone not in patients_state:
                    patients_state[from_phone] = {
                        'id': len(patients_state) + 1,
                        'state': 'new',
                        'phone': from_phone
                    }
                
                patient = patients_state[from_phone]
                print(f"👤 Patient ID: {patient['id']}, State: {patient['state']}")
                
                # Store phone in chatbot context for saving appointment
                chatbot.conversation_context.setdefault(patient['id'], {})['phone'] = from_phone
                
                # Process message using chatbot engine
                bot_response = chatbot.process_message(
                    patient_id=patient['id'],
                    message=message_text,
                    conversation_state=patient['state']
                )
                
                # Update patient state
                patient['state'] = bot_response['new_state']
                
                print(f"\n🤖 Bot Response:")
                print(f"   {bot_response['response'][:100]}...")
                print(f"   New State: {bot_response['new_state']}")
                
                # Send reply via WhatsApp Business API
                send_result = send_whatsapp_message(from_phone, bot_response['response'])
                
                if 'error' not in send_result:
                    print(f"\n✅ Message sent successfully!")
                else:
                    print(f"\n❌ Failed to send message: {send_result}")
                
                print(f"{'='*60}\n")
            else:
                # Status update (delivered, read, etc.) - ignore
                print("📊 Status update received (not a message)")
                
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "WhatsApp Webhook Server",
        "patients_active": len(patients_state)
    }), 200


@app.route('/', methods=['GET'])
def home():
    """Home page"""
    return """
    <html>
    <head><title>WhatsApp Webhook Server</title></head>
    <body style="font-family: Arial; padding: 40px; background: #1a1a2e; color: white;">
        <h1>🏥 Hospital WhatsApp Chatbot</h1>
        <p>✅ Server is running!</p>
        <hr>
        <h3>Endpoints:</h3>
        <ul>
            <li><b>GET/POST</b> /webhook/whatsapp - Meta webhook</li>
            <li><b>GET</b> /health - Health check</li>
        </ul>
        <hr>
        <p>📱 Verify Token: <code>whatsapp_verify_token</code></p>
    </body>
    </html>
    """


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🏥 HOSPITAL WHATSAPP CHATBOT SERVER")
    print("=" * 60)
    print("\n📍 Local URL: http://localhost:5679")
    print("🌐 Webhook Path: /webhook/whatsapp")
    print("\n⚙️  Configuration:")
    print(f"   • Verify Token: {VERIFY_TOKEN}")
    print(f"   • Phone Number ID: {PHONE_NUMBER_ID}")
    print(f"   • Token: {WHATSAPP_TOKEN[:20]}...")
    print("\n📝 Setup in Meta Developer Console:")
    print("   1. Go to WhatsApp > Configuration > Webhook")
    print("   2. Callback URL: https://YOUR_NGROK_URL/webhook/whatsapp")
    print(f"   3. Verify Token: {VERIFY_TOKEN}")
    print("   4. Subscribe to: messages")
    print("\n✅ Server ready!")
    print("=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5679)
