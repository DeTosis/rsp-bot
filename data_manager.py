import json
from pathlib import Path
from datetime import datetime
import locale
import schedule_parsing as sp
import date_time_converter as dtc

no_res = "❌ Расписание на день не найдено"
no_les = "❌ Расписание на день не найдено\n Или нет пар"

def get_date_lessons(date: datetime) -> str:
    f_path = Path("./data/schedules.json")

    if f_path.exists() and f_path.stat().st_size > 0:
        with open(f_path, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    else:
        print("Schedule file not found")
        return no_res

    formatted_date = dtc.convert_date_to_usurt_format(date)

    existing_days = {item["day"] for item in existing_data}

    result = ""
    for item in existing_data:
        if item["day"] == formatted_date:

            result += f'<u>{formatted_date}</u>\n\n'
            if (not item["lessons"]):
                return no_les
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
        return no_res

    return result

if __name__ == '__main__':
    exit