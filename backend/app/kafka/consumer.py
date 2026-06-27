"""
Kafka consumer — processes cricket.ball-events and cricket.match-state topics,
persists events to PostgreSQL, and fans-out to Redis pub/sub for WebSocket clients.
"""

import asyncio
import json
from confluent_kafka import Consumer, KafkaError

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.core.redis_client import get_redis
from app.models.ball_event import BallEvent


TOPICS = ["cricket.ball-events", "cricket.match-state"]


async def handle_ball_event(data: dict, db: AsyncSession, redis):
    match_id = data.get("match_id")
    if not match_id:
        return

    event = BallEvent(
        match_id=match_id,
        over=data.get("over", 0),
        ball=data.get("ball", 1),
        innings=data.get("innings", 1),
        batsman=data.get("batsman"),
        bowler=data.get("bowler"),
        runs=data.get("runs", 0),
        extras=data.get("extras", 0),
        extra_type=data.get("extra_type"),
        is_wicket=data.get("is_wicket", False),
        wicket_type=data.get("wicket_type"),
        wicket_player=data.get("wicket_player"),
        is_boundary=data.get("is_boundary", False),
        is_six=data.get("is_six", False),
        total_runs=data.get("total_runs", 0),
        total_wickets=data.get("total_wickets", 0),
        run_rate=data.get("run_rate"),
    )
    db.add(event)
    await db.commit()


async def handle_match_state(data: dict, redis):
    match_id = data.get("match_id")
    if not match_id:
        return
    # Fan-out live state to WebSocket subscribers via Redis pub/sub
    await redis.publish(f"match:{match_id}", json.dumps(data))
    # Cache latest state (TTL 60s)
    await redis.setex(f"live:{match_id}", 60, json.dumps(data))


async def consume_loop():
    consumer = Consumer({
        "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
        "group.id": "gamesense-consumer",
        "auto.offset.reset": "latest",
        "enable.auto.commit": True,
    })
    consumer.subscribe(TOPICS)

    redis = await get_redis()

    async with AsyncSessionLocal() as db:
        print("[Kafka Consumer] Started, listening on:", TOPICS)
        try:
            while True:
                msg = consumer.poll(timeout=1.0)
                if msg is None:
                    await asyncio.sleep(0.1)
                    continue
                if msg.error():
                    if msg.error().code() != KafkaError._PARTITION_EOF:
                        print(f"[Kafka] Error: {msg.error()}")
                    continue

                try:
                    payload = json.loads(msg.value().decode())
                    topic = msg.topic()

                    if topic == "cricket.ball-events":
                        await handle_ball_event(payload, db, redis)
                    elif topic == "cricket.match-state":
                        await handle_match_state(payload, redis)
                except Exception as e:
                    print(f"[Kafka Consumer] Processing error: {e}")
        finally:
            consumer.close()


if __name__ == "__main__":
    asyncio.run(consume_loop())
