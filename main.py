import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
FLOWISE_URL = os.getenv("CHATFLOW_URL")

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    requests.post(url, json=payload)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        user_message = data["message"]["text"]
        chat_id = data["message"]["chat"]["id"]

        response = requests.post(FLOWISE_URL, json={"question": user_message})
        if response.status_code == 200:
            answer = response.json().get("text")
            if not answer:
                answer = "Flowise 沒有回應，請稍後再試。"
        else:
            answer = "Flowise 連線失敗。"

        send_telegram_message(chat_id, answer)

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
