from celery import Celery
from app.core.config import settings

celery = Celery(
    "gamesense",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.workers.poller"],
)

celery.conf.beat_schedule = {
    "poll-live-matches": {
        "task": "app.workers.poller.poll_live_matches",
        "schedule": settings.POLL_INTERVAL_SECONDS,
        "options": {"queue": "cricket-poller"},
    },
}
celery.conf.timezone = "UTC"
