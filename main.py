import os
import json
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("API_TOKEN not found!")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

ADMIN_ID = 5253715504

TRC20_ADDRESS = "TV1KzpGSz3foZvXgsbwyGUEDgjpguQYrMT"
BEP20_ADDRESS = "0xB83CB5ed29C30998cAc769eE7FbFBf6Fb7C79C7b"

DB_FILE = "users.json"

# ================= DATABASE ================= #

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ================= START ================= #

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = str(message.from_user.id)
    db = load_db()

    if user_id not in db:
        db[user_id] = {
            "platform_id": None,
            "balance": 0,
            "history": []
        }
        save_db(db)
        await message.answer("👋 Send your Platform UserID to register.")
        return

    await send_main_menu(message, new=True)

# ================= SAVE USER ID ================= #

@dp.message_handler(lambda m: m.text.isdigit())
async def save_userid(message: types.Message):
    user_id = str(message.from_user.id)
    db = load_db()

    if db[user_id]["platform_id"] is None:
        db[user_id]["platform_id"] = message.text
        save_db(db)
        await message.answer("✅ UserID saved successfully.")
        await send_main_menu(message, new=True)

# ================= MAIN MENU ================= #

async def send_main_menu(message, new=False):

    text = (
        "🇮🇳 NRXPAY - India's #1 USD Exchange Platform\n\n"
        "💵 Gaming: ₹110\n"
        "📈 Stock: ₹120\n"
        "🌀 Mixed: ₹124\n\n"
        "Fast Withdrawals | Safe Funds | High Commissions"
    )

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🚀 Join Platform", url="https://nrxpay.vercel.app/"))
    kb.add(types.InlineKeyboardButton("📘 Earning Guide", callback_data="guide"))
    kb.add(types.InlineKeyboardButton("🤝 Become Agent", callback_data="agent"))
    kb.add(types.InlineKeyboardButton("🏦 Safe Deposit Plans", callback_data="deposit"))
    kb.add(types.InlineKeyboardButton("🪙 Crypto Exchange", callback_data="crypto"))
    kb.add(types.InlineKeyboardButton("💳 Recharge", callback_data="recharge"))
    kb.add(types.InlineKeyboardButton("📊 Dashboard", callback_data="dashboard"))
    kb.add(types.InlineKeyboardButton("💬 Support", callback_data="support"))

    if new:
        await message.answer(text, reply_markup=kb)
    else:
        await message.edit_text(text, reply_markup=kb)

# ================= BACK ================= #

@dp.callback_query_handler(lambda c: c.data == "back")
async def back(call: types.CallbackQuery):
    await send_main_menu(call.message)

# ================= GUIDE ================= #

@dp.callback_query_handler(lambda c: c.data == "guide")
async def guide(call: types.CallbackQuery):

    text = (
        "📘 Earning Guide\n\n"
        "1️⃣ Exchange USD at Best Rates\n"
        "Gaming 110 | Stock 120 | Mix 124\n\n"
        "2️⃣ Upload Bank Accounts & Earn Daily\n"
        "Current: ₹30k+ | Corporate: ₹1L+\n\n"
        "3️⃣ Crypto Exchange 15–20% Profit\n\n"
        "4️⃣ Agent Income 3.5% + 0.5%"
    )

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("⬅ Back", callback_data="back"))

    await call.message.edit_text(text, reply_markup=kb)

# ================= DASHBOARD ================= #

@dp.callback_query_handler(lambda c: c.data == "dashboard")
async def dashboard(call: types.CallbackQuery):

    user_id = str(call.from_user.id)
    db = load_db()

    balance = db[user_id]["balance"]
    history = db[user_id]["history"]

    text = f"📊 Your Wallet\n\n💰 Balance: {balance} USD\n\n"

    if history:
        for h in history[-5:]:
            text += f"{h['type']} +{h['amount']} USD\n"
    else:
        text += "No transactions yet."

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("⬅ Back", callback_data="back"))

    await call.message.edit_text(text, reply_markup=kb)

# ================= RECHARGE ================= #

pending_txn = {}
pending_requests = {}
request_id_counter = 1

