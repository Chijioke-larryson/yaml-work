# Microservices Voting App

A minimal, production-like microservices application for learning and containerization practice.

## Architecture

```
┌──────────────┐       ┌───────────┐       ┌────────────┐       ┌──────────────┐
│   Browser    │──────▶│  Vote App │──────▶│   Redis    │◀──────│   Worker     │
│              │       │  (Flask)  │       │  (Queue)   │       │  (Python)    │
└──────────────┘       └───────────┘       └────────────┘       └──────┬───────┘
                                                                       │
                                                                       ▼
                                                                ┌──────────────┐
                                                                │  PostgreSQL  │
                                                                │  (Storage)   │
                                                                └──────────────┘
```

## Folder Structure

```
voting-app/
├── vote/
│   ├── app.py              # Flask web app
│   ├── templates/
│   │   └── index.html      # Voting UI
│   └── requirements.txt
├── worker/
│   ├── worker.py           # Redis → PostgreSQL consumer
│   └── requirements.txt
├── schema.sql              # Database schema
└── README.md
```

## Prerequisites

- Python 3.9+
- Redis server
- PostgreSQL server

## Local Setup

### 1. Start Redis

```bash
# macOS (Homebrew)
brew install redis
brew services start redis

# Or run directly
redis-server
```

### 2. Set up PostgreSQL

```bash
# Create the database
createdb votes_db

# Apply the schema
psql -d votes_db -f schema.sql
```

### 3. Start the Vote App

```bash
cd vote
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables (defaults work for local dev)
export REDIS_HOST=localhost

python app.py
```

The voting UI is now available at **http://localhost:5000**.

### 4. Start the Worker

Open a **new terminal**:

```bash
cd worker
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables
export REDIS_HOST=localhost
export POSTGRES_HOST=localhost
export POSTGRES_DB=votes_db
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres

python worker.py
```

### 5. Verify

1. Open http://localhost:5000 and click **Cats** or **Dogs**.
2. Watch the worker terminal — you should see logs like `Vote 'cats' saved to PostgreSQL`.
3. Query the database:

```bash
psql -d votes_db -c "SELECT * FROM votes;"
```

## Environment Variables

| Variable            | Default     | Used By       |
|---------------------|-------------|---------------|
| `REDIS_HOST`        | `localhost` | vote, worker  |
| `REDIS_PORT`        | `6379`      | vote, worker  |
| `POSTGRES_HOST`     | `localhost` | worker        |
| `POSTGRES_PORT`     | `5432`      | worker        |
| `POSTGRES_DB`       | `votes_db`  | worker        |
| `POSTGRES_USER`     | `postgres`  | worker        |
| `POSTGRES_PASSWORD` | `postgres`  | worker        |
