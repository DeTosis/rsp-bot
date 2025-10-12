from telegram import Update, ReplyKeyboardMarkup 
from telegram.ext import ApplicationBuilder, CommandHandler, filters, MessageHandler, ContextTypes, filters

from dotenv import load_dotenv
import os

from datetime import datetime, timedelta
import data_manager
import re

bot_api_key = ""
bot_username = ""

def load_secrets():
    global bot_api_key, bot_username
    load_dotenv()
    bot_api_key = os.getenv("BOT_API_KEY")
    bot_username = os.getenv("BOT_USERNAME")

def schedule_bot():
    load_secrets()

# ******************************
#           BOT COMMANDS
# ******************************

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tdtm = [
        ["Сегодня", "Завтра"],
        ["Пн","Вт","Ср"],
        ["Чт","Пт","Сб"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        tdtm,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    await update.message.reply_text(
        "Бот создан для получения расписания группы ИТ-125, ЭТФ",
        reply_markup=reply_markup
    )

weekdays = {
    "Пн": 0,
    "Вт": 1,
    "Ср": 2,
    "Чт": 3,
    "Пт": 4,
    "Сб": 5,
    "Вс": 6
}

def next_weekday(weekday_name: str) -> datetime:
    today = datetime.now()
    target_weekday = weekdays[weekday_name]

    days_ahead = target_weekday - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7

    return today + timedelta(days=days_ahead)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Сегодня":
        res = data_manager.get_date_lessons(datetime.now())
        await update.message.reply_text((res), parse_mode="HTML")
        return
    if text == "Завтра":
        res = data_manager.get_date_lessons(datetime.now() + timedelta(days=1))
        await update.message.reply_text((res), parse_mode="HTML")
        return
    else:
        res = data_manager.get_date_lessons(next_weekday(text).date())
        await update.message.reply_text((res), parse_mode="HTML")
        return
if __name__ == '__main__':
    schedule_bot()
    app = ApplicationBuilder().token(bot_api_key).build()
    
    app.add_handler(CommandHandler('start', cmd_start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    app.run_polling()