@dp.callback_query_handler(lambda c: c.data == "recharge")
async def recharge_menu(call: types.CallbackQuery):

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("TRC20", callback_data="trc20"))
    kb.add(types.InlineKeyboardButton("BEP20", callback_data="bep20"))
    kb.add(types.InlineKeyboardButton("⬅ Back", callback_data="back"))

    await call.message.edit_text("Minimum Deposit: 100 USD", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == "trc20")
async def trc20(call: types.CallbackQuery):

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Send Txn Hash", callback_data="send_trc20"))
    kb.add(types.InlineKeyboardButton("⬅ Back", callback_data="recharge"))

    await call.message.edit_text(
        f"TRC20 Address:\n`{TRC20_ADDRESS}`\n\n"
        "Deposit 100 USD or above\n\n"
        "⏳ Complete your deposit\nTime left: 04:59",
        parse_mode="Markdown",
        reply_markup=kb
    )

@dp.callback_query_handler(lambda c: c.data == "bep20")
async def bep20(call: types.CallbackQuery):

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Send Txn Hash", callback_data="send_bep20"))
    kb.add(types.InlineKeyboardButton("⬅ Back", callback_data="recharge"))

    await call.message.edit_text(
        f"BEP20 Address:\n`{BEP20_ADDRESS}`\n\n"
        "Deposit 100 USD or above\n\n"
        "⏳ Complete your deposit\nTime left: 04:59",
        parse_mode="Markdown",
        reply_markup=kb
    )

@dp.callback_query_handler(lambda c: c.data.startswith("send_"))
async def ask_txn(call: types.CallbackQuery):
    pending_txn[str(call.from_user.id)] = call.data
    await call.message.edit_text("Send your Transaction Hash.")

# ================= RECEIVE TXN ================= #

@dp.message_handler(lambda m: str(m.from_user.id) in pending_txn)
async def receive_txn(message: types.Message):

    global request_id_counter

    user_id = str(message.from_user.id)
    db = load_db()

    network = "TRC20" if "trc20" in pending_txn[user_id] else "BEP20"
    txid = message.text
    platform_id = db[user_id]["platform_id"]

    req_id = str(request_id_counter)
    request_id_counter += 1

    pending_requests[req_id] = {
        "user_id": user_id,
        "network": network,
        "txid": txid
    }

    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("✅ Approve", callback_data=f"approve_{req_id}"),
        types.InlineKeyboardButton("❌ Reject", callback_data=f"reject_{req_id}")
    )

    await bot.send_message(
        ADMIN_ID,
        f"🆕 Recharge Request\n\n"
        f"Platform ID: {platform_id}\n"
        f"Network: {network}\n"
        f"Txn: {txid}",
        reply_markup=kb
    )

    await message.answer("Waiting for admin approval.")
    pending_txn.pop(user_id)

# ================= ADMIN APPROVE ================= #

@dp.callback_query_handler(lambda c: c.data.startswith("approve_"))
async def approve(call: types.CallbackQuery):

    req_id = call.data.split("_")[1]
    if req_id not in pending_requests:
        return

    db = load_db()
    user_id = pending_requests[req_id]["user_id"]

    db[user_id]["balance"] += 100
    db[user_id]["history"].append({
        "type": "Deposit",
        "amount": 100
    })

    save_db(db)

    await bot.send_message(user_id, "🎉 Recharge Approved. 100 USD credited.")
    await call.message.edit_text("Approved ✅")

    pending_requests.pop(req_id)

# ================= ADMIN REJECT ================= #

@dp.callback_query_handler(lambda c: c.data.startswith("reject_"))
async def reject(call: types.CallbackQuery):

    req_id = call.data.split("_")[1]
    if req_id not in pending_requests:
        return

    user_id = pending_requests[req_id]["user_id"]

    await bot.send_message(user_id, "❌ Recharge Rejected.")
    await call.message.edit_text("Rejected ❌")

    pending_requests.pop(req_id)

# ================= ADMIN PANEL ================= #

@dp.message_handler(commands=['admin'])
async def admin_panel(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        return

    db = load_db()
    total_users = len(db)
    total_balance = sum(u["balance"] for u in db.values())

    text = (
        f"👑 Admin Panel\n\n"
        f"Total Users: {total_users}\n"
        f"Total Wallet Balance: {total_balance} USD\n\n"
        f"Pending Requests: {len(pending_requests)}"
    )

    await message.answer(text)

# ================= RUN ================= #

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
