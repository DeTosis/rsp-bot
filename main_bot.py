from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from dotenv import load_dotenv
import os

bot_api_key = ""
bot_username = ""
def load_secrets():
    load_dotenv()
    bot_api_key = os.getenv("BOT_API_KEY")
    bot_username = os.getenv("BOT_USERNAME")
    
    print("API_KEY: ", bot_api_key)
    print("API_SECRET: ", bot_api_key)

def schedule_bot():
    load_secrets()

if __name__ == '__main__':
    schedule_bot()