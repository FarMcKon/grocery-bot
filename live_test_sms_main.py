#!/usr/bin/env python3
"""
SMS Service Test Tool for Grocery Bot
Command line tool to test sms_service.py functionality

"""

import sys
import json
from datetime import datetime
from sms_service import TwilioSMSService
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()


@click.group()
def cli():
    """SMS Service Test Tool for Grocery Bot"""
    console.print(Panel.fit("🤖 Grocery Bot SMS Service Tester", style="bold green"))


@cli.command()
def connect():
    connect_inner()


def connect_inner():
    """Builds SMS connector bridge, runs tests."""
    console.print("[bold]Testing SMS Connection[/bold]")
    console.print("-" * 50)

    sms_service = TwilioSMSService(do_inbound_server=True)

    if sms_service:
        console.print(" SMS client created.")
        if sms_service.check_outbound_connection():
            console.print(
                "[green]✓ SMS Outbound service is connected and ready[/green]"
            )
        else:
            console.print("[yellow]⚠ SMS Outbound service not connected[/yellow]")
        if sms_service.check_inbound_connection():
            console.print("[green]✓ SMS Inbound service is connected and ready[/green]")
        else:
            console.print("[yellow]⚠ SMS Inbound service not connected[/yellow]")
    else:  # no client object
        console.print("[yellow]⚠ SMS service not created client [/yellow]")
        console.print("[yellow]⚠ Function Calls will simply print to console[/yellow]")
        console.print("See contributing.md for how to configure credentials")
    return sms_service


@cli.command()
@click.option(
    "--from_phone", "-f", default="+15551234567", help="Phone number receiving message"
)
# @click.option('--message', '-m', required=True, help='Message content to simulate receiving')
# @click.option('--message_sid', '-s', default='test_msg_123', help='Twilio message SID')
def receive_via_flask(from_phone):  # , message, message_sid):
    """Test receiving one SMS message (simulate Twilio webhook)"""
    console.print(f"[bold]Testing SMS Receive[/bold]")
    console.print(f"From (mock?) Phone: {from_phone}")
    #    console.print(f"Message: {message}")
    #    console.print(f"Message SID: {message_sid}")
    console.print("-" * 50)

    # create our SMS connection
    sms_service = connect_inner()

    if sms_service:
        # check flags to make sure we have ngrok ?
        ## Flask runs in the background forever after this call (for now)
        sms_service.run_flask_receiver()

    # Create simulated Twilio webhook data
    mock_webhook_data = {
        "From": "+15558675309",  # fake of phone that sent the message,
        "Body": "Ahoy World!",  # sms message,
    }  # See [1] below for example live data


#     console.print("[blue]Simulated webhook data:[/blue]")
#     console.print(json.dumps(webhook_data, indent=2))
#     console.print("-" * 30)

#     # Parse the webhook data
#     parsed_data = sms_service.parse_twilio_webhook(webhook_data)

#     console.print("[green]Parsed webhook data:[/green]")
#     table = Table(show_header=True, header_style="bold magenta")
#     table.add_column("Field", style="cyan")
#     table.add_column("Value", style="white")

#     for key, value in parsed_data.items():
#         table.add_row(key, str(value))

#     console.print(table)

#     # Generate TwiML response
#     #response_message = f"Received: '{message}' from {parsed_data['phone_number']}"
#     response_message = "Faked response message during dev"
#     twiml_response = sms_service.create_twiml_response(response_message)

#     console.print(f"\n[green]Generated TwiML response:[/green]")
#     console.print(twiml_response)

#     console.print(f"\n[yellow]✓ Successfully simulated receiving SMS message[/yellow]")

# Footnote [1]
# Example data ontained from twilio webhook data, removed for id leakage

@cli.command()
@click.option("--to_phone", "-t", default="5551234567", help="Phone number to send to")
@click.option("--message", "-m", required=True, help="Message to send")
def send(to_phone, message):
    """Test sending SMS message"""
    console.print(f"[bold]Testing SMS Send[/bold]")
    console.print(f"To: {to_phone}")
    console.print(f"Message: {message}")
    console.print("-" * 50)

    # sms_service = TwilioSMSService()
    sms_service = connect_inner()
    result = sms_service.send_sms(to_phone, message)

    if result:
        console.print(f"[green]✓ SMS sent successfully! SID: {result}[/green]")
    else:
        console.print(
            "[yellow]⚠ SMS sending disabled (no credentials) - printed to console[/yellow]"
        )


# @cli.command()
# @click.option('--message', '-m', required=True, help='Response message for TwiML')
# def twiml(message):
#     """Test TwiML response generation"""
#     console.print(f"[bold]Testing TwiML Response Generation[/bold]")
#     console.print(f"Message: {message}")
#     console.print("-" * 50)

#     sms_service = TwilioSMSService()
#     twiml_response = sms_service.create_twiml_response(message)

#     console.print("[green]Generated TwiML:[/green]")
#     console.print(twiml_response)

# @cli.command()
# @click.option('--from-phone', '-f', default='+15551234567', help='From phone number')
# @click.option('--message', '-m', required=True, help='Message content')
# @click.option('--sid', '-s', default='test_message_sid', help='Message SID')
# def parse(from_phone, message, sid):
#     """Test Twilio webhook data parsing"""
#     console.print(f"[bold]Testing Webhook Data Parsing[/bold]")

