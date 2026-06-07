import os

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
    BOT_USERNAME = os.getenv("BOT_USERNAME", "your_bot")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "YOUR_KEY")
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "YOUR_STRIPE")
    STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "YOUR_WEBHOOK")
    STRIPE_SUCCESS_URL = os.getenv("STRIPE_SUCCESS_URL", "https://t.me/your_bot")
    STRIPE_CANCEL_URL = os.getenv("STRIPE_CANCEL_URL", "https://t.me/your_bot")
    ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "123456789").split(",")))
    REFERRAL_CREDITS = 10
    NEW_USER_CREDITS = 5
    DOWNLOAD_COST = 2
    AI_MESSAGE_COST = 1
