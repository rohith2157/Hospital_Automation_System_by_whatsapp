from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import requests

webhooks_bp = Blueprint('webhooks', __name__)

# ===========================================
# TWILIO WHATSAPP API
# ===========================================

def send_whatsapp_message(phone_number, message):
    """
    Send WhatsApp message using Twilio WhatsApp API
    """
    account_sid = current_app.config.get('TWILIO_ACCOUNT_SID')
    auth_token = current_app.config.get('TWILIO_AUTH_TOKEN')
    twilio_number = current_app.config.get('TWILIO_WHATSAPP_NUMBER')
    
    if not account_sid or not auth_token or not twilio_number:
        print("⚠️ Twilio credentials not configured. Message logged only.")
        return None
    
    # Clean phone number (ensure country code, add whatsapp: prefix)
    clean_phone = phone_number.replace("whatsapp:", "").replace("+", "").strip()
    if not clean_phone.startswith("91"):
        clean_phone = f"91{clean_phone}"
    
    to_number = f"whatsapp:+{clean_phone}"
    
    try:
        client = Client(account_sid, auth_token)
        
        message_obj = client.messages.create(
            body=message,
            from_=twilio_number,
            to=to_number
        )
        
        print(f"✅ Twilio WhatsApp message sent! SID: {message_obj.sid}")
        return {"id": message_obj.sid}
    except Exception as e:
        print(f"❌ Error sending Twilio WhatsApp message: {e}")
        return None


@webhooks_bp.route('/webhooks/twilio', methods=['POST'])
def twilio_webhook():
    """
    Handle incoming WhatsApp messages from Twilio
    """
    try:
        # Twilio sends form data (application/x-www-form-urlencoded)
        from_number = request.form.get('From', '')
        incoming_msg = request.form.get('Body', '')
        
        # Strip "whatsapp:" prefix for our chatbot logic
        clean_from_number = from_number.replace('whatsapp:', '').replace('+', '')
        
        print("\n" + "="*60)
        print("📩 Incoming WhatsApp Message (Twilio API):")
        print(f"From: {clean_from_number}")
        print(f"Message: {incoming_msg}")
        print(f"Timestamp: {datetime.now()}")
        print("="*60 + "\n")
        
        # Process message through chatbot
        from app.utils.chatbot import ChatbotLogic
        response_text = ChatbotLogic.handle_chat(incoming_msg, clean_from_number)
        
        print(f"✅ Replying to {clean_from_number}: {response_text[:50]}...\n")
        
        # Explicitly send the message using our Twilio client function
        send_whatsapp_message(clean_from_number, response_text)
        
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        print(f"❌ Error processing Twilio webhook: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ===========================================
# API ENDPOINT FOR n8n INTEGRATION
# ===========================================

@webhooks_bp.route('/api/chatbot/message', methods=['POST'])
def chatbot_message():
    """
    API endpoint for n8n to send messages and get chatbot responses
    This is called by n8n HTTP Request node
    """
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        phone = data.get('phone', 'unknown')
        
        print("\n" + "="*60)
        print("🤖 Chatbot API Request (from n8n):")
        print(f"Phone: {phone}")
        print(f"Message: {message}")
        print("="*60 + "\n")
        
        # Process message through chatbot
        from app.utils.chatbot import ChatbotLogic
        response = ChatbotLogic.handle_chat(message, phone)
        
        print(f"💬 Chatbot Response: {response[:100]}...")
        
        return jsonify({
            'status': 'success',
            'response': response,
            'phone': phone,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        print(f"❌ Error in chatbot API: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@webhooks_bp.route('/webhooks/send-whatsapp', methods=['POST'])
def send_whatsapp():
    """Send WhatsApp message via Meta WhatsApp Business Cloud API (FREE!)"""
    data = request.get_json() or {}
    phone = data.get('phone')
    message = data.get('message')
    
    # Validate input
    if not phone or not message:
        return jsonify({'status': 'error', 'message': 'Phone and message are required'}), 400
    
    # Send via Twilio API
    result = send_whatsapp_message(phone, message)
    
    if result:
        print("\n" + "="*60)
        print("📱 WhatsApp Message Sent (Twilio API):")
        print(f"To: {phone}")
        print(f"Message: {message}")
        print(f"Message ID: {result.get('id')}")
        print(f"Timestamp: {datetime.now()}")
        print("="*60 + "\n")
        
        return jsonify({
            'status': 'success',
            'message': 'WhatsApp message sent via Twilio API',
            'phone': phone,
            'message_id': result.get('id'),
            'timestamp': datetime.now().isoformat()
        }), 200
    else:
        # Fallback: Log only (for testing without WhatsApp credentials)
        print("\n" + "="*60)
        print("📱 WhatsApp Message (TEST MODE - No Meta credentials):")
        print(f"To: {phone}")
        print(f"Message: {message}")
        print(f"Timestamp: {datetime.now()}")
        print("="*60 + "\n")
        
        return jsonify({
            'status': 'success',
            'message': 'WhatsApp message logged (TEST MODE)',
            'phone': phone,
            'timestamp': datetime.now().isoformat()
        }), 200
