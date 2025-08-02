import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_schedule(user_input: str) -> str:
    prompt = f"""
Ты — умный Telegram-бот-помощник. Пользователь присылает тебе список задач и пожеланий на день в свободной форме.
Твоя задача — составить подробное расписание с временем. Учитывай указанные желания и предпочтения по времени.
Ответ верни строго в виде расписания — без пояснений, без приветствий, только таймлайн.

Пример:
10:00–10:30 Завтрак
10:30–12:30 Учёба
12:30–13:00 Подготовка к прогулке
13:00–18:00 Прогулка
...

Вот текст от пользователя:
{user_input.strip()}
"""

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourproject.example",  # Укажи свой сайт или просто заглушку
        "X-Title": "ScheduleBot"
    }
    payload = {
        "model": "anthropic/claude-3-haiku",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
        "max_tokens": 500
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Ошибка API: {response.status_code} - {response.text}")
    
    return response.json()["choices"][0]["message"]["content"].strip()
