#!/usr/bin/env python3
"""
WhatsApp Chat Simulator - Real-time Chat with Chatbot Responses
Simulates real WhatsApp interactions with booking confirmations
"""

import requests
from datetime import datetime
import time

# Configuration
WEBHOOK_URL = "http://localhost:5679/webhook/whatsapp"
API_BASE_URL = "http://localhost:5000/api"
TEST_PHONE = "919010444486"
TEST_RECIPIENT = "827223013816682"

class ChatSimulator:
    def __init__(self):
        self.token = None
        self.login()
    
    def login(self):
        """Login to backend API"""
        try:
            response = requests.post(f"{API_BASE_URL}/auth/login", json={
                "username": "rohith",
                "password": "password123"
            })
            if response.status_code == 200:
                self.token = response.json().get('access_token')
                print("✅ Connected to Hospital System\n")
            else:
                print("⚠️ Warning: Could not connect to backend\n")
        except Exception as e:
            print(f"⚠️ Warning: {e}\n")
    
    def send_webhook_message(self, message_text):
        """Send message through webhook and get chatbot response"""
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
            response = requests.post(WEBHOOK_URL, json=payload, timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def get_chatbot_response(self, user_message):
        """Generate chatbot response based on message"""
        msg_lower = user_message.lower()
        
        # Greeting responses
        if any(word in msg_lower for word in ['hi', 'hello', 'hey', 'hii', 'greetings']):
            return "Hi there! 👋 Welcome to Hospital Management System. How can I help you today?\n\nYou can:\n• Book an appointment\n• Check doctors list\n• Get appointment status"
        
        # Doctor inquiry
        if any(word in msg_lower for word in ['doctor', 'doctors', 'specialist', 'cardiologist', 'pediatrician', 'dermatologist']):
            return "👨‍⚕️ Available Doctors:\n\n🔹 Dr. John Smith - Cardiologist (ID: 1)\n🔹 Dr. Sarah Johnson - Pediatrician (ID: 2)\n🔹 Dr. Mike Davis - Dermatologist (ID: 3)\n\nWould you like to book an appointment with any of them?"
        
        # Appointment booking
        if any(word in msg_lower for word in ['book', 'appointment', 'schedule', 'slot']):
            return "📅 Appointment Booking\n\nPlease provide:\n1. Doctor ID (1, 2, or 3)\n2. Date (YYYY-MM-DD)\n3. Time (HH:MM)\n\nExample: 'Book appointment with doctor 1 on 2025-11-30 at 10:00'"
        
        # Process booking request
        if any(word in msg_lower for word in ['2025-11', '2025-12', 'appointment with doctor']):
            return "✅ Appointment Confirmed!\n\n📋 Booking Details:\n• Doctor ID: 1\n• Date: 2025-11-30\n• Time: 10:00 AM\n• Status: CONFIRMED\n\nYour appointment has been saved. You'll receive a reminder 24 hours before."
        
        # Status check
        if any(word in msg_lower for word in ['status', 'check', 'confirm', 'appointment status']):
            return "📊 Your Appointment Status:\n\n✅ CONFIRMED\n• Date: 2025-11-29\n• Doctor: Dr. Smith\n• Time: 10:00 AM\n• Location: Room 201"
        
        # Default response
        return "I understand. 🤔 How else can I help you?\n\nTry saying:\n• 'Book appointment'\n• 'Show doctors'\n• 'Check status'"
    
    def get_appointments(self):
        """Fetch all appointments from database"""
        try:
            headers = {}
            if self.token:
                headers['Authorization'] = f'Bearer {self.token}'
            response = requests.get(f"{API_BASE_URL}/appointments", headers=headers)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception:
            return []
    
    def get_doctors(self):
        """Fetch all doctors from database"""
        try:
            headers = {}
            if self.token:
                headers['Authorization'] = f'Bearer {self.token}'
            response = requests.get(f"{API_BASE_URL}/doctors", headers=headers)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception:
            return []
    
    def display_chat_bubble(self, sender, message):
        """Display message in WhatsApp-like format"""
        timestamp = datetime.now().strftime("%H:%M")
        
        if sender == "You":
            print(f"\n{'':>40}👤 You")
            for line in message.split('\n'):
                print(f"{'':>35}{line}")
            print(f"{'':>38}{timestamp}")
        else:
            print("\n🤖 Chatbot")
            for line in message.split('\n'):
                print(f"{line}")
            print(f"{timestamp}\n")
    
    def display_appointments(self):
        """Show saved appointments from database"""
        appointments = self.get_appointments()
        if appointments:
            print("\n" + "="*70)
            print(f"📅 SAVED APPOINTMENTS ({len(appointments)} total)")
            print("="*70)
            for i, apt in enumerate(appointments[-5:], 1):
                print(f"\n{i}. Patient: {apt.get('patient_name', 'N/A')}")
                print(f"   Phone: {apt.get('patient_phone', 'N/A')}")
                print(f"   Doctor ID: {apt.get('doctor_id', 'N/A')}")
                print(f"   Date/Time: {apt.get('scheduled_at', 'N/A')}")
                print(f"   Status: {apt.get('status', 'N/A')}")
        else:
            print("\n❌ No appointments saved yet\n")
    
    def display_doctors(self):
        """Show available doctors from database"""
        doctors = self.get_doctors()
        if doctors:
            print("\n" + "="*70)
            print("👨‍⚕️ AVAILABLE DOCTORS")
            print("="*70)
            for doc in doctors:
                print(f"\nID: {doc.get('id')} | {doc.get('name')}")
                print(f"Specialization: {doc.get('specialization', 'N/A')}")
                print(f"Branch: {doc.get('branch_id', 'N/A')}")
        else:
            print("\n❌ No doctors found\n")
    
    def chat(self):
        """Interactive real-time chat"""
        print("\n" + "="*70)
        print("🏥 HOSPITAL WHATSAPP CHATBOT - REAL-TIME CHAT")
        print("="*70)
        print("\n📱 Chat Interface (like WhatsApp):")
        print("   • Type messages and get instant responses")
        print("   • Type 'doctors' to see available doctors")
        print("   • Type 'appointments' to see booked appointments")
        print("   • Type 'exit' to quit")
        print("\n" + "="*70 + "\n")
        
        while True:
            try:
                user_input = input("👤 You: ").strip()
                
                if user_input.lower() == 'exit':
                    print("\n" + "="*70)
                    print("👋 Chat ended. Thank you!")
                    print("="*70 + "\n")
                    break
                
                if user_input.lower() == 'doctors':
                    self.display_doctors()
                    continue
                
                if user_input.lower() == 'appointments':
                    self.display_appointments()
                    continue
                
                if not user_input:
                    continue
                
                # Send message through webhook
                self.display_chat_bubble("You", user_input)
                print("⏳ Processing... ", end="", flush=True)
                
                if self.send_webhook_message(user_input):
                    print("✅")
                    time.sleep(1)
                    
                    # Get and display chatbot response
                    response = self.get_chatbot_response(user_input)
                    self.display_chat_bubble("Chatbot", response)
                else:
                    print("❌")
                    print("\n❌ Error: Webhook server not responding")
                    print("   Make sure to run: python whatsapp_webhook_server.py\n")
                    
            except KeyboardInterrupt:
                print("\n\n" + "="*70)
                print("👋 Chat ended by user")
                print("="*70 + "\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")

def main():
    simulator = ChatSimulator()
    simulator.chat()

if __name__ == "__main__":
    main()
