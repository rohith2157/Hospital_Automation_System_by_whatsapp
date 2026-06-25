"""
Interactive WhatsApp Chatbot Simulator
Test your chatbot like you're using WhatsApp
"""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(__file__))

# Import Flask app components
from app.init import create_app
from app.utils.chatbot import ChatbotLogic

app = create_app()

def print_bot_message(message):
    """Print bot message with formatting"""
    print("\n" + "="*60)
    print("🤖 BOT:")
    print("-"*60)
    print(message)
    print("="*60 + "\n")

def print_user_message(message):
    """Print user message"""
    print(f"👤 YOU: {message}\n")

def main():
    print("\n" + "="*60)
    print("📱 WHATSAPP CHATBOT SIMULATOR")
    print("="*60)
    print("\nTest your hospital appointment booking chatbot!")
    print("Type your messages like you would in WhatsApp.")
    print("Type 'exit' or 'quit' to stop.\n")
    print("="*60 + "\n")
    
    # Test phone number
    test_phone = "9876543210"
    
    with app.app_context():
        while True:
            # Get user input
            try:
                user_message = input("👤 YOU: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n\n👋 Goodbye!")
                break
            
            if not user_message:
                continue
            
            if user_message.lower() in ['exit', 'quit', 'bye']:
                print("\n👋 Goodbye!")
                break
            
            # Process through chatbot
            try:
                bot_response = ChatbotLogic.handle_chat(user_message, test_phone)
                print_bot_message(bot_response)
            except Exception as e:
                print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()
