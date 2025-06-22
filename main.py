import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.exceptions import TelegramBadRequest

API_TOKEN = '8174530370:AAFLY-V9vZIJggaNEPZERo53O5xgvJhPfpQ'
CHANNEL_ID = '-1002114691305'  # ID канала, куда должна быть подписка

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Кнопка перехода на канал
subscribe_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Підписатись", url="https://t.me/+6IStyfIw0G9jNDky")],
    [InlineKeyboardButton(text="🔄 Я підписався", callback_data="check_sub")]
])

# Кнопка вакансий
vacancy_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🎮 Перейти до завдання", url="https://example.com")]
])

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.answer(
        "👋 Вітаємо в сервісі підбору підробітку! Щоб переглянути доступні вакансії, спершу підпишіться на наш канал:",
        reply_markup=subscribe_keyboard
    )

@dp.callback_query(lambda c: c.data == 'check_sub')
async def check_subscription(callback_query: types.CallbackQuery):
    try:
        user_status = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=callback_query.from_user.id)
        if user_status.status in ['member', 'creator', 'administrator']:
            await callback_query.message.answer(
                "✅ Дякуємо за підписку! Ось одна з найпопулярніших підробітків сьогодні:",
                reply_markup=vacancy_keyboard
            )
        else:
            await callback_query.message.answer("❌ Ви ще не підписались на канал.", reply_markup=subscribe_keyboard)
    except TelegramBadRequest:
        await callback_query.message.answer("⚠️ Сталася помилка перевірки. Спробуйте ще раз пізніше.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())