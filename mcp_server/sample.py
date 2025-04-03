import os
from dotenv import load_dotenv
load_dotenv()
import asyncio
import requests
import os

# Load bot token and chat ID from environment variables
# Load bot token and chat ID from environment variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Your bot token
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Your chat ID
FILE_PATH = "C:/Users/Manu/Desktop/Drive_AI/uploads/myInvoice (48).pdf"
MESSAGE = "🚀 Here is your file sent from Manu.AI!"

