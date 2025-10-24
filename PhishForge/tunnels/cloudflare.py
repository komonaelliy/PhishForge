# tunnels/cloudflare.py
import re
import time
import subprocess

def start_tunnel(port):
    proc = subprocess.Popen(
        ["./tunnels/cloudflared", "tunnel", "--url", f"http://localhost:{port}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(8)
    output = proc.stdout.read().decode()
    match = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", output)
    return match.group(0) if match else "TUNNEL FAILED"