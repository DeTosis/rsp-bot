import os
import json
from pathlib import Path
from datetime import datetime, timedelta

import bot.constants as cst
import bot.modules.serviceLogger as Logger


MONTHS = [
    "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря"
    ]

WEEKDAYS = [
        "понедельник", "вторник", "среда", "четверг",
        "пятница", "суббота", "воскресенье"
    ]

# Returns next closes weekday including today or wraps week around +=7
def next_weekday(weekdays: dict,  weekday_name: str) -> datetime:
        today = datetime.now()
        target_weekday = weekdays[weekday_name]

        days_ahead = target_weekday - today.weekday()
        if days_ahead < 0:
            days_ahead += 7

        return today + timedelta(days=days_ahead)

def convert_date_to_usurt_format(date: datetime) -> str:
    day = f'{date.day}' if int(date.day) >= 10 else f'0{date.day}'

    formatted_date = f"{day} {MONTHS[date.month - 1]} {WEEKDAYS[date.weekday()]}"
    return formatted_date

def convert_usurt_format_to_date(date:str, year:str) -> datetime:
    data = date.split(' ')

    day = "{:02d}".format(int(data[0]))
    month = "{:02d}".format(int(MONTHS.index(data[1]) + 1))
    return datetime.strptime(f'{year} {month} {day}', '%Y %m %d')

def load_schedule_file() -> str:
    f_path = Path(os.getenv('SCHEDULES_JSON'))
    if (not f_path.exists()):
        raise Exception(f'Path for a schedule file `{f_path}` does not exist')

    if (f_path.stat().st_size == 0):
        raise Exception(f'Schedule file `{f_path}` is empty')

    with open(f_path, "r", encoding="utf-8") as f:
        existing_data = json.load(f)
        return existing_data

def get_lessons_at_date(date: datetime) -> str:
    try:
        data = load_schedule_file()
    except Exception as e:
        Logger.appendInternalLog(Logger.LogPrefix.ERR, e)
        return ""

    formatted_date = convert_date_to_usurt_format(date)

    result = ""
    for item in data:
        if item["day"] == formatted_date:
            result += f'<u>{formatted_date}</u>\n\n'

            if (not item["lessons"]):
                return cst.SCHEDULE_NO_LESSONS
            
            for lesson in item["lessons"]:
                for i, (_, details) in enumerate(lesson.items()):
                    if i == 0:
                        result += "⏰  "
                        result += f"<b>{details}</b>\n"
                    else:
                        result += f"{details}\n"
                result += '\n'
            break
    else:
        return cst.SCHEDULE_NOT_FOUND

    return result