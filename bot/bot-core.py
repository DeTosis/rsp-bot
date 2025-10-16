from telegram.ext import ApplicationBuilder, CommandHandler, filters, MessageHandler, filters
from pathlib import Path
from dotenv import load_dotenv
import os

from bot.modules.core_modules.bot_commands import BotCommands
from bot.modules.data_helpers.lessons_data_provider import LessonData
from bot.modules.date_helpers.date_time_helper import DateHelper

bot_api_key = ""
bot_username = ""

def load_secrets():
    global bot_api_key, bot_username
    load_dotenv()
    bot_api_key = os.getenv("BOT_API_KEY")
    bot_username = os.getenv("BOT_USERNAME")

def schedule_bot():
    load_secrets()

if __name__ == '__main__':
    welcome_msg = "Бот создан для получения расписания группы ИТ-125, ЭТФ"
    schdeule_nf_msg = "❌ Расписание на день не найдено"
    no_lessons_msg = "❌ Расписание на день не найдено\n Или нет пар"

    schedule_dir = './bot/bot_data/schedules/parsed'
    schedule_file = 'schedules.json'
    schedules_path = Path(schedule_dir) / schedule_file

    logs_dir = './bot/bot_data/logs'
    logs_file = 'log.json'
    logs_path = Path(logs_dir) / logs_file

    lesson_data = LessonData(schdeule_nf_msg, no_lessons_msg, schedules_path)
    date_helper = DateHelper()
    commands_handler = BotCommands(lesson_data, date_helper, logs_path) 
    schedule_bot()
    app = ApplicationBuilder().token(bot_api_key).build()
    
    app.add_handler(CommandHandler(
        'start', 
        lambda update, context:
        commands_handler.start(update, context, welcome_msg)
    ))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), commands_handler.handle_message))

    app.run_polling()