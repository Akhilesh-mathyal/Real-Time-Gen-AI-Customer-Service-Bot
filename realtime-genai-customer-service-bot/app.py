"""Flask application for the real-time customer service bot."""
from __future__ import annotations

import json
import os

from dotenv import load_dotenv
from flask import Flask, Response, jsonify, render_template, request, stream_with_context

from service import stream_reply

load_dotenv()
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024


def sse(event: str, data: str) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/chat/stream")
def chat_stream():
    payload = request.get_json(silent=True) or {}
    message = payload.get("message", "").strip()
    history = payload.get("history", [])
    if not isinstance(message, str) or not message:
        return jsonify(error="Message is required."), 400
    if len(message) > 2000:
        return jsonify(error="Message must be 2,000 characters or fewer."), 400
    if not isinstance(history, list):
        return jsonify(error="History must be a list."), 400
    safe_history = [turn for turn in history if isinstance(turn, dict) and turn.get("role") in {"user", "assistant"} and isinstance(turn.get("content"), str) and len(turn["content"]) <= 4000]

    def generate():
        try:
            for event, text in stream_reply(message, safe_history):
                yield sse(event, text)
            yield sse("done", "")
        except Exception:
            app.logger.exception("Chat generation failed")
            yield sse("error", "I’m sorry, the chat service is temporarily unavailable. Please try again or contact human support.")
            yield sse("done", "")

    return Response(stream_with_context(generate()), mimetype="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify(error="Request is too large."), 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
