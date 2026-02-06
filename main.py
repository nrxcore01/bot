import os
import json
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("API_TOKEN not found in environment!")

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
            "Please send your **Platform UserID** to register you."
        )
        return

    await send_main_menu(message, new=True)

# ---------------------- SAVE USER ID ---------------------- #
@dp.message_handler(lambda m: m.text.isdigit())
async def save_userid(message: types.Message):
    user_id = str(message.from_user.id)
    db = load_db()

    if db.get(user_id, {}).get("platform_id") is None:
        db[user_id]["platform_id"] = message.text
        save_db(db)
        await message.answer("✅ Your Platform **UserID saved successfully!**")
        await send_main_menu(message, new=True)
    else:
        await message.answer("✅ Your UserID is already saved.\nUse /start to open menu.")

# ---------------------- MAIN MENU ---------------------- #
async def send_main_menu(message, new=False):

    text = (
        "👋 **Welcome to India’s #1 USD Exchange Platform!**\n\n"
        "💵 **USD Exchange Rates:**\n"
        "🎮 Gaming – ₹110/USD\n"
        "📈 Stock – ₹120/USD\n"
        "🌀 Mixed – ₹124/USD\n\n"
        "👇 Choose an option:"
    )

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🚀 Join Platform", url="https://nrxpay.vercel.app/"))
    kb.add(types.InlineKeyboardButton("📘 Earning Guide", callback_data="guide"))
    kb.add(types.InlineKeyboardButton("🤝 Become Agent", callback_data="agent"))
    kb.add(types.InlineKeyboardButton("🏦 Safe Deposit Earning", callback_data="safedeposit"))
    kb.add(types.InlineKeyboardButton("🪙 Crypto Exchange", callback_data="crypto"))
    kb.add(types.InlineKeyboardButton("💬 Support Chat", callback_data="support"))
    kb.add(types.InlineKeyboardButton("💳 Recharge", callback_data="recharge"))

    if new:
        await message.answer(text, parse_mode="Markdown", reply_markup=kb)
    else:
        await message.edit_text(text, parse_mode="Markdown", reply_markup=kb)

# ---------------------- BACK BUTTON ---------------------- #
def back_button():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("⬅ Back to Menu", callback_data="back"))
    return kb

@dp.callback_query_handler(lambda c: c.data == "back")
async def go_back(call: types.CallbackQuery):
    await send_main_menu(call.message)

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
        "• Earn up to **₹30,000/day** (current accounts)\n"
        "• Earn up to **₹1,00,000+/day** (corporate accounts)\n"
        "• Use 95% limit + highest commissions\n\n"
        "3️⃣ **Crypto Exchange Profit (15–20%)**\n"
        "• BTC, ETH, SOL, LTC supported\n\n"
        "4️⃣ **Become an Agent**\n"
        "• Earn 3.5% recharge commission\n"
        "• Earn 0.5% run-life commission"
    )

    await call.message.edit_text(text, parse_mode="Markdown", reply_markup=back_button())

# ---------------------- SAFE DEPOSIT ---------------------- #
@dp.callback_query_handler(lambda c: c.data == 'safedeposit')
async def safe_deposit(call: types.CallbackQuery):

    text = (
        "🏦 **Safe Deposit Investment Plans**\n\n"
        "📅 50 Days → 💰 0.7% Daily\n"
        "📅 100 Days → 💰 1% Daily\n"
        "📅 200 Days → 💰 1.5% Daily\n\n"
        "Withdraw anytime. Instant safe earnings."
    )

    await call.message.edit_text(text, parse_mode="Markdown", reply_markup=back_button())

# ---------------------- AGENT SYSTEM ---------------------- #
@dp.callback_query_handler(lambda c: c.data == 'agent')
async def agent_system(call: types.CallbackQuery):

    text = (
        "🤝 **Agent Income System**\n\n"
        "• Earn **3.5%** from sub-user recharges\n"
        "• Earn **0.5%** account run commissions\n"
        "• Build network & earn lifetime!"
    )

    await call.message.edit_text(text, parse_mode="Markdown", reply_markup=back_button())

# ---------------------- CRYPTO ---------------------- #
@dp.callback_query_handler(lambda c: c.data == 'crypto')
async def crypto_exchange(call: types.CallbackQuery):

    text = (
        "🪙 **Crypto Exchange Profits (15–20%)**\n\n"
        "Supported Coins:\n"
        "• Bitcoin (BTC)\n"
        "• Ethereum (ETH)\n"
        "• Solana (SOL)\n"
        "• Litecoin (LTC)\n\n"
        "High-profit safe conversion to INR."
    )

    await call.message.edit_text(text, parse_mode="Markdown", reply_markup=back_button())

