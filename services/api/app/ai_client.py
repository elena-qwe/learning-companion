import json
import logging
import re

from openai import OpenAI
from services.api.app.config import api_key

logger = logging.getLogger(__name__)  # Глобальный логгер
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)


def generate_question(prompt_text: str) -> dict:
    # Улучшенный промпт
    json_prompt = f"""Ответь ТОЛЬКО валидным JSON в следующем формате, без дополнительного текста:

{{
  "question": "твой вопрос здесь", 
  "answer": "подробное объяснение здесь"
}}

Тема: {prompt_text}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": json_prompt}],  # ← ИСПРАВЛЕНО
            max_tokens=200,
            temperature=0.3
        )

        content = response.choices[0].message.content.strip()
        logger.info(f"AI response: {repr(content[:200])}")

        # Простой парсинг ВСЕГО контента
        data = json.loads(content)

    except json.JSONDecodeError as e:
        logger.error(f"JSON error: {e}. Content: {repr(content[:300])}")
        raise ValueError("AI response is not valid JSON")
    except Exception as e:
        logger.error(f"API error: {e}")
        raise ValueError("Failed to generate question")

    question = data.get("question", "").strip()
    answer = re.sub(r"[#*_`]", "", data.get("answer", "")).strip()

    if not question or not answer:
        raise ValueError("Missing question or answer")

    return {"question": question, "answer": answer}
