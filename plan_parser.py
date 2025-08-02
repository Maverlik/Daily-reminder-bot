import re
from datetime import datetime, timedelta

def parse_schedule(text: str, base_date: datetime) -> list:
    """
    Парсим расписание из текста.
    base_date — дата, к которой привязаны часы (например, сегодня)
    Возвращаем список событий с datetime начала и конца и описанием.
    """

    pattern = re.compile(r"(\d{1,2}[:.]\d{2})\s*[-–]\s*(\d{1,2}[:.]\d{2})\s*(.+)")
    events = []

    for line in text.splitlines():
        match = pattern.match(line)
        if not match:
            continue

        start_str, end_str, task = match.groups()
        start_time = datetime.strptime(start_str.replace(".", ":"), "%H:%M").time()
        end_time = datetime.strptime(end_str.replace(".", ":"), "%H:%M").time()

        start_dt = datetime.combine(base_date.date(), start_time)
        end_dt = datetime.combine(base_date.date(), end_time)

        # Если время начала позже времени конца, значит конец на следующий день
        if end_dt <= start_dt:
            end_dt += timedelta(days=1)

        events.append({"start": start_dt, "end": end_dt, "task": task.strip()})

    return events
