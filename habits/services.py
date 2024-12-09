import os

import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")


def send_message(text, chat_id):
    params = {
        'text': text,
        'chat_id': chat_id,
    }
    response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', params=params)



