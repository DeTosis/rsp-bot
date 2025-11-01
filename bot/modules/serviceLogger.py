from telegram import Update 

from datetime import datetime
import os
from enum import Enum
from pathlib import Path


class LogPrefix(Enum):
    INFO  = ' INFO '
    WARN  = ' WARN '
    ERR   = ' ERROR'
    FAIL  = ' FAIL '
    DEBUG = ' DEBUG'

class RespondStatus(Enum):
    SUCC  = ' SUCC '
    FAIL  = ' FAIL '

def appendInternalLog(prefix: LogPrefix, msg: str, postInTerminal: bool=False):
    f_path = Path(os.getenv('LOGS_DIR'))
    f_path.mkdir(parents=True, exist_ok=True)
    f_path = Path(f_path) / os.getenv('INTERNAL_LOG')

    res = f'{datetime.now().replace(microsecond=0)} {prefix.value} {msg}\n'
    if (postInTerminal):
        print(res[:-1])

    with open(f_path, 'a', encoding="utf-8") as f:
        f.write(res)
    
    return

def appendRecentRequestsLog(responded: RespondStatus, update: Update):
    try:
        user = update.message.from_user
        user_id = str(user.id)
        user_name = user.full_name
        msgTime = str(update.message.date.astimezone()).split('+')[0]
        text = update.message.text
    except Exception as e:
        appendInternalLog(LogPrefix.ERR, f'An error occured while trying to append request log: {e}')

    f_path = Path(os.getenv('LOGS_DIR'))
    f_path.mkdir(parents=True, exist_ok=True)
    f_path = Path(f_path) / os.getenv('USER_REQUESTS_LOG')

    with open(f_path, 'a', encoding="utf-8") as f:
        f.write(f'REQ:{msgTime} RESP:{datetime.now().replace(microsecond=0)} {responded.value} {user_id} {user_name.replace(' ', '-')} {text} \n')
    return