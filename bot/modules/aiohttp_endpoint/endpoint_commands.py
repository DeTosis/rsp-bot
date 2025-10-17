import asyncio

from bot.modules.core_modules.telegram_bot import TelegramBot

TASKS = []

async def shutdown():
    bot_task = None
    for t in asyncio.all_tasks():
        if t.get_name() == 'bot_task':
            bot_task = t
            break

    if bot_task == None or not bot_task in TASKS:
        print('[ WARN ] Bot task is not running')
        return

    if bot_task and not bot_task.done():
        print('[ INFO ] Shutting down the bot')
        if bot_task in TASKS:
            TASKS.remove(bot_task)

        bot_task.cancel()
        await bot_task

async def start(bot: TelegramBot):
    for t in asyncio.all_tasks():
        if t.get_name() == 'bot_task':
            print('[ WARN ] Bot task is already running')
            return

    print('[ INFO ] Starting up the bot')
    bot_task = asyncio.create_task(bot.start(), name='bot_task')
    TASKS.append(bot_task)