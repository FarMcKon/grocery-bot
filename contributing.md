## Requirements
- Python 3.8+
- See `requirements.txt` for Python dependencies


## Getting Started
 See contributing.md for instructions on how to run the bot.

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

b) cry ? What next here?  


## See Also 
Other readings, especially tool or libraries this uses
- [python-dotenv](https://github.com/theskumar/python-dotenv)