import os
import time
import requests
import telebot

# Получаем токены из GitHub Secrets
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# API Binance (публичный)
BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price"

# Список монет, которые отслеживаем
COINS = ["ACTUSDT", "ETHUSDT", "SOLUSDT"]  # Добавь свои монеты

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def get_crypto_prices():
    prices = {}
    for coin in COINS:
        response = requests.get(f"{BINANCE_API_URL}?symbol={coin}")
        if response.status_code == 200:
            data = response.json()
            prices[coin] = float(data["price"])
    return prices

def send_crypto_update():
    prices = get_crypto_prices()
    message = "\n".join([f"{coin}: {price} USDT" for coin, price in prices.items()])
    bot.send_message(TELEGRAM_CHAT_ID, f"📊 *Криптосводка на сегодня:*\n\n{message}", parse_mode="Markdown")

if __name__ == "__main__":
    while True:
        send_crypto_update()
        time.sleep(12 * 60 * 60)  # Отправлять раз в 12 часов