#     # Create sample Twilio webhook data
#     webhook_data = {
#         'From': from_phone,
#         'Body': message,
#         'MessageSid': sid,
#         'AccountSid': 'test_account_sid',
#         'FromCity': 'San Francisco',
#         'FromState': 'CA',
#         'FromCountry': 'US'
#     }

#     console.print("[blue]Input webhook data:[/blue]")
#     console.print(json.dumps(webhook_data, indent=2))
#     console.print("-" * 50)

#     sms_service = TwilioSMSService()
#     parsed_data = sms_service.parse_twilio_webhook(webhook_data)

#     console.print("[green]Parsed data:[/green]")

#     table = Table(show_header=True, header_style="bold magenta")
#     table.add_column("Field", style="cyan")
#     table.add_column("Value", style="white")

#     for key, value in parsed_data.items():
#         table.add_row(key, str(value))

#     console.print(table)

# @cli.command()
# def status():
#     """Check SMS service status and configuration"""
#     console.print(f"[bold]SMS Service Status Check[/bold]")
#     console.print("-" * 50)

#     sms_service = TwilioSMSService()

#     table = Table(show_header=True, header_style="bold magenta")
#     table.add_column("Configuration", style="cyan")
#     table.add_column("Status", style="white")
#     table.add_column("Value", style="yellow")

#     # Check configuration
#     has_sid = bool(sms_service.account_sid)
#     has_token = bool(sms_service.auth_token)
#     has_phone = bool(sms_service.from_number)
#     has_client = bool(sms_service.client)

#     table.add_row("Account SID", "✓" if has_sid else "✗", sms_service.account_sid or "Not configured")
#     table.add_row("Auth Token", "✓" if has_token else "✗", "***" if has_token else "Not configured")
#     table.add_row("Phone Number", "✓" if has_phone else "✗", sms_service.from_number or "Not configured")
#     table.add_row("Twilio Client", "✓" if has_client else "✗", "Active" if has_client else "Disabled")

#     console.print(table)

#     if has_client:
#         console.print("[green]✓ SMS service is fully configured and ready[/green]")
#     else:
#         console.print("[yellow]⚠ SMS service running in test mode (no credentials)[/yellow]")
#         console.print("To enable real SMS sending, configure Twilio credentials in .env file")

# @cli.command()
# @click.option('--phone', '-p', default='5551234567', help='Phone number for simulation')
# def simulate(phone):
#     """Simulate a complete SMS conversation flow"""
#     console.print(f"[bold]Simulating SMS Conversation Flow[/bold]")
#     console.print(f"Phone: {phone}")
#     console.print("-" * 50)

#     sms_service = TwilioSMSService()

#     # Simulate incoming messages and responses
#     test_messages = [
#         "add milk",
#         "add bread",
#         "add eggs",
#         "show",
#         "remove milk",
#         "show",
#         "clear"
#     ]

#     for i, message in enumerate(test_messages, 1):
#         console.print(f"\n[bold blue]Step {i}: Incoming SMS[/bold blue]")

#         # Parse incoming webhook
#         webhook_data = {
#             'From': f"+1{phone}",
#             'Body': message,
#             'MessageSid': f'test_msg_{i}',
#             'AccountSid': 'test_account'
#         }

#         parsed = sms_service.parse_twilio_webhook(webhook_data)
#         console.print(f"📱 Received: '{message}' from {parsed['phone_number']}")

#         # Simulate response (you would normally get this from your command processor)
#         if message.startswith('add'):
#             item = message.split(' ', 1)[1]
#             response = f"Added '{item}' to Grocery List"
#         elif message == 'show':
#             response = "Grocery List:\n1. milk\n2. bread\n3. eggs"
#         elif message.startswith('remove'):
#             response = "Removed 'milk' from Grocery List"
#         elif message == 'clear':
#             response = "Cleared all items from Grocery List"
#         else:
#             response = "Command not recognized"

#         # Test TwiML response
#         twiml = sms_service.create_twiml_response(response)
#         console.print(f"📤 Response: '{response}'")

#         # Test sending SMS
#         sms_service.send_sms(phone, response)

# @cli.command()
# @click.option('--count', '-c', default=5, help='Number of test messages to send')
# @click.option('--phone', '-p', default='5551234567', help='Phone number for load test')
# def load_test(count, phone):
#     """Run load test with multiple SMS operations"""
#     console.print(f"[bold]SMS Load Test[/bold]")
#     console.print(f"Sending {count} test messages to {phone}")
#     console.print("-" * 50)

#     sms_service = TwilioSMSService()

#     start_time = datetime.now()
#     success_count = 0

#     with console.status("[bold green]Running load test...") as status:
#         for i in range(count):
#             message = f"Test message {i+1} - {datetime.now().strftime('%H:%M:%S')}"
#             result = sms_service.send_sms(phone, message)

#             if result or not sms_service.client:  # Count as success if no client (test mode)
#                 success_count += 1

#             status.update(f"[bold green]Sent {i+1}/{count} messages...")

#     end_time = datetime.now()
#     duration = (end_time - start_time).total_seconds()

#     console.print(f"\n[green]Load Test Results:[/green]")
#     console.print(f"Messages sent: {success_count}/{count}")
#     console.print(f"Duration: {duration:.2f} seconds")
#     console.print(f"Rate: {count/duration:.2f} messages/second")

if __name__ == "__main__":
    cli()
