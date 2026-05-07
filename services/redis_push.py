"""Queue helpers (stub: log until Redis worker is wired)."""

from typing import Any

from app.core.loggers import app_logger as logger


def redis_lpush(payload: dict[str, Any]) -> None:
    logger.info(
        f"redis_lpush (stub) queue={payload.get('queue_name')} op={payload.get('operation')}"
    )
