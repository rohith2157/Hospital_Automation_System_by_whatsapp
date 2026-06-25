"""
Rule-Based Chatbot Engine for Hospital WhatsApp System
No AI API required - uses pattern matching and state machine
100% FREE - No OpenAI, No Twilio!
"""

import re
from datetime import datetime, timedelta
from typing import Dict, Optional, List


# Database helper functions (will be set by webhook server)
db_save_appointment = None
db_get_or_create_patient = None
db_get_doctors = None  # New: Get doctors from database


def set_db_functions(save_appointment_func, get_or_create_patient_func, get_doctors_func=None):
    """Set database functions from the Flask app context"""
    global db_save_appointment, db_get_or_create_patient, db_get_doctors
    db_save_appointment = save_appointment_func
    db_get_or_create_patient = get_or_create_patient_func
    db_get_doctors = get_doctors_func


class ChatbotEngine:
    """
    Rule-based chatbot using:
    - Intent detection via keyword matching
    - State machine for conversation flow
    - Entity extraction with regex
    """
    
    # Intent patterns
    INTENT_PATTERNS = {
        'appointment_booking': [
            r'\b(book|appointment|schedule|meet|visit|consultation)\b',
            r'\b(doctor|dr|physician)\b',
            r'\b(want to see|need to see)\b'
        ],
        'appointment_reschedule': [
            r'\b(reschedule|change|modify|postpone|shift)\b',
            r'\b(different time|another date)\b'
        ],
        'appointment_cancel': [
            r'\b(cancel|delete|remove)\b.*\b(appointment)\b',
            r'\bdon\'?t want\b'
        ],
        'appointment_status': [
            r'\b(check|status|when|what time)\b.*\b(appointment)\b',
            r'\b(my appointment|appointment status)\b'
        ],
        'feedback': [
            r'\b(feedback|review|rating|complaint|compliment)\b',
            r'\b(experience|service|treatment)\b'
        ],
        'greeting': [
            r'\b(hi|hello|hey|good morning|good afternoon|good evening)\b',
            r'\b(start|begin)\b'
        ],
        'help': [
            r'\b(help|assist|support|guide)\b',
            r'\b(how to|what can)\b'
        ]
    }
    
    def __init__(self):
        self.conversation_context = {}
    
    def detect_intent(self, message: str) -> str:
        """Detect user intent using pattern matching"""
        message_lower = message.lower()
        
        intent_scores = {}
        
        for intent, patterns in self.INTENT_PATTERNS.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    score += 1
            if score > 0:
                intent_scores[intent] = score
        
        if intent_scores:
            return max(intent_scores, key=intent_scores.get)
        
        return 'unknown'
    
    def process_message(self, patient_id: int, message: str, conversation_state: str) -> Dict:
        """
        Main message processor - guides users step-by-step
        Returns: {'response': str, 'new_state': str, 'data': dict}
        """
        message_clean = message.strip()
        intent = self.detect_intent(message_clean)
        
        # Initialize context for this patient
        if patient_id not in self.conversation_context:
            self.conversation_context[patient_id] = {}
        
        context = self.conversation_context[patient_id]
        
        # State machine logic
        if conversation_state == 'new' or intent == 'greeting':
            return self._handle_greeting()
        
        elif intent == 'help':
            return self._handle_help()
        
        elif intent == 'appointment_booking' or conversation_state.startswith('booking_'):
            return self._handle_appointment_booking(message_clean, conversation_state, context)
        
        elif intent == 'appointment_status':
            return self._handle_appointment_status()
        
        elif intent == 'appointment_cancel':
            return self._handle_appointment_cancel()
        
        elif intent == 'feedback' or conversation_state.startswith('feedback_'):
            return self._handle_feedback(message_clean, conversation_state, context)
        
        else:
            return self._handle_unknown()
    
    def _get_doctors_list(self):
        """Get doctors from database or fallback to defaults"""
        if db_get_doctors:
            try:
                doctors = db_get_doctors()
                if doctors:
                    # Ensure consistent format for all doctors
                    formatted_doctors = []
                    for doc in doctors:
                        if isinstance(doc, dict):
                            formatted_doctor = {
                                'id': doc.get('id'),
                                'name': doc.get('name') or f"{doc.get('first_name', '')} {doc.get('last_name', '')}".strip(),
                                'specialization': doc.get('specialization') or doc.get('specialties', 'N/A')
                            }
                        else:
                            # Handle object format
                            formatted_doctor = {
                                'id': getattr(doc, 'id', None),
                                'name': getattr(doc, 'name', f"{getattr(doc, 'first_name', '')} {getattr(doc, 'last_name', '')}".strip()),
                                'specialization': getattr(doc, 'specialization', None) or getattr(doc, 'specialties', 'N/A')
                            }
                        formatted_doctors.append(formatted_doctor)
                    return formatted_doctors
            except Exception as e:
                print(f"Error getting doctors: {e}")
        
        # Fallback default doctors
        return [
            {'id': 1, 'name': 'Dr. John Smith', 'specialization': 'Cardiology'},
            {'id': 2, 'name': 'Dr. Sarah Johnson', 'specialization': 'Pediatrics'},
            {'id': 3, 'name': 'Dr. Michael Brown', 'specialization': 'Orthopedics'}
        ]
    
    def _handle_greeting(self) -> Dict:
        """Welcome message with doctor list from database"""
        doctors = self._get_doctors_list()
        
        # Build doctor list message
        doctor_lines = []
        for i, doc in enumerate(doctors, 1):
            # Handle both dict format from DB and fallback format
            name = doc.get('name') or f"{doc.get('first_name', '')} {doc.get('last_name', '')}".strip()
            spec = doc.get('specialization') or doc.get('specialties', 'N/A')
            doctor_lines.append(f"{i}. {name} ({spec})")
        
        doctor_list = "\n".join(doctor_lines)
        total_doctors = len(doctors)
        
        response = f"""Hi! Welcome to Hospital Appointment Booking 👋

📋 Available Doctors ({total_doctors} in total):
{doctor_list}

Please type the doctor's number (1 to {total_doctors})"""
        
        return {
            'response': response,
            'new_state': 'booking_doctor',
            'data': {'doctors': doctors}
        }
    
    def _handle_help(self) -> Dict:
        """Help menu"""
        response = """ℹ️ *Help Menu*

I can assist you with:

✅ *Book Appointment:* Say "book appointment"
✅ *Check Status:* Say "my appointment status"
✅ *Cancel:* Say "cancel my appointment"
✅ *Feedback:* Say "give feedback"

What would you like to do?"""
        
        return {
            'response': response,
            'new_state': 'menu',
            'data': {}
        }
    
    def _handle_appointment_booking(self, message: str, state: str, context: Dict) -> Dict:
        """Multi-step appointment booking flow"""
        
        # STEP 1: Select Doctor
        if state == 'booking_doctor':
            # Get doctors from database
            doctors = context.get('doctors') or self._get_doctors_list()
            
            message_lower = message.lower().strip()
            selected_doctor = None
            selected_doctor_id = None
            
            # Check if user entered a number
            if message.strip().isdigit():
                idx = int(message.strip()) - 1
                if 0 <= idx < len(doctors):
                    selected_doctor = doctors[idx]['name']
                    selected_doctor_id = doctors[idx]['id']
            else:
                # Check if user entered doctor name
                for doc in doctors:
                    doc_name_lower = doc['name'].lower()
                    if any(part in message_lower for part in doc_name_lower.split()):
                        selected_doctor = doc['name']
                        selected_doctor_id = doc['id']
                        break
            
            if not selected_doctor:
                doctor_nums = ", ".join([str(i+1) for i in range(len(doctors))])
                return {
                    'response': f'❌ Please select a valid doctor ({doctor_nums})',
                    'new_state': 'booking_doctor',
                    'data': context
                }
            
            context['doctor'] = selected_doctor
            context['doctor_id'] = selected_doctor_id
            
            response = f"""Great! You selected {selected_doctor} ✅

What date do you prefer?

Please enter in format: YYYY-MM-DD
Example: 2025-11-28"""
            
            return {
                'response': response,
                'new_state': 'booking_date',
                'data': context
            }
        
        # STEP 2: Select Date
        elif state == 'booking_date':
            date_pattern = r'^\d{4}-\d{2}-\d{2}$'
            
            if not re.match(date_pattern, message.strip()):
                return {
                    'response': '❌ Invalid format!\n\nPlease enter date as: YYYY-MM-DD\nExample: 2025-11-28',
                    'new_state': 'booking_date',
                    'data': context
                }
            
            context['date'] = message.strip()
            
            response = """Perfect! 📅

⏰ Available time slots:
• 10:00 AM
• 11:00 AM
• 2:00 PM
• 3:00 PM
• 4:00 PM
• 5:00 PM

Please type time like: 3:00 PM"""
            
            return {
                'response': response,
                'new_state': 'booking_time',
                'data': context
            }
        
        # STEP 3: Select Time
        elif state == 'booking_time':
            message_clean = message.strip().upper()
            
            valid_times = ['10:00 AM', '11:00 AM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM']
            
            time_found = None
            for valid_time in valid_times:
                if valid_time in message_clean or valid_time.replace(' ', '') in message_clean.replace(' ', ''):
                    time_found = valid_time
                    break
            
            if not time_found:
                return {
                    'response': '❌ Please select a valid time:\n• 10:00 AM\n• 11:00 AM\n• 2:00 PM\n• 3:00 PM\n• 4:00 PM\n• 5:00 PM',
                    'new_state': 'booking_time',
                    'data': context
                }
            
            context['time'] = time_found
            
            response = """Almost done! 🎉

Please provide your full name:"""
            
            return {
                'response': response,
                'new_state': 'booking_name',
                'data': context
            }
        
        # STEP 4: Get Name & Confirm
        elif state == 'booking_name':
            patient_name = message.strip()
            
            if len(patient_name) < 2:
                return {
                    'response': '❌ Please provide a valid name (at least 2 characters)',
                    'new_state': 'booking_name',
                    'data': context
                }
            
            context['patient_name'] = patient_name
            
            # Save appointment to database
            appointment_id = None
            phone = context.get('phone', '')
            print(f"📞 Saving appointment for phone: {phone}")
            print(f"📋 Context: {context}")
            print(f"🔗 DB Function available: {db_save_appointment is not None}")
            
            if db_save_appointment:
                try:
                    # Convert time to 24-hour format
                    time_str = context.get('time', '10:00 AM')
                    time_obj = datetime.strptime(time_str, '%I:%M %p')
                    time_24h = time_obj.strftime('%H:%M')
                    
                    scheduled_at = f"{context.get('date')}T{time_24h}:00"
                    
                    # Get doctor ID from context (set during doctor selection)
                    doctor_id = context.get('doctor_id', 1)
                    
                    print("💾 Calling db_save_appointment with:")
                    print(f"   Name: {patient_name}")
                    print(f"   Phone: {phone}")
                    print(f"   Doctor ID: {doctor_id}")
                    print(f"   Scheduled: {scheduled_at}")
                    
                    appointment_id = db_save_appointment(
                        patient_name=patient_name,
                        patient_phone=phone,
                        doctor_id=doctor_id,
                        scheduled_at=scheduled_at,
                        source='whatsapp'
                    )
                    print(f"✅ Appointment saved to DB with ID: {appointment_id}")
                except Exception as e:
                    print(f"❌ Error saving appointment to DB: {e}")
                    import traceback
                    traceback.print_exc()
                    appointment_id = datetime.now().strftime('%Y%m%d%H%M%S')[-6:]
            else:
                # Fallback: generate fake ID if DB not connected
                print("⚠️ db_save_appointment is None - using fake ID")
                appointment_id = datetime.now().strftime('%Y%m%d%H%M%S')[-6:]
            
            # Create confirmation message
            if appointment_id and isinstance(appointment_id, int):
                status_msg = "✅ CONFIRMED & SAVED TO SYSTEM"
            else:
                status_msg = "⚠️ Booking received (offline mode)"
            
            response = f"""✅ *Appointment Booked Successfully!*

{status_msg}

👤 Patient: {context.get('patient_name')}
👨‍⚕️ Doctor: {context.get('doctor')}
📅 Date: {context.get('date')}
🕐 Time: {context.get('time')}
🔖 Appointment ID: #{appointment_id}

You will receive reminders before your appointment.

💡 Commands:
• Type 'reschedule' to change
• Type 'cancel' to cancel
• Type 'hi' for new booking"""
            
            return {
                'response': response,
                'new_state': 'menu',
                'data': context,
                'booking_confirmed': True,
                'appointment_id': appointment_id
            }
        
        return self._handle_unknown()
    
    def _handle_appointment_status(self) -> Dict:
        """Check appointment status"""
        response = """🔍 *Checking Appointments...*

Please provide your appointment ID or phone number to check status."""
        
        return {
            'response': response,
            'new_state': 'status_check',
            'data': {}
        }
    
    def _handle_appointment_cancel(self) -> Dict:
        """Cancel appointment"""
        response = """❌ *Cancel Appointment*

Please provide your appointment ID to cancel.
Example: #123456"""
        
        return {
            'response': response,
            'new_state': 'cancel_appointment',
            'data': {}
        }
    
    def _handle_feedback(self, message: str, state: str, context: Dict) -> Dict:
        """Handle feedback collection"""
        
        if 'feedback' not in state:
            response = """⭐ *Feedback*

Please rate your visit (1-5):
1 ⭐ = Poor
2 ⭐⭐ = Fair
3 ⭐⭐⭐ = Good
4 ⭐⭐⭐⭐ = Very Good
5 ⭐⭐⭐⭐⭐ = Excellent

Just type the number (1-5)"""
            
            return {
                'response': response,
                'new_state': 'feedback_rating',
                'data': {}
            }
        
        elif state == 'feedback_rating':
            try:
                rating = int(message.strip())
                if 1 <= rating <= 5:
                    context['rating'] = rating
                    stars = '⭐' * rating
                    
                    response = f"""Thank you for the {rating}-star rating! {stars}

Would you like to add comments? (Optional)

Type your comments or SKIP to finish."""
                    
                    return {
                        'response': response,
                        'new_state': 'feedback_comments',
                        'data': context
                    }
                else:
                    return {
                        'response': '❌ Please rate between 1-5',
                        'new_state': 'feedback_rating',
                        'data': context
                    }
            except ValueError:
                return {
                    'response': '❌ Please enter a number between 1-5',
                    'new_state': 'feedback_rating',
                    'data': context
                }
        
        elif state == 'feedback_comments':
            if message.lower().strip() != 'skip':
                context['comments'] = message
            
            response = f"""✅ *Feedback Submitted!*

Rating: {'⭐' * context.get('rating', 0)}
{f"Comments: {context.get('comments', '')}" if context.get('comments') else ''}

Thank you! 🙏

Type 'hi' to start over."""
            
            return {
                'response': response,
                'new_state': 'menu',
                'data': context,
                'feedback_submitted': True
            }
        
        return self._handle_unknown()
    
    def _handle_unknown(self) -> Dict:
        """Handle unknown inputs"""
        response = """❓ I didn't understand that.

I can help you with:
📅 *Book* - Book an appointment
🔍 *Status* - Check appointment status
⭐ *Feedback* - Give feedback

What would you like to do?"""
        
        return {
            'response': response,
            'new_state': 'menu',
            'data': {}
        }


# Global chatbot instance
chatbot = ChatbotEngine()
