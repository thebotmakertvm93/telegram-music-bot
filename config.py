import os

# Telegram API Credentials (from my.telegram.org)
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")

# Your standard Bot Token (from @BotFather)
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Pyrogram Session String (The user account that joins the voice chat)
SESSION_STRING = os.environ.get("SESSION_STRING", "")

# The port Render assigns to our web service
PORT = int(os.environ.get("PORT", "8080"))
