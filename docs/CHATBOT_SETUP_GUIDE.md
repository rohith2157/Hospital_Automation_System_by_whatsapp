# 🤖 WhatsApp AI Chatbot - Setup Guide

## ✅ What's Implemented

### 1. **Chatbot Features**
- ✅ Book appointments via WhatsApp
- ✅ Reschedule appointments
- ✅ Cancel appointments  
- ✅ Context memory (multi-turn conversations)
- ✅ Doctor selection from database
- ✅ Date and time slot selection
- ✅ Patient name collection
- ✅ Confirmation messages

### 2. **Database Tables Created**
- ✅ `chat_context` - Store conversation state
- ✅ `opd_feedback` - OPD feedback collection
- ✅ `ipd_feedback` - IPD feedback collection
- ✅ `doctor_leave` - Doctor availability management
- ✅ Added `slot_duration` and `max_patients` to doctors table

### 3. **API Endpoints**
- ✅ `POST /api/webhooks/whatsapp` - Receive WhatsApp messages
- ✅ `POST /api/webhooks/send-whatsapp` - Send WhatsApp messages
- ✅ `POST /api/feedback/opd` - Submit OPD feedback
- ✅ `GET /api/feedback/opd` - Get OPD feedback
- ✅ `POST /api/feedback/ipd` - Submit IPD feedback
- ✅ `GET /api/feedback/ipd` - Get IPD feedback

---

## 📝 Step 1: Setup Database Tables

Run this command to create all required tables:

```powershell
.venv\Scripts\python.exe Api\setup_chatbot_tables.py
```

This will create:
- chat_context table
- opd_feedback table
- ipd_feedback table
- doctor_leave table
- Add slot_duration and max_patients columns to doctors

---

## 📝 Step 2: Configure Twilio Webhook

### A. Get Your Public URL

Since you're running locally, you need to expose your Flask server to the internet using ngrok:

1. **Download ngrok**: https://ngrok.com/download
2. **Run ngrok**:
```powershell
ngrok http 5000
```

3. **Copy the HTTPS URL** (example: `https://1234-abcd-5678.ngrok.io`)

### B. Configure Twilio Webhook

1. Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
2. Find "Sandbox settings"
3. Set "When a message comes in" to:
   ```
   https://YOUR-NGROK-URL/api/webhooks/whatsapp
   ```
   Example: `https://1234-abcd-5678.ngrok.io/api/webhooks/whatsapp`

4. Save settings

---

## 📝 Step 3: Restart Flask Backend

```powershell
.venv\Scripts\python.exe Api\run.py
```

---

## 📝 Step 4: Test Chatbot Flow

### Send message to your Twilio WhatsApp number:

**Test Conversation:**

```
You: book
Bot: Hi! Welcome to Hospital Appointment Booking 👋

📋 Available Doctors:
1. Dr. John Smith (Cardiology)
2. Dr. Sarah Johnson (Pediatrics)
3. Dr. Michael Brown (Orthopedics)

Please type the doctor's name or number.

You: 1
Bot: Great! What date do you prefer?

Please enter in format: YYYY-MM-DD
Example: 2025-11-22

You: 2025-11-22
Bot: Perfect! What time works best for you?

⏰ Available slots:
• 10:00 AM
• 11:00 AM
• 2:00 PM
• 3:00 PM
• 4:00 PM
• 5:00 PM

Please type time like: 3:00 PM

You: 3:00 PM
Bot: Almost done! 👤

Please provide your full name:

You: Rohini
Bot: ✅ Appointment Booked Successfully!

👤 Patient: Rohini
📱 Phone: 9010444486
👨‍⚕ Doctor: Dr. John Smith
📅 Date: 2025-11-22
⏰ Time: 3:00 PM
🎫 Appointment ID: 12

You will receive reminders before your appointment.

💡 Commands:
• Type 'reschedule' to change appointment
• Type 'cancel' to cancel appointment
• Type 'book' for new appointment
```

---

## 🎯 Chatbot Commands

| Command | Description |
|---------|-------------|
| `book` or `hi` | Start booking new appointment |
| `reschedule` | Reschedule existing appointment |
| `cancel` | Cancel appointment |

---

## 🔥 How It Works

### 1. **Incoming Message Flow**
```
WhatsApp Message → Twilio → Your Flask /webhooks/whatsapp endpoint
→ Chatbot Logic → Response → Twilio → WhatsApp
```

### 2. **Context Management**
The chatbot remembers where you are in the conversation using the `chat_context` table:

- `state` - Current conversation step (ASK_DOCTOR, ASK_DATE, etc.)
- `doctor` - Selected doctor
- `date` - Selected date
- `time` - Selected time
- `appt_id` - Appointment ID for reschedule/cancel

### 3. **Appointment Storage**
When booking is complete, appointment is saved to `appointments` table with:
- `patient_name`
- `patient_phone`
- `doctor_id`
- `scheduled_at`
- `status = 'booked'`
- `source = 'whatsapp'`

---

## 📊 Feedback System

### OPD Feedback (After Appointment)

**POST /api/feedback/opd**
```json
{
  "appointment_id": 12,
  "doctor_rating": 5,
  "waiting_time_rating": 4,
  "overall_rating": 5,
  "comments": "Excellent service"
}
```

### IPD Feedback (For Admitted Patients)

**POST /api/feedback/ipd**
```json
{
  "patient_id": 3,
  "room_cleanliness": 5,
  "nursing_care": 5,
  "doctor_visit": 4,
  "food_quality": 3,
  "overall_rating": 4,
  "comments": "Good care overall"
}
```

---

## 🛠️ Troubleshooting

### ❌ "Module 'app.utils.chatbot' not found"
- Restart Flask server

### ❌ "Table 'chat_context' doesn't exist"
- Run: `.venv\Scripts\python.exe Api\setup_chatbot_tables.py`

### ❌ Webhook not receiving messages
- Check ngrok is running
- Verify webhook URL in Twilio console
- Check Flask server logs

### ❌ Bot not responding
- Check Twilio credentials in .env file
- Check Flask terminal for errors
- Verify `TWILIO_WHATSAPP_FROM` number

---

## 🎯 Next Steps (Future Enhancements)

1. **Natural Language Processing (NLP)**
   - Understand "I want to see a heart doctor" → Cardiology
   - Detect dates: "tomorrow", "next Monday"

2. **Smart Slot Management**
   - Show only available slots
   - Prevent double booking
   - Check doctor leave

3. **AI-Powered FAQ**
   - Integrate OpenAI GPT
   - Answer common questions
   - Multi-language support

4. **Feedback Collection via WhatsApp**
   - Auto-send feedback request after appointment
   - Collect ratings via chat

5. **Multi-Branch Support**
   - Ask patient for location
   - Show nearby branches

---

## ✅ Testing Checklist

- [ ] Database tables created
- [ ] Flask backend running
- [ ] ngrok tunnel active
- [ ] Twilio webhook configured
- [ ] Test booking flow works
- [ ] Test reschedule works
- [ ] Test cancel works
- [ ] Appointments saved to database
- [ ] Check appointment appears in frontend

---

## 📞 Support

For issues, check:
1. Flask terminal logs
2. Twilio message logs: https://console.twilio.com/
3. Database records in `chat_context` and `appointments`

**Your WhatsApp chatbot is now ready!** 🎉
