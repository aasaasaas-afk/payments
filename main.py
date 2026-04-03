# =========================
# main.py (FIXED - WHITE LABEL VERSION)
# =========================

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

from pay import create_payment, check_payment_status

BOT_TOKEN = "8775877729:AAER8B3a4FnLJW59ihfkZ49hfnF880AOPvg"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# store user -> track_id
user_payments = {}
user_network = {}


@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.reply("Send /buy to test crypto payment ($1)")


# STEP 1: Choose network
@dp.message_handler(commands=["buy"])
async def buy(msg: types.Message):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("USDT TRC20", callback_data="TRC20"),
        InlineKeyboardButton("USDT BEP20", callback_data="BSC")
    )

    await msg.reply("Select payment network:", reply_markup=kb)


# STEP 2: Create payment
@dp.callback_query_handler(lambda c: c.data in ["TRC20", "BSC"])
async def select_network(cb: types.CallbackQuery):
    user_id = str(cb.from_user.id)
    network = cb.data  # TRC20 or BSC

    payment = create_payment(user_id)

    if not payment:
        await cb.message.answer("❌ Failed to create payment")
        return

    # extract new structure
    track_id = payment["track_id"]
    address = payment["address"]
    amount = payment["amount"]
    currency = payment["currency"]
    network_name = payment["network"]
    qr = payment["qr"]

    user_payments[user_id] = track_id
    user_network[user_id] = network_name

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("✅ I HAVE PAID", callback_data="check_payment"))

    await cb.message.answer(
        f"💰 Payment Details\n\n"
        f"Amount: {amount} {currency}\n"
        f"Network: {network_name}\n\n"
        f"Address:\n`{address}`\n\n"
        f"⚠️ Send exact amount\n"
        f"⏳ Valid 30 minutes",
        parse_mode="Markdown",
        reply_markup=kb
    )

    # send QR
    await bot.send_photo(cb.from_user.id, qr)


# STEP 3: Verify payment
@dp.callback_query_handler(lambda c: c.data == "check_payment")
async def check_payment(cb: types.CallbackQuery):
    user_id = str(cb.from_user.id)

    track_id = user_payments.get(user_id)

    if not track_id:
        await cb.answer("❌ No payment found", show_alert=True)
        return

    status = check_payment_status(track_id)

    if not status:
        await cb.answer("⚠️ Error checking payment", show_alert=True)
        return

    # ✅ Correct status handling
    if status == "paid":
        await cb.message.answer("✅ Payment Approved!\nPremium Activated (test)")
    elif status in ["waiting", "paying"]:
        await cb.answer("⏳ Payment not received yet", show_alert=True)
    elif status == "expired":
        await cb.answer("⌛ Payment expired", show_alert=True)
    elif status == "underpaid":
        await cb.answer("⚠️ Underpaid amount", show_alert=True)
    else:
        await cb.answer(f"❌ Payment {status}", show_alert=True)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
