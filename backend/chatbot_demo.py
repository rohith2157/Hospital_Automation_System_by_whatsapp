"""
Simple Chatbot Response Simulator
Shows what responses the bot would give
"""

def simulate_conversation():
    print("\n" + "="*70)
    print("🤖 WHATSAPP CHATBOT - CONVERSATION SIMULATOR")
    print("="*70)
    
    conversation = [
        {
            "input": "book",
            "response": """Hi! Welcome to Hospital Appointment Booking 👋

📋 Available Doctors:
1. Dr. John Smith (Cardiology)
2. Dr. Sarah Johnson (Pediatrics)
3. Dr. Michael Brown (Orthopedics)

Please type the doctor's name or number."""
        },
        {
            "input": "1",
            "response": """Great! What date do you prefer?

Please enter in format: YYYY-MM-DD
Example: 2025-11-22"""
        },
        {
            "input": "2025-11-23",
            "response": """Perfect! What time works best for you?

⏰ Available slots:
• 10:00 AM
• 11:00 AM
• 2:00 PM
• 3:00 PM
• 4:00 PM
• 5:00 PM

Please type time like: 3:00 PM"""
        },
        {
            "input": "3:00 PM",
            "response": """Almost done! 👤

Please provide your full name:"""
        },
        {
            "input": "Rohini",
            "response": """✅ Appointment Booked Successfully!

👤 Patient: Rohini
📱 Phone: 9010444486
👨‍⚕️ Doctor: Dr. John Smith
📅 Date: 2025-11-23
⏰ Time: 3:00 PM
🎫 Appointment ID: [AUTO-GENERATED]

You will receive reminders before your appointment.

💡 Commands:
• Type 'reschedule' to change appointment
• Type 'cancel' to cancel appointment
• Type 'book' for new appointment"""
        }
    ]
    
    for step in conversation:
        print(f"\n👤 YOU: {step['input']}")
        print(f"\n🤖 BOT RESPONSE:")
        print(step['response'])
        print("\n" + "-"*70)
    
    print("\n" + "="*70)
    print("✅ BOOKING FLOW COMPLETE!")
    print("="*70)
    
    # Show other commands
    print("\n📝 OTHER AVAILABLE COMMANDS:\n")
    
    print("1️⃣  RESCHEDULE:")
    print("   YOU: reschedule")
    print("   BOT: Please provide your appointment ID to reschedule:")
    print("   YOU: 15")
    print("   BOT: What new date would you like?")
    print("   ... (continues)")
    
    print("\n2️⃣  CANCEL:")
    print("   YOU: cancel")
    print("   BOT: Please provide your appointment ID to cancel:")
    print("   YOU: 15")
    print("   BOT: ❌ Appointment ID 15 has been cancelled.")
    
    print("\n3️⃣  FALLBACK:")
    print("   YOU: help")
    print("   BOT: I can help you with:")
    print("        📅 Book appointment - Type 'book'")
    print("        🔄 Reschedule - Type 'reschedule'")
    print("        ❌ Cancel - Type 'cancel'")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    simulate_conversation()
