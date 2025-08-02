import os
from gpt_utils import generate_schedule
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from plan_parser import parse_schedule
from scheduler import schedule_reminders
from datetime import datetime


# Загружаем токены из .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши мне свои дела и пожелания на день, а я составлю тебе расписание.")

async def send_reminder(text, context):
    await context.bot.send_message(chat_id=context.job.chat_id, text=text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.effective_chat.id

    await update.message.reply_text("Принял! Сейчас подумаю...")

    try:
        schedule_text = generate_schedule(user_text)
        await update.message.reply_text("Вот твоё расписание:\n\n" + schedule_text)

        # Парсим расписание
        events = parse_schedule(schedule_text, datetime.now())

        # Функция-обёртка для отправки сообщений
        async def reminder_callback(text):
            await context.bot.send_message(chat_id=chat_id, text=text)

        # Запускаем напоминания
        schedule_reminders(events, reminder_callback)

    except Exception as e:
        await update.message.reply_text("Ошибка при обработке расписания.")
        print("Ошибка:", e)


if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен!")
    app.run_polling()
