import os
import yaml
import traceback
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils.gen_utils import get_logger

with open("configs/global.yml", "r") as target:
    glob_cnfg = yaml.load(target, Loader=yaml.FullLoader)

gmailc = glob_cnfg.get("gmailc")
CREDS = gmailc.get("gservice_acc")
LOGF = glob_cnfg.get("logs")
SUB = gmailc.get("subject")
FROM = gmailc.get("from")
PASS = gmailc.get("pass")
TEXT1 = gmailc.get("text1")
TEXT2 = gmailc.get("text2")
THRESH = gmailc.get("threshold")

if not os.path.exists(LOGF): os.makedirs(LOGF)
logger = get_logger("{}/emailer.log".format(LOGF))

def create_message(to, score):
    message = MIMEMultipart()
    message['From'] = FROM
    message['To'] = to
    message['Subject'] = SUB
    text = TEXT1.format(score.get("ret_score"))
    if score.get("log_score") >= THRESH:
        text = TEXT2.format(score.get("ret_score"))
    message.attach(MIMEText(text, 'plain'))
    return message

def send_email(to, score):
    message = create_message(to, **{"score": score})
    try:
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(FROM, PASS)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(FROM, to, text)
        session.quit()
        logger.info('Mail Sent to [{}], Mail Info [{}]'.format(to, text))
    except Exception as err:
        logger.error("Exception occured, mail not sent. [{}]".format(traceback.format_exc()))
