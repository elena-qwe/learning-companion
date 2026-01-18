import re

def clean_text(text: str) -> str:
    """Убираем вложенные ``` и лишние спецсимволы"""
    text = text.replace("```", "")
    return text

def escape_markdown_v2(text: str) -> str:
    """Экранируем спецсимволы для MarkdownV2"""
    escape_chars = r"_*[]()~`>#+-=|{}.!\""
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

def extract_code(answer: str):
    """
    Ищем код в ответе AI, который начинается с python\n или ```python
    Разделяем на текст и код.
    """
    import re
    code_match = re.search(r"(?:```python\n|python\n)(.+)", answer, flags=re.DOTALL)
    if code_match:
        code_text = code_match.group(1).strip()
        # Убираем все ``` в коде
        code_text = code_text.replace("```", "").strip()
        # Текст до кода
        text_before = answer[:code_match.start()].strip()
        return text_before, code_text
    return answer, None