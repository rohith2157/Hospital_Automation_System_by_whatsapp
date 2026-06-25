"""
WhatsApp Chatbot Test Script
Simulates conversation flow without sending actual WhatsApp messages
"""
from app.utils.chatbot import ChatbotLogic

def test_chatbot():
    print("\n" + "="*60)
    print("🤖 WHATSAPP CHATBOT SIMULATOR")
    print("="*60)
    
    # Test phone number
    phone = "9010444486"
    
    print("\n📱 Testing with phone:", phone)
    print("\nType your messages (or 'quit' to exit)")
    print("-"*60)
    
    while True:
        user_input = input("\n👤 You: ").strip()
        
        if user_input.lower() == 'quit':
            print("\n✅ Test session ended!")
            break
        
        if not user_input:
            continue
        
        # Process through chatbot
        response = ChatbotLogic.handle_chat(user_input, phone)
        
        print(f"\n🤖 Bot:\n{response}")
        print("-"*60)

if __name__ == "__main__":
    test_chatbot()
