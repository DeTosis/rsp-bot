from dotenv import load_dotenv
import os

import asyncio

from bot.modules.aiohttp_endpoint.ui_endpoint import ServerEndpoint
from bot.modules.core_modules.telegram_bot import TelegramBot
import bot.modules.aiohttp_endpoint.endpoint_commands as ec

import bot.modules.data_helpers.schedule_file_cleaner as sfc

bot_api_key = ""
web_ui_port = 7901

def load_secrets():
    global bot_api_key, bot_username
    load_dotenv()
    bot_api_key = os.getenv("BOT_API_KEY")

async def run(bot: TelegramBot, server: ServerEndpoint):

    bot_task = asyncio.create_task(bot.telegram_bot(), name='bot_task') 
    server_task = asyncio.create_task(server.bot_server(), name='server_task') 

    ec.TASKS.append(bot_task)
    ec.TASKS.append(server_task)

    await asyncio.gather(*ec.TASKS)

if __name__ == '__main__':
    load_secrets()
    sfc.cleanup()

    bot = TelegramBot(bot_api_key)
    server = ServerEndpoint(web_ui_port, bot)

    try:
        asyncio.run(run(bot, server))
    except KeyboardInterrupt:
        exit