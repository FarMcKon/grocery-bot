# #!/usr/bin/env python3
# """
# Grocery Bot - SMS-based grocery list management
# Main Flask server for handling SMS webhooks and API endpoints
# """

# import os
# import json
# from datetime import datetime
# from flask import Flask, request, jsonify
from rich.console import Console

from dotenv import load_dotenv

#Load environment variables, globals
load_dotenv()
console = Console()

# app = Flask(__name__)
# app.config["SECRET_KEY"] = os.getenv(
#     "SECRET_KEY", "dev-secret-key-change-in-production"
# )

# # In-memory storage for development (replace with database later)
# users = {}
# lists = {}
# list_access = {}
# sms_messages = []


# # Simple data models as dictionaries for now
# def create_user(phone_number, email=None, name=None):
#     user_id = f"user_{len(users) + 1}"
#     user = {
#         "id": user_id,
#         "phone_number": phone_number,
#         "email": email,
#         "name": name,
#         "created_date": datetime.now().isoformat(),
#         "last_active": datetime.now().isoformat(),
#         "is_active": True,
#     }
#     users[user_id] = user
#     return user


# def create_list(name, owner_id):
#     list_id = f"list_{len(lists) + 1}"
#     grocery_list = {
#         "id": list_id,
#         "name": name,
#         "owner_id": owner_id,
#         "created_date": datetime.now().isoformat(),
#         "updated_date": datetime.now().isoformat(),
#         "deleted_date": None,
#         "items": [],
#         "is_active": True,
#     }
#     lists[list_id] = grocery_list

#     # Create list access for owner
#     access_id = f"access_{len(list_access) + 1}"
#     list_access[access_id] = {
#         "id": access_id,
#         "list_id": list_id,
#         "user_id": owner_id,
#         "permission_level": "owner",
#         "granted_date": datetime.now().isoformat(),
#         "is_current_active": True,
#     }

#     return grocery_list


# def log_sms_message(
#     phone_number, message_content, direction, user_id=None, list_id=None
# ):
#     message = {
#         "id": f"msg_{len(sms_messages) + 1}",
#         "user_id": user_id,
#         "phone_number": phone_number,
#         "message_content": message_content,
#         "direction": direction,
#         "timestamp": datetime.now().isoformat(),
#         "processed": False,
#         "list_id": list_id,
#     }
#     sms_messages.append(message)
#     return message


# def find_user_by_phone(phone_number):
#     for user in users.values():
#         if user["phone_number"] == phone_number:
#             return user
#     return None


# def get_user_active_list(user_id):
#     for access in list_access.values():
#         if access["user_id"] == user_id and access["is_current_active"]:
#             return lists.get(access["list_id"])
#     return None


# def parse_sms_command(message_content):
#     """Parse SMS message and return command and parameters"""
#     content = message_content.strip().lower()

#     if content.startswith("add "):
#         return "add", content[4:].strip()
#     elif content.startswith("remove "):
#         return "remove", content[7:].strip()
#     elif content.startswith("check "):
#         return "check", content[6:].strip()
#     elif content.startswith("uncheck "):
#         return "uncheck", content[8:].strip()
#     elif content in ["show", "show list"]:
#         return "show", None
#     elif content.startswith("show "):
#         return "show", content[5:].strip()
#     elif content in ["clear", "clear list"]:
#         return "clear", None
#     elif content.startswith("clear "):
#         return "clear", content[6:].strip()
#     elif content.startswith("tell "):
#         return "tell", content[5:].strip()
#     elif content == "tell" or content == "tell list":
#         return "tell", None
#     elif content.startswith("link "):
#         return "link", content[5:].strip()
#     else:
#         return "unknown", content


# @app.route("/")
# def health_check():
#     """Health check endpoint"""
#     return jsonify(
#         {
#             "status": "healthy",
#             "service": "grocery-bot",
#             "timestamp": datetime.now().isoformat(),
#         }
#     )


# @app.route("/sms/webhook", methods=["POST"])
# def sms_webhook():
#     """Handle incoming SMS messages from SMS provider (Twilio, etc.)"""
#     try:
#         # Get SMS data from request (format depends on SMS provider)
#         data = request.get_json() or {}
#         phone_number = (
#             data.get("From", "").replace("+1", "").replace("-", "").replace(" ", "")
#         )
#         message_content = data.get("Body", "").strip()

#         if not phone_number or not message_content:
#             return jsonify({"error": "Missing phone number or message content"}), 400

#         # Log incoming message
#         log_sms_message(phone_number, message_content, "inbound")

#         # Find or create user
#         user = find_user_by_phone(phone_number)
#         if not user:
#             user = create_user(phone_number)
#             # Create default grocery list for new user
#             default_list = create_list("Grocery List", user["id"])

#         # Update user last active
#         user["last_active"] = datetime.now().isoformat()

