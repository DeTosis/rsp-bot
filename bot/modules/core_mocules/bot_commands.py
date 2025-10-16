from telegram import Update, ReplyKeyboardMarkup 
from telegram.ext import ContextTypes
from datetime import datetime, timedelta

from data_helpers.lessons_data_provider import LessonData
from date_helpers.date_time_helper import DateHelper
import bot.modules.info_and_debug.logger as logger

class BotCommands:
    weekdays = {
        "Пн": 0,
        "Вт": 1,
        "Ср": 2,
        "Чт": 3,
        "Пт": 4,
        "Сб": 5,
        "Вс": 6
    }

    markup_keyboard = [
        ["Сегодня", "Завтра"],
        ["Пн","Вт","Ср"],
        ["Чт","Пт","Сб"]
    ]

    def __init__(self, lessonData: LessonData, dateHeper: DateHelper, logPath: str):
        self.LessonData = lessonData
        self.Datehelper = dateHeper
        self.logPath = logPath
        self.hashLength = 16

    # Initialisation command, used to introduce bot to a user
    # and initialize a onscreen markup-keyboard
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE, welcome_text: str):
        reply_markup = ReplyKeyboardMarkup(
            self.markup_keyboard,
            resize_keyboard=True,
            one_time_keyboard=False
        )

        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup
        )

        #Logging
        logger.appendLog_with_user_data(update=update)
        

# **************************************************

    # Keyboard markup message processing and response building
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        logger.appendLog_with_user_data(update=update)

        if text == "Сегодня":
            res = self.LessonData.get_lessons_at_date(datetime.now())
            await update.message.reply_text((res), parse_mode="HTML")
        if text == "Завтра":
            res = self.LessonData.get_lessons_at_date(datetime.now() + timedelta(days=1))
            await update.message.reply_text((res), parse_mode="HTML")
        elif text in self.weekdays:
            res = self.LessonData.get_lessons_at_date(self.Datehelper.next_weekday(text).date())
            await update.message.reply_text((res), parse_mode="HTML")

# **************************************************