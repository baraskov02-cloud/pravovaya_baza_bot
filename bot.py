import logging
import asyncio
import random
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters,
    ContextTypes
)
from quotes import get_quote

TOKEN = "8958811199:AAHyEb4r83PqCw7Ga7ETcnF4njgqquCIxP0"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

USER_NAMES = {
    832072176: 'Саня',
    2117431709: 'Ярик',
    5299703937: 'Лалик',
    6665494648: 'Денис'
}

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
    
    quote_type = random.choice(['good', 'bad'])
    name = USER_NAMES.get(5299703937, 'Лалик')
    quote = get_quote(name, quote_type)
    
    mood = "✅ " if quote_type == 'good' else "💀 "
    
    await message.reply_text(f"{mood}{quote}")
    logger.info(f"Sent quote in {chat.title}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Бот Правовой Базы запущен!\n\n"
        "📌 На каждое сообщение приходит цитата про Лалика\n"
        "🎲 50% хорошие / 50% плохие\n\n"
        "👑 Команды:\n"
        "/good — хорошая цитата\n"
        "/bad — плохая цитата\n"
        "/random — случайная"
    )

async def good_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = USER_NAMES.get(5299703937, 'Лалик')
    quote = get_quote(name, 'good')
    await update.message.reply_text(f"✅ {quote}")

async def bad_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = USER_NAMES.get(5299703937, 'Лалик')
    quote = get_quote(name, 'bad')
    await update.message.reply_text(f"💀 {quote}")

async def random_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = USER_NAMES.get(5299703937, 'Лалик')
    quote = get_quote(name, 'random')
    await update.message.reply_text(f"🎲 {quote}")

async def main():
    print("🚀 Бот запущен на Railway!")
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("good", good_quote))
    app.add_handler(CommandHandler("bad", bad_quote))
    app.add_handler(CommandHandler("random", random_quote))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
    
    print("✅ Бот работает!")
    
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