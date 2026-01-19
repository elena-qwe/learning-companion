from fastapi import FastAPI, HTTPException
from services.api.app.ai_client import generate_question
from services.api.app.logic.mode import choose_mode
from services.api.app.logic.prompt_builder import build_prompt

app = FastAPI(title="Learning Companion API")

@app.post("/session/start")
def start_session():
    return {
        "message": (
            "Привет! Добро пожаловать в Learning Companion Bot.\n\n"
            "Я могу помочь тебе учиться, отвечать на вопросы и генерировать новые вопросы по выбранной теме.\n"
            "Для подробностей используй команду /help."
        )
    }

@app.post("/session/help")
def help_session():
    return {
        "message": (
            "Привет! Вот что я умею:\n"
            "/start — проверить, что бот онлайн\n"
            "/question — сгенерировать вопрос и ответ по выбранной теме\n"
            "/help — получить эту подсказку\n"
            "/choose_topic — чтобы выбрать тему, используй команду"
        )
    }

@app.get("/question/generate")
def question_generate(topic: str, level: str = "junior"):
    mode = choose_mode(topic, None, level)
    prompt = build_prompt(topic, mode, level)
    return generate_question(prompt)

@app.post("/question/ask")
def ask_question(topic: str, question: str, level: str = "junior"):
    mode = choose_mode(topic, question, level)
    prompt = build_prompt(topic, mode, question, level)
    return generate_question(prompt)