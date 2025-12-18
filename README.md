# Contest Bot Template

Telegram bot template with SQLite database, user registration, and admin broadcast functionality.

## Features

- 📝 User registration on `/start` command
- 📢 Admin broadcast to all users with `/broadcast` command
- 💾 SQLite database for persistent storage
- 🔌 DB-agnostic design (easily switch to PostgreSQL/MySQL/RDS)

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Edit `.env` file with your values:
```
TELEGRAM_TOKEN=your_bot_token_here
ADMIN_ID=your_telegram_id_here
DATABASE_URL=sqlite:///./contest_bot_db.db
```

To get your Telegram ID, send `/start` to [@userinfobot](https://t.me/userinfobot)

### 3. Run the bot

```bash
python main.py
```

## Commands

- `/start` - Register user in the database
- `/broadcast` - Send message to all users (admin only)
  - After typing `/broadcast`, you can either:
    - Write a custom message
    - Forward a message from another chat

## Project Structure

```
.
├── bot/
│   ├── config.py          # Settings (token, admin ID, database URL)
│   ├── app.py             # Bot initialization
│   ├── models/
│   │   └── user.py        # User data model
│   ├── handlers/
│   │   ├── start.py       # /start command handler
│   │   └── broadcast.py   # /broadcast command handler
│   └── services/
│       └── user_service.py # Business logic
├── db/
│   ├── __init__.py        # Database factory
│   ├── base.py            # Repository interface
│   └── sqlite_impl.py     # SQLite implementation
├── main.py                # Entry point
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
└── README.md
```

## Switching Database Backends

The code is designed to support multiple databases. To switch from SQLite to PostgreSQL:

1. Create `db/postgres_impl.py` implementing the same interface as `SqliteUserRepo`
2. Update `db/__init__.py` to detect PostgreSQL URLs and return the new implementation
3. Update `.env`:
   ```
   DATABASE_URL=postgresql://user:password@localhost/botdb
   ```

No changes needed in handlers or services!
