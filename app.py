from flask import Flask, request
import os
import requests
import json

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
WEBHOOK_SECRET = BOT_TOKEN  # для простоты, можно заменить

def send_message(chat_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    requests.post(f"{API_URL}/sendMessage", data=payload)

@app.route(f"/webhook/{WEBHOOK_SECRET}", methods=["POST"])
def webhook():
    data = request.json
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            send_message(chat_id, "Привет! Добро пожаловать в магазин сахарной пудры. Напиши /catalog чтобы посмотреть ассортимент.")
        elif text == "/catalog":
            with open("catalog.json", encoding="utf-8") as f:
                catalog = json.load(f)
            message = "📦 <b>Наши товары:</b>\n\n"
            for item in catalog:
                message += f"🔹 <b>{item['name']}</b> — {item['price']}₽\n"
            send_message(chat_id, message)
        else:
            send_message(chat_id, "Я не понимаю эту команду. Напиши /catalog чтобы посмотреть товары.")
    return "ok"
@app.route("/", methods=["GET"])
def index():
    return "Pudrovyy bot is working!"
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
