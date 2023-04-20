import imghdr
import os
import smtplib
import sys
from datetime import datetime
from email.message import EmailMessage
import requests
from telegram import Bot
import base64

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import FlaskApp.database as database

db = database.Database("setting")


class Alert:
    def sendMessageToEndpoint(self, receiver, subject, message, imagePath=None):
        endpoint=os.environ["API_URL"]
        base64String = ""
       
        if(imagePath is not None):
            with open(imagePath, "rb") as f:
                file_data = f.read()
                base64String = base64.b64encode(file_data)
                
        r = requests.post(endpoint, data={'receiver': receiver, 'subject': subject, 'message': message,"base64String":base64String})
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

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = receiver
        msg.set_content(message)

        try: 
            if imagePath is not None:
                with open(imagePath, "rb") as f:
                    file_data = f.read()
                    file_type = imghdr.what(f.name)
                msg.add_attachment(
                    file_data, maintype="image", subtype=file_type, filename="Website image"
                )
            #with smtplib.SMTP_SSL(EMAIL_SERVER, 465) as smtp:
            with smtplib.SMTP(EMAIL_SERVER, 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
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
            bot1 = Bot(TOKEN)
            first_name = bot1.getMe().first_name
            title = bot1.getChat(CHAT_ID).title
            return first_name, title
        except:
            return "ERROR"


# alert = Alert()
# print(alert.getBotInfo())
