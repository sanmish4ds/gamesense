"""
Celery task — polls CricAPI for live match updates, persists to PostgreSQL,
and publishes state changes to Kafka for downstream processing.
"""

import asyncio
import httpx
from celery_app import celery
from sqlalchemy.dialects.postgresql import insert

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.models.match import Match
from app.kafka.producer import publish_event

CRICAPI_BASE = "https://api.cricapi.com/v1"


def _run_async(coro):
    return asyncio.run(coro)


@celery.task(name="app.workers.poller.poll_live_matches", bind=True, max_retries=3)
def poll_live_matches(self):
    try:
        _run_async(_poll())
    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)


async def _fetch(client: httpx.AsyncClient, endpoint: str, params: dict | None = None) -> dict:
    p = params or {}
    p["apikey"] = settings.CRICAPI_KEY
    resp = await client.get(f"{CRICAPI_BASE}/{endpoint}", params=p, timeout=15.0)
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != "success":
        raise ValueError(f"CricAPI error on {endpoint}: {data.get('info', data)}")
    return data


async def _poll():
    async with httpx.AsyncClient() as client:
        data = await _fetch(client, "currentMatches", {"offset": 0})
        matches = data.get("data", [])
        if not matches:
            return

        async with AsyncSessionLocal() as db:
            for m in matches:
                match_id = m.get("id")
                if not match_id:
                    continue

                # Fetch detailed scorecard only for active live matches
                scorecard = None
                if m.get("matchStarted") and not m.get("matchEnded"):
                    try:
                        sc_data = await _fetch(client, "match_scorecard", {"id": match_id})
                        scorecard = sc_data.get("data")
                    except Exception:
                        pass

                values = {
                    "id": match_id,
                    "name": m.get("name", ""),
                    "match_type": m.get("matchType"),
                    "status": m.get("status"),
                    "venue": m.get("venue"),
                    "date": m.get("date"),
                    "date_time_gmt": m.get("dateTimeGMT"),
                    "team1_name": (m.get("teams") or [None])[0],
                    "team2_name": (m.get("teams") or [None, None])[1] if len(m.get("teams") or []) > 1 else None,
                    "is_live": bool(m.get("matchStarted") and not m.get("matchEnded")),
                    "score": m.get("score"),
                    "toss": m.get("tossResults"),
                    "batting_team": _get_batting_team(m),
                    "bowling_team": _get_bowling_team(m),
                    "current_over": _get_current_over(m),
                    "match_winner": m.get("matchWinner"),
                    "scorecard": scorecard,
                }

                stmt = insert(Match).values(**values).on_conflict_do_update(
                    index_elements=["id"],
                    set_={k: v for k, v in values.items() if k != "id"},
                )
                await db.execute(stmt)

                payload = {**values, "match_id": match_id}
                payload.pop("scorecard", None)
                publish_event("cricket.match-state", match_id, payload)

            await db.commit()


def _get_batting_team(m: dict) -> str | None:
    score = m.get("score") or []
    if score:
        return score[-1].get("inning", "").replace(" Inning 1", "").replace(" Inning 2", "") or None
    return None


def _get_bowling_team(m: dict) -> str | None:
    teams = m.get("teams") or []
    batting = _get_batting_team(m)
    if batting and teams:
        for t in teams:
            if t != batting:
                return t
    return None


def _get_current_over(m: dict) -> float | None:
    score = m.get("score") or []
    if score:
        try:
            return float(score[-1].get("o", 0))
        except (TypeError, ValueError):
            return None
    return None
