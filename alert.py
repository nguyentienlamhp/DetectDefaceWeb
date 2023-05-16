import imghdr
import os
import smtplib
import sys
from datetime import datetime
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formataddr
from email.utils import make_msgid
from email.utils import formatdate

import base64
import requests
import json

from telegram import Bot

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import FlaskApp.database as database

db = database.Database("setting")

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


class Alert:
    def sendMessageToEndpoint(self, url, receiver, deface, message, imagePath=None, id_domain=None):
        endpoint = os.environ["API_URL"]
        print("endpoint: " + endpoint)
        base64String = ""

        if(imagePath is not None):
            with open(imagePath, "rb") as f:
                file_data = f.read()
                base64_bytes = base64.b64encode(file_data)
                #base64String = base64_bytes.decode('ascii')
                base64String = base64_bytes.decode('utf-8')
                #base64String = base64.b64encode(file_data).decode('utf-8')
                
        headers = {'content-type': 'application/json'}
        #payload = {'domain':url,'type': 4, 'metadata': {'receiver':receiver,'base64String': base64String,'deface': deface}, 'message': message}
        #payload = {'domain':url,'type': 4,'base64String': base64String,'deface': deface,'message': message}
        payload = {"domain":url,"type": 4, "imagePath": imagePath, "deface": deface,"message": message, "id_deaface_map": id_domain}
        r = requests.post(endpoint, data=json.dumps(payload), headers=headers)
        print(r.status_code)
        print(r.reason)

    def sendMessage(self, receiver, subject, message, imagePath=None):
        for data in db.get_multiple_data():
            if "smtp" not in data:
                smtpArray = []
            else:
                smtpArray = data["smtp"]
        if len(smtpArray) == 0:
            return "1"
        for smtp in smtpArray:
            EMAIL_SERVER = smtp["smtp_server"]
            EMAIL_ADDRESS = smtp["smtp_address"]
            EMAIL_PASSWORD = smtp["smtp_password"]

        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        #msg['To'] = COMMASPACE.join(receiver)
        msg['Date'] = formatdate(localtime=True)
        msg['To'] = receiver
        msg['Subject'] = subject

        msg.attach(MIMEText(message))

        try:
            if imagePath is not None:
                with open(imagePath, "rb") as f:
                    file_data = f.read()
                    file_type = imghdr.what(f.name)
                    part = MIMEApplication(
                        f.read(),
                        Name=f.name
                    )
                    part['Content-Disposition'] = 'attachment; filename="%s"' % f.name
                    msg.attach(part)
                    # msg.add_attachment(
                    #     file_data, maintype="image", subtype=file_type, filename="Website image"
                    # )
            # with smtplib.SMTP_SSL(EMAIL_SERVER, 465) as smtp:
            with smtplib.SMTP(EMAIL_SERVER, 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                # smtp.send_message(msg)
                smtp.encode()
                smtp.sendmail(EMAIL_ADDRESS, receiver, msg.as_string())
                smtp.close()
        except smtplib.SMTPException as e:
            print(e)

    def sendBot(self, url, img_path):
        for data in db.get_multiple_data():
            if "telegram" not in data:
                telegramArray = []
            else:
                telegramArray = data["telegram"]

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if len(telegramArray) == 0:
            return "1"
        for telegram in telegramArray:
            CHAT_ID = telegram["chat_id"]
            TOKEN = telegram["token"]

        bot = Bot(TOKEN)
        try:
            bot.sendPhoto(
                CHAT_ID,
                photo=open(img_path, "rb"),
                caption="⚠️"
                + "Website "
                + url
                + " was defaced!\n"
                + "At "
                + current_time,
            )
        except:
            print("Looks like CHAT_ID or TOKEN of telegram-bot was wrong!")

    def getBotInfo(self, CHAT_ID, TOKEN):
        try:
            #bot1 = Bot(TOKEN)
            #first_name = bot1.getMe().first_name
            #title = bot1.getChat(CHAT_ID).title
            #return first_name, title
            return TOKEN, CHAT_ID
        except:
            return "ERROR"


# alert = Alert()
# print(alert.getBotInfo())
