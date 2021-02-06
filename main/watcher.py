import os
import yaml
import json
import time
import gspread
import traceback
from oauth2client.service_account import ServiceAccountCredentials
from main.emailer import send_email
from utils.gen_utils import get_logger

with open("configs/global.yml", "r") as target:
    glob_cnfg = yaml.load(target, Loader=yaml.FullLoader)

gsheetc = glob_cnfg.get("gsheets")
SHEET_NAME = gsheetc.get("sheet_name")
WSHEET_NAME = gsheetc.get("wsheet_name")
SCOPE = gsheetc.get("gs_scope")
CREDS = gsheetc.get("gservice_acc")
CACHE = gsheetc.get("cache")
SLEEP = gsheetc.get("sleep")
LOGF = glob_cnfg.get("logs")
WEIGHTS = gsheetc.get("weights")

logger = get_logger("{}/watcher.log".format(LOGF))
if not os.path.exists(CACHE.split("/")[0]): os.makedirs(CACHE.split("/")[0])

creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS, SCOPE)
client = gspread.authorize(creds)

def watch(client, gsheet_n, wsheet_n):
    while True:
        # import pdb; pdb.set_trace()
        try:
            with open(CACHE, "r") as target:
                cached = json.load(target)
            cache_counter = cached.get("counter")
        except:
            cached, cache_counter = {}, 0
        try:
            gsheet = client.open(gsheet_n)
            gsheet = gsheet.worksheet(wsheet_n)
            gsheet = gsheet.get_all_records()
            counter = len(gsheet)
            for rec in gsheet[cache_counter:counter]:
                email = rec.get("Email address")
                score = calculate_score(rec)
                logger.info("email [{}], scores [{}]".format(email, score))
                send_email(email, **{"score": score})
                logger.info("Mail Sent to [{}]".format(email))
                cached.update({"counter": counter})
        except Exception as err:
            logger.error("Error occured: {}".format(traceback.format_exc()))
        if counter > cache_counter:
            with open(CACHE, "w") as target:
                json.dump(cached, target)
        time.sleep(SLEEP)

def calculate_score(rec):
    log_score = 0
    ret_score = 0
    for k,v in rec.items():
        try:
            if "how" in k.lower() and (not "buck" in k.lower()): # questions
                log_score += WEIGHTS.get(v)
                ret_score += v
        except: pass
    ret_score = 100 - float(ret_score)*100/44
    return {"log_score": int(log_score), "ret_score":int(ret_score)}


if __name__ == '__main__':
    watch(client, SHEET_NAME, WSHEET_NAME)