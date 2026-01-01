import logging
import os
import sys
import time
import threading
import meilisearch
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from .config import settings


# Custom Time + Size Handler
class TimedRotatingFileHandlerWithSize(TimedRotatingFileHandler):
    def __init__(
        self,
        filename,
        when="D",
        interval=1,
        backupCount=0,
        encoding=None,
        maxBytes=0,
        delay=False,
        utc=False,
        atTime=None,
    ):
        super().__init__(
            filename,
            when=when,
            interval=interval,
            backupCount=backupCount,
            encoding=encoding,
            delay=delay,
            utc=utc,
            atTime=atTime,
        )
        self.maxBytes = maxBytes

    def shouldRollover(self, record):
        if super().shouldRollover(record):
            return True

        if self.maxBytes > 0:
            try:
                if os.path.getsize(self.baseFilename) >= self.maxBytes:
                    return True
            except OSError:
                pass

        return False


# Logger Setup
class SetupLogger:
    """
    Centralized logging for AutoMeet services.
    - Console logging (dev)
    - Rotating file logging (prod)
    - Optional Meilisearch logging (async & safe)
    """

    def __init__(
        self,
        logger_name: str,
        log_file: str,
        meili_index: str | None = None,
        max_bytes: int = 5 * 1024 * 1024,
        when: str = "D",
        interval: int = 1,
        backup_count: int = 7,
    ):
        os.makedirs("logs", exist_ok=True)

        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        # ❗ Prevent duplicate handlers (FastAPI reload issue)
        if self.logger.handlers:
            return

        log_format = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        # Console (only useful in development)
        if settings.ENVIRONMENT != "production":
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(log_format)
            self.logger.addHandler(console_handler)

        # File logging (always enabled)
        file_handler = TimedRotatingFileHandlerWithSize(
            log_file,
            when=when,
            interval=interval,
            backupCount=backup_count,
            encoding="utf-8",
            maxBytes=max_bytes,
        )
        file_handler.setFormatter(log_format)
        self.logger.addHandler(file_handler)


        # Meilisearch (Optional)
        
        self.meili_enabled = False
        self.meili_index = None

        if (
            settings.MEILI_SEARCH_URL
            and settings.MEILI_SEARCH_API_KEY
            and meili_index
        ):
            try:
                client = meilisearch.Client(
                    settings.MEILI_SEARCH_URL,
                    settings.MEILI_SEARCH_API_KEY,
                )
                self.meili_index = client.index(meili_index)
                self.meili_enabled = True

                self.meili_index.update_filterable_attributes(
                    ["timestamp", "level", "service", "logger"]
                )
                self.meili_index.update_sortable_attributes(
                    ["timestamp", "level"]
                )
            except Exception as e:
                self.logger.error(f"Meilisearch init failed: {e}")

    
    # Internal helpers
    def _send_to_meili_async(self, log_entry: dict):
        def task():
            try:
                self.meili_index.add_documents([log_entry])
            except Exception:
                # Never break app flow because of logging
                pass

        threading.Thread(target=task, daemon=True).start()

    def _log_to_meilisearch(self, level: str, message: str):
        if not self.meili_enabled:
            return

        log_entry = {
            "id": f"{int(time.time() * 1000)}-{level}",
            "timestamp": int(time.time()),
            "level": level,
            "message": message,
            "service": settings.SERVICE_NAME,
            "logger": self.logger.name,
            "environment": settings.ENVIRONMENT,
        }

        self._send_to_meili_async(log_entry)

    
    # Public logging methods
    def info(self, message: str):
        self.logger.info(message)
        self._log_to_meilisearch("INFO", message)

    def warning(self, message: str):
        self.logger.warning(message)
        self._log_to_meilisearch("WARNING", message)

    def error(self, message: str):
        self.logger.error(message)
        self._log_to_meilisearch("ERROR", message)

    def debug(self, message: str):
        if settings.ENVIRONMENT != "production":
            self.logger.debug(message)
            self._log_to_meilisearch("DEBUG", message)

    def critical(self, message: str):
        self.logger.critical(message)
        self._log_to_meilisearch("CRITICAL", message)


# AutoMeet Core Loggers
app_logger = SetupLogger(
    "app",
    "logs/app.log",
    meili_index=settings.MEILI_SEARCH_INDEX,
)

db_logger = SetupLogger(
    "database",
    "logs/database.log",
    meili_index=settings.MEILI_SEARCH_INDEX,
)

security_logger = SetupLogger(
    "security",
    "logs/security.log",
    meili_index=settings.MEILI_SEARCH_INDEX,
)

scheduler_logger = SetupLogger(
    "scheduler",
    "logs/scheduler.log",
    meili_index=settings.MEILI_SEARCH_INDEX,
)

redis_logger = SetupLogger(
    "redis",
    "logs/redis.log",
    meili_index=settings.MEILI_SEARCH_INDEX,
)
