# ai_lure.py
import random
from datetime import datetime

LURES = {
    "instagram": [
        "Hey {name}, your account was flagged at {time}. Verify now: {link}",
        "{name}, someone tried to log in from {device}. Secure it: {link}"
    ],
    "linkedin": [
        "{name}, [CEO] wants to connect. Accept: {link}",
        "47 recruiters viewed your profile. Update: {link}"
    ],
    "facebook": [
        "{name}, your account is at risk. Appeal: {link}"
    ],
    "generic": [
        "Urgent: Session expired. Re-login: {link}"
    ]
}

def generate_lure(platform, link, name="User", company="Acme Corp", device="iPhone"):
    template = random.choice(LURES.get(platform.lower(), LURES["generic"]))
    time_str = datetime.now().strftime("%I:%M %p")
    return template.format(name=name, company=company, time=time_str, link=link, device=device)