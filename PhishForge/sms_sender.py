# sms_sender.py
from twilio.rest import Client
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

def send_sms(to, message):
    client = Client(config['twilio']['sid'], config['twilio']['token'])
    msg = client.messages.create(body=message, from_=config['twilio']['from'], to=to)
    print(f"[SMS] Sent → {msg.sid}")