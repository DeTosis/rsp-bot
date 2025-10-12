from datetime import datetime, timedelta

def convert_date_to_usurt_format(date: datetime) -> str:
    months = [
    "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря"
    ]

    weekdays = [
        "понедельник", "вторник", "среда", "четверг",
        "пятница", "суббота", "воскресенье"
    ]
    formatted_date = f"{date.day} {months[date.month - 1]} {weekdays[date.weekday()]}"
    return formatted_date

if __name__ == '__main__':
    exit