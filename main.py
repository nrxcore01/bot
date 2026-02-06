import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import InlineKeyboardBuilder

API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(commands=["start"])
async def start_cmd(message: types.Message):

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

    kb = InlineKeyboardBuilder()
    kb.button(text="🚀 Join Platform", url="https://nrxpay.vercel.app/")
    kb.button(text="📘 Earning Guide", callback_data="guide")
    kb.button(text="🤝 Join as Agent", callback_data="agent")
    kb.button(text="❓ FAQs", callback_data="faqs")
    kb.button(text="🪙 Crypto Exchange", callback_data="crypto")
    kb.button(text="💬 Support Chat", callback_data="support")
    kb.adjust(1)

    await message.answer(text, parse_mode="Markdown", reply_markup=kb.as_markup())


@dp.callback_query(lambda c: c.data == "guide")
async def earning_guide(callback: types.CallbackQuery):
    await callback.message.answer("📘 *Earning Guide coming soon.*", parse_mode="Markdown")

@dp.callback_query(lambda c: c.data == "agent")
async def join_agent(callback: types.CallbackQuery):
    await callback.message.answer("🤝 *Agent program coming soon.*", parse_mode="Markdown")

@dp.callback_query(lambda c: c.data == "faqs")
async def faqs(callback: types.CallbackQuery):
    await callback.message.answer("❓ *FAQs coming soon.*", parse_mode="Markdown")

@dp.callback_query(lambda c: c.data == "crypto")
async def crypto_exchange(callback: types.CallbackQuery):
    await callback.message.answer("🪙 *Crypto exchange features coming soon.*", parse_mode="Markdown")

@dp.callback_query(lambda c: c.data == "support")
async def support_chat(callback: types.CallbackQuery):
    await callback.message.answer("💬 *Support chat coming soon.*", parse_mode="Markdown")


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
