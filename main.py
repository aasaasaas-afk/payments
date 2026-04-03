# =========================
# main.py (UPDATED - PAYMENT API VERSION)
# =========================

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

from pay import create_payment, check_payment_status

BOT_TOKEN = "8775877729:AAER8B3a4FnLJW59ihfkZ49hfnF880AOPvg"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# store user -> payment_id
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
        InlineKeyboardButton("USDT TRC20", callback_data="trc20"),
        InlineKeyboardButton("USDT BEP20", callback_data="bep20")
    )

    await msg.reply("Select payment network:", reply_markup=kb)


# STEP 2: Create payment
@dp.callback_query_handler(lambda c: c.data in ["trc20", "bep20"])
async def select_network(cb: types.CallbackQuery):
    user_id = str(cb.from_user.id)

    if cb.data == "trc20":
        pay_currency = "usdttrc20"
        network_name = "TRC20"
    else:
        pay_currency = "usdtbep20"
        network_name = "BEP20"

    payment = create_payment(user_id, pay_currency)

    if not payment or "payment_id" not in payment:
        await cb.message.answer("❌ Failed to create payment")
        return

    payment_id = payment["payment_id"]
    address = payment["pay_address"]
    amount = payment["pay_amount"]
    currency = payment["pay_currency"]

    user_payments[user_id] = payment_id
    user_network[user_id] = network_name

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("✅ I HAVE PAID", callback_data="check_payment"))

    await cb.message.answer(
        f"💰 Send exactly: {amount} {currency}\n\n"
        f"📡 Network: {network_name}\n"
        f"🏦 Address:\n`{address}`\n\n"
        f"After payment click confirm",
        parse_mode="Markdown",
        reply_markup=kb
    )


# STEP 3: Verify payment
@dp.callback_query_handler(lambda c: c.data == "check_payment")
async def check_payment(cb: types.CallbackQuery):
    user_id = str(cb.from_user.id)

    payment_id = user_payments.get(user_id)

    if not payment_id:
        await cb.answer("❌ No payment found", show_alert=True)
        return

    status = check_payment_status(payment_id)

    if not status:
        await cb.answer("⚠️ Error checking payment", show_alert=True)
        return

    if status == "finished":
        await cb.message.answer("✅ Payment Approved!\nPremium Activated (test)")
    elif status in ["waiting", "confirming"]:
        await cb.answer("⏳ Payment not confirmed yet", show_alert=True)
    else:
        await cb.answer(f"❌ Payment {status}", show_alert=True)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
