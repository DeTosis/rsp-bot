import pandas as pd
import json
from pathlib import Path
from pprint import pprint

schedules_dir = "./schedules/"

def parse_shedule(exc_path: str):
    f_path = Path("./data/schedules.json")

    if f_path.exists() and f_path.stat().st_size > 0:
        with open(f_path, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_days = {item["day"] for item in existing_data}

    xls_p = schedules_dir + exc_path
    data = pd.read_excel(
        xls_p, 
        header=2,
        usecols=['День', 'Часы', 'ИТ-125'],
        engine='xlrd' 
    )

    data['День'] = data['День'].str.replace('\n', ' ', regex=False).str.strip()
    data['День'] = data['День'].ffill()

    for day, df_day in data.groupby('День'):
        if day in existing_days:
            continue

        lessons = df_day[['Часы', 'ИТ-125']].to_dict(orient='records')

        for i, hour in enumerate(lessons):
            if (pd.isna(hour.get('Часы')) and i > 0):
                hour['Часы'] = lessons[i-1].get('Часы') 

        lessons = [lesson for lesson in lessons if lesson.get('ИТ-125', '').strip() != '']

        new_entry = {
            "day": day,
            "lessons": lessons
        }

        existing_data.append(new_entry)
        existing_days.add(day)

    with open(f_path, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    parse_shedule("ЭТФ 1 курс нечетная.xls")