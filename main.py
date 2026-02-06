import os
import json
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ---------------------- USER DATABASE ---------------------- #
DB_FILE = "users.json"

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------------- START COMMAND ---------------------- #
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = str(message.from_user.id)
    db = load_db()

    if user_id not in db:
        db[user_id] = {"platform_id": None}
        save_db(db)
        await message.answer(
            "👋 Welcome to **NRXPAY Platform**!\n\n"
            "Before continuing, please send me your **Platform UserID** to register you."
        )
        return

    await send_main_menu(message)

# Ask for UserID
@dp.message_handler(lambda m: m.text.isdigit())
async def save_userid(message: types.Message):
    user_id = str(message.from_user.id)
    db = load_db()

    if db.get(user_id, {}).get("platform_id") is None:
        db[user_id]["platform_id"] = message.text
        save_db(db)
        await message.answer("✅ Your **Platform UserID** has been saved successfully!")
        await send_main_menu(message)
    else:
        await message.answer("✅ Your UserID is already saved.\nUse /start to open menu.")

# ---------------------- MAIN MENU ---------------------- #
async def send_main_menu(message):
    text = (
        "👋 **Welcome to India’s #1 USD Exchange Platform!**\n\n"
        "💵 **USD Exchange Rates:**\n"
        "🎮 Gaming – ₹110/USD\n"
        "📈 Stock – ₹120/USD\n"
        "🌀 Mixed – ₹124/USD\n\n"
        "👇 Choose an option:"
    )

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🚀 Join Platform", url="https://nrxpay.vercel.app/"))
    keyboard.add(types.InlineKeyboardButton("📘 Earning Guide", callback_data="guide"))
    keyboard.add(types.InlineKeyboardButton("🤝 Join as Agent", callback_data="agent"))
    keyboard.add(types.InlineKeyboardButton("🏦 Safe Deposit Earning", callback_data="safedeposit"))
    keyboard.add(types.InlineKeyboardButton("🪙 Crypto Exchange", callback_data="crypto"))
    keyboard.add(types.InlineKeyboardButton("💬 Support Chat", callback_data="support"))

    await message.answer(text, parse_mode="Markdown", reply_markup=keyboard)

# ---------------------- EARNING GUIDE ---------------------- #
@dp.callback_query_handler(lambda c: c.data == 'guide')
async def earning_guide(call: types.CallbackQuery):
    text = (
        "📘 **Earning Guide**\n\n"
        "1️⃣ **Exchange USD at Best Rates**\n"
        "• Gaming Funds – ₹110 per USD\n"
        "• Stock Funds – ₹120 per USD\n"
        "• Mixed Funds – ₹124 per USD\n\n"
        "2️⃣ **Upload Bank Accounts & Earn Daily**\n"
        "Earn up to **₹30,000/day** using current accounts and **₹1,00,000+/day** using corporate accounts.\n"
        "Use 95% of your limit with the **highest commissions**.\n\n"
        "3️⃣ **Exchange Crypto at 15–20% Profit**\n"
        "Supported: BTC, ETH, SOL, LTC\n"
        "Withdraw the safest funds at high profit.\n\n"
        "4️⃣ **Become an Agent**\n"
        "Earn **3.5%** of every user's recharge + **0.5%** account running commission."
    )

    await call.message.answer(text, parse_mode="Markdown")

# ---------------------- SAFE DEPOSIT EARNING ---------------------- #
@dp.callback_query_handler(lambda c: c.data == 'safedeposit')
async def safe_deposit(call: types.CallbackQuery):
    text = (
        "🏦 **Safe Deposit Investment Plans**\n\n"
        "📅 **50 Days** → 💰 0.7% per day\n"
        "📅 **100 Days** → 💰 1% per day\n"
        "📅 **200 Days** → 💰 1.5% per day\n\n"
        "Invest safely and earn passive daily returns. Withdraw anytime!"
    )

    await call.message.answer(text, parse_mode="Markdown")

# ---------------------- AGENT PROGRAM ---------------------- #
@dp.callback_query_handler(lambda c: c.data == 'agent')
async def agent_system(call: types.CallbackQuery):
    text = (
        "🤝 **Agent Income System**\n\n"
        "• Earn **3.5%** from each sub-user recharge\n"
        "• Earn **0.5%** from their account run commission\n"
        "• Your network earns for you 24/7!\n\n"
        "Grow your chain → Grow your income."
    )
    await call.message.answer(text, parse_mode="Markdown")

# ---------------------- CRYPTO SECTION ---------------------- #
@dp.callback_query_handler(lambda c: c.data == 'crypto')
async def crypto_exchange(call: types.CallbackQuery):
    text = (
        "🪙 **Crypto Exchange Profits**\n\n"
        "Earn **15–20% profit** on crypto → INR exchanges.\n"
        "Supported:\n"
        "• Bitcoin (BTC)\n"
        "• Ethereum (ETH)\n"
        "• Solana (SOL)\n"
        "• Litecoin (LTC)\n\n"
        "Trade smart & withdraw safely."
    )
    await call.message.answer(text, parse_mode="Markdown")

# ---------------------- SUPPORT CHAT ---------------------- #
@dp.callback_query_handler(lambda c: c.data == 'support')
async def support(call: types.CallbackQuery):
    await call.message.answer("💬 Support chat coming soon.")

# ---------------------- BOT RUN ---------------------- #
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
