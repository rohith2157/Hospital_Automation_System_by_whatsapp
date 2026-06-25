# 🚀 n8n + WhatsApp Business API Setup Guide

## ✅ What Changed: Twilio → WhatsApp Business API

| Before | After |
|--------|-------|
| ❌ Twilio (PAID) | ✅ Meta WhatsApp Business API (FREE!) |
| ❌ OpenAI (PAID) | ✅ Rule-based Chatbot (FREE!) |
| 💸 Monthly costs | 💰 100% FREE |

---

## 📋 Step 1: Get Meta WhatsApp Business API Credentials

### 1.1 Create Meta Developer Account
1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Click "My Apps" → "Create App"
3. Select "Business" → Enter app name
4. Add "WhatsApp" product to your app

### 1.2 Get Your Credentials
From **WhatsApp > API Setup** in your Meta Developer Console:

| Credential | Where to Find |
|------------|---------------|
| **Phone Number ID** | WhatsApp > API Setup > Phone Number ID |
| **Access Token** | WhatsApp > API Setup > Temporary Access Token (or generate permanent) |
| **Verify Token** | You create this (any string like `hospital_verify_123`) |

### 1.3 Add a Phone Number
1. In WhatsApp > API Setup, add a phone number
2. You can use the test number provided by Meta for development

---

## 📋 Step 2: Configure Your Flask API

### 2.1 Set Environment Variables

Create a `.env` file in your `Api` folder:

```env
# WhatsApp Business API (Meta) - FREE!
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id_here
WHATSAPP_ACCESS_TOKEN=your_access_token_here
WHATSAPP_VERIFY_TOKEN=hospital_verify_token
WHATSAPP_BUSINESS_ACCOUNT_ID=your_business_account_id
```

### 2.2 Start Your Flask API

```bash
cd Api
python run.py
```

Your API will be running at `http://localhost:5000`

---

## 📋 Step 3: Set Up n8n Workflow

### 3.1 Open n8n
Go to `http://localhost:5678` (your n8n instance)

### 3.2 Create New Workflow
Click "Add first step..." to start

---

### 🔷 Node 1: WhatsApp Trigger (Receives incoming messages)

1. Click **"+"** → Search "WhatsApp Business Cloud"
2. Select **"On Message Received"** trigger
3. **Configure Credentials:**
   - Click "Create New Credential"
   - **Access Token**: Paste your Meta access token
   - Save

4. **Copy the Webhook URL** shown (you'll need this for Meta)

---

### 🔷 Node 2: HTTP Request (Calls your chatbot API)

1. Click **"+"** after WhatsApp Trigger
2. Search **"HTTP Request"**
3. **Configure:**
   - **Method**: `POST`
   - **URL**: `http://localhost:5000/api/chatbot/message`
   - **Authentication**: None
   - **Send Body**: Yes
   - **Body Content Type**: JSON
   - **Body Parameters**:
     ```
     message: {{ $json.messages[0].text.body }}
     phone: {{ $json.messages[0].from }}
     ```

   Or use **JSON** body:
   ```json
   {
     "message": "{{ $json.messages[0].text.body }}",
     "phone": "{{ $json.messages[0].from }}"
   }
   ```

---

### 🔷 Node 3: WhatsApp Send Message (Sends reply)

1. Click **"+"** after HTTP Request
2. Search **"WhatsApp Business Cloud"**
3. Select **"Send Message"**
4. **Configure:**
   - **Credential**: Same as trigger
   - **Phone Number ID**: Your Meta phone number ID
   - **Recipient Phone Number**: 
     ```
     {{ $('WhatsApp Trigger').item.json.messages[0].from }}
     ```
   - **Message Type**: Text
   - **Text Body**:
     ```
     {{ $json.response }}
     ```

---

### 3.3 Your Final Workflow Should Look Like:

```
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  WhatsApp        │───▶│  HTTP Request    │───▶│  WhatsApp        │
│  Trigger         │    │  POST localhost  │    │  Send Message    │
│  (receive msg)   │    │  :5000/api/...   │    │  (reply)         │
└──────────────────┘    └──────────────────┘    └──────────────────┘
```

---

## 📋 Step 4: Configure Meta Webhook

### 4.1 Go to Meta Developer Console
1. Open [Meta for Developers](https://developers.facebook.com/)
2. Select your app → WhatsApp → Configuration

### 4.2 Configure Webhook
1. **Callback URL**: Paste the n8n webhook URL
   - Example: `https://your-n8n-domain.com/webhook/abc123`
   
2. **Verify Token**: Enter `hospital_verify_token` (or whatever you set)

3. **Webhook Fields**: Subscribe to:
   - ✅ `messages`
   - ✅ `messaging_postbacks` (optional)

### 4.3 For Local Development (Use ngrok)
If running locally, use ngrok to expose your n8n:

```bash
ngrok http 5678
```

Use the ngrok URL for your webhook callback.

---

## 📋 Step 5: Test Your Setup

### 5.1 Activate Workflow
1. In n8n, click the **"Active"** toggle (top right)
2. Click **"Save"**

### 5.2 Send Test Message
1. Open WhatsApp on your phone
2. Send a message to your WhatsApp Business number
3. You should receive an automated response!

### 5.3 Check Logs
- **n8n**: Check "Executions" tab
- **Flask**: Check terminal output

---

## 🔧 Troubleshooting

### "Webhook verification failed"
- Make sure verify tokens match in n8n and Meta console

### "No response from chatbot"
- Ensure Flask API is running: `python run.py`
- Check Flask terminal for errors

### "WhatsApp message not sending"
- Verify your access token is valid
- Check phone number ID is correct
- Ensure recipient phone number format is correct (with country code)

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chatbot/message` | POST | Send message to chatbot, get response |
| `/webhooks/whatsapp` | GET/POST | Meta webhook (verification & messages) |
| `/webhooks/send-whatsapp` | POST | Manually send WhatsApp message |

### Example API Request:
```bash
curl -X POST http://localhost:5000/api/chatbot/message \
  -H "Content-Type: application/json" \
  -d '{"message": "book appointment", "phone": "919876543210"}'
```

---

## 💰 Cost Comparison

| Service | Before | After |
|---------|--------|-------|
| WhatsApp API | Twilio (~$0.05/msg) | Meta (FREE!) |
| AI/Chatbot | OpenAI (~$0.002/msg) | Rule-based (FREE!) |
| **Total** | **~$50-100/month** | **$0/month** |

---

## 🎉 You're Done!

Your Hospital WhatsApp Automation now uses:
- ✅ **Meta WhatsApp Business Cloud API** (FREE!)
- ✅ **n8n** for workflow automation (FREE & Open Source!)
- ✅ **Rule-based chatbot** (No AI costs!)

Happy automating! 🚀
