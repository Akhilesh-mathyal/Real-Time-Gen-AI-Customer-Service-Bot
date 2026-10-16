# Real-Time Gen AI Customer Service Bot

A full-stack customer-service chat application with real-time streaming answers, a small product knowledge base, suggested prompts, and human-support escalation. It uses the OpenAI Responses API when `OPENAI_API_KEY` is configured and provides a safe offline demo responder otherwise.

## Features

- Streaming customer replies in the browser
- Configurable system instructions and support tone
- Product FAQ grounding from `data/knowledge_base.json`
- Clear human-support handoff for unresolved issues
- No API key exposed to the browser
- Offline/demo fallback for presentations without API credentials
- Tests for the API, fallback, and input validation

## Run it

```powershell
cd realtime-genai-customer-service-bot
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Add OPENAI_API_KEY to .env to use a live model
python app.py
```

Visit `http://127.0.0.1:5000`. Without a key, the app runs in demo mode.

## Test

```powershell
pytest -q
```

## Live-model configuration

Set `OPENAI_API_KEY` and optionally `OPENAI_MODEL` in `.env`. The default is `gpt-6-astra`; change it to a model available to your project. Keep the key server-side and never commit `.env`.

The server sends Responses API output text deltas to the browser over a server-sent event stream. See the [official OpenAI streaming guide](https://developers.openai.com/api/docs/guides/streaming-responses).

## API

`POST /api/chat/stream`

```json
{"message":"Where is my order?", "history":[{"role":"user","content":"Hello"}]}
```

The response is `text/event-stream` with `token`, `mode`, `error`, and `done` events.

## Submission links

Replace after you publish the repository and create a Drive folder for the editable sample knowledge-base data:

- GitHub repository: `https://github.com/<your-account>/realtime-genai-customer-service-bot`
- Google Drive folder: `https://drive.google.com/drive/folders/<your-folder-id>`

## Project layout

```
app.py                 Flask server and streaming endpoint
service.py             Live and fallback chat services
data/knowledge_base.json  Editable demo FAQs
static/                Chat UI assets
tests/                 Automated tests
docs/                  architecture, setup, security and test plan
```
