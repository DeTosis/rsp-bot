from telegram import Update 
from telegram.ext import ContextTypes
from pathlib import Path
import os
import json

def appendLog(data:str, path:str):
    if os.path.exists(path):
        with open(path, 'a', encoding="utf-8") as logFile:
            logFile.write(data)
    else:
        with open(path, 'w', encoding="utf-8") as logFile:
            logFile.write(data)

def appendLog_with_user_data(update: Update, context: ContextTypes.DEFAULT_TYPE, hashLength: int, logPath: Path):
    user = update.message.from_user
    user_id = str(user.id)
    user_name = user.full_name
    msg_date = update.message.date.isoformat()
    text = update.message.text

    if logPath.exists() and logPath.stat().st_size > 0:
        with logPath.open("r", encoding="utf-8") as f:
            log_data = json.load(f)
    else:
        log_data = {}

    if user_id not in log_data:
        log_data[user_id] = []

    log_data[user_id].append({
        "name": user_name,
        "date": msg_date,
        "msg": text
    })
    
    with logPath.open("w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=4, ensure_ascii=False)

def LogError(msg: str): print(f' [ ERR  ] {msg}')
def LogWarn(msg: str) : print(f' [ WARN ] {msg}')
def LogInfo(msg: str) : print(f' [ INFO ] {msg}')