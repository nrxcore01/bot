import os
import json
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("API_TOKEN not found in environment!")

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
        await message.answer("Send your Platform UserID to register.")
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
        await message.answer("UserID saved ✅")
        await send_main_menu(message, new=True)

# ================= MAIN MENU ================= #

async def send_main_menu(message, new=False):

    text = (
        "👋 Welcome to NRXPAY\n\n"
        "💰 Gaming: ₹110\n"
        "📈 Stock: ₹120\n"
        "🌀 Mixed: ₹124"
    )

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("📊 Dashboard", callback_data="dashboard"))
    kb.add(types.InlineKeyboardButton("💳 Recharge", callback_data="recharge"))
    kb.add(types.InlineKeyboardButton("📘 Earning Guide", callback_data="guide"))

    if new:
        await message.answer(text, reply_markup=kb)
    else:
        await message.edit_text(text, reply_markup=kb)

# ================= DASHBOARD ================= #

@dp.callback_query_handler(lambda c: c.data == "dashboard")
async def dashboard(call: types.CallbackQuery):

    user_id = str(call.from_user.id)
    db = load_db()

    balance = db[user_id]["balance"]
    history = db[user_id]["history"]

    text = f"📊 Wallet Balance: {balance} USD\n\n"

    if history:
        text += "Recent Transactions:\n"
        for h in history[-5:]:
            text += f"{h['type']} +{h['amount']} USD\n"
    else:
        text += "No transactions yet."

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("⬅ Back", callback_data="back"))

    await call.message.edit_text(text, reply_markup=kb)

# ================= BACK ================= #

@dp.callback_query_handler(lambda c: c.data == "back")
async def go_back(call: types.CallbackQuery):
    await send_main_menu(call.message)

# ================= RECHARGE ================= #

pending_txn = {}
pending_requests = {}
request_counter = 1

@dp.callback_query_handler(lambda c: c.data == "recharge")
async def recharge_menu(call: types.CallbackQuery):

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("TRC20", callback_data="net_trc20"))
    kb.add(types.InlineKeyboardButton("BEP20", callback_data="net_bep20"))
    kb.add(types.InlineKeyboardButton("⬅ Back", callback_data="back"))

    await call.message.edit_text(
        "Minimum deposit: 100 USD",
        reply_markup=kb
    )

@dp.callback_query_handler(lambda c: c.data == "net_trc20")
async def trc20(call: types.CallbackQuery):

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Send Txn Hash", callback_data="send_trc20"))
    kb.add(types.InlineKeyboardButton("⬅ Back", callback_data="recharge"))

    await call.message.edit_text(
        f"TRC20 Address:\n`{TRC20_ADDRESS}`\n\n"
        "Deposit 100 USD or above\n"
        "⏳ Complete your deposit\nTime left: 04:59",
        parse_mode="Markdown",
        reply_markup=kb
    )

@dp.callback_query_handler(lambda c: c.data == "net_bep20")
async def bep20(call: types.CallbackQuery):

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Send Txn Hash", callback_data="send_bep20"))
    kb.add(types.InlineKeyboardButton("⬅ Back", callback_data="recharge"))

    await call.message.edit_text(
        f"BEP20 Address:\n`{BEP20_ADDRESS}`\n\n"
        "Deposit 100 USD or above\n"
        "⏳ Complete your deposit\nTime left: 04:59",
        parse_mode="Markdown",
        reply_markup=kb
    )

@dp.callback_query_handler(lambda c: c.data.startswith("send_"))
async def ask_txn(call: types.CallbackQuery):

    user_id = str(call.from_user.id)
    network = "TRC20" if "trc20" in call.data else "BEP20"

    pending_txn[user_id] = network

    await call.message.edit_text("Send your Transaction Hash.")

# ================= RECEIVE TXN ================= #

@dp.message_handler(lambda m: str(m.from_user.id) in pending_txn)
async def receive_txn(message: types.Message):

    global request_counter

    user_id = str(message.from_user.id)
    db = load_db()

    network = pending_txn[user_id]
    txid = message.text
    platform_id = db[user_id]["platform_id"]

    request_id = str(request_counter)
    request_counter += 1

    pending_requests[request_id] = {
        "user_id": user_id,
        "network": network,
        "txid": txid
    }

    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("✅ Approve", callback_data=f"approve_{request_id}"),
        types.InlineKeyboardButton("❌ Reject", callback_data=f"reject_{request_id}")
    )

    await bot.send_message(
        ADMIN_ID,
        f"Recharge Request\n"
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

    request_id = call.data.split("_")[1]

    if request_id not in pending_requests:
        return

    db = load_db()
    data = pending_requests[request_id]
    user_id = data["user_id"]

    db[user_id]["balance"] += 100

    db[user_id]["history"].append({
        "type": "Deposit",
        "amount": 100
    })

    save_db(db)

    await bot.send_message(user_id, "Recharge Approved ✅ 100 USD credited.")
    await call.message.edit_text("Approved ✅")

    pending_requests.pop(request_id)

# ================= ADMIN REJECT ================= #

@dp.callback_query_handler(lambda c: c.data.startswith("reject_"))
async def reject(call: types.CallbackQuery):

    request_id = call.data.split("_")[1]

    if request_id not in pending_requests:
        return

    user_id = pending_requests[request_id]["user_id"]

    await bot.send_message(user_id, "Recharge Rejected ❌")

    await call.message.edit_text("Rejected ❌")

    pending_requests.pop(request_id)

# ================= ADMIN DASHBOARD ================= #

@dp.message_handler(commands=['admin'])
async def admin_panel(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        return

    text = "Pending Requests:\n"

    if not pending_requests:
        text += "None"
    else:
        for rid, data in pending_requests.items():
            text += f"ID {rid} → {data['network']}\n"

    await message.answer(text)

# ================= RUN ================= #

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
