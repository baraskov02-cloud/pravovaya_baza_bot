import logging
import asyncio
import random
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters,
    ContextTypes
)
from quotes import get_random_user_id, get_quote, USER_NAMES

TOKEN = "8958811199:AAHyEb4r83PqCw7Ga7ETcnF4njgqquCIxP0"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    
    chat = update.effective_chat
    message = update.message
    
    if message.text and message.text.startswith('/'):
        return
    
    if message.from_user and message.from_user.is_bot:
        return
    
    if chat.title != "правовая база Artem_L":
        return
    
    # Выбираем случайного пользователя и цитату
    user_id = get_random_user_id()
    quote, quote_type, user_id_actual = get_quote(user_id, 'random')
    name = USER_NAMES.get(user_id_actual, 'Кто-то')
    
    mood = "✅ " if quote_type == 'good' else "💀 "
    
    await message.reply_text(f"{mood}{quote}")
    logger.info(f"Sent {quote_type} quote about {name} in {chat.title}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Бот Правовой Базы запущен!\n\n"
        "📌 На каждое сообщение — случайная цитата про одного из участников:\n"
        "👤 Саня, Ярик, Лалик, Денис\n\n"
        "🎲 50% хорошие / 50% плохие\n\n"
        "👑 Команды:\n"
        "/good @имя — хорошая цитата\n"
        "/bad @имя — плохая цитата\n"
        "/random @имя — случайная"
    )

async def quote_command(update: Update, context: ContextTypes.DEFAULT_TYPE, quote_type='random'):
    if not context.args:
        await update.message.reply_text("Укажи пользователя: /good @саня")
        return
    
    mention = context.args[0].lower().replace('@', '')
    
    # Простой поиск по именам
    name_map = {
        'саня': 832072176,
        'ярик': 2117431709,
        'лалик': 5299703937,
        'денис': 6665494648,
        'denis': 6665494648,
        'yarik': 2117431709,
        'lalik': 5299703937,
        'sanya': 832072176,
    }
    
    user_id = name_map.get(mention)
    if not user_id:
        await update.message.reply_text("Кого? (саня, ярик, лалик, денис)")
        return
    
    quote, _, _ = get_quote(user_id, quote_type)
    mood = "✅ " if quote_type == 'good' else "💀 "
    await update.message.reply_text(f"{mood}{quote}")

async def good_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await quote_command(update, context, 'good')

async def bad_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await quote_command(update, context, 'bad')

async def random_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await quote_command(update, context, 'random')

async def main():
    print("🚀 Бот запущен на Railway!")
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("good", good_command))
    app.add_handler(CommandHandler("bad", bad_command))
    app.add_handler(CommandHandler("random", random_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
    
    print("✅ Бот работает! Цитаты про всех участников")
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
