import requests


def send_telegram_message(token, telegram_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": telegram_id,
        "text": message,
    }

    response = requests.post(url, data=data)

    return response.json()
