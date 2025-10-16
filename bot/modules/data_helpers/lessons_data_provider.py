import json
from pathlib import Path
from datetime import datetime

import bot.modules.info_and_debug.logger as logger
import bot.modules.date_helpers.date_time_helper as dtc

class LessonData:
    def __init__(
            self, 
            schedules_nf_msg:str,
            no_lessons_msg:str, 
            sch_data: Path
        ):
        self.schedules_nf = schedules_nf_msg or ''
        self.no_lessons = no_lessons_msg or ''
        self.sch_data = sch_data or Path()
        self.dateHelper = dtc.DateHelper()

    def validate_scedule_file(self) -> tuple[bool, str]:
        f_path = self.sch_data

        if f_path.exists() and f_path.stat().st_size > 0:
            with open(f_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
                return (True, existing_data)
        else:
            logger.LogError(f'Schedule file not found at path: {f_path}')
            return (False, self.schedules_nf)


    def get_lessons_at_date(self, date: datetime) -> str:
        validity = self.validate_scedule_file()
        if not validity[0]:
            logger.appendLog(validity[1], './bot/bot_data/logs/errorLog.txt')
            return validity[1]
        else:
            existing_data = validity[1]

        formatted_date = self.dateHelper.convert_date_to_usurt_format(date)

        existing_days = {item["day"] for item in existing_data}

        result = ""
        for item in existing_data:
            if item["day"] == formatted_date:
                result += f'<u>{formatted_date}</u>\n\n'

                if (not item["lessons"]):
                    return self.no_lessons
                
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
            return self.schedules_nf

        return result