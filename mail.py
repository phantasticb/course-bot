import smtplib
from email.message import EmailMessage

if __name__ == "__main__":
    msg = EmailMessage()
    msg.set_content("Test!")
    msg['From'] = 'jeff'
    msg['To'] = 'phantasticb@gmail.com'

    obj = smtplib.SMTP('localhost')
    obj.send_message(msg)