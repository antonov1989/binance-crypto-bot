import os
import requests
import telebot  # ✅ Этот импорт теперь будет работать

# Получаем токены
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")

# Проверка, что токены загружены
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("❌ Ошибка: TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID не установлены!")

# Binance API
BINANCE_API_URL = "https://api2.binance.com/api/v3/ticker/price"
COINS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def get_crypto_prices():
    prices = {}
    for coin in COINS:
        try:
            response = requests.get(f"{BINANCE_API_URL}?symbol={coin}", timeout=5)
            response.raise_for_status()
            data = response.json()
            prices[coin] = float(data["price"])
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении {coin}: {e}")
    return prices

def send_crypto_update():
    prices = get_crypto_prices()
    if not prices:
        bot.send_message(TELEGRAM_CHAT_ID, "⚠️ Ошибка получения данных с Binance.")
        return

    message = "\n".join([f"{coin}: {price} USDT" for coin, price in prices.items()])
    bot.send_message(TELEGRAM_CHAT_ID, f"📊 *Криптосводка:*\n\n{message}", parse_mode="Markdown")

if __name__ == "__main__":
    send_crypto_update()
