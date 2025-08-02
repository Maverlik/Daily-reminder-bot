from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import asyncio

scheduler = AsyncIOScheduler()

def schedule_reminders(events, send_message_callback):
    """
    events — список событий из parse_schedule
    send_message_callback — async функция, которая шлёт сообщение пользователю
    """

    scheduler.remove_all_jobs()  # чистим предыдущие задачи

    now = datetime.now()

    for event in events:
        start_time = event["start"]

        if start_time > now:
            job_id = f"reminder_{start_time.strftime('%H%M')}"
            scheduler.add_job(
                send_message_callback,
                "date",
                run_date=start_time,
                args=[f"Не забудь про  {event['task']}"],
                id=job_id
            )

    if not scheduler.running:
        scheduler.start()
