from telegram.ext import ApplicationBuilder
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler
from config import BOT_TOKEN, API_URL, CATEGORIES, TOPICS_BY_CATEGORY
from services.bot.helpers import escape_markdown_v2, clean_text
from telegram.ext import MessageHandler, filters


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
    topic = context.user_data.get("topic", "Python основы")
    level = context.user_data.get("level", "junior")

    response = requests.get(
        f"{API_URL}/question/generate",
        params={
            "topic": topic,
            "level": level,
        },
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

async def user_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    topic = context.user_data.get("topic", "Python основы")
    level = context.user_data.get("level", "junior")
    response = requests.post(
        f"{API_URL}/question/ask",
        params={
            "topic": topic,
            "question": user_text,
            "level": level
        },
        timeout=15
    )

    data = response.json()

    answer = clean_text(data.get("answer", "Нет ответа"))
    answer = escape_markdown_v2(answer)

    if not context.user_data.get("topic"):
        await update.message.reply_text(
            "Сначала выберите тему через /choose_topic"
        )
        return

    await update.message.reply_text(
        f"💡 *Ответ:*\n{answer}",
        parse_mode="MarkdownV2"
    )

async def choose_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🟢 Junior", callback_data="level:junior")],
        [InlineKeyboardButton("🟡 Middle", callback_data="level:middle")],
        [InlineKeyboardButton("🔴 Senior", callback_data="level:senior")],
    ]

    await update.message.reply_text(
        "Выберите уровень сложности вопросов:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def level_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    level = query.data.replace("level:", "")
    context.user_data["level"] = level

    keyboard = [
        [InlineKeyboardButton(text, callback_data=f"cat:{key}")]
        for key, text in CATEGORIES.items()
    ]

    await query.edit_message_text(
        f"✅ Уровень установлен: {level.upper()}\n\nТеперь выберите категорию:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def category_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    category_key = query.data.replace("cat:", "")
    topics = TOPICS_BY_CATEGORY.get(category_key)

    keyboard = [
        [InlineKeyboardButton(name, callback_data=f"topic:{key}")]
        for key, name in topics.items()
    ]

    await query.edit_message_text(
        "Выберите тему:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def topic_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    topic_key = query.data.replace("topic:", "")
    level = context.user_data.get("level", "junior")  # Берем из user_data
    topic_name = None
    for topics in TOPICS_BY_CATEGORY.values():
        if topic_key in topics:
            topic_name = topics[topic_key]
            break

    context.user_data["topic"] = topic_name
    context.user_data["level"] = level

    await query.edit_message_text(
        f"✅ Тема выбрана:\n{topic_name}\n\n"
        f"✅ Сложность выбрана:\n{level}\n\n"
        f"🎉 Настройки готовы!\n\n"
        f"Используйте:\n"
        f"/question - получить вопрос\n"
        f" Или просто напишите вопрос боту"
    )

# Запуск бота
app = ApplicationBuilder().token(BOT_TOKEN).build()
# порядок важен
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("question", question))
app.add_handler(CommandHandler("choose_topic", choose_topic))
app.add_handler(CallbackQueryHandler(level_selected, pattern="^level:"))
app.add_handler(CallbackQueryHandler(category_selected, pattern="^cat:"))
app.add_handler(CallbackQueryHandler(topic_selected, pattern="^topic:"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, user_question))

app.run_polling()
