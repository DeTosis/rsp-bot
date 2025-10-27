from datetime import datetime, timedelta

class DateHelper:
    months = [
        "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря"
        ]

    weekdays = [
            "понедельник", "вторник", "среда", "четверг",
            "пятница", "суббота", "воскресенье"
        ]

    # Returns next closes weekday including today or wraps week around +=7
    def next_weekday(self, weekdays: dict,  weekday_name: str) -> datetime:
            today = datetime.now()
            target_weekday = weekdays[weekday_name]

            days_ahead = target_weekday - today.weekday()
            if days_ahead < 0:
                days_ahead += 7

            return today + timedelta(days=days_ahead)
    
    def convert_date_to_usurt_format(self, date: datetime) -> str:

        formatted_date = f"{date.day} {self.months[date.month - 1]} {self.weekdays[date.weekday()]}"
        return formatted_date
    
    def convert_usurt_format_to_date(self, date:str, year:str) -> datetime:
        data = date.split(' ')

        day = "{:02d}".format(int(data[0]))
        month = "{:02d}".format(int(self.months.index(data[1]) + 1))
        return datetime.strptime(f'{year} {month} {day}', '%Y %m %d')