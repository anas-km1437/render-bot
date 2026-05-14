from flask import Flask
import threading
import time
import hashlib
import json
import os

app = Flask(__name__)

SEEN_FILE = "seen.json"
LOG_FILE = "logs.txt"

# ===== تحميل الرسائل المحفوظة =====
if os.path.exists(SEEN_FILE):
    with open(SEEN_FILE, "r") as f:
        seen = set(json.load(f))
else:
    seen = set()


def save_seen():
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


# ===== مثال مؤقت =====
def get_data():

    # هنا لاحقًا نضع Pinterest

    return [
        "test message",
        "hello"
    ]


# ===== البوت =====
def bot_loop():

    while True:

        try:

            data = get_data()

            for msg in data:

                msg_hash = hashlib.md5(msg.encode()).hexdigest()

                if msg_hash not in seen:

                    seen.add(msg_hash)

                    with open(LOG_FILE, "a", encoding="utf-8") as f:
                        f.write(msg + "\n")

                    save_seen()

                    print("NEW:", msg)

        except Exception as e:
            print("ERROR:", e)

        time.sleep(10)


# تشغيل البوت بالخلفية
threading.Thread(target=bot_loop, daemon=True).start()


# ===== الصفحة الرئيسية =====
@app.route("/")
def home():
    return "Bot is running 24/7"


# ===== السجلات =====
@app.route("/logs")
def logs():

    if not os.path.exists(LOG_FILE):
        return "No logs"

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return f"<pre>{f.read()}</pre>"


# ===== تشغيل Flask =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)