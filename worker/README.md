# Worker Service for Redis and PostgreSQL

This repository contains a Python-based worker service that listens for votes on a Redis queue and saves them to a PostgreSQL database. The worker is designed to handle connection retries, logging, and error handling for robust operation in a containerized environment.

---

## Features

- **Redis Integration**: Listens for votes on a Redis queue (`votes`) using the `BLPOP` command.
- **PostgreSQL Integration**: Saves received votes into a PostgreSQL database table.
- **Retry Mechanism**: Implements exponential backoff for Redis and PostgreSQL connection retries.
- **Logging**: Provides detailed logs for debugging and monitoring.
- **Graceful Shutdown**: Handles `KeyboardInterrupt` for clean shutdown.

---

## Prerequisites

- Python 3.8+
- Docker (for containerized deployment)
- Redis
- PostgreSQL

---

## Environment Variables

The worker service uses the following environment variables for configuration:

| Variable Name       | Default Value | Description                          |
|---------------------|---------------|--------------------------------------|
| [`REDIS_HOST`](command:_github.copilot.openSymbolFromReferences?%5B%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2FUsers%2Fjioke%2F.gemini%2Fantigravity%2Fscratch%2Fvoting-app%2Fworker%2Fworker.py%22%2C%22scheme%22%3A%22file%22%7D%2C%7B%22line%22%3A10%2C%22character%22%3A0%7D%5D "worker/worker.py")        | `localhost`   | Redis server hostname                |
| [`REDIS_PORT`](command:_github.copilot.openSymbolFromReferences?%5B%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2FUsers%2Fjioke%2F.gemini%2Fantigravity%2Fscratch%2Fvoting-app%2Fworker%2Fworker.py%22%2C%22scheme%22%3A%22file%22%7D%2C%7B%22line%22%3A11%2C%22character%22%3A0%7D%5D "worker/worker.py")        | `6380`        | Redis server port                    |
| [`POSTGRES_HOST`](command:_github.copilot.openSymbolFromReferences?%5B%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2FUsers%2Fjioke%2F.gemini%2Fantigravity%2Fscratch%2Fvoting-app%2Fworker%2Fworker.py%22%2C%22scheme%22%3A%22file%22%7D%2C%7B%22line%22%3A13%2C%22character%22%3A0%7D%5D "worker/worker.py")     | `localhost`   | PostgreSQL server hostname           |
| [`POSTGRES_PORT`](command:_github.copilot.openSymbolFromReferences?%5B%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2FUsers%2Fjioke%2F.gemini%2Fantigravity%2Fscratch%2Fvoting-app%2Fworker%2Fworker.py%22%2C%22scheme%22%3A%22file%22%7D%2C%7B%22line%22%3A14%2C%22character%22%3A0%7D%5D "worker/worker.py")     | `5432`        | PostgreSQL server port               |
| [`POSTGRES_DB`](command:_github.copilot.openSymbolFromReferences?%5B%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2FUsers%2Fjioke%2F.gemini%2Fantigravity%2Fscratch%2Fvoting-app%2Fworker%2Fworker.py%22%2C%22scheme%22%3A%22file%22%7D%2C%7B%22line%22%3A15%2C%22character%22%3A0%7D%5D "worker/worker.py")       | `votes_db`    | PostgreSQL database name             |
| [`POSTGRES_USER`](command:_github.copilot.openSymbolFromReferences?%5B%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2FUsers%2Fjioke%2F.gemini%2Fantigravity%2Fscratch%2Fvoting-app%2Fworker%2Fworker.py%22%2C%22scheme%22%3A%22file%22%7D%2C%7B%22line%22%3A16%2C%22character%22%3A0%7D%5D "worker/worker.py")     | `postgres`    | PostgreSQL username                  |
| [`POSTGRES_PASSWORD`](command:_github.copilot.openSymbolFromReferences?%5B%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2FUsers%2Fjioke%2F.gemini%2Fantigravity%2Fscratch%2Fvoting-app%2Fworker%2Fworker.py%22%2C%22scheme%22%3A%22file%22%7D%2C%7B%22line%22%3A17%2C%22character%22%3A0%7D%5D "worker/worker.py") | `postgres`    | PostgreSQL password                  |

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/<repository-name>.git
cd <repository-name>