from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

# إنشاء الملف إذا غير موجود
if not os.path.exists(DATA_FILE):

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)


# تحميل البيانات
def load_data():

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# حفظ البيانات
def save_data(data):

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


# الصفحة الرئيسية
@app.route("/")
def home():

    return "Pinterest Collector API is running"


# استقبال البيانات
@app.route("/add", methods=["POST"])
def add():

    try:

        new_data = request.json

        data = load_data()

        data.append(new_data)

        save_data(data)

        print("NEW DATA:", new_data)

        return jsonify({
            "status": "saved"
        })

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "error": str(e)
        })


# عرض البيانات
@app.route("/logs")
def logs():

    data = load_data()

    return jsonify(data)


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
