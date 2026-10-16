"""Customer-service response generation with an optional OpenAI streaming backend."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Generator

from openai import OpenAI

BASE_DIR = Path(__file__).parent
KNOWLEDGE_BASE = json.loads((BASE_DIR / "data" / "knowledge_base.json").read_text(encoding="utf-8"))
SYSTEM_INSTRUCTIONS = """You are Acme Shop's helpful customer-service assistant. Be concise, warm, and accurate.
Use only the supplied knowledge-base context for company policies. Never request passwords, payment-card numbers, one-time codes, or other sensitive data. For order-specific, billing, account-verification, or unresolved issues, offer human support. Do not invent order status, discounts, policies, or guarantees."""


def relevant_context(message: str) -> str:
    words = message.lower()
    matches = [item["answer"] for item in KNOWLEDGE_BASE if any(key in words for key in item["keywords"])]
    return "\n".join(matches) or "No matching policy was found. Offer to connect the customer to human support."


def fallback_reply(message: str) -> str:
    context = relevant_context(message)
    if "No matching" in context:
        return "I don’t have enough information to answer that accurately. I can connect you with a support agent who can help."
    return f"Here’s what I can share: {context} Would you like help with anything else?"


def stream_reply(message: str, history: list[dict[str, str]]) -> Generator[tuple[str, str], None, None]:
    """Yield (event name, text) tuples; falls back when no API key is set."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        yield "mode", "demo"
        yield "token", fallback_reply(message)
        return
    client = OpenAI(api_key=api_key)
    instructions = f"{SYSTEM_INSTRUCTIONS}\n\nRelevant context:\n{relevant_context(message)}"
    input_messages = []
    input_messages.extend({"role": turn["role"], "content": turn["content"]} for turn in history[-8:])
    input_messages.append({"role": "user", "content": message})
    stream = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-6-astra"),
        instructions=instructions,
        input=input_messages,
        stream=True,
    )
    yield "mode", "live"
    for event in stream:
        if event.type == "response.output_text.delta":
            yield "token", event.delta
