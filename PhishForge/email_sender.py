# email_sender.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

def send_email(to, subject, body, spoof_from):
    msg = MIMEMultipart()
    msg['From'] = spoof_from
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP(config['smtp']['server'], config['smtp']['port'])
    server.starttls()
    server.login(config['smtp']['user'], config['smtp']['pass'])
    server.send_message(msg)
    server.quit()
    print(f"[EMAIL] Sent to {to}")