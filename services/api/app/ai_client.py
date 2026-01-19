import json
import re
import logging
from openai import OpenAI

from services.api.app.config import api_key



client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

def generate_question(prompt_text: str) -> dict:
    logging.basicConfig(
        filename="prompts.log",
        level=logging.INFO,
        format="%(asctime)s | %(message)s",
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt_text}],
        max_tokens=200,
        temperature=0.2
    )



    content = response.choices[0].message.content.strip()

    match = re.search(r"\{.*\}", content, re.DOTALL)
    if not match:
        raise ValueError("AI response does not contain JSON")

    json_str = match.group(0)

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON from AI")

    question = data.get("question", "").strip()
    answer = data.get("answer", "").strip()

    if not question or not answer:
        raise ValueError("Missing question or answer")

    question = question[:200]
    answer = answer[:300]

    answer = re.sub(r"[#*_`]", "", answer)
    answer = " ".join(answer.split())

    return {
        "question": question,
        "answer": answer
    }