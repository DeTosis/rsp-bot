from telegram import Update, ReplyKeyboardMarkup 
from telegram.ext import ContextTypes
from datetime import datetime, timedelta

import bot.modules.scheduleManager as schm
import bot.modules.serviceLogger as Logger
import bot.constants as cst

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
    #["Вся Неделя"],
    ["Сегодня", "Завтра"],
    ["Пн","Вт","Ср"],
    ["Чт","Пт","Сб"]
]

# Initialisation command, used to introduce bot to a user
# and initialize a onscreen markup-keyboard
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, welcome_text: str):
    reply_markup = ReplyKeyboardMarkup(
        markup_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
    responded = Logger.RespondStatus.FAIL
    try:
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup
        )
        responded = Logger.RespondStatus.SUCC
    except Exception as e:
        Logger.appendInternalLog(Logger.LogPrefix.ERR, e)
    finally:
        Logger.appendRecentRequestsLog(responded, update)

# Keyboard markup message processing and response building
async def trySendMessage(update: Update, msg:str):
    if (not msg):
        Logger.appendInternalLog(Logger.LogPrefix.ERR, f'Response text is empty for `{update.message.text}` message')
        await trySendMessage(update, cst.INTERNAL_ERROR)
    
    responded = Logger.RespondStatus.FAIL
    try:
        await update.message.reply_text((msg), parse_mode="HTML")
        responded = Logger.RespondStatus.SUCC
    except Exception as e:
        Logger.appendInternalLog(Logger.LogPrefix.ERR, e)
    finally:
        Logger.appendRecentRequestsLog(responded, update)
    return

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    msg = ""
    if text == "Сегодня":
        msg = schm.get_lessons_at_date(datetime.now())
    elif text == "Завтра":
        msg = schm.get_lessons_at_date(datetime.now() + timedelta(days=1))
    elif text in weekdays:
        msg = schm.get_lessons_at_date(schm.next_weekday(weekdays, text).date())
    else:
        msg = cst.NOT_SUPPORTED
        Logger.appendInternalLog(Logger.LogPrefix.INFO, f'Use of unsopported command `{text}`')

    await trySendMessage(update, msg)