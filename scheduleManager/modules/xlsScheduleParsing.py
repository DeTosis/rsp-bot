import pandas as pd
from io import BytesIO

def parseXLS(xls: bytes) -> list:
    parsed_data = []
    xls_data = pd.read_excel(
        BytesIO(xls), 
        header=2,
        usecols=['День', 'Часы', 'ИТ-125'],
        engine='xlrd' 
    )

    xls_data['День'] = xls_data['День'].str.replace('\n', ' ', regex=False).str.strip()
    xls_data['День'] = xls_data['День'].ffill()

    for day, df_day in xls_data.groupby('День'):
        lessons = df_day[['Часы', 'ИТ-125']].to_dict(orient='records')

        for i, hour in enumerate(lessons):
            if (pd.isna(hour.get('Часы')) and i > 0):
                hour['Часы'] = lessons[i-1].get('Часы')

        lessons = [lesson for lesson in lessons if lesson.get('ИТ-125', '').strip() != '']
        new_entry = {
            "day": day,
            "lessons": lessons
        }
        
        parsed_data.append(new_entry)
    
    return parsed_data