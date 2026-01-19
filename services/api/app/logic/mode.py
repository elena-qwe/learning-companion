# решает КАК отвечать

DETAILED_TOPICS = {
    "MongoDB (Motor)",
    "Redis (aioredis)",
    "PostgreSQL (asyncpg)",
}

def choose_mode(
    topic: str,
    user_question: str | None,
    level: str
) -> str:
    if user_question:
        return "detailed"

    if level in {"middle", "senior"}:
        return "detailed"

    return "short"
