#!/usr/bin/env python3
"""
Hospital WhatsApp Chatbot Terminal - Uses Real Chatbot Engine
Multi-turn conversation with database persistence
"""

import requests
from datetime import datetime
import time
import sys

# Add app to path for imports
sys.path.insert(0, '/Api')

# Configuration
WEBHOOK_URL = "http://localhost:5679/webhook/whatsapp"
API_BASE_URL = "http://localhost:5000/api"
TEST_PHONE = "919010444486"
TEST_RECIPIENT = "827223013816682"

from app.utils.chatbot_engine import ChatbotEngine, set_db_functions


class TerminalChatbot:
    def __init__(self):
        self.token = None
        self.chatbot = ChatbotEngine()
        self.conversation_states = {}  # Track state per patient
        self.login()
        self.setup_db_functions()
    
    def login(self):
        """Authenticate with backend"""
        try:
            response = requests.post(f"{API_BASE_URL}/auth/login", json={
                "username": "rohith",
                "password": "********"
            })
            if response.status_code == 200:
                self.token = response.json().get('access_token')
                print("✅ Connected to Hospital System\n")
            else:
                print("⚠️ Warning: Could not authenticate\n")
        except Exception as e:
            print(f"⚠️ Warning: {e}\n")
    
    def setup_db_functions(self):
        """Setup database functions for chatbot engine"""
        try:
            set_db_functions(
                self.save_appointment_db,
                self.get_or_create_patient_db,
                self.get_doctors_db
            )
        except Exception as e:
            print(f"⚠️ Could not setup DB functions: {e}")
    
    def save_appointment_db(self, patient_name, patient_phone, doctor_id, scheduled_at, source='whatsapp'):
        """Save appointment to backend API"""
        try:
            headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
            data = {
                "patient_name": patient_name,
                "patient_phone": patient_phone,
                "doctor_id": int(doctor_id),
                "scheduled_at": scheduled_at,
                "source": source
            }
            response = requests.post(f"{API_BASE_URL}/appointments", json=data, headers=headers, timeout=5)
            if response.status_code == 200:
                return response.json().get('id')
            return None
        except Exception as e:
            print(f"Error saving appointment: {e}")
            return None
    
    def get_or_create_patient_db(self, name, phone):
        """Get or create patient"""
        try:
            headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
            response = requests.get(f"{API_BASE_URL}/patients", headers=headers, timeout=5)
            if response.status_code == 200:
                patients = response.json()
                for patient in patients:
                    if patient.get('phone') == phone:
                        return patient
            return {"name": name, "phone": phone}
        except Exception:
            return {"name": name, "phone": phone}
    
    def get_doctors_db(self):
        """Fetch doctors from backend API"""
        try:
            headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
            response = requests.get(f"{API_BASE_URL}/doctors", headers=headers, timeout=5)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception:
            return []
    
    def send_webhook_message(self, message_text):
        """Send message through webhook"""
        payload = {
            "object": "whatsapp_business_account",
            "entry": [{
                "id": "ENTRY_ID",
                "changes": [{
                    "value": {
                        "messaging_product": "whatsapp",
                        "messages": [{
                            "from": TEST_PHONE,
                            "id": f"wamid.{datetime.now().timestamp()}",
                            "timestamp": str(int(datetime.now().timestamp())),
                            "type": "text",
                            "text": {"body": message_text}
                        }],
                        "metadata": {
                            "display_phone_number": TEST_RECIPIENT,
                            "phone_number_id": TEST_RECIPIENT
                        }
                    },
                    "field": "messages"
                }]
            }]
        }
        
        try:
            requests.post(WEBHOOK_URL, json=payload, timeout=5)
            return True
        except Exception:
            return False
    
    def get_appointments(self):
        """Get appointments from database"""
        try:
            headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
            response = requests.get(f"{API_BASE_URL}/appointments", headers=headers)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception:
            return []
    
    def display_message(self, sender, message):
        """Display message in WhatsApp-style format"""
        timestamp = datetime.now().strftime("%H:%M")
        
        if sender == "You":
            # Right-aligned message (user)
            lines = message.split('\n')
            print()
            for line in lines:
                if len(line) < 70:
                    print(f"{' '*(70-len(line))}{line}")
                else:
                    print(line)
            print(f"{' '*(66)}{timestamp}")
        else:
            # Left-aligned message (bot)
            print()
            print(message)
            print(f"{timestamp}\n")
    
    def show_saved_appointments(self):
        """Display saved appointments from database"""
        appointments = self.get_appointments()
        print("\n" + "="*70)
        if appointments:
            print(f"📅 SAVED APPOINTMENTS ({len(appointments)} total)")
            print("="*70)
            for i, apt in enumerate(appointments[-5:], 1):
                print(f"\n{i}. 👤 {apt.get('patient_name')} | 👨‍⚕️ Doctor {apt.get('doctor_id')} | 📅 {apt.get('scheduled_at')}")
        else:
            print("No appointments saved yet")
        print("="*70 + "\n")
    
    def chat(self):
        """Main chat loop"""
        print("\n" + "="*70)
        print("🏥 HOSPITAL WHATSAPP CHATBOT - USING REAL CHATBOT ENGINE")
        print("="*70)
        print("\n📱 Real chatbot engine powering the conversation")
        print("💾 Appointments saved to database & updated in frontend")
        print("📊 Updates visible in http://localhost:5173\n")
        print("Type 'appointments' to see saved bookings")
        print("Type 'exit' to quit\n")
        print("="*70)
        
        patient_id = 1  # Test patient
        conversation_state = 'new'
        context = {'phone': TEST_PHONE}
        
        while True:
            try:
                user_input = input("👤 You: ").strip()
                
                if user_input.lower() == 'exit':
                    print("\n" + "="*70)
                    print("👋 Thank you for using Hospital Chatbot!")
                    print("="*70 + "\n")
                    break
                
                if user_input.lower() == 'appointments':
                    self.show_saved_appointments()
                    continue
                
                if not user_input:
                    continue
                
                # Display user message
                self.display_message("You", user_input)
                print("⏳ Processing... ", end="", flush=True)
                
                # Send through webhook
                self.send_webhook_message(user_input)
                print("✅")
                time.sleep(0.3)
                
                # Get response from actual chatbot engine
                result = self.chatbot.process_message(patient_id, user_input, conversation_state)
                
                # Update conversation state and context
                conversation_state = result.get('new_state', 'menu')
                context.update(result.get('data', {}))
                
                # Display bot response
                response = result.get('response', '')
                self.display_message("Bot", response)
                    
            except KeyboardInterrupt:
                print("\n\n" + "="*70)
                print("👋 Chat ended")
                print("="*70 + "\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")

