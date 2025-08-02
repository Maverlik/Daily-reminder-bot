import os
from gpt_utils import generate_schedule
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

# Загружаем токены из .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши мне свои дела и пожелания на день, а я составлю тебе расписание.")

# Обработка обычных сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("Принял! Сейчас подумаю...")

    try:
        schedule = generate_schedule(user_text)
        await update.message.reply_text("Вот твоё расписание:\n\n" + schedule)
    except Exception as e:
        await update.message.reply_text("Ошибка при обращении к GPT. Попробуй позже.")
        print("Ошибка:", e)


if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен!")
    app.run_polling()
