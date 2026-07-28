import json
from confluent_kafka import Producer
from app.core.config import settings

_producer: Producer | None = None


def _kafka_config() -> dict:
    cfg: dict = {"bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS}
    if settings.KAFKA_SECURITY_PROTOCOL != "PLAINTEXT":
        cfg["security.protocol"] = settings.KAFKA_SECURITY_PROTOCOL
        cfg["sasl.mechanism"] = settings.KAFKA_SASL_MECHANISM
        cfg["sasl.username"] = settings.KAFKA_SASL_USERNAME
        cfg["sasl.password"] = settings.KAFKA_SASL_PASSWORD
    return cfg


def get_producer() -> Producer:
    global _producer
    if _producer is None:
        _producer = Producer(_kafka_config())
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
