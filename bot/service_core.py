from dotenv import load_dotenv
import asyncio

from bot.modules.botCore import TelegramBot
import bot.modules.serviceLogger as Logger

if __name__ == '__main__':
    load_dotenv('.env')

    bot = TelegramBot()
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        exit
    except Exception as e:
        Logger.appendInternalLog(Logger.LogPrefix.ERR, f'Failed to start the bot: {e}')
        exit(-1)
