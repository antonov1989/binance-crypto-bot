import os
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
        try:
            response = requests.get(f"{BINANCE_API_URL}?symbol={coin}")
            response.raise_for_status()
            data = response.json()
            prices[coin] = float(data["price"])
        except requests.RequestException as e:
            print(f"Ошибка при получении {coin}: {e}")
    return prices

def send_crypto_update():
    prices = get_crypto_prices()
    if not prices:
        bot.send_message(TELEGRAM_CHAT_ID, "⚠️ Ошибка получения данных с Binance.")
        return

    message = "📊 *Криптосводка на сегодня:*\n\n"
    message += "\n".join([f"💰 {coin}: `{price}` USDT" for coin, price in prices.items()])

    bot.send_message(TELEGRAM_CHAT_ID, message, parse_mode="Markdown")

if __name__ == "__main__":
    send_crypto_update()  # Одиночный запуск
