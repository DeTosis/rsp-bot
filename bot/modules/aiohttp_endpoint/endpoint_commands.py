import asyncio
from telegram import Bot

import os
from pathlib import Path
import json

from bot.modules.botCore import TelegramBot

TASKS = []

async def shutdown() -> str:
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
    
    return "done"

async def start(bot: TelegramBot):
    for t in asyncio.all_tasks():
        if t.get_name() == 'bot_task':
            print('[ WARN ] Bot task is already running')
            return

    print('[ INFO ] Starting up the bot')
    bot_task = asyncio.create_task(bot.start(), name='bot_task')
    TASKS.append(bot_task)

async def validate() -> bool:
    token = os.getenv('BOT_API_KEY')
    bot = Bot(token=token)
    try:
        validity = await bot.get_me()
        return True
    except Exception as e:
        print(f'[ ERR ] Exception [{e}] rised while trying to validate bot state')
        return False
    #return any(t.get_name() == 'bot_task' for t in asyncio.all_tasks())

async def retriveRecent(bot: TelegramBot) -> list:
    json_list = []
    with open(bot.resent_path, 'r', encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(maxsplit=4)
            if len(parts) != 5:
                continue 

            timestamp = parts[3].split('+')[0]

            record = {
                "id": int(parts[0]),
                "name": parts[1],
                "timestamp": parts[2] + ' ' + timestamp,
                "msg": parts[4]
            }
            json_list.append(record)

    json_list = list(reversed(json_list))
    return json_list

async def retriveSchedules():
    sch_path_str = os.getenv('PARSED_SCHEDULES')
    if not sch_path_str:
        print('[ ERR ] Schedule file could not be found')
        return {'error:' 'file not found'}
    
    sch_path = Path(sch_path_str)
    with sch_path.open("r", encoding="utf-8") as f:
        log_data = json.load(f)
        return log_data