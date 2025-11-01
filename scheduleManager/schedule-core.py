import json
import os
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import shutil

import bot.modules.serviceLogger as Logger
import scheduleManager.modules.xlsScheduleParsing as xlsParser

def getSchedules() -> dict:
    load_dotenv()
    session = requests.Session()

    url = "https://bb.usurt.ru/"
    response = session.get(url)

    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    nonce = soup.find("input", {"name": "blackboard.platform.security.NonceUtil.nonce"})["value"]

    payload = {
        "user_id":os.getenv('LOGIN'),
        "password":os.getenv('PASSWORD'),
        "login":"Войти",
        "action":"login",
        "new_loc":"",
        "blackboard.platform.security.NonceUtil.nonce":nonce
    }

    post_url = "https://bb.usurt.ru/webapps/login/"
    response = session.post(post_url, data=payload, allow_redirects=True)

    odd = session.get(os.getenv('ODD_WEEK_URL'))
    if (odd.status_code != 200):
        raise Exception()
    
    even = session.get(os.getenv('EVEN_WEEK_URL'))
    if (even.status_code != 200):
        raise Exception()

    schedules = {
        'odd' : odd.content,
        'even' : even.content
    }
    return schedules


if __name__ == '__main__':
    try:
        schedules = getSchedules() 
    except Exception as e:
        Logger.appendInternalLog(Logger.LogPrefix.ERR, f'An error occured trying to get schedules from BlackBoard: {e}')

    status = Logger.LogPrefix.ERR
    try:
        result = []
        for x in schedules:
            result.extend(xlsParser.parseXLS(schedules[x]))

        f_path = os.getenv('SCHEDULES_JSON')

        if Path(f_path).exists:
            shutil.copyfile(f_path, f_path + '.bk.json')

        with open(f_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        status = Logger.LogPrefix.INFO
    except Exception as e:
        Logger.appendInternalLog(Logger.LogPrefix.ERR, e)
    finally:
        Logger.appendInternalLog(status, 'Schedule parsing operation complete')