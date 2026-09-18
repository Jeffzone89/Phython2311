import time

import requests

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"


class TelegramSendError(Exception):
    pass


def send_message(text, max_retries=2):
    url = TELEGRAM_API.format(token=TELEGRAM_BOT_TOKEN)
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}

    attempt = 0
    while True:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 200:
            return
        if attempt < max_retries:
            time.sleep(2 ** attempt)
            attempt += 1
            continue
        raise TelegramSendError(f"텔레그램 전송 실패: {resp.status_code} {resp.text}")
