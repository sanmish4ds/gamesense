import json
from confluent_kafka import Producer
from app.core.config import settings

_producer: Producer | None = None


def get_producer() -> Producer:
    global _producer
    if _producer is None:
        _producer = Producer({"bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS})
    return _producer


def publish_event(topic: str, key: str, payload: dict) -> None:
    producer = get_producer()
    producer.produce(
        topic,
        key=key.encode(),
        value=json.dumps(payload).encode(),
        callback=_delivery_report,
    )
    producer.poll(0)


def _delivery_report(err, msg):
    if err:
        print(f"[Kafka] Delivery failed: {err}")


def flush():
    get_producer().flush()