# ---------------------- SUPPORT ---------------------- #
@dp.callback_query_handler(lambda c: c.data == 'support')
async def support(call: types.CallbackQuery):

    await call.message.edit_text(
        "💬 Support chat coming soon...",
        reply_markup=back_button()
    )

# ================================================================= #
#                          RECHARGE SYSTEM                          #
# ================================================================= #

ADMIN_ID = 5253715504

TRC20_ADDRESS = "TV1KzpGSz3foZvXgsbwyGUEDgjpguQYrMT"
BEP20_ADDRESS = "0xB83CB5ed29C30998cAc769eE7FbFBf6Fb7C79C7b"

pending_txn = {}  # user_id → network

# Menu
@dp.callback_query_handler(lambda c: c.data == 'recharge')
async def recharge_menu(call: types.CallbackQuery):

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("TRC20 (USDT)", callback_data="net_trc20"))
    kb.add(types.InlineKeyboardButton("BEP20 (USDT)", callback_data="net_bep20"))
    kb.add(types.InlineKeyboardButton("⬅ Back", callback_data="back"))

    await call.message.edit_text(
        "💳 **Choose Recharge Network**\n\n"
        "Minimum deposit: **100 USD**\n"
        "Funds auto-added after confirmation.",
        parse_mode="Markdown",
        reply_markup=kb
    )

# TRC20
@dp.callback_query_handler(lambda c: c.data == "net_trc20")
async def trc20_selected(call: types.CallbackQuery):

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Copy Address", url=f"https://t.me/share/url?url={TRC20_ADDRESS}"))
    kb.add(types.InlineKeyboardButton("Send Txn Hash", callback_data="send_txn_trc20"))
    kb.add(types.InlineKeyboardButton("⬅ Back", callback_data="recharge"))

    await call.message.edit_text(
        f"🧾 **TRC20 Deposit Details**\n\n"
        f"🔗 **Address:** `{TRC20_ADDRESS}`\n"
        f"💰 Deposit **100 USD or above**\n"
        f"🟢 Auto-added after confirmation\n\n"
        f"⏳ **Complete your deposit**\n"
        f"Time left: 04:59",
        parse_mode="Markdown",
        reply_markup=kb
    )

# BEP20
@dp.callback_query_handler(lambda c: c.data == "net_bep20")
async def bep20_selected(call: types.CallbackQuery):

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Copy Address", url=f"https://t.me/share/url?url={BEP20_ADDRESS}"))
    kb.add(types.InlineKeyboardButton("Send Txn Hash", callback_data="send_txn_bep20"))
    kb.add(types.InlineKeyboardButton("⬅ Back", callback_data="recharge"))

    await call.message.edit_text(
        f"🧾 **BEP20 Deposit Details**\n\n"
        f"🔗 **Address:** `{BEP20_ADDRESS}`\n"
        f"💰 Deposit **100 USD or above**\n"
        f"🟢 Auto-added after confirmation\n\n"
        f"⏳ **Complete your deposit**\n"
        f"Time left: 04:59",
        parse_mode="Markdown",
        reply_markup=kb
    )

# Ask Txn Hash
@dp.callback_query_handler(lambda c: c.data.startswith("send_txn"))
async def ask_txn(call: types.CallbackQuery):

    user_id = str(call.from_user.id)

    if call.data == "send_txn_trc20":
        pending_txn[user_id] = "TRC20"
    else:
        pending_txn[user_id] = "BEP20"

    await call.message.edit_text(
        "📨 **Send your Transaction Hash (Txn ID)**\n"
        "Reply here with the Txn ID after transferring.",
        parse_mode="Markdown",
        reply_markup=back_button()
    )

# Receive Txn Hash
@dp.message_handler(lambda m: str(m.from_user.id) in pending_txn)
async def receive_txn(message: types.Message):

    user_id = str(message.from_user.id)
    db = load_db()

    network = pending_txn[user_id]
    txid = message.text
    platform_id = db[user_id]["platform_id"]

    await bot.send_message(
        ADMIN_ID,
        f"🆕 **New Recharge Request**\n\n"
        f"📌 Platform ID: `{platform_id}`\n"
        f"🌐 Network: **{network}**\n"
        f"🔗 Txn ID: `{txid}`",
        parse_mode="Markdown"
    )

    await message.answer(
        "✅ **Your transaction has been submitted!**\n"
        "It will be verified shortly.",
        parse_mode="Markdown"
    )

    pending_txn.pop(user_id, None)

# ---------------------- RUN BOT ---------------------- #
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
