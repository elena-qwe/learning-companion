def build_prompt(
    topic: str,
    mode: str,
    level: str,
    user_question: str | None = None,
) -> str:

    level_hint = {
        "junior": "ответ для junior разработчика",
        "middle": "ответ уровня middle, с примерами",
        "senior": "ответ уровня senior, с архитектурным мышлением",
    }[level]

    if mode == "detailed":
        return f"""
Ответь как на собеседовании Python Developer.
{level_hint}

Тема: {topic}

Вопрос:
{user_question if user_question else "Сформулируй вопрос сам"}

Требования:
- 5–7 строк
- можно маркеры
- без воды
- формулировки, которые можно заучивать

Верни JSON:
{{"question": "...", "answer": "..."}}
"""
    else:
        return f"""
Дай короткое определение по теме {topic}.
Уровень: {level_hint}
1–2 предложения.

Верни JSON:
{{"question": "...", "answer": "..."}}
"""
