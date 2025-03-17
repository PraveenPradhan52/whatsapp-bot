from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Environment Variables for Security
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

app = Flask(__name__)

# Verify Webhook Endpoint
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Verification failed", 403

# Handle Incoming Messages
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    # Check if 'messages' exist in the payload
    try:
        if 'messages' in data['entry'][0]['changes'][0]['value']:
            messages = data['entry'][0]['changes'][0]['value']['messages']
            for msg in messages:
                sender_id = msg['from']
                text = msg['text']['body'].strip().lower()

                # Command-Based Responses
                if text in ["hello", "hi"]:
                    send_whatsapp_message(sender_id, "👋 Hello! How can I assist you today?")
                elif text == "info":
                    send_whatsapp_message(sender_id, "ℹ️ We provide AI solutions and automation tools.")
                elif text == "image":
                    send_whatsapp_image(sender_id, "https://example.com/sample-image.jpg")
                elif text == "button":
                    send_whatsapp_button(sender_id)
                else:
                    send_whatsapp_message(sender_id, "❓ I'm not sure what you mean. Try 'hello' or 'info'.")
    except Exception as e:
        print(f"Error processing webhook data: {e}")

    return "EVENT_RECEIVED", 200

# Function to Send a Text Message
def send_whatsapp_message(recipient_id, message):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "text": {"body": message}
    }
    requests.post(url, json=data, headers=headers)

# Function to Send an Image
def send_whatsapp_image(recipient_id, image_url):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "type": "image",
        "image": {"link": image_url}
    }
    requests.post(url, json=data, headers=headers)

# Function to Send a Button-Based Message
def send_whatsapp_button(recipient_id):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": "Choose an option:"},
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": "option_1", "title": "📄 Learn More"}},
                    {"type": "reply", "reply": {"id": "option_2", "title": "💬 Contact Support"}}
            ]
        }
    }
}
