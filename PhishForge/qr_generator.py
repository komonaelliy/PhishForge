# qr_generator.py
import qrcode
import os

def generate_qr(link, filename="qr_phish.png"):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"[QR] Saved → {os.path.abspath(filename)}")