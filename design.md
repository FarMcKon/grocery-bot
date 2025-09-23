# Grocery Bot - Design Document

## Overview
The Grocery Bot is an SMS based application to quickly store information (a-la a grocery list) and 
retreve it for the user. Default and examaple list is 'Grocery List'. 

It helps users manage their grocery shopping list by making addition, removal, updates easy and fast, 
and share-able.

## Architecture
Overview of design 

### Core Components

#### 1. User Account: 
- **Purpose**: Create, read, update, and delete user account 
- **Responsibilities**: 
  - OAuth / API authetnication 
  - Connect name / email / OAuth certs, etc 

#### 2. List Access Manager 
- **Purpose**: Manage list accsss - 
- **Responsibilities**:
  - List Owner (singular)
  - Lists Guests, and guest permission level 
  - Link to current active list (singular)
  - Link to pasts lists (plural)
  - Name of list / date created, updated, deleted, etc

#### 3. List 
- **Purpose**:  The lisit object. Simple numbered text list 
- **Responsibilities**:
  - CRUD opeartions on the list, auto-numbering
  - Simple 'Combine / merge' behavior of lists 
  - 

#### 4. CLI Interface
- **Purpose**: Debugging interface with command-line interaction
- **Responsibilities**:
  - Parse user commands
  - Display formatted output using Rich library
  - Handle user input validation
  - Provide help and usage information

### 5. SMS Gateway
- **Purpose**: SMS Gateway for sending and receiving SMS messages
- **Responsibilities**:
  - Send SMS messages
  - Receive SMS messages
  - Parse SMS messages
  - Send SMS messages

## Data Models

### User
```python
class User:
    id: str
    phone_number: str
    email: Optional[str]
    name: Optional[str]
    oauth_provider: Optional[str]  # e.g., "google", "facebook"
    oauth_id: Optional[str]
    created_date: datetime
    last_active: datetime
    is_active: bool
```

### List
```python
class List:
    id: str
    name: str
    owner_id: str  # Foreign key to User
    created_date: datetime
    updated_date: datetime
    deleted_date: Optional[datetime]
    items: List[str]  # Simple numbered text items
    is_active: bool
```

### ListAccess
```python
class ListAccess:
    id: str
    list_id: str  # Foreign key to List
    user_id: str  # Foreign key to User
    permission_level: str  # "owner", "editor", "viewer"
    granted_date: datetime
    is_current_active: bool  # User's currently active list
```

### SMSMessage
```python
class SMSMessage:
    id: str
    user_id: str  # Foreign key to User
    phone_number: str
    message_content: str
    direction: str  # "inbound" or "outbound"
    timestamp: datetime
    processed: bool
    list_id: Optional[str]  # Associated list if applicable
```

## File Structure
```
grocery-bot/
├── grocery_bot.py          # Main entry point
├── models/
│   ├── __init__.py
│   ├── shopping_list.py    # ShoppingList class
│   ├── grocery_item.py     # GroceryItem class
│   └── price_history.py    # PriceHistory class
├── services/
│   ├── __init__.py
│   ├── list_manager.py     # Shopping list operations
│   ├── categorizer.py      # Item categorization logic
│   └── price_tracker.py    # Price tracking and comparison
├── cli/
│   ├── __init__.py
│   ├── commands.py         # CLI command definitions
│   └── display.py          # Output formatting
├── data/
│   ├── lists.json          # Stored shopping lists
│   ├── prices.json         # Price history data
│   └── categories.json     # Category mappings
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_services.py
    └── test_cli.py
```

## Command Line Interface

### List Management
- `gbot create <list_name>` - Create a new shopping list
- `gbot list` - Show all shopping lists
- `gbot show <list_name>` - Display items in a specific list
- `gbot delete <list_name>` - Delete a shopping list

### Item Management
- `gbot add <item> [--list <list_name>] [--quantity <qty>] [--category <cat>]`
- `gbot remove <item> [--list <list_name>]`
- `gbot check <item> [--list <list_name>]` - Mark as purchased
- `gbot uncheck <item> [--list <list_name>]` - Mark as not purchased

### Utility Commands
- `gbot export <list_name> [--format json|text]` - Export list
- `gbot import <file>` - Import list from file
- `gbot categories` - Show all categories
- `gbot total <list_name>` - Calculate estimated total cost


<!--
### Command Line Commands
- `grocery-bot create <list_name>` - Create a new shopping list
- `grocery-bot list` - Show all shopping lists
- `grocery-bot show <list_name>` - Display items in a specific list
- `grocery-bot delete <list_name>` - Delete a shopping list

### SMS Item Management
- `grocery-bot add <item> [--list <list_name>] [--quantity <qty>] 
- `grocery-bot remove <item> [--list <list_name>]`
- `grocery-bot check <item> [--list <list_name>]` - Mark as purchased
- `grocery-bot uncheck <item> [--list <list_name>]` - Mark as not purchased

### SMS Utility Commands
- `grocery-bot export <list_name> [--format json|text]` - Export list
- `grocery-bot import <file>` - Import list from file
- `grocery-bot categories` - Show all categories
-->

## SMS Interface
Super simple SMS interface 
### Link account 
- `link me to <email-provided-grocery-list-ID>`
- `link <cell-number> to <google-provided-ID>`

## Add / Remove items 
-  `add <item>`
-  `remove <item>`
-  `check <item>`
-  `uncheck <item>`

## List Management 
- `show` or  `show list`  or `show <list-name>`
- `clear` or `clear list`  or `clear <list-name>`
- `tell` or `tell list` or `tell <list-name>`

## Data Storage

### Local Storage
- JSON files for persistence
- Simple file-based approach for initial version
- Easy to backup and version control

### Future Considerations
- SQLite database for better querying
- Cloud sync capabilities
- Multi-user support

## User Experience

### Color Coding
- Green: Purchased items
- Yellow: Items on sale
- Red: Expensive items or price increases
- Blue: Category headers

### Smart Features
- Auto-complete for common grocery items
- Suggest categories based on item names
- Remember frequently purchased items
- Warn about duplicate items

## Configuration

### Settings File (.env)
```
DEFAULT_LIST_NAME=weekly
PRICE_ALERT_THRESHOLD=0.20
DEFAULT_STORE=local_grocery
AUTO_CATEGORIZE=true
```

## Error Handling
- Graceful handling of missing files
- Input validation with helpful error messages
- Backup creation before destructive operations
- Recovery options for corrupted data

## Testing Strategy
- Unit tests for all models and services
- Integration tests for CLI commands
- Mock data for consistent testing
- Test coverage reporting
