# Architecture

```text
Browser UI → POST /api/chat/stream → Flask server → Responses API
                 ↑                       ↓
           streamed SSE tokens     policy context + FAQ knowledge base
```

The browser never receives an API key. It sends its current message and a limited conversation history to the Flask service. The server finds relevant FAQ snippets, adds customer-service instructions, and streams only output-text deltas back as SSE events. When no API key is configured, a deterministic FAQ fallback enables demos and automated tests.

For production, add authentication, a rate limiter, structured logs without message bodies, monitoring, a real help-desk handoff, and a reviewed retrieval pipeline.
