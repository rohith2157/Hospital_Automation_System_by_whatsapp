#!/usr/bin/env python3
"""
Terminal WhatsApp Chat Simulator
Tests the complete system: webhook → chatbot → database → frontend
"""

import requests
from datetime import datetime

# Configuration
WEBHOOK_URL = "http://localhost:5679/webhook/whatsapp"
API_BASE_URL = "http://localhost:5000/api"
VERIFY_TOKEN = "hospital_verify_token"

# Test phone numbers
TEST_PHONE = "919010444486"  # Your test phone
TEST_RECIPIENT = "827223013816682"  # Phone number ID

class WhatsAppChatSimulator:
    def __init__(self):
        self.phone = TEST_PHONE
        self.recipient_id = TEST_RECIPIENT
        
    def send_message(self, message_text):
        """Simulate sending a WhatsApp message"""
        # Create webhook payload (same format Meta sends)
        payload = {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "id": "ENTRY_ID",
                    "changes": [
                        {
                            "value": {
                                "messaging_product": "whatsapp",
                                "messages": [
                                    {
                                        "from": self.phone,
                                        "id": f"wamid.{datetime.now().timestamp()}",
                                        "timestamp": str(int(datetime.now().timestamp())),
                                        "type": "text",
                                        "text": {
                                            "body": message_text
                                        }
                                    }
                                ],
                                "metadata": {
                                    "display_phone_number": self.recipient_id,
                                    "phone_number_id": self.recipient_id
                                }
                            },
                            "field": "messages"
                        }
                    ]
                }
            ]
        }
        
        try:
            response = requests.post(WEBHOOK_URL, json=payload)
            print(f"\n✅ Message sent: {message_text}")
            print(f"   Status: {response.status_code}")
            if response.status_code != 200:
                print(f"   Response: {response.text}")
            return response
        except requests.exceptions.ConnectionError:
            print(f"\n❌ ERROR: Cannot connect to webhook server at {WEBHOOK_URL}")
            print("   Make sure to run: python whatsapp_webhook_server.py")
            return None
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            return None
    
    def get_appointments(self, token=None):
        """Fetch appointments from backend"""
        try:
            headers = {}
            if token:
                headers['Authorization'] = f'Bearer {token}'
            response = requests.get(f"{API_BASE_URL}/appointments", headers=headers)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception:
            return []
    
    def get_doctors(self, token=None):
        """Fetch doctors from backend"""
        try:
            headers = {}
            if token:
                headers['Authorization'] = f'Bearer {token}'
            response = requests.get(f"{API_BASE_URL}/doctors", headers=headers)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception:
            return []
    
    def display_menu(self):
        """Display interactive menu"""
        print("\n" + "="*60)
        print("🏥 HOSPITAL WHATSAPP CHAT SIMULATOR")
        print("="*60)
        print("\nOptions:")
        print("1. Send greeting message")
        print("2. Ask for doctors list")
        print("3. Book an appointment")
        print("4. Send custom message")
        print("5. View saved appointments (from DB)")
        print("6. View doctors (from DB)")
        print("0. Exit")
        print("-"*60)
        return input("\nChoose option (0-6): ").strip()

def main():
    simulator = WhatsAppChatSimulator()
    
    print("\n🚀 Starting WhatsApp Chat Simulator...")
    print(f"   Webhook URL: {WEBHOOK_URL}")
    print(f"   API URL: {API_BASE_URL}")
    print(f"   Test Phone: +{simulator.phone}")
    
    while True:
        choice = simulator.display_menu()
        
        if choice == "1":
            simulator.send_message("Hi, I need medical help")
            
        elif choice == "2":
            simulator.send_message("Can you tell me the doctors available?")
            
        elif choice == "3":
            simulator.send_message("I want to book an appointment with Dr. Smith on 2025-11-29 at 10:00")
            
        elif choice == "4":
            msg = input("\nEnter your message: ").strip()
            if msg:
                simulator.send_message(msg)
            
        elif choice == "5":
            print("\n📅 Fetching appointments from database...")
            appointments = simulator.get_appointments()
            if appointments:
                print(f"\nFound {len(appointments)} appointments:")
                for apt in appointments:
                    print(f"\n  • ID: {apt.get('id')}")
                    print(f"    Patient: {apt.get('patient_name')}")
                    print(f"    Phone: {apt.get('patient_phone')}")
                    print(f"    Doctor ID: {apt.get('doctor_id')}")
                    print(f"    Date/Time: {apt.get('scheduled_at')}")
                    print(f"    Status: {apt.get('status')}")
            else:
                print("\n❌ No appointments found or DB not connected")
                
        elif choice == "6":
            print("\n👨‍⚕️ Fetching doctors from database...")
            doctors = simulator.get_doctors()
            if doctors:
                print(f"\nFound {len(doctors)} doctors:")
                for doc in doctors:
                    print(f"\n  • ID: {doc.get('id')}")
                    print(f"    Name: {doc.get('name')}")
                    print(f"    Specialization: {doc.get('specialization')}")
                    print(f"    Branch ID: {doc.get('branch_id')}")
            else:
                print("\n❌ No doctors found or DB not connected")
                
        elif choice == "0":
            print("\n👋 Goodbye!")
            break
            
        else:
            print("\n❌ Invalid option. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Chat ended by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
