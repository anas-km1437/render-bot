from flask import Flask
import threading
import time
import hashlib
import json
import os
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

app = Flask(__name__)

SEEN_FILE = "seen.json"
LOG_FILE = "logs.txt"
IMAGE_FOLDER = "images"

os.makedirs(IMAGE_FOLDER, exist_ok=True)

# تحميل البيانات السابقة
if os.path.exists(SEEN_FILE):
    with open(SEEN_FILE, "r") as f:
        seen = set(json.load(f))
else:
    seen = set()


def save_seen():
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


def save_image(url, name):
    try:
        r = requests.get(url, timeout=10)
        path = f"{IMAGE_FOLDER}/{name}.jpg"
        with open(path, "wb") as f:
            f.write(r.content)
        print("IMAGE SAVED:", path)
    except Exception as e:
        print("IMAGE ERROR:", e)


def get_data():

    results = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        context = browser.new_context(
            storage_state="state.json"
        )

        page = context.new_page()

        page.goto("https://www.pinterest.com/messages/")

        page.wait_for_timeout(8000)

        html = page.content()

        soup = BeautifulSoup(html, "html.parser")

        # نصوص
        text = soup.get_text()
        results.append({"type": "text", "content": text})

        # صور
        images = soup.find_all("img")

        for img in images:
            src = img.get("src")

            if src and "http" in src:

                img_id = hashlib.md5(src.encode()).hexdigest()

                save_image(src, img_id)

                results.append({"type": "image", "content": src})

        browser.close()

    return results


def bot_loop():

    while True:

        try:
            data = get_data()

            for item in data:

                key = hashlib.md5(str(item).encode()).hexdigest()

                if key not in seen:

                    seen.add(key)

                    with open(LOG_FILE, "a", encoding="utf-8") as f:
                        f.write(str(item) + "\n\n")

                    save_seen()

                    print("NEW DATA SAVED")

        except Exception as e:
            print("ERROR:", e)

        time.sleep(60)


threading.Thread(target=bot_loop, daemon=True).start()


@app.route("/")
def home():
    return "Bot is running 24/7"


@app.route("/logs")
def logs():

    if not os.path.exists(LOG_FILE):
        return "No logs"

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return f"<pre>{f.read()}</pre>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)