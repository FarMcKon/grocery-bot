"""
Database Storage Module for Grocery Bot
Handles all database operations for users, lists, and list access.
"""

# import os
import json

# import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from tinydb import TinyDB, Query
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class List:
    """For now, reminder to devs. To be used soon / future"""

    name: str
    owner_id: str
    created_date: str
    updated_date: str
    deleted_date: str
    # created_date: str
    # updated_date: str
    # deleted_date: str
    archvied_on: int


@dataclass
class User:
    """For now, reminder to devs. To be used soon / future"""

    name: str
    phone_number: str
    email: str
    # created_date: str
    # updated_date: str
    # deleted_date: str
    archvied_on: int


class Database:
    """Database handler for Grocery Bot using SQLite."""

    DB_TYPES = ["tiny_db", "sqlite3"]

    def __init__(self, db_path: str = "grocery_bot.json", db_type="tiny_db"):
        """Initialize the database connection and create tables if they don't exist."""
        self.db_path = db_path
        self.db_type = db_type
        self.do_init_or_upgrade_db = True
        self.db_object = None

        # for now, always init or upgrade
        if self.do_init_or_upgrade_db:
            print("doing init of Database")
            self._init_or_upgrade_db()

    def _init_or_upgrade_db(self, force_init=False, force_upgrade=False) -> None:
        """Initialize the database with required tables."""
        print("Starting init or upgrade of DB")
        if self.db_type not in Database.DB_TYPES:
            raise ValueError(
                f"Invalid database type: {self.db_type}. Valid types are: {Database.DB_TYPES}"
            )

        if self.db_type == "tiny_db":
            if not self.db_path:
                raise ValueError("No database path specified")

            # if we do not have a filename,  create one now and warn
            if not Path(self.db_path).exists():
                print(f"Creating new database file: {self.db_path}")
                self.db_object = TinyDB(self.db_path)
                vQuery = Query()
                self.db_object.search(vQuery.version == "0.2")
                if len(self.db_object.search(vQuery.version == "0.2")) == 0:
                    print("Labeling version to DB_Upgrading DB")
                    self.db_object.insert({"version": "0.2"})
                else:
                    print("DB already has version info? WTF? This is not right")
            else:
                print("opening existing DB")
                self.db_object = TinyDB(self.db_path)
                self.db_object.search
                vQuery = Query()
                self.db_object.search(vQuery.version == "0.2")
                if len(self.db_object.search(vQuery.version == "0.2")) == 0:
                    print("Upgrading DB")
                    self.db_object.insert({"version": "0.2"})
            # if we have a file, open it make sure it has version info
            # if we don't have a file, create it and log reation
            print("Finised tinyDB init or upgrade of DB")
            return

        if self.db_type == "sqlite3":
            print(" Not able to create / upgrade SQLite database yet")
            return

    # User operations
    def upsert_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user."""
        required_fields = ["name", "phone_number", "email"]
        if not all(field in user_data for field in required_fields):
            raise ValueError("Missing required user fields in payload")
        if not self.db_object:
            raise ValueError("Database object not initialized")

        # upsert
        search_dict = {"phone_number": user_data["phone_number"]}
        self.db_object.upsert(
            user_data, Query().phone_number == user_data["phone_number"]
        )
        print("Upserted user " + user_data["name"])

    def get_user_id(self, search_dict):
        """Get a user doc_id by phone number."""

        if not self.db_object:
            raise ValueError("Database object not initialized")

        # for v1, only search by phone_number
        matched = self.db_object.search(
            Query().phone_number == search_dict["phone_number"]
        )
        # print ("got a doc ID buddy? " + str(matched.doc_id))
        if len(matched) == 0:
            raise ValueError("User not found")
        if len(matched) == 1:
            return matched[0].doc_id
        raise ValueError("Multiple users found by phone number. Not good")

    def upsert_list(self, list_data):
        """add or update a grocery list. owner doc_id and name only"""

        # assume 'search dict' has owner_id and 'name' only, 'is_default_list' is optional
        lQuery = Query()
        list_obj = self.db_object.upsert(
            list_data,
            (lQuery.owner_id == list_data["owner_id"])
            & (lQuery.name == list_data["name"]),
        )
        if list_obj:
            print("Upserted list " + list_data["name"] + " at id" + str(list_obj))
        else:
            print("Failed to upsert list " + list_data["name"])

    def get_list(self, search_dict):
        """Get a list doc_id by owner_id and name."""

        if not self.db_object:
            raise ValueError("Database object not initialized")

        # for v1, only search by owner_id and name only
        matched = self.db_object.search(
            (Query().owner_id == search_dict["owner_id"])
            & (Query().name == search_dict["name"])
        )
        if len(matched) == 0:
            raise ValueError("List not found for" + str(search_dict))
        if len(matched) == 1:
            return matched[0]
        raise ValueError("Multiple lists found by owner_id and name. Not good")
        print("got a doc ID buddy? " + str(matched.doc_id))


class DatabaseCursor:
    """
    Holder for cursor based snippits for later
    """

    #     def _get_connection(self) -> sqlite3.Connection:
    #         """Get a database connection."""
    #         conn = sqlite3.connect(self.db_path)
    #         conn.row_factory = sqlite3.Row  # This enables column access by name
    #         return conn

    #   def create_or_update_db(self):
    # with self._get_connection() as conn:
    #     cursor = conn.cursor()
    #             # Users table
    #             cursor.execute('''
    #                 CREATE TABLE IF NOT EXISTS users (
    #                     id TEXT PRIMARY KEY,
    #                     phone_number TEXT UNIQUE NOT NULL,
    #                     email TEXT,
    #                     name TEXT,
    #                     created_date TEXT NOT NULL,
    #                     last_active TEXT NOT NULL,
    #                     is_active INTEGER DEFAULT 1
    #                 )
    #             ''')

    #             # Lists table
    #             cursor.execute('''
    #                 CREATE TABLE IF NOT EXISTS lists (
    #                     id TEXT PRIMARY KEY,
    #                     name TEXT NOT NULL,
    #                     owner_id TEXT NOT NULL,
    #                     created_date TEXT NOT NULL,
    #                     updated_date TEXT NOT NULL,
    #                     deleted_date TEXT,
    #                     is_active INTEGER DEFAULT 1,
    #                     FOREIGN KEY (owner_id) REFERENCES users (id)
    #                 )
    #             ''')

    #             # List items table (one-to-many relationship with lists)
    #             cursor.execute('''
    #                 CREATE TABLE IF NOT EXISTS list_items (
    #                     id TEXT PRIMARY KEY,
    #                     list_id TEXT NOT NULL,
    #                     content TEXT NOT NULL,
    #                     is_checked INTEGER DEFAULT 0,
    #                     created_date TEXT NOT NULL,
    #                     updated_date TEXT NOT NULL,
    #                     position INTEGER NOT NULL,
    #                     FOREIGN KEY (list_id) REFERENCES lists (id) ON DELETE CASCADE
    #                 )
    #             ''')

    #             # List access table (many-to-many relationship between users and lists)
    #             cursor.execute('''
    #                 CREATE TABLE IF NOT EXISTS list_access (
    #                     id TEXT PRIMARY KEY,
    #                     list_id TEXT NOT NULL,
    #                     user_id TEXT NOT NULL,
    #                     permission_level TEXT NOT NULL,
    #                     granted_date TEXT NOT NULL,
    #                     is_current_active INTEGER DEFAULT 0,
    #                     FOREIGN KEY (list_id) REFERENCES lists (id) ON DELETE CASCADE,
    #                     FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    #                     UNIQUE(list_id, user_id)
    #                 )
    #             ''')

    #             # SMS messages log
    #             cursor.execute('''
    #                 CREATE TABLE IF NOT EXISTS sms_messages (
    #                     id TEXT PRIMARY KEY,
    #                     user_id TEXT,
    #                     phone_number TEXT NOT NULL,
    #                     message_content TEXT NOT NULL,
    #                     direction TEXT NOT NULL,
    #                     timestamp TEXT NOT NULL,
    #                     processed INTEGER DEFAULT 0,
    #                     list_id TEXT,
    #                     FOREIGN KEY (user_id) REFERENCES users (id),
    #                     FOREIGN KEY (list_id) REFERENCES lists (id)
    #                 )
    #             ''')

    #             conn.commit()
    # def make_user_cursor(self):
    #         with self._get_connection() as conn:
    #             cursor = conn.cursor()
    #             cursor.execute('''
    #                 INSERT INTO users (id, phone_number, email, name, created_date, last_active, is_active)
    #                 VALUES (:id, :phone_number, :email, :name, :created_date, :last_active, :is_active)
    #             ''', user_data)
    #             conn.commit()

    #         return self.get_user(user_data['id'])

    #     def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
    #         """Get a user by ID."""
    #         with self._get_connection() as conn:
    #             cursor = conn.cursor()
    #             cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    #             row = cursor.fetchone()
    #             return dict(row) if row else None

    #     def get_user_by_phone(self, phone_number: str) -> Optional[Dict[str, Any]]:
    #         """Get a user by phone number."""
    #         with self._get_connection() as conn:
    #             cursor = conn.cursor()
    #             cursor.execute('SELECT * FROM users WHERE phone_number = ?', (phone_number,))
    #             row = cursor.fetchone()
    #             return dict(row) if row else None

    #     def update_user(self, user_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    #         """Update user information."""
    #         if not updates:
    #             return self.get_user(user_id)

    #         updates['last_active'] = datetime.now().isoformat()

    #         set_clause = ", ".join(f"{k} = :{k}" for k in updates)

    #         with self._get_connection() as conn:
    #             cursor = conn.cursor()
    #             cursor.execute(
    #                 f'UPDATE users SET {set_clause} WHERE id = :user_id',
    #                 {**updates, 'user_id': user_id}
    #             )
    #             conn.commit()

    #             if cursor.rowcount == 0:
    #                 return None

    #         return self.get_user(user_id)

    # List operations
    def create_list(self, list_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new grocery list."""
        required_fields = ["id", "name", "owner_id"]
        if not all(field in list_data for field in required_fields):
            raise ValueError("Missing required list fields")

        now = datetime.now().isoformat()
        list_data.setdefault("created_date", now)
        list_data.setdefault("updated_date", now)
        list_data.setdefault("is_active", True)

        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Create the list
            cursor.execute(
                """
                INSERT INTO lists (id, name, owner_id, created_date, updated_date, is_active)
                VALUES (:id, :name, :owner_id, :created_date, :updated_date, :is_active)
            """,
                list_data,
            )

            # Create list access for the owner
            access_data = {
                "id": f"access_{list_data['id']}",
                "list_id": list_data["id"],
                "user_id": list_data["owner_id"],
                "permission_level": "owner",
                "granted_date": now,
                "is_current_active": 1,
            }

            cursor.execute(
                """
                INSERT INTO list_access (id, list_id, user_id, permission_level, granted_date, is_current_active)
                VALUES (:id, :list_id, :user_id, :permission_level, :granted_date, :is_current_active)
            """,
                access_data,
            )

            conn.commit()

        return self.get_list(list_data["id"])


