# =========================
# main.py
# =========================
# Telegram bot (aiogram) with /buy + verify button

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

from pay import create_invoice, check_payment_status

BOT_TOKEN = "8775877729:AAER8B3a4FnLJW59ihfkZ49hfnF880AOPvg"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# store last invoice per user (for testing)
user_payments = {}


@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.reply("Send /buy to test crypto payment ($1)")


@dp.message_handler(commands=["buy"])
async def buy(msg: types.Message):
    user_id = str(msg.from_user.id)

    invoice = create_invoice(user_id)

    if not invoice:
        await msg.reply("❌ Failed to create invoice")
        return

    payment_id = invoice.get("id")
    invoice_url = invoice.get("invoice_url")

    user_payments[user_id] = payment_id

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("💳 Pay Now", url=invoice_url))
    kb.add(InlineKeyboardButton("✅ Transaction Succeeded", callback_data="check_payment"))

    await msg.reply(
        f"💰 Amount: $1\nClick below to pay",
        reply_markup=kb
    )


@dp.callback_query_handler(lambda c: c.data == "check_payment")
async def check_payment(cb: types.CallbackQuery):
    user_id = str(cb.from_user.id)

    payment_id = user_payments.get(user_id)

    if not payment_id:
        await cb.answer("No payment found", show_alert=True)
        return

    status = check_payment_status(payment_id)

    if not status:
        await cb.answer("Error checking payment", show_alert=True)
        return

    if status == "finished":
        await cb.message.answer("✅ Payment Approved! Premium Activated (test)")
    elif status in ["waiting", "confirming"]:
        await cb.answer("⏳ Payment not confirmed yet", show_alert=True)
    else:
        await cb.answer(f"❌ Payment {status}", show_alert=True)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


