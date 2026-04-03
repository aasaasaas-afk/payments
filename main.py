# =========================
# main.py (COINREMITTER VERSION)
# =========================

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

from pay import create_payment, check_payment_status

BOT_TOKEN = "8775877729:AAER8B3a4FnLJW59ihfkZ49hfnF880AOPvg"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# store user data
user_address = {}
expected_amount = 1.0  # $1


@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.reply("Send /buy to purchase ($1)")


# STEP 1: Generate address
@dp.message_handler(commands=["buy"])
async def buy(msg: types.Message):
    user_id = str(msg.from_user.id)

    address = create_payment(user_id)

    if not address:
        await msg.reply("❌ Failed to generate address")
        return

    user_address[user_id] = address

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("✅ I HAVE PAID", callback_data="check_payment"))

    await msg.reply(
        f"💰 Send exactly: {expected_amount} USDT\n\n"
        f"📡 Network: TRC20\n"
        f"🏦 Address:\n`{address}`\n\n"
        f"After payment click confirm",
        parse_mode="Markdown",
        reply_markup=kb
    )


# STEP 2: Verify payment
@dp.callback_query_handler(lambda c: c.data == "check_payment")
async def check_payment(cb: types.CallbackQuery):
    user_id = str(cb.from_user.id)

    address = user_address.get(user_id)

    if not address:
        await cb.answer("❌ No payment found", show_alert=True)
        return

    balance = check_payment_status(address)

    if balance >= expected_amount:
        await cb.message.answer("✅ Payment Approved!\nPremium Activated")
    else:
        await cb.answer("⏳ Payment not received yet", show_alert=True)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