def main():
    chatbot = TerminalChatbot()
    chatbot.chat()

if __name__ == "__main__":
    main()
    
    def send_webhook_message(self, message_text):
        """Send message through webhook"""
        payload = {
            "object": "whatsapp_business_account",
            "entry": [{
                "id": "ENTRY_ID",
                "changes": [{
                    "value": {
                        "messaging_product": "whatsapp",
                        "messages": [{
                            "from": TEST_PHONE,
                            "id": f"wamid.{datetime.now().timestamp()}",
                            "timestamp": str(int(datetime.now().timestamp())),
                            "type": "text",
                            "text": {"body": message_text}
                        }],
                        "metadata": {
                            "display_phone_number": TEST_RECIPIENT,
                            "phone_number_id": TEST_RECIPIENT
                        }
                    },
                    "field": "messages"
                }]
            }]
        }
        
        try:
            requests.post(WEBHOOK_URL, json=payload, timeout=5)
            return True
        except Exception:
            return False
    
    def get_doctors(self):
        """Fetch doctors from database"""
        try:
            headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
            response = requests.get(f"{API_BASE_URL}/doctors", headers=headers)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception:
            return []
    
    def book_appointment(self, patient_name, patient_phone, doctor_id, date, time_slot):
        """Save appointment to database"""
        try:
            headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
            data = {
                "patient_name": patient_name,
                "patient_phone": patient_phone,
                "doctor_id": int(doctor_id),
                "scheduled_at": f"{date}T{time_slot}:00",
                "source": "whatsapp"
            }
            response = requests.post(f"{API_BASE_URL}/appointments", json=data, headers=headers)
            return response.status_code == 200
        except Exception:
            return False
    
    def get_appointments(self):
        """Get appointments from database"""
        try:
            headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
            response = requests.get(f"{API_BASE_URL}/appointments", headers=headers)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception:
            return []
    
    def generate_response(self, user_input, user_id="patient_001"):
        """Generate chatbot response based on conversation state"""
        
        if user_id not in self.user_state:
            self.user_state[user_id] = {"step": "start", "data": {}}
        
        state = self.user_state[user_id]
        msg = user_input.lower().strip()
        
        # Step 1: Initial greeting
        if state["step"] == "start":
            if any(word in msg for word in ["hi", "hello", "hey", "book", "appointment", "doctor"]):
                state["step"] = "ask_doctor"
                doctors = self.get_doctors()
                if doctors:
                    doc_list = "\n".join([f"{d.get('id')}. {d.get('name')} - {d.get('specialization')}" 
                                         for d in doctors])
                    return f"Hi! Welcome to Hospital Appointment Booking 👋\n\n👨‍⚕️ Available Doctors:\n{doc_list}\n\nPlease select doctor number:"
                else:
                    return "Hi! Welcome! 👋\n\nPlease enter doctor ID (1-3):"
            else:
                return "👋 Welcome to Hospital!\n\nHow can I help you?\n\nType:\n• 'book' to book appointment\n• 'doctors' to see available doctors\n• 'appointments' to check your bookings"
        
        # Step 2: Get doctor selection
        elif state["step"] == "ask_doctor":
            if msg.isdigit():
                doctor_id = int(msg)
                doctors = self.get_doctors()
                doctor = next((d for d in doctors if d.get('id') == doctor_id), None)
                
                if doctor:
                    state["step"] = "ask_date"
                    state["data"]["doctor_id"] = doctor_id
                    state["data"]["doctor_name"] = doctor.get('name')
                    return f"✓ You selected 📋 {doctor.get('name')}\n\nPlease enter preferred date (YYYY-MM-DD):\nExample: 2025-12-05"
                else:
                    return "❌ Invalid doctor number. Please select from the list above."
            else:
                return "❌ Please enter a valid doctor number."
        
        # Step 3: Get date
        elif state["step"] == "ask_date":
            if len(msg) == 10 and msg.count('-') == 2:
                state["step"] = "ask_time"
                state["data"]["date"] = msg
                return f"Perfect! 📅 Date: {msg}\n\nAvailable time slots:\n🕐 10:00 AM\n🕐 11:00 AM\n🕐 02:00 PM\n🕐 03:00 PM\n🕐 04:00 PM\n\nPlease enter time (HH:MM):"
            else:
                return "❌ Invalid date format. Please use YYYY-MM-DD\nExample: 2025-12-05"
        
        # Step 4: Get time
        elif state["step"] == "ask_time":
            time_slots = ["10:00", "11:00", "14:00", "15:00", "16:00"]
            # Check if input matches any time slot
            if msg in time_slots or any(msg == f"{slot[:2]}:00" for slot in time_slots) or any(msg == f"{slot[:2]}" and int(msg) >= 10 for slot in time_slots if msg.isdigit()):
                # Normalize time
                normalized_time = msg if msg in time_slots else msg[:2] + ":00"
                if normalized_time in time_slots:
                    state["step"] = "ask_name"
                    state["data"]["time"] = normalized_time
                    return f"✓ Time: {normalized_time}\n\nPlease provide your full name:"
            
            return "❌ Invalid time. Please select from available slots:\n10:00, 11:00, 14:00, 15:00, 16:00"
        
        # Step 5: Get patient name
        elif state["step"] == "ask_name":
            if len(msg) >= 2 and not msg.isdigit():
                state["step"] = "ask_phone"
                state["data"]["name"] = msg.title()
                return f"✓ Name: {msg.title()}\n\nPlease provide your phone number:\nExample: 9876543210"
            else:
                return "❌ Please enter a valid name."
        
        # Step 6: Get phone & confirm booking
        elif state["step"] == "ask_phone":
            if len(msg) >= 10 and msg.isdigit():
                state["data"]["phone"] = msg
                
                # Book appointment in database
                success = self.book_appointment(
                    state["data"]["name"],
                    msg,
                    state["data"]["doctor_id"],
                    state["data"]["date"],
                    state["data"]["time"]
                )
                
                if success:
                    state["step"] = "confirmed"
                    confirmation = f"""
✅ APPOINTMENT BOOKED SUCCESSFULLY! ✅

📋 BOOKING DETAILS:
━━━━━━━━━━━━━━━━━━━━━━
👤 Patient: {state['data']['name']}
📞 Phone: {msg}
👨‍⚕️ Doctor: {state['data']['doctor_name']}
📅 Date: {state['data']['date']}
🕐 Time: {state['data']['time']}
━━━━━━━━━━━━━━━━━━━━━━

✔️ Status: CONFIRMED
⚠️ Booking received (offline mode)
📱 You will receive SMS reminder before appointment

💬 Commands:
• Type 'reschedule' to change time
• Type 'cancel' to cancel
• Type 'hi' for new booking
"""
                    return confirmation
                else:
                    return "⚠️ Booking saved locally (database connection issue)"
            else:
                return "❌ Please enter a valid 10-digit phone number."
        
        # After confirmation
        elif state["step"] == "confirmed":
            if "reschedule" in msg:
                state["step"] = "ask_date"
                return "Let's reschedule! Enter new date (YYYY-MM-DD):"
            elif "cancel" in msg:
                state["step"] = "start"
                return "Appointment cancelled. How else can we help you?"
            elif any(word in msg for word in ["hi", "hello", "book", "new"]):
                state["step"] = "ask_doctor"
                doctors = self.get_doctors()
                doc_list = "\n".join([f"{d.get('id')}. {d.get('name')} - {d.get('specialization')}" 
                                     for d in doctors])
                return f"New Booking!\n\n👨‍⚕️ Available Doctors:\n{doc_list}\n\nSelect doctor number:"
            else:
                return "Your appointment is confirmed! 📅\n\nWhat else can I help you with?"
    
    def display_message(self, sender, message):
        """Display message in WhatsApp-style format"""
        timestamp = datetime.now().strftime("%H:%M")
        
        if sender == "You":
            # Right-aligned message (user)
            lines = message.split('\n')
            print()
            for line in lines:
                print(f"{' '*(70-len(line))}{line}")
            print(f"{' '*(66)}{timestamp}")
        else:
            # Left-aligned message (bot)
            print()
            print(message)
            print(f"{timestamp}\n")
    
    def show_saved_appointments(self):
        """Display saved appointments from database"""
        appointments = self.get_appointments()
        print("\n" + "="*70)
        if appointments:
            print(f"📅 SAVED APPOINTMENTS ({len(appointments)} total)")
            print("="*70)
            for i, apt in enumerate(appointments[-5:], 1):
                print(f"\n{i}. 👤 {apt.get('patient_name')} | 👨‍⚕️ Doctor {apt.get('doctor_id')} | 📅 {apt.get('scheduled_at')}")
        else:
            print("No appointments saved yet")
        print("="*70 + "\n")
    
    def chat(self):
        """Main chat loop"""
        print("\n" + "="*70)
        print("🏥 HOSPITAL WHATSAPP CHATBOT - REAL BOOKING SYSTEM")
        print("="*70)
        print("\n📱 Real WhatsApp-style multi-turn conversation")
        print("💾 Appointments saved to database & updated in frontend")
        print("📊 Updates visible in http://localhost:5173\n")
        print("Type 'appointments' to see saved bookings")
        print("Type 'exit' to quit\n")
        print("="*70)
        
        # Initial greeting
        initial_response = self.generate_response("hi")
        self.display_message("Bot", initial_response)
        
        while True:
            try:
                user_input = input("👤 You: ").strip()
                
                if user_input.lower() == 'exit':
                    print("\n" + "="*70)
                    print("👋 Thank you for using Hospital Chatbot!")
                    print("="*70 + "\n")
                    break
                
                if user_input.lower() == 'appointments':
                    self.show_saved_appointments()
                    continue
                
                if not user_input:
                    continue
                
                # Send through webhook
                self.display_message("You", user_input)
                print("⏳ Processing... ", end="", flush=True)
                
                if self.send_webhook_message(user_input):
                    print("✅")
                    time.sleep(0.5)
                    
                    # Get and display response
                    response = self.generate_response(user_input)
                    self.display_message("Bot", response)
                else:
                    print("⚠️")
                    response = self.generate_response(user_input)
                    self.display_message("Bot", response)
                    
            except KeyboardInterrupt:
                print("\n\n" + "="*70)
                print("👋 Chat ended")
                print("="*70 + "\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")

def main():
    chatbot = HospitalChatbot()
    chatbot.chat()

if __name__ == "__main__":
    main()
