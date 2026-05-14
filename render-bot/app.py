from flask import Flask
import threading
import time
import hashlib
import json
import os
import requests

app = Flask(__name__)

SEEN_FILE = "seen.json"
LOG_FILE = "logs.txt"

# ===== TELEGRAM =====
ENABLE_TELEGRAM = False

BOT_TOKEN = "PUT_TOKEN_HERE"
CHAT_ID = "PUT_CHAT_ID_HERE"

# ====================

# تحميل البيانات القديمة
if os.path.exists(SEEN_FILE):
    with open(SEEN_FILE, "r") as f:
        seen = set(json.load(f))
else:
    seen = set()


def save_seen():
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


def send_telegram(msg):
    if not ENABLE_TELEGRAM:
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    try:
        requests.post(url, data=data)
    except:
        pass


# ===== مصدر البيانات =====
def get_data():

    # مثال تجريبي
    # هنا ضع API أو scraping أو أي مصدر

    return [
        "message 1",
        "message 2",
        "message 3"
    ]


# ===== البوت الرئيسي =====
def bot_loop():

    while True:

        try:
            data = get_data()

            for msg in data:

                msg_hash = hashlib.md5(msg.encode()).hexdigest()

                if msg_hash not in seen:

                    seen.add(msg_hash)

                    print("NEW:", msg)

                    with open(LOG_FILE, "a", encoding="utf-8") as f:
                        f.write(msg + "\n")

                    save_seen()

                    send_telegram(f"NEW MESSAGE:\n{msg}")

        except Exception as e:
            print("ERROR:", e)

        time.sleep(10)


# تشغيل البوت بالخلفية
threading.Thread(target=bot_loop).start()


# ===== Flask =====
@app.route("/")
def home():
    return "Bot is running 24/7"


@app.route("/logs")
def logs():

    if not os.path.exists(LOG_FILE):
        return "No logs yet"

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return f"<pre>{f.read()}</pre>"


# تشغيل السيرفر
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)