# =========================
# main.py (OXAPAY INVOICE VERSION - FINAL)
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


@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.reply("Send /buy to test crypto payment ($1)")


# STEP 1: Buy command (no network needed for invoice)
@dp.message_handler(commands=["buy"])
async def buy(msg: types.Message):
    user_id = str(msg.from_user.id)

    payment = create_payment(user_id)

    if not payment:
        await msg.reply("❌ Failed to create payment")
        return

    track_id = payment["track_id"]
    payment_url = payment["payment_url"]

    user_payments[user_id] = track_id

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("💳 Pay Now", url=payment_url))
    kb.add(InlineKeyboardButton("✅ I HAVE PAID", callback_data="check_payment"))

    await msg.reply(
        "💰 Amount: $1\n\nClick below to pay",
        reply_markup=kb
    )


# STEP 2: Verify payment
@dp.callback_query_handler(lambda c: c.data == "check_payment")
async def check_payment(cb: types.CallbackQuery):
    user_id = str(cb.from_user.id)

    track_id = user_payments.get(user_id)

    if not track_id:
        await cb.answer("❌ No payment found", show_alert=True)
        return

    status = check_payment_status(track_id)

    if status is None:
        await cb.answer("⚠️ Error checking payment", show_alert=True)
        return

    # 🔥 OxaPay status handling
    if status == 100:
        await cb.message.answer("✅ Payment Approved!\nPremium Activated (test)")
    elif status in [0, 1]:
        await cb.answer("⏳ Payment not confirmed yet", show_alert=True)
    elif status == -1:
        await cb.answer("❌ Payment expired", show_alert=True)
    else:
        await cb.answer(f"❌ Status: {status}", show_alert=True)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
