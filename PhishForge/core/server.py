# core/server.py
import subprocess
import os

def start_php_server(template, port):
    os.chdir(f"sites/{template}")
    subprocess.Popen(
        ["php", "-S", f"127.0.0.1:{port}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )