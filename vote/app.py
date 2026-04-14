import os
from flask import Flask, render_template, request, redirect, url_for
import redis

app = Flask(__name__)

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))


def get_redis():
    """Create a Redis connection."""
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/vote", methods=["POST"])
def vote():
    vote_value = request.form.get("vote")
    if vote_value not in ("cats", "dogs"):
        return "Invalid vote", 400

    try:
        r = get_redis()
        r.rpush("votes", vote_value)
    except redis.RedisError as e:
        return f"Failed to submit vote: {e}", 500

    return render_template("index.html", message=f"Thank you! You voted for {vote_value.title()}.")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