#     def get_list(self, list_id: str) -> Optional[Dict[str, Any]]:
#         """Get a list by ID with its items."""
#         with self._get_connection() as conn:
#             cursor = conn.cursor()

#             # Get list details
#             cursor.execute('SELECT * FROM lists WHERE id = ?', (list_id,))
#             list_data = cursor.fetchone()

#             if not list_data:
#                 return None

#             list_data = dict(list_data)

#             # Get list items
#             cursor.execute('''
#                 SELECT id, content, is_checked, position
#                 FROM list_items
#                 WHERE list_id = ?
#                 ORDER BY position
#             ''', (list_id,))

#             items = [dict(row) for row in cursor.fetchall()]
#             list_data['items'] = items

#             return list_data

#     def get_user_lists(self, user_id: str) -> List[Dict[str, Any]]:
#         """Get all lists accessible by a user."""
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 SELECT l.* FROM lists l
#                 JOIN list_access la ON l.id = la.list_id
#                 WHERE la.user_id = ? AND l.is_active = 1
#                 ORDER BY la.is_current_active DESC, l.updated_date DESC
#             ''', (user_id,))

#             return [dict(row) for row in cursor.fetchall()]

#     def get_user_active_list(self, user_id: str) -> Optional[Dict[str, Any]]:
#         """Get the user's currently active list."""
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 SELECT l.* FROM lists l
#                 JOIN list_access la ON l.id = la.list_id
#                 WHERE la.user_id = ? AND la.is_current_active = 1 AND l.is_active = 1
#                 LIMIT 1
#             ''', (user_id,))

#             row = cursor.fetchone()
#             if not row:
#                 return None

#             list_data = dict(row)

#             # Get list items
#             cursor.execute('''
#                 SELECT id, content, is_checked, position
#                 FROM list_items
#                 WHERE list_id = ?
#                 ORDER BY position
#             ''', (list_data['id'],))

#             items = [dict(row) for row in cursor.fetchall()]
#             list_data['items'] = items

#             return list_data

#     def update_list(self, list_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
#         """Update list information."""
#         if not updates:
#             return self.get_list(list_id)

#         updates['updated_date'] = datetime.now().isoformat()

#         set_clause = ", ".join(f"{k} = :{k}" for k in updates)

#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(
#                 f'UPDATE lists SET {set_clause} WHERE id = :list_id',
#                 {**updates, 'list_id': list_id}
#             )
#             conn.commit()

#             if cursor.rowcount == 0:
#                 return None

#         return self.get_list(list_id)

#     def delete_list(self, list_id: str) -> bool:
#         """Soft delete a list."""
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 UPDATE lists
#                 SET is_active = 0, updated_date = ?, deleted_date = ?
#                 WHERE id = ?
#             ''', (datetime.now().isoformat(), datetime.now().isoformat(), list_id))

#             conn.commit()
#             return cursor.rowcount > 0

#     # List item operations
#     def add_list_item(self, list_id: str, item_data: Dict[str, Any]) -> Dict[str, Any]:
#         """Add an item to a list."""
#         required_fields = ['id', 'content']
#         if not all(field in item_data for field in required_fields):
#             raise ValueError("Missing required item fields")

#         now = datetime.now().isoformat()
#         item_data.setdefault('created_date', now)
#         item_data.setdefault('updated_date', now)
#         item_data.setdefault('is_checked', False)
#         item_data['list_id'] = list_id

#         # Get the next position
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 SELECT COALESCE(MAX(position), 0) + 1
#                 FROM list_items
#                 WHERE list_id = ?
#             ''', (list_id,))

#             item_data['position'] = cursor.fetchone()[0]

#             # Insert the item
#             cursor.execute('''
#                 INSERT INTO list_items
#                 (id, list_id, content, is_checked, created_date, updated_date, position)
#                 VALUES
#                 (:id, :list_id, :content, :is_checked, :created_date, :updated_date, :position)
#             ''', item_data)

#             # Update the list's updated_date
#             cursor.execute('''
#                 UPDATE lists
#                 SET updated_date = ?
#                 WHERE id = ?
#             ''', (now, list_id))

#             conn.commit()

#         return self.get_list_item(item_data['id'])

#     def get_list_item(self, item_id: str) -> Optional[Dict[str, Any]]:
#         """Get a list item by ID."""
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('SELECT * FROM list_items WHERE id = ?', (item_id,))
#             row = cursor.fetchone()
#             return dict(row) if row else None

#     def update_list_item(self, item_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
#         """Update a list item."""
#         if not updates:
#             return self.get_list_item(item_id)

#         updates['updated_date'] = datetime.now().isoformat()

#         set_clause = ", ".join(f"{k} = :{k}" for k in updates)

#         with self._get_connection() as conn:
#             cursor = conn.cursor()

#             # Get the current item to update the list's updated_date if needed
#             cursor.execute('SELECT list_id FROM list_items WHERE id = ?', (item_id,))
#             row = cursor.fetchone()
#             if not row:
#                 return None

#             list_id = row[0]

#             # Update the item
#             cursor.execute(
#                 f'UPDATE list_items SET {set_clause} WHERE id = :item_id',
#                 {**updates, 'item_id': item_id}
#             )

#             # Update the list's updated_date
#             cursor.execute('''
#                 UPDATE lists
#                 SET updated_date = ?
#                 WHERE id = ?
#             ''', (updates['updated_date'], list_id))

#             conn.commit()

#             if cursor.rowcount == 0:
#                 return None

#         return self.get_list_item(item_id)

#     def delete_list_item(self, item_id: str) -> bool:
#         """Delete a list item."""
#         with self._get_connection() as conn:
#             cursor = conn.cursor()

#             # Get the list_id to update the list's updated_date
#             cursor.execute('SELECT list_id FROM list_items WHERE id = ?', (item_id,))
#             row = cursor.fetchone()
#             if not row:
#                 return False

#             list_id = row[0]

#             # Delete the item
#             cursor.execute('DELETE FROM list_items WHERE id = ?', (item_id,))

#             # Update the list's updated_date
#             cursor.execute('''
#                 UPDATE lists
#                 SET updated_date = ?
#                 WHERE id = ?
#             ''', (datetime.now().isoformat(), list_id))

#             # Update positions of remaining items
#             cursor.execute('''
#                 UPDATE list_items
#                 SET position = position - 1
#                 WHERE list_id = ? AND position > (
#                     SELECT COALESCE(MAX(position), 0)
#                     FROM list_items
#                     WHERE id = ?
#                 )
#             ''', (list_id, item_id))

#             conn.commit()
#             return cursor.rowcount > 0

#     # List access operations
#     def grant_list_access(self, access_data: Dict[str, Any]) -> Dict[str, Any]:
#         """Grant a user access to a list."""
#         required_fields = ['id', 'list_id', 'user_id', 'permission_level']
#         if not all(field in access_data for field in required_fields):
#             raise ValueError("Missing required access fields")

#         access_data.setdefault('granted_date', datetime.now().isoformat())
#         access_data.setdefault('is_current_active', False)

#         with self._get_connection() as conn:
#             cursor = conn.cursor()

#             # Check if access already exists
#             cursor.execute('''
#                 SELECT * FROM list_access
#                 WHERE list_id = :list_id AND user_id = :user_id
#             ''', access_data)

#             if cursor.fetchone():
#                 # Update existing access
#                 cursor.execute('''
#                     UPDATE list_access
#                     SET permission_level = :permission_level,
#                         is_current_active = :is_current_active
#                     WHERE list_id = :list_id AND user_id = :user_id
#                 ''', access_data)
#             else:
#                 # Create new access
#                 cursor.execute('''
#                     INSERT INTO list_access
#                     (id, list_id, user_id, permission_level, granted_date, is_current_active)
#                     VALUES
#                     (:id, :list_id, :user_id, :permission_level, :granted_date, :is_current_active)
#                 ''', access_data)

#             conn.commit()

#         return self.get_list_access(access_data['id'])

#     def get_list_access(self, access_id: str) -> Optional[Dict[str, Any]]:
#         """Get list access by ID."""
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('SELECT * FROM list_access WHERE id = ?', (access_id,))
#             row = cursor.fetchone()
#             return dict(row) if row else None

#     def get_list_access_by_user_and_list(self, user_id: str, list_id: str) -> Optional[Dict[str, Any]]:
#         """Get list access for a specific user and list."""
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 SELECT * FROM list_access
#                 WHERE user_id = ? AND list_id = ?
#             ''', (user_id, list_id))

#             row = cursor.fetchone()
#             return dict(row) if row else None

#     def set_active_list(self, user_id: str, list_id: str) -> bool:
#         """Set a list as the user's active list."""
#         with self._get_connection() as conn:
#             cursor = conn.cursor()

#             # First, unset any currently active list for this user
#             cursor.execute('''
#                 UPDATE list_access
#                 SET is_current_active = 0
#                 WHERE user_id = ? AND is_current_active = 1
#             ''', (user_id,))

#             # Set the new active list
#             cursor.execute('''
#                 UPDATE list_access
#                 SET is_current_active = 1
#                 WHERE user_id = ? AND list_id = ?
#             ''', (user_id, list_id))

#             conn.commit()
#             return cursor.rowcount > 0

#     def revoke_list_access(self, access_id: str) -> bool:
#         """Revoke a user's access to a list."""
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('DELETE FROM list_access WHERE id = ?', (access_id,))
#             conn.commit()
#             return cursor.rowcount > 0

#     # SMS message logging
#     def log_sms_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
#         """Log an SMS message."""
#         required_fields = ['id', 'phone_number', 'message_content', 'direction']
#         if not all(field in message_data for field in required_fields):
#             raise ValueError("Missing required message fields")

#         message_data.setdefault('timestamp', datetime.now().isoformat())
#         message_data.setdefault('processed', False)

#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 INSERT INTO sms_messages
#                 (id, user_id, phone_number, message_content, direction, timestamp, processed, list_id)
#                 VALUES
#                 (:id, :user_id, :phone_number, :message_content, :direction, :timestamp, :processed, :list_id)
#             ''', message_data)

#             conn.commit()

#         return self.get_sms_message(message_data['id'])

#     def get_sms_message(self, message_id: str) -> Optional[Dict[str, Any]]:
#         """Get an SMS message by ID."""
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('SELECT * FROM sms_messages WHERE id = ?', (message_id,))
#             row = cursor.fetchone()
#             return dict(row) if row else None

#     def get_sms_messages_by_user(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
#         """Get SMS messages for a user, most recent first."""
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 SELECT * FROM sms_messages
#                 WHERE user_id = ?
#                 ORDER BY timestamp DESC
#                 LIMIT ?
#             ''', (user_id, limit))

#             return [dict(row) for row in cursor.fetchall()]

#     def mark_sms_message_processed(self, message_id: str) -> bool:
#         """Mark an SMS message as processed."""
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 UPDATE sms_messages
#                 SET processed = 1
#                 WHERE id = ?
#             ''', (message_id,))

#             conn.commit()
#             return cursor.rowcount > 0
