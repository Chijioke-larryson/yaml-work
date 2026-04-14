import os
import sys
import time
import logging
import redis
import psycopg2

# ---------------------------------------------------------------------------
# Configuration from environment variables
# ---------------------------------------------------------------------------
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6380))

POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.environ.get("POSTGRES_PORT", 5432))
POSTGRES_DB = os.environ.get("POSTGRES_DB", "votes_db")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("worker")

# ---------------------------------------------------------------------------
# Connection helpers with retry / reconnect
# ---------------------------------------------------------------------------
MAX_RETRIES = 10
RETRY_DELAY = 2  # seconds (doubles on each retry, capped at 30s)


def connect_redis():
    """Connect to Redis with retries."""
    delay = RETRY_DELAY
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
            r.ping()
            logger.info("Connected to Redis at %s:%s", REDIS_HOST, REDIS_PORT)
            return r
        except redis.RedisError as e:
            logger.warning("Redis connection attempt %d/%d failed: %s", attempt, MAX_RETRIES, e)
            time.sleep(delay)
            delay = min(delay * 2, 30)
    logger.error("Could not connect to Redis after %d attempts. Exiting.", MAX_RETRIES)
    sys.exit(1)


def connect_postgres():
    """Connect to PostgreSQL with retries."""
    delay = RETRY_DELAY
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            conn = psycopg2.connect(
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                dbname=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
            )
            conn.autocommit = True
            logger.info("Connected to PostgreSQL at %s:%s/%s", POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB)
            return conn
        except psycopg2.Error as e:
            logger.warning("PostgreSQL connection attempt %d/%d failed: %s", attempt, MAX_RETRIES, e)
            time.sleep(delay)
            delay = min(delay * 2, 30)
    logger.error("Could not connect to PostgreSQL after %d attempts. Exiting.", MAX_RETRIES)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
def main():
    logger.info("Worker starting up …")

    redis_conn = connect_redis()
    pg_conn = connect_postgres()
    cursor = pg_conn.cursor()

    logger.info("Listening for votes on Redis queue 'votes' …")

    while True:
        try:
            # BLPOP blocks until an item is available (timeout 0 = block forever)
            result = redis_conn.blpop("votes", timeout=0)
            if result is None:
                continue

            _, vote_value = result  # result is (key, value)
            logger.info("Received vote: %s", vote_value)

            cursor.execute(
                "INSERT INTO votes (vote) VALUES (%s)",
                (vote_value,),
            )
            logger.info("Vote '%s' saved to PostgreSQL", vote_value)

        except redis.RedisError as e:
            logger.error("Redis error: %s — reconnecting …", e)
            redis_conn = connect_redis()

        except psycopg2.Error as e:
            logger.error("PostgreSQL error: %s — reconnecting …", e)
            pg_conn = connect_postgres()
            cursor = pg_conn.cursor()

        except KeyboardInterrupt:
            logger.info("Shutting down worker …")
            break

        except Exception as e:
            logger.error("Unexpected error: %s", e)
            time.sleep(RETRY_DELAY)

    # Cleanup
    try:
        cursor.close()
        pg_conn.close()
    except Exception:
        pass

    logger.info("Worker stopped.")


if __name__ == "__main__":
    main()
