require('dotenv').config();
const axios = require('axios');
const TelegramBot = require('node-telegram-bot-api');

// Загружаем API-ключи из переменных окружения
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const TELEGRAM_CHAT_ID = process.env.TELEGRAM_CHAT_ID;

const COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price";
const COINS = ["ethereum", "solana", "act-i-the-ai-prophecy", "pepe", "bonk"]; // Укажи нужные монеты
const CURRENCY = "usd";

const bot = new TelegramBot(TELEGRAM_BOT_TOKEN);

async function getCryptoPrices() {
    let prices = {};
    try {
        const response = await axios.get(COINGECKO_API_URL, {
            params: {
                ids: COINS.join(","), // Запрос сразу для нескольких монет
                vs_currencies: CURRENCY
            }
        });

        for (const coin of COINS) {
            if (response.data[coin]) {
                prices[coin] = parseFloat(response.data[coin][CURRENCY]);
            } else {
                console.warn(`⚠️ Монета ${coin} не найдена на CoinGecko`);
            }
        }
    } catch (error) {
        console.error('❌ Ошибка при получении данных с Binance:', error);
    }
    return prices;
}

async function sendCryptoUpdate() {
    console.log("🚀 Бот запущен!");

    const prices = await getCryptoPrices();
    if (Object.keys(prices).length === 0) {
        //await bot.sendMessage(TELEGRAM_CHAT_ID, '⚠️ Ошибка получения данных с Binance.');
        return;
    }

    let message = '📊 *Криптосводка:*\n\n' +
        Object.entries(prices).map(([symbol, price]) => `${symbol}: ${price} USDT`).join('\n');

    await bot.sendMessage(TELEGRAM_CHAT_ID, message, { parse_mode: 'Markdown' });
}

sendCryptoUpdate();
