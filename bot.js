require('dotenv').config();
const axios = require('axios');
const TelegramBot = require('node-telegram-bot-api');

// Загружаем API-ключи из переменных окружения
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const TELEGRAM_CHAT_ID = process.env.TELEGRAM_CHAT_ID;

const BINANCE_API_URL = 'https://api2.binance.com/api/v3/ticker/price';
const COINS = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT']; // Укажи свои монеты

const bot = new TelegramBot(TELEGRAM_BOT_TOKEN);

async function getCryptoPrices() {
    let prices = {};
    try {
        for (const coin of COINS) {
            const response = await axios.get(`${BINANCE_API_URL}?symbol=${coin}`, {
                proxy: {
                    host: "18.223.25.15",
                    port: 80,
                }
            });
            prices[coin] = parseFloat(response.data.price);
        }
    } catch (error) {
        console.error('❌ Ошибка при получении данных с Binance:', error);
    }
    return prices;
}

async function sendCryptoUpdate() {
    const prices = await getCryptoPrices();
    if (Object.keys(prices).length === 0) {
        await bot.sendMessage(TELEGRAM_CHAT_ID, '⚠️ Ошибка получения данных с Binance.');
        return;
    }

    let message = '📊 *Криптосводка:*\n\n' +
        Object.entries(prices).map(([coin, price]) => `${coin}: ${price} USDT`).join('\n');

    await bot.sendMessage(TELEGRAM_CHAT_ID, message, { parse_mode: 'Markdown' });
}

sendCryptoUpdate();
