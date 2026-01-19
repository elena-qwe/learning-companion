import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

LEVELS = {
    "junior": "Junior",
    "middle": "Middle",
    "senior": "Senior",
}

# Словарь короткий ключ -> полное название темы
TOPICS_BY_CATEGORY = {
    "python_core": {
        "py_commercial": "Python 3.9+ коммерческая разработка (3–4+ года)",
        "oop": "ООП в Python",
        "django_vs_flask": "Django vs Flask сравнение",
    },
    "backend": {
        "rest": "REST API и микросервисы",
        "fastapi": "FastAPI (async endpoints)",
        "pydantic": "Pydantic (валидация моделей)",
    },
    "async": {
        "asyncio": "Асинхронное программирование asyncio",
        "aiohttp": "aiohttp для HTTP запросов",
        "highload": "Высоконагруженные проекты (финтех)",
    },
    "db": {
        "postgres": "PostgreSQL (asyncpg)",
        "redis": "Redis (aioredis)",
        "mongo": "MongoDB (Motor)",
    },
    "devops": {
        "docker": "Docker (Dockerfile, compose)",
        "k8s": "Kubernetes основы (deploy)",
        "containers": "Контейнеризация",
    },
    "ai": {
        "llm": "LLM пайплайны и AI-агенты",
        "langchain": "LangChain (chains, agents, tools)",
        "langgraph": "LangGraph (графы состояний)",
        "crewai": "CrewAI (команды агентов)",
    },
}

CATEGORIES = {
    "python_core": "🐍 Python",
    "backend": "🌐 Backend",
    "async": "⚡ Async / Highload",
    "db": "🗄 Базы данных",
    "devops": "🐳 DevOps",
    "ai": "🤖 AI / LLM",
}

ANSWER_DEPTH = {
    "short": "короткий ответ (1–2 предложения)",
    "interview": "ответ уровня собеседования (структурированный, 5–7 строк)"
}

TOPIC_DEPTH_MAP = {
    "MongoDB (Motor)": "interview",
    "PostgreSQL (asyncpg)": "interview",
    "Redis (aioredis)": "interview",
    "Высоконагруженные проекты (финтех)": "interview",
    "FastAPI (async endpoints)": "interview",

    # остальные — короткие
}