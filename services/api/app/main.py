import json
import re

from fastapi import FastAPI, Query, HTTPException

from services.api.app.ai_client import client, generate_question

app = FastAPI(title="Learning Companion API")

@app.post("/session/start")
def start_session():
    return {
        "message": (
            "Привет! Добро пожаловать в Learning Companion Bot.\n\n"
            "Вот что я умею:\n"
            "/start — проверить, что бот онлайн\n"
            "/question — сгенерировать вопрос и ответ по выбранной теме\n"
            "/help — получить эту подсказку"
        )
    }

@app.post("/session/help")
def help_session():
    return {
        "message": (
            "В разработке..."
        )
    }

@app.get("/question/generate")
def question_generate(topic: str):
    prompt = f"""
            Верни ТОЛЬКО JSON:
            
            {{
              "question": "один короткий вопрос по теме {topic}",
              "answer": "один короткий правильный ответ"
            }}
            
            Правила:
            - один вопрос
            - один ответ
            - без списков
            - без markdown
            - только русский
            """

    try:
        data = generate_question(prompt)
        return data
    except Exception as e:
        print("ERROR IN /question/generate:", e)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
