"""
WhatsApp Chatbot Context Management
Handles conversation state and memory for multi-turn dialogues
"""
from app.init import db
from datetime import datetime
from sqlalchemy import text

class ChatContext:
    """Manage chatbot conversation context"""
    
    @staticmethod
    def set_context(phone, key, value):
        """Save or update context for a user"""
        try:
            # Delete existing context
            db.session.execute(
                text("DELETE FROM chat_context WHERE phone = :phone AND context_key = :key"),
                {"phone": phone, "key": key}
            )
            
            # Insert new context
            db.session.execute(
                text("INSERT INTO chat_context (phone, context_key, context_value) VALUES (:phone, :key, :value)"),
                {"phone": phone, "key": key, "value": value}
            )
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error setting context: {e}")
            db.session.rollback()
            return False
    
    @staticmethod
    def get_context(phone, key):
        """Retrieve context value for a user"""
        try:
            result = db.session.execute(
                text("SELECT context_value FROM chat_context WHERE phone = :phone AND context_key = :key"),
                {"phone": phone, "key": key}
            ).fetchone()
            
            return result[0] if result else None
        except Exception as e:
            print(f"Error getting context: {e}")
            return None
    
    @staticmethod
    def clear_context(phone):
        """Clear all context for a user (start fresh conversation)"""
        try:
            db.session.execute(
                text("DELETE FROM chat_context WHERE phone = :phone"),
                {"phone": phone}
            )
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error clearing context: {e}")
            db.session.rollback()
            return False
    
    @staticmethod
    def get_all_context(phone):
        """Get all context data for debugging"""
        try:
            results = db.session.execute(
                text("SELECT context_key, context_value FROM chat_context WHERE phone = :phone"),
                {"phone": phone}
            ).fetchall()
            
            return {row[0]: row[1] for row in results}
        except Exception as e:
            print(f"Error getting all context: {e}")
            return {}


class ChatbotLogic:
    """Main chatbot conversation flow"""
    
    @staticmethod
    def handle_chat(msg, phone):
        """Main handler for incoming WhatsApp messages"""
        msg = msg.strip().lower()
        
        # Remove whatsapp: prefix from phone number
        phone = phone.replace("whatsapp:", "").replace("+91", "").strip()
        
        # START BOOKING FLOW
        if "book" in msg or "appointment" in msg or msg == "hi" or msg == "hello":
            ChatContext.clear_context(phone)
            ChatContext.set_context(phone, "state", "ASK_DOCTOR")
            
            # Get available doctors
            from app.models import Doctor
            doctors = Doctor.query.filter_by(is_active=True).all()
            doctor_list = "\n".join([f"{i+1}. Dr. {d.first_name} {d.last_name} ({d.specialties})" 
                                    for i, d in enumerate(doctors)])
            
            return f"Hi! Welcome to Hospital Appointment Booking 👋\n\n📋 Available Doctors:\n{doctor_list}\n\nPlease type the doctor's name or number."
        
        # Get current conversation state
        state = ChatContext.get_context(phone, "state")
        
        # STEP 1: ASK DOCTOR
        if state == "ASK_DOCTOR":
            from app.models import Doctor
            doctor_obj = None
            if msg.isdigit():
                doctors = Doctor.query.filter_by(is_active=True).all()
                if 1 <= int(msg) <= len(doctors):
                    doctor_obj = doctors[int(msg) - 1]
            else:
                doctor_obj = Doctor.query.filter(
                    (Doctor.first_name.ilike(f"%{msg}%")) | 
                    (Doctor.last_name.ilike(f"%{msg}%"))
                ).first()
                
            if not doctor_obj:
                return "❌ Sorry, I couldn't find that doctor. Please check the list and try again (type the number or name)."
            
            # Save doctor selection (save the ID to be safe)
            ChatContext.set_context(phone, "doctor_id", str(doctor_obj.id))
            ChatContext.set_context(phone, "state", "ASK_DATE")
            
            return f"Great! You selected Dr. {doctor_obj.first_name} {doctor_obj.last_name}.\n\nWhat date do you prefer?\nPlease enter in format: YYYY-MM-DD\nExample: 2025-11-22"
        
        # STEP 2: ASK DATE
        if state == "ASK_DATE":
            import re
            from datetime import datetime
            
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", msg):
                return "❌ Invalid date format.\n\nPlease use exactly this format: YYYY-MM-DD\nExample: 2025-11-22"
                
            try:
                # Also check if it's a real calendar date
                parsed_date = datetime.strptime(msg, "%Y-%m-%d")
                if parsed_date.date() < datetime.now().date():
                    return "❌ You cannot book an appointment in the past. Please choose a future date (YYYY-MM-DD)."
            except ValueError:
                return "❌ That date doesn't exist. Please check the month and day (YYYY-MM-DD)."
                
            ChatContext.set_context(phone, "date", msg)
            ChatContext.set_context(phone, "state", "ASK_TIME")
            
            return "Perfect! What time works best for you?\n\n⏰ Available slots:\n• 10:00 AM\n• 11:00 AM\n• 2:00 PM\n• 3:00 PM\n• 4:00 PM\n• 5:00 PM\n\nPlease type time like: 3:00 PM"
        
        # STEP 3: ASK TIME
        if state == "ASK_TIME":
            from datetime import datetime
            date = ChatContext.get_context(phone, "date")
            
            try:
                # Validate if they provided a proper time that we can parse
                datetime.strptime(f"{date} {msg}", "%Y-%m-%d %I:%M %p")
            except ValueError:
                try:
                    datetime.strptime(f"{date} {msg}", "%Y-%m-%d %H:%M")
                except ValueError:
                    return "❌ Invalid time format.\n\nPlease type a time like '3:00 PM' or '15:00'."
                    
            ChatContext.set_context(phone, "time", msg)
            ChatContext.set_context(phone, "state", "ASK_NAME")
            
            return "Almost done! 👤\n\nPlease provide your full name:"
        
        # STEP 4: ASK NAME & CONFIRM
        if state == "ASK_NAME":
            patient_name = msg
            if len(patient_name) < 3:
                return "❌ Name is too short. Please provide your full real name."
                
            doctor_id = ChatContext.get_context(phone, "doctor_id")
            date = ChatContext.get_context(phone, "date")
            time = ChatContext.get_context(phone, "time")
            
            # Save appointment to database
            from app.models import Appointment, Doctor
            from datetime import datetime
            
            doctor_obj = Doctor.query.get(int(doctor_id))
            
            if not doctor_obj:
                ChatContext.clear_context(phone)
                return "Sorry, something went wrong with the doctor selection. Please type 'book' to start again."
            
            # Parse datetime
            try:
                scheduled_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %I:%M %p")
            except:
                scheduled_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            
            # Create appointment
            appointment = Appointment(
                doctor_id=doctor_obj.id,
                patient_name=patient_name,
                patient_phone=phone,
                scheduled_at=scheduled_datetime,
                status='booked',
                source='whatsapp'
            )
            
            db.session.add(appointment)
            db.session.commit()
            
            ChatContext.clear_context(phone)
            
            return f"""✅ Appointment Booked Successfully!

👤 Patient: {patient_name}
📱 Phone: {phone}
👨‍⚕️ Doctor: Dr. {doctor_obj.first_name} {doctor_obj.last_name}
📅 Date: {date}
⏰ Time: {time}
🎫 Appointment ID: {appointment.id}

You will receive reminders before your appointment.

💡 Commands:
• Type 'reschedule' to change appointment
• Type 'cancel' to cancel appointment
• Type 'book' for new appointment"""
        
        # RESCHEDULE FLOW
        if "reschedule" in msg:
            ChatContext.clear_context(phone)
            ChatContext.set_context(phone, "state", "ASK_APPT_ID")
            return "Please provide your appointment ID to reschedule:"
        
        if state == "ASK_APPT_ID":
            ChatContext.set_context(phone, "appt_id", msg)
            ChatContext.set_context(phone, "state", "ASK_NEW_DATE")
            return "What new date would you like?\n\nFormat: YYYY-MM-DD\nExample: 2025-11-22"
        
        if state == "ASK_NEW_DATE":
            import re
            from datetime import datetime
            
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", msg):
                return "❌ Invalid date format.\n\nPlease use exactly this format: YYYY-MM-DD\nExample: 2025-11-22"
            
            try:
                parsed_date = datetime.strptime(msg, "%Y-%m-%d")
                if parsed_date.date() < datetime.now().date():
                    return "❌ You cannot reschedule to the past. Please choose a future date (YYYY-MM-DD)."
            except ValueError:
                return "❌ That date doesn't exist. Please try again (YYYY-MM-DD)."
                
            ChatContext.set_context(phone, "new_date", msg)
            ChatContext.set_context(phone, "state", "ASK_NEW_TIME")
            return "What new time?\n\n⏰ Available slots:\n• 10:00 AM\n• 11:00 AM\n• 2:00 PM\n• 3:00 PM\n• 4:00 PM\n• 5:00 PM"
        
        if state == "ASK_NEW_TIME":
            appt_id = ChatContext.get_context(phone, "appt_id")
            new_date = ChatContext.get_context(phone, "new_date")
            new_time = msg
            
            from app.models import Appointment
            from datetime import datetime
            
            try:
                new_datetime = datetime.strptime(f"{new_date} {new_time}", "%Y-%m-%d %I:%M %p")
            except ValueError:
                try:
                    new_datetime = datetime.strptime(f"{new_date} {new_time}", "%Y-%m-%d %H:%M")
                except ValueError:
                    return "❌ Invalid time format.\n\nPlease type a time like '3:00 PM' or '15:00'."
            
            appointment = Appointment.query.get(appt_id)
            if appointment and appointment.patient_phone == phone:
                appointment.scheduled_at = new_datetime
                db.session.commit()
                
                ChatContext.clear_context(phone)
                
                return f"""✅ Appointment Rescheduled!

🎫 ID: {appt_id}
📅 New Date: {new_date}
⏰ New Time: {new_time}

Type 'book' for new appointment."""
            else:
                ChatContext.clear_context(phone)
                return "Appointment not found or doesn't belong to you."
        
        # CANCEL FLOW
        if "cancel" in msg:
            ChatContext.clear_context(phone)
            ChatContext.set_context(phone, "state", "ASK_CANCEL_ID")
            return "Please provide your appointment ID to cancel:"
        
        if state == "ASK_CANCEL_ID":
            appt_id = msg
            
            from app.models import Appointment
            appointment = Appointment.query.get(appt_id)
            
            if appointment and appointment.patient_phone == phone:
                appointment.status = 'cancelled'
                db.session.commit()
                
                ChatContext.clear_context(phone)
                
                return f"❌ Appointment ID {appt_id} has been cancelled.\n\nType 'book' for new appointment."
            else:
                ChatContext.clear_context(phone)
                return "Appointment not found or doesn't belong to you."
        
        # FALLBACK
        return """I can help you with:

📅 Book appointment - Type 'book'
🔄 Reschedule - Type 'reschedule'
❌ Cancel - Type 'cancel'

How can I assist you today?"""
