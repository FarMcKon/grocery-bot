## Requirements
- Python 3.8+
- See `requirements.txt` for Python dependencies


## Getting Started


### First thing, make sure SMS Sending and reciving via Twilio work: 

### A)  Pull the repo , and make sure that is OK 
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd grocery-bot
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env file with your Twilio credentials (optional for testing)
   ```

3. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### B) Setup SMS outbound gateway (twilio) and makee sure that is OK 
 1. Setup a Twilio account and get your credentials
 2. Set up your environment variables
 3. Run 'Send SMS test' via twilio API 
 4. Celebrate ! You can now talk to phones. 

### C) Setup SMS inbound gateway (twilio + ngrok) and makee sure that is OK 
 1. setup ngrok account 
   (install ngrok to OS if needed)
   (run ngork localhost service in second termial )
   (get public url from ngrok)

   you will need to follow their setup, on thepr page like: https://dashboard.ngrok.com/get-started/setup/macos
   (you will want to run and leave running ngrok in another terminal window)

   After geting ngrok running / installed, get wget for testing 
   ``` brew install wget 
   ```

   2. weget test 
   wget --post-data='<html><body><h1>Hello, World!</h1></body></html>' --header="Content-Type: text/html"  https://f527102ff619.ngrok-free.app/sms/webhook

   mock curl
   ```
   Open code block in new page

curl 'https://api.twilio.com/2010-04-01/Accounts/ACbc2adfaa4027522eefdf0d6389c7b7e2/Messages.json' -X POST \
--data-urlencode 'To=+18777804236' \
--data-urlencode 'MessagingServiceSid=MGb186c5fa0e8e5957e58362ff09f3d2d5' \
--data-urlencode 'Body=Ahoy 👋' \
-u ACbc2adfaa4027522eefdf0d6389c7b7e2:[AuthToken]

```
'''
EnvironHeaders([('Host', 'f527102ff619.ngrok-free.app'), ('User-Agent', 'TwilioProxy/1.1'), ('Content-Length', '465'), ('Accept', '*/*'), ('Content-Type', 'application/x-www-form-urlencoded'), ('I-Twilio-Idempotency-Token', 'a52c8a32-68da-44c9-88bf-ee61bd450376'), ('X-Forwarded-For', '54.158.16.248'), ('X-Forwarded-Host', 'f527102ff619.ngrok-free.app'), ('X-Forwarded-Proto', 'https'), ('X-Home-Region', 'us1'), ('X-Twilio-Signature', 'vpJz5WupAGjlzHeMedSTk593JGE='), ('Accept-Encoding', 'gzip')])

(Pdb) request.content_type
'application/x-www-form-urlencoded'
(Pdb) request.form
ImmutableMultiDict([('ToCountry', 'US'), ('ToState', ''), ('SmsMessageSid', 'SMef812c554489ed70ba2fb0674d7b9277'), ('NumMedia', '0'), ('ToCity', ''), ('FromZip', '19103'), ('SmsSid', 'SMef812c554489ed70ba2fb0674d7b9277'), ('FromState', 'PA'), ('SmsStatus', 'received'), ('FromCity', 'PHILADELPHIA'), ('Body', 'Test 1'), ('FromCountry', 'US'), ('To', '+18889008911'), ('MessagingServiceSid', 'MGb186c5fa0e8e5957e58362ff09f3d2d5'), ('ToZip', ''), ('NumSegments', '1'), ('MessageSid', 'SMef812c554489ed70ba2fb0674d7b9277'), ('AccountSid', 'ACbc2adfaa4027522eefdf0d6389c7b7e2'), ('From', '+12158286822'), ('ApiVersion', '2010-04-01')])

wget --post-data "param1=value1&param2=value2" --header "Content-Type: application/x-www-form-urlencoded" http://example.com/endpoint

wget --post-data='Body=Hello,%20World!' --header="Content-Type: text/x-www-form-urlencoded"  https://f527102ff619.ngrok-free.app/sms/webhook

''''

   See flask endpoint running, showing request body? Good, ngrok & flask are working. 
   Yeah!? Take a sip of coffee, ngrok local workls

   3. set twillio to use our ngrok forwarding
   (go to twillio , do these instruction)

 3. Run 'receive SMS test' 
 4. Celebrate ! Phones can now talk back to you.

### D) Setup db and storeage 

### E) make your grocery list magic ! 



5. **Run the SMS server**
   ```bash
   python main.py
   ```
<!-- 6. **Test SMS functionality** (optional)
   ```bash
   # Test SMS service connection
   python test_sms_main.py connect
   
   # Test sending SMS
   python test_sms_main.py send -p 5551234567 -m "add milk"
   ```
 -->

## Suggested testing as you deploy

a) Test SMS gateway functionaloty
    a.1) set Twilio environment variables in .env file (or by secrets)
    a.2) run SMS test to your twilio 'virtual phone' as 'to phone' target
        `python live_test_sms_main.py send --message "yo #3"  --to_phone "+18777804236`

b) Test receiving and processing incoming SMS messages
   b.1) Use ngrok to expose your local server to the internet
   b.2) Test receive and process incoming SMS messages


## See Also 
Other readings, especially tool or libraries this uses
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [ngrok to expose local server to the internet](https://www.twilio.com/docs/usage/tutorials/how-to-set-up-your-python-and-flask-development-environment#install-ngrok)