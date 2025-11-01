import os
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler, filters
from telegram.error import NetworkError
import asyncio

import bot.modules.messageHandler as mh
import bot.modules.serviceLogger as Logger
import bot.constants as cst

class TelegramBot():
    def __init__(self):
        self.app = ApplicationBuilder().token(os.getenv("BOT_API_KEY")).build()
        self.addHandlers()

    def addHandlers(self):
        self.app.add_handler(CommandHandler(
            'start', 
            lambda update, context: mh.start(update, context, cst.WELCOME)
        ))
        self.app.add_handler(MessageHandler(
            filters.TEXT & (~filters.COMMAND), mh.handle_message
        ))
        self.app.add_handler(CommandHandler(
            'rest',
            lambda update, context: mh.rest(update, context)
        ))

        self.app.add_handler(CommandHandler(
            'all',
            lambda update, context: mh.all(update, context)
        ))
        return

    def error_callback(update: object, context: ContextTypes.DEFAULT_TYPE):
        if isinstance(context, NetworkError):
            Logger.appendInternalLog(Logger.LogPrefix.ERR, f"Network Error: {context}")
        else:
            Logger.appendInternalLog(Logger.LogPrefix.ERR, f"Unhandled Callback Error: {context}")
        return

    async def start(self):
        await self.app.initialize()
        await self.app.start()

        Logger.appendInternalLog(Logger.LogPrefix.INFO, 'Bot Initialized', True)

        await self.app.updater.start_polling(error_callback=self.error_callback)

        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            Logger.appendInternalLog(Logger.LogPrefix.INFO, 'Shutting down the bot', True)
            try:
                await self.shutdown()
            except Exception as e:
                Logger.appendInternalLog(Logger.LogPrefix.ERR, f'Exception rised in shutdown process: {e}')
            finally:
                Logger.appendInternalLog(Logger.LogPrefix.INFO, f'Bot shutted down', True)
            return

    async def shutdown(self):
        await self.app.updater.stop()
        await self.app.stop()
        await self.app.shutdown()
        