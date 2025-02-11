import os
import requests
from telegram import Bot

# Получаем токены из GitHub Secrets
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# API Binance (публичный)
BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price"
COINS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def get_crypto_prices():
    prices = {}
    for coin in COINS:
        try:
            response = requests.get(
                f"{BINANCE_API_URL}?symbol={coin}",
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            prices[coin] = float(data["price"])
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении {coin}: {e}")
    return prices

def send_crypto_update():
    prices = get_crypto_prices()
    if not prices:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="⚠️ Ошибка получения данных с Binance.")
        return

    message = "\n".join([f"{coin}: {price} USDT" for coin, price in prices.items()])
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"📊 Криптосводка:\n\n{message}")

if __name__ == "__main__":
    send_crypto_update()
