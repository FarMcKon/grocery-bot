#!/usr/bin/env python3
"""
SMS Service Module for Grocery Bot
Handles Twilio SMS integration for sending and receiving messages
"""

import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

# for callback / inbound message handling
from flask import Flask, request, redirect


# ============ Endppoints to receive  Twilio callbacks. Flask based ======================

### 
# You need to set-up Twilio to send inbound callback messages to this code.
# To do that, this code is in a global singlton flas app for dev speed / convience. 
# in desktop developer mode, use ngrok to expose this callback endpoint to the internet.
#
# https://www.twilio.com/docs/messaging/tutorials/how-to-receive-and-reply/python#configure-your-webhook-url
#
# https://www.twilio.com/en-us/blog/automating-ngrok-python-twilio-applications-pyngrok
### 


#from pyngrok import ngrok

#running in termial to test 
#g_ngrok_url = None
#g_use_ngrok = True #debuggign only remove from final design
g_app = None

load_dotenv()

# if g_use_ngrok:
#     try: 
#         g_ngrok_url = ngrok.connect(5000).public_url
#         print("ngrok tunnel url: " + g_ngrok_url)
#     except Exception as e:
#         print("ngrok connection failed: " + str(e))

g_app = Flask(__name__)

@g_app.route("/sms/webhook", methods=['GET', 'POST'])
def sms_reply():
    """
    This is the webhook listener for data sent to a SMS to phone. 
    hits twillio,. forwards via ngrok to this code,.  
    """
    ## data is encoded as a url-form  

    """Respond to incoming calls with a simple text message."""
    print("SMS received")
    #import pdb; pdb.set_trace()

    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    print(body)
    
    # Determine the right reply for this message
    resp = MessagingResponse()

    resp.message("<Response></Response>")

    return str(resp)



# TODO :Add to setup docs , that you need this 
# TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
# TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
# TWILIO_PHONE_NUMBER=+1234567890


class TwilioSMSService:
    """
    Dirt simple interface to Twilio Service API
    """

    def __init__(self, do_inbound_server=False, dev_mode=True):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_PHONE_NUMBER')
        self.ngrok_url = os.getenv('NGROK_URL')
        self.dev_mode = dev_mode
        self.inbound_server = None
        self.client = None
        
        if not all([self.account_sid, self.auth_token, self.from_number]):
            print("Warning: Twilio credentials not configured. SMS sending will be disabled.")
            self.client = None
        else:
            self.client = Client(self.account_sid, self.auth_token)

        if do_inbound_server and self.dev_mode:

            # set the SMS webhook
            ph_numbers = self.client.incoming_phone_numbers.list(phone_number=os.getenv('TWILIO_PHONE_NUMBER'))
            if not self.ngrok_url:
                print("Error: ngrok is not configured locally. SMS inbound server will not be started.")
            else:
                for ph_number in ph_numbers:
                    print(f"Setting ngrok tunnnel for {ph_number}")
                    ph_number.update( sms_url=str(self.ngrok_url) + "/sms/webhook" )
                    #ph_nummber.update( voice_url=VOICE_URL)

            print("Connecting g_app to Twilio instance.")
            self.inbound_server = g_app

    def check_inbound_connection(self):
        #this checks if ngrok or other inbound system is working 
        print("Running check_inbound_connection")
        try:
            if self.inbound_server:
            #     for call in self.callback_system.api.account.calls.list(limit=1):
            #         print("Call sid " + call.sid + ": " + str(call.duration) + " seconds.")
                return True
            else:
                print("SMS could not run recive data from API. Credentials bad.")

                return False
        except Exception as e:
            print("SMS could not run receive data from API. Exception:")
            print(e)
            return False
        return False 

    def check_outbound_connection(self):
        """ check connection by listing last call """
        # TODO : should this nuke / reset self.client to fall-back to console debugging ?
        print("Running check_outbound_connection")
        try:
            if self.client:
                for call in self.client.api.account.calls.list(limit=1):
                    print("Call sid " + call.sid + ": " + str(call.duration) + " seconds.")
                return True
            else:
                print("SMS could not run check-call to API. Credentials bad.")
                return False
    
        except Exception as e:
            print("SMS could not run check-call to API. Credentials bad.")
            print(e)
            return False
        return False 
    
    def send_sms(self, to_phone, message):
        """Send SMS message via Twilio"""
        if not self.client:
            print(f"SMS sending disabled. Would send to {to_phone}: {message}")
            return None
        
        try:
            # Ensure phone number has country code
            if not to_phone.startswith('+'):
                to_phone = f"+1{to_phone}"
            
            message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_phone
            )
            
            #print(f"SMS sent successfully. SID: {message.sid}")
            return message.sid
            
        except Exception as e:
            print(f"Error sending SMS to {to_phone}: {e}")
            return None
    
    def create_twiml_response(self, message):
        """Create TwiML response for Twilio webhook"""
        response = MessagingResponse()
        response.message(message)
        return str(response)
    
    def parse_twilio_webhook(self, request_data):
        """Parse incoming Twilio webhook data"""
        return {
            'phone_number': request_data.get('From', '').replace('+1', '').replace('-', '').replace(' ', ''),
            'message_content': request_data.get('Body', '').strip(),
            'message_sid': request_data.get('MessageSid', ''),
            'account_sid': request_data.get('AccountSid', ''),
            'from_city': request_data.get('FromCity', ''),
            'from_state': request_data.get('FromState', ''),
            'from_country': request_data.get('FromCountry', ''),
        }
    
    def validate_twilio_request(self, request_url, post_data, signature):
        """Validate that the request came from Twilio"""
        from twilio.request_validator import RequestValidator
        
        if not self.auth_token:
            return True  # Skip validation if no auth token configured
        
        validator = RequestValidator(self.auth_token)
        return validator.validate(request_url, post_data, signature)

    def run_flask_receiver(self):
       g_app.run(debug=True, port=80) 


# Global singleton SMS service instance
g_sms_service = TwilioSMSService()
