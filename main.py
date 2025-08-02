import os
from gpt_utils import generate_schedule
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    filters
)
from plan_parser import parse_schedule
from scheduler import schedule_reminders
from datetime import datetime
from scheduler import clear_all_jobs

# Загружаем токены из .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

def get_clear_schedule_keyboard():
    keyboard = [
        [InlineKeyboardButton("🗑 Очистить расписание", callback_data="clear_schedule")]
    ]
    return InlineKeyboardMarkup(keyboard)


async def clear_schedule_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # чтобы убрать "часики"
    clear_all_jobs()
    await query.edit_message_text("Расписание очищено. Можешь отправить новые задачи.")

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
        await update.message.reply_text(
            f"Вот твоё расписание на день:\n\n{schedule_text}",
            reply_markup=get_clear_schedule_keyboard()
        )

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
    app.add_handler(CallbackQueryHandler(clear_schedule_callback, pattern="^clear_schedule$"))

    print("Бот запущен!")
    app.run_polling()
