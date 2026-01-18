from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

from config import BOT_TOKEN, API_URL
from services.api.app.ai_client import generate_question
from services.bot.helpers import escape_markdown_v2, clean_text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.post(f"{API_URL}/session/start").json()

    message = response.get("message", "Привет! Добро пожаловать.")

    await update.message.reply_text(
        f"{message}\n"
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.post(f"{API_URL}/session/help").json()

    message = response.get("message")
    print(message)
    await update.message.reply_text(
        f"{message}\n"
    )

async def question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = "FastAPI"

    response = requests.get(
        f"{API_URL}/question/generate",
        params={"topic": topic},
        timeout=10
    )

    data = response.json()

    question_text = clean_text(data.get("question", "Ошибка генерации"))
    answer_text = clean_text(data.get("answer", "Нет ответа"))

    question_text = escape_markdown_v2(question_text)
    answer_text = escape_markdown_v2(answer_text)
    topic_escaped = escape_markdown_v2(topic)

    message = (
        f"📝 *Тема:* {topic_escaped}\n\n"
        f"❓ *Вопрос:*\n{question_text}\n\n"
        f"💡 *Ответ:*\n{answer_text}"
    )

    await update.message.reply_text(message, parse_mode="MarkdownV2")

# Запуск бота
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("question", question))

app.run_polling()
