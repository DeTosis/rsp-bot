# Cleans schedule log so it saves only last two weeks at most

from pathlib import Path
import json
from datetime import datetime, timedelta

from bot.modules.date_helpers.date_time_helper import DateHelper

schedules_dir = "./bot/bot_data/schedules/parsed/"
schedules_file = 'schedules.json' #

def cleanup():
    f_path = Path(schedules_dir, schedules_file)

    json_schedules = []
    try:
        with open(f_path, 'r', encoding="utf-8") as f:
            json_schedules = json.load(f)
    except:
        print('[ ERR ] Schedules cleanup error')
        print(f'[ >>> ] File {f_path} could not be found, open, or treated as a json')
        return
    
    dh = DateHelper()

    today = datetime.now()
    cleanup_date = today - timedelta(7)

    to_remove = []
    for item in json_schedules:
        day = item['day']
        currcurrent_date = dh.convert_usurt_format_to_date(day, 2025)

        if (currcurrent_date < cleanup_date - timedelta(1)):
            to_remove.append(item)

    json_schedules = [item for item in json_schedules if item not in to_remove]

    with open(f_path, "w", encoding="utf-8") as f:
        json.dump(json_schedules, f, ensure_ascii=False, indent=2)