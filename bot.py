import requests
import telebot
import time

# API токен бота (замени на свой)
TELEGRAM_BOT_TOKEN = "7674187229:AAH5JrO3tq_tb5HVVC0yG6pGhudg0NsXzZk"

# ID чата (чтобы бот отправлял сообщения только тебе)
TELEGRAM_CHAT_ID = "563527435"

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
