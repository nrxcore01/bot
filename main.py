import os
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    text = (
        "👋 **Welcome to India’s #1 USD Exchange Platform!**\n\n"
        "Welcome to **NRXPAY** — India's most trusted & highest-paying USD exchange service.\n\n"
        "💵 **USD Exchange Rates:**\n"
        "🎮 Gaming Funds – ₹110 / USD\n"
        "📈 Stock / Investment – ₹120 / USD\n"
        "🔄 Mixed Usage – ₹124 / USD\n\n"
        "🔐 **Why NRXPAY?**\n"
        "⚡ Fastest withdrawals\n"
        "🛡️ Safest funds\n"
        "🏦 Bank account works upto limit\n"
        "💰 Refund on freeze / lien\n\n"
        "👇 Choose an option to continue:"
    )

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🚀 Join Platform", url="https://nrxpay.vercel.app/"))
    keyboard.add(types.InlineKeyboardButton("📘 Earning Guide", callback_data="guide"))
    keyboard.add(types.InlineKeyboardButton("🤝 Join as Agent", callback_data="agent"))
    keyboard.add(types.InlineKeyboardButton("❓ FAQs", callback_data="faqs"))
    keyboard.add(types.InlineKeyboardButton("🪙 Crypto Exchange", callback_data="crypto"))
    keyboard.add(types.InlineKeyboardButton("💬 Support Chat", callback_data="support"))

    await message.answer(text, parse_mode="Markdown", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'guide')
async def guide_callback(call: types.CallbackQuery):
    await call.message.answer("📘 *Earning Guide coming soon.*", parse_mode="Markdown")


@dp.callback_query_handler(lambda c: c.data == 'agent')
async def agent_callback(call: types.CallbackQuery):
    await call.message.answer("🤝 *Agent program coming soon.*", parse_mode="Markdown")


@dp.callback_query_handler(lambda c: c.data == 'faqs')
async def faqs_callback(call: types.CallbackQuery):
    await call.message.answer("❓ *FAQs coming soon.*", parse_mode="Markdown")


@dp.callback_query_handler(lambda c: c.data == 'crypto')
async def crypto_callback(call: types.CallbackQuery):
    await call.message.answer("🪙 *Crypto exchange features coming soon.*", parse_mode="Markdown")


@dp.callback_query_handler(lambda c: c.data == 'support')
async def support_callback(call: types.CallbackQuery):
    await call.message.answer("💬 *Support chat coming soon.*", parse_mode="Markdown")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
