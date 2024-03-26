import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import sys
class MailService:

    def __init__(self,subject,to,body):

        self.subject = subject
        self.to = to 
        self.body = body
        self.mailGonder()

    def mailGonder(self):
        try:
            mail = smtplib.SMTP_SSL("mail.mekmar.com",465)
            mail.login("goz@mekmar.com", "_bwt64h-3SR_-G2O")

            mesaj = MIMEMultipart()
            mesaj["From"] = "goz@mekmar.com"           # Gönderen
            mesaj["Subject"] = self.subject

            mesaj["To"] = self.to
            body_text = MIMEText(self.body, "html")  #
            mesaj.attach(body_text)
            print('Mail Başarıyla Gönderildi')
            mail.sendmail(mesaj["From"], mesaj["To"], mesaj.as_string())
            mail.close()
        except:
            print("Hata:", sys.exc_info()[0])
            