#         # Parse command
#         command, params = parse_sms_command(message_content)
#         response_message = process_sms_command(user, command, params)

#         # Log outbound message
#         log_sms_message(phone_number, response_message, "outbound", user["id"])

#         # Return response for SMS provider
#         return jsonify({"message": response_message, "status": "processed"})

#     except Exception as e:
#         print(f"Error processing SMS webhook: {e}")
#         return jsonify({"error": "Internal server error"}), 500


# def process_sms_command(user, command, params):
#     """Process SMS command and return response message"""
#     try:
#         active_list = get_user_active_list(user["id"])

#         if command == "add" and params:
#             if active_list:
#                 item_number = len(active_list["items"]) + 1
#                 active_list["items"].append(f"{item_number}. {params}")
#                 active_list["updated_date"] = datetime.now().isoformat()
#                 return f"Added '{params}' to {active_list['name']} (#{item_number})"
#             else:
#                 return "No active list found. Please create a list first."

#         elif command == "remove" and params:
#             if active_list and active_list["items"]:
#                 # Try to remove by item text or number
#                 removed = False
#                 for i, item in enumerate(active_list["items"]):
#                     if params in item.lower() or params == str(i + 1):
#                         removed_item = active_list["items"].pop(i)
#                         # Renumber remaining items
#                         for j in range(i, len(active_list["items"])):
#                             old_item = active_list["items"][j]
#                             # Extract text after number
#                             text_part = (
#                                 old_item.split(". ", 1)[1]
#                                 if ". " in old_item
#                                 else old_item
#                             )
#                             active_list["items"][j] = f"{j + 1}. {text_part}"
#                         active_list["updated_date"] = datetime.now().isoformat()
#                         return f"Removed '{removed_item}' from {active_list['name']}"
#                 return f"Item '{params}' not found in {active_list['name']}"
#             else:
#                 return "No items to remove from your list."

#         elif command == "show":
#             if active_list and active_list["items"]:
#                 items_text = "\n".join(active_list["items"])
#                 return f"{active_list['name']}:\n{items_text}"
#             else:
#                 return f"Your {active_list['name'] if active_list else 'grocery list'} is empty."

#         elif command == "clear":
#             if active_list:
#                 active_list["items"] = []
#                 active_list["updated_date"] = datetime.now().isoformat()
#                 return f"Cleared all items from {active_list['name']}"
#             else:
#                 return "No active list to clear."

#         elif command == "tell":
#             if active_list and active_list["items"]:
#                 items_text = "\n".join(active_list["items"])
#                 return f"Your {active_list['name']}:\n{items_text}\n\nTotal items: {len(active_list['items'])}"
#             else:
#                 return f"Your {active_list['name'] if active_list else 'grocery list'} is empty."

#         else:
#             return (
#                 "Commands: 'add [item]', 'remove [item]', 'show', 'clear', 'tell'\n"
#                 "Example: 'add milk' or 'remove 2'"
#             )

#     except Exception as e:
#         print(f"Error processing command {command}: {e}")
#         return "Sorry, there was an error processing your request."


# @app.route("/api/users", methods=["GET"])
# def get_users():
#     """Get all users (for debugging)"""
#     return jsonify(list(users.values()))


# @app.route("/api/lists", methods=["GET"])
# def get_lists():
#     """Get all lists (for debugging)"""
#     return jsonify(list(lists.values()))


# @app.route("/api/messages", methods=["GET"])
# def get_messages():
#     """Get SMS message history (for debugging)"""
#     return jsonify(sms_messages)


# @app.route("/api/test-sms", methods=["POST"])
# def test_sms():
#     """Test SMS processing without actual SMS provider"""
#     data = request.get_json()
#     phone_number = data.get("phone_number", "5551234567")
#     message = data.get("message", "show")

#     # Simulate SMS webhook
#     test_data = {"From": phone_number, "Body": message}

#     # Process through SMS webhook logic
#     with app.test_request_context("/sms/webhook", json=test_data, method="POST"):
#         request._cached_json = test_data
#         response = sms_webhook()
#         return response


if __name__ == "__main__":
    console.print("[red] NOT Starting Grocery Bot SMS Server...[/red]")
    console.print("Still building this, sorry!\n")

#     print("Starting Grocery Bot SMS Server...")
#     print("Available endpoints:")
#     print("  GET  /              - Health check")
#     print("  POST /sms/webhook   - SMS webhook (for SMS provider)")
#     print("  POST /api/test-sms  - Test SMS processing")
#     print("  GET  /api/users     - View users (debug)")
#     print("  GET  /api/lists     - View lists (debug)")
#     print("  GET  /api/messages  - View SMS history (debug)")

#     # Run development server
#     app.run(
#         host=os.getenv("HOST", "127.0.0.1"),
#         port=int(os.getenv("PORT", 5000)),
#         debug=os.getenv("DEBUG", "True").lower() == "true",
#     )
