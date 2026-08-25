# ================== TELEGRAM API CONFIG ==================

# Get these from https://my.telegram.org/apps
API_ID = 33319256
API_HASH = "6b2a9c9c721fe7cdce6fc054e2565e30"

# Bot token from @BotFather
BOT_TOKEN = "7793461414:AAHSHVLCi2eAQtYt_kMJ8OumTnCdmOUwVpk"


# ================== REDIS DATABASE CONFIG ==================

# Redis Host / Port / Password
HOST = "127.0.0.1"
PORT = 6379
PASSWORD = None   # Set to None if Redis has no password


# ================== BOT SETTINGS ==================

# Private storage chat where files are uploaded
# Use your private channel / chat ID (must be integer)
PRIVATE_CHAT_ID = -1003970353038


# Admin user IDs (MUST be integers)
# Add multiple IDs inside list
ADMINS = [
    7302497948,   # Example: Your Telegram ID
    # 123456789,
]


# ================== OPTIONAL FLAGS ==================

# If you still want to support single ADMIN broadcast logs etc.
# (Used in old redeem handler — safe to keep)
ADMIN_ID = 7302497948

TERABOX_API_BASE = "https://teradown1.nepcoder.workers.dev/api/resolve"
#TERABOX_API_TOKEN = "NTMPASS"

TERABOX_API_TEMPLATE = (
    f"{TERABOX_API_BASE}?url={{url}}"
)
