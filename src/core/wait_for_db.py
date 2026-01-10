import time
import logging
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)

def wait_for_db(
    engine: Engine,
    max_retries: int = 10,
    delay_seconds: int = 2,
) -> None:
    """
    Blocks until the database is available or retries are exhausted.
    """
    for attempt in range(1, max_retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database connection successful")
            return
        except OperationalError as e:
            logger.warning(
                f"Database not ready (attempt {attempt}/{max_retries}): {e}). "
                f"Retrying in {delay_seconds}s..."
            )
            time.sleep(delay_seconds)

    raise RuntimeError("Database not available after retries")
