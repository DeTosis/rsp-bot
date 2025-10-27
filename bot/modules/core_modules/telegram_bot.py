from telegram.ext import ApplicationBuilder, CommandHandler, filters, MessageHandler, filters
from telegram.error import NetworkError, TimedOut
from pathlib import Path
import asyncio

from bot.modules.core_modules.bot_commands import BotCommands
from bot.modules.data_helpers.lessons_data_provider import LessonData
from bot.modules.date_helpers.date_time_helper import DateHelper

class TelegramBot():

    def __init__(self, bot_api_key:str):
        self.bot_api_key = bot_api_key        

    async def start(self):
        self.app = ApplicationBuilder().token(self.bot_api_key).build()

        self.app.add_handler(CommandHandler(
            'start', 
            lambda update, context:
            self.commands_handler.start(update, context, self.welcome_msg)
        ))
        self.app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.commands_handler.handle_message))

        await self.app.initialize()
        await self.app.start()

        print('[ INFO ] Bot started')
        try:
            await self.app.updater.start_polling()
            await asyncio.Event().wait()

        except (NetworkError, TimedOut, TimeoutError):
            await self.shutdown()
            print('[ INFO ] Network error rised')
            return

        except asyncio.CancelledError:
            await self.shutdown()
            print('[ INFO ] Bot task cancelled')
            return

    async def shutdown(self):
        await self.app.updater.stop()
        await self.app.stop()
        await self.app.shutdown()

    async def telegram_bot(self):
        self.welcome_msg = "Бот создан для получения расписания группы ИТ-125, ЭТФ"
        schdeule_nf_msg = "❌ Расписание на день не найдено"
        no_lessons_msg = "❌ Расписание на день не найдено\n Или нет пар"

        schedule_dir = './bot/bot_data/schedules/parsed'
        schedule_file = 'schedules.json'
        schedules_path = Path(schedule_dir) / schedule_file

        logs_dir = './bot/bot_data/logs'
        logs_file = 'log.json'
        logs_path = Path(logs_dir) / logs_file
        resent_file = 'resent.txt'
        self.resent_path = Path(logs_dir) / resent_file

        lesson_data = LessonData(schdeule_nf_msg, no_lessons_msg, schedules_path)
        date_helper = DateHelper()
        self.commands_handler = BotCommands(lesson_data, date_helper, logs_path, self.resent_path) 
        await self.start()