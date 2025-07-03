import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

# App Initialization
load_dotenv()
app = Flask(__name__)

# Sample service providers list
providers = [
    {'id': 1, 'name': 'Cherly', 'category': 'Cleaner', 'rating': 4.2, 'times': ['08:00 AM', '02:30 PM']},
    {'id': 2, 'name': 'Matthew', 'category': 'Web Developer', 'rating': 5.0, 'times': ['09:00 AM', '03:30 PM']},
    {'id': 3, 'name': 'Mandla', 'category': 'Security', 'rating': 3.9, 'times': ['06:00 AM'- '06:00 PM']},  
    {'id': 4, 'name': 'Given', 'category': 'Painter', 'rating': 5.0, 'times': ['07:00 AM', '12:30 PM']},  
    {'id': 5, 'name': 'Luyanda', 'category': 'Electrician', 'rating': 4.1, 'times': ['08:00 AM', '02:00 PM']},  
    {'id': 6, 'name': 'Quinton', 'category': 'Gaderner', 'rating': 5.0, 'times': ['09:00 AM', '03:30 PM']},  
    {'id': 7, 'name': 'Antony', 'category': 'Transporter', 'rating': 2.3, 'times': ['09:00 AM', '09:30 PM']},  
    {'id': 8, 'name': 'Siyabonga', 'category': 'FastFood', 'rating': 4.5, 'times': ['09:00 AM'- '03:30 PM']},  
    {'id': 9, 'name': 'Sophy', 'category': ' Laundry', 'rating': 5.0, 'times': ['09:00 AM', '03:30 PM']},  
    {'id': 10, 'name': 'Ayanda', 'category': 'Carpenter', 'rating': 5.0, 'times': ['09:00 AM', '03:30 PM']}  
]

# Session store
sessions = {}

# Route for incoming WhatsApp messages
@app.route('/whatsapp', methods=['POST'])  # FIXED: slash direction and method name
@app.route('/')
def index():
    return "FixIt WhatsApp Bot is Active."

def whatsapp():
    incoming_msg = request.values.get('Body', '').strip().lower()
    user = request.values.get('From')
    resp = MessagingResponse()
    msg = resp.message()

    # First time user greeting
    if user not in sessions:
        sessions[user] = {'step': 0}
        msg.body('👋Hello! Welcome to FixIt.\nReply with the service you need (e.g., Cleaner, Plumber, Painter)')  # FIXED: typo in FixIt
        return str(resp)  # FIXED: return after greeting

    session = sessions[user]

    # Service category
    if session['step'] == 0:
        category = incoming_msg
        matched = [p for p in providers if p['category'].lower() == category]
        if not matched:
            msg.body(f"Sorry, no providers available for '{category}'. Try something else")
        else:
            session['category'] = category
            session['step'] = 1
            response = f"Available {category}s:\n"
            for p in matched:
                response += f"{p['id']}) {p['name']} - ⭐{p['rating']}\n"
            response += "\nReply with the number to choose"
            msg.body(response)
        return str(resp)  # FIXED: return after handling step 0

    # Provider selection
    elif session['step'] == 1:
        try:
            selected = int(incoming_msg)
        except ValueError:
            msg.body("Please reply with the number of your preferred provider")
            return str(resp)
        provider = next((p for p in providers if p['id'] == selected and p['category'].lower() == session['category']), None)
        if not provider:
            msg.body("Invalid selection. Please reply with the number of your preferred provider.")
        else:
            session['provider'] = provider
            session['step'] = 2
            times = "\n".join(provider['times'])
            msg.body(f"You chose {provider['name']}.\nAvailable times:\n{times}\n\nReply with your preferred time.")  # FIXED: typo 'probider'
        return str(resp)  # FIXED: return after handling step 1

    # Time selection
    elif session['step'] == 2:
        provider = session['provider']  # FIXED: get provider from session
        if incoming_msg not in [t.lower() for t in provider['times']]:
            msg.body("Please reply with one of the available times.")
        else:
            session['time'] = incoming_msg
            session['step'] = 3
            msg.body(f"Booking confirmed with {provider['name']} at {incoming_msg}.\nPlease pay a deposit via Mpesa to 0766 355 966.\nReply 'PAID' after the payment.")
        return str(resp)  # FIXED: return after handling step 2

    # Payment confirmation
    elif session['step'] == 3:
        if incoming_msg == 'paid':  # FIXED: assignment to comparison
            msg.body(f"✅ Payment confirmed! {session['provider']['name']} will meet you at {session['time']}.\nThank you for using FixIt Booking.")
            sessions.pop(user)  # FIXED: pop from sessions, not session
        else:
            msg.body("Awaiting payment confirmation. Reply 'PAID' after completing the deposit.")
        return str(resp)  # FIXED: return after handling step 3

    # Default fallback
    msg.body("Sorry, I didn't understand that. Please try again.")
    return str(resp)

# Server start
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)