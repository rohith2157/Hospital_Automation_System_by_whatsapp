#!/usr/bin/env python3
"""
Hospital WhatsApp Chatbot Terminal - Uses Real Chatbot Engine
Multi-turn conversation with database persistence and real-time updates
"""

import sys
import os
import requests
from datetime import datetime
import time

# Add API path for imports
api_path = os.path.join(os.path.dirname(__file__))
if api_path not in sys.path:
    sys.path.insert(0, api_path)
WEBHOOK_URL = "http://localhost:5679/webhook/whatsapp"
API_BASE_URL = "http://localhost:5000/api"
TEST_PHONE = "919010444486"
TEST_RECIPIENT = "827223013816682"

# Import chatbot engine
try:
    from app.utils.chatbot_engine import ChatbotEngine, set_db_functions
except ImportError as e:
    print(f"Error importing chatbot engine: {e}")
    print("Make sure to run this from the Api directory")
    sys.exit(1)


class TerminalHospitalChatbot:
    def __init__(self):
        self.token = None
        self.chatbot = ChatbotEngine()
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
        """Display saved appointments from database with delete option"""
        appointments = self.get_appointments()
        print("\n" + "="*70)
        if appointments:
            print(f"📅 SAVED APPOINTMENTS ({len(appointments)} total)")
            print("="*70)
            for i, apt in enumerate(appointments[-5:], 1):
                apt_id = apt.get('id')
                print(f"\n{i}. 👤 {apt.get('patient_name')} | 👨‍⚕️ Doctor {apt.get('doctor_id')} | 📅 {apt.get('scheduled_at')}")
                print(f"   ID: {apt_id} | Type 'delete {apt_id}' to cancel")
        else:
            print("No appointments saved yet")
        print("="*70 + "\n")
    
    def chat(self):
        """Main chat loop using real chatbot engine"""
        print("\n" + "="*70)
        print("🏥 HOSPITAL WHATSAPP CHATBOT - REAL CHATBOT ENGINE")
        print("="*70)
        print("\n📱 Using your actual chatbot engine")
        print("💾 All appointments saved to database")
        print("📊 Real-time updates in http://localhost:5173\n")
        print("Type 'appointments' to see saved bookings")
        print("Type 'exit' to quit\n")
        print("="*70)
        
        patient_id = 1  # Test patient ID
        conversation_state = 'new'
        context = {'phone': TEST_PHONE}
        
        # Show initial greeting
        initial_result = self.chatbot.process_message(patient_id, "hi", conversation_state)
        conversation_state = initial_result.get('new_state', 'menu')
        context.update(initial_result.get('data', {}))
        self.display_message("Bot", initial_result.get('response', ''))
        
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
                
                # Get response from chatbot engine
                result = self.chatbot.process_message(patient_id, user_input, conversation_state)
                
                # Update state and context
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
    chatbot = TerminalHospitalChatbot()
    chatbot.chat()

if __name__ == "__main__":
    main()
