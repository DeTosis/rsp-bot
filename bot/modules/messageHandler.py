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
    ["Сегодня", "Завтра", "/?"],
    ["Пн","Вт","Ср"],
    ["Чт","Пт","Сб"]
]

#command:description
sub_commands_title = "<code>✓ Дополнительные опции: (Нажать для вызова)</code>"
sub_commands = {
    "/rest":"Получить расписание на остаток недели от текущего дня (пн-сб)",
    "/all ":"Получить расписание на всю текущую неделю (пн-сб) [Следующую, если команда вызвана в воскресенье]"
}

# Initialisation command, used to introduce bot to a user
# and initialize a onscreen markup-keyboard
async def sendMarkupKeyboard(update: Update, msg: str):
    reply_markup = ReplyKeyboardMarkup(
        markup_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    await update.message.reply_text(msg,reply_markup=reply_markup, parse_mode="HTML")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, welcome_text: str):

    responded = Logger.RespondStatus.FAIL
    try:
        await sendMarkupKeyboard(update, welcome_text)
        responded = Logger.RespondStatus.SUCC
    except Exception as e:
        Logger.appendInternalLog(Logger.LogPrefix.ERR, e)
    finally:
        Logger.appendRecentRequestsLog(responded, update)

async def trySendMessage(update: Update, msg:str):
    if (not msg):
        Logger.appendInternalLog(Logger.LogPrefix.ERR, f'Response text is empty for `{update.message.text}` message')
        await trySendMessage(update, cst.INTERNAL_ERROR)
    
    responded = Logger.RespondStatus.FAIL
    try:
        await sendMarkupKeyboard(update, msg)
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
        if (datetime.now() + timedelta(days=1)).weekday() == 6:
            msg = cst.SCHEDULE_NO_LESSONS
        else:
            msg = schm.get_lessons_at_date(datetime.now() + timedelta(days=1))
    elif text in weekdays:
        msg = schm.get_lessons_at_date(schm.next_weekday(weekdays, text).date())
    elif text == "/?":
        msg += f'{sub_commands_title}\n\n'
        for i, c in enumerate(sub_commands):
            msg += f' • {c} <code>{sub_commands[c]}</code>\n'
            if i != len(sub_commands) - 1:
                msg += '\u2500' * 28 + '\n'
    else:
        msg = cst.NOT_SUPPORTED
        Logger.appendInternalLog(Logger.LogPrefix.INFO, f'Use of unsopported command `{text}`')

    await trySendMessage(update, msg)

async def rest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = ""
    if datetime.now().weekday() == 6:
        msg = f'<u>Воскресенье</u>\n{cst.SCHEDULE_NO_LESSONS}'
    else:
        i = 0
        while (datetime.now() + timedelta(days=i)).weekday() != 6:
            msg += schm.get_lessons_at_date(datetime.now() + timedelta(days=i))
            i += 1
    
    await trySendMessage(update, msg)

async def all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = ""
    if datetime.now().weekday() == 6:
        i = 1
        while (datetime.now() + timedelta(days=i)).weekday() != 6:
            msg += schm.get_lessons_at_date(datetime.now() + timedelta(days=i))
            msg += '\u2500' * 28 + '\n'
            i += 1
    else:
        i = datetime.now().weekday() * -1
        while (datetime.now() + timedelta(days=i)).weekday() != 6:
            msg += schm.get_lessons_at_date(datetime.now() + timedelta(days=i))
            msg += '\u2500' * 28 + '\n'
            i += 1
    await trySendMessage(update, msg)