from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)


def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


@app.route("/")
def home():
    return "Pinterest Collector API is running"


# استقبال الرسائل من الإضافة
@app.route("/add", methods=["POST"])
def add():

    new_data = request.json

    data = load_data()
    data.append(new_data)

    save_data(data)

    return jsonify({"status": "saved"})


# عرض البيانات
@app.route("/logs")
def logs():

    data = load_data()

    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)