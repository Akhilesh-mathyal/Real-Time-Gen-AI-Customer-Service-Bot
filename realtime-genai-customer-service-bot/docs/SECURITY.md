# Security and responsible deployment

- Keep `OPENAI_API_KEY` only in the server environment; `.env` is ignored by Git.
- Do not collect passwords, payment data, authentication codes, or other secrets in the chat.
- Minimize retention of customer messages and document retention periods.
- Enforce authentication, authorization, rate limits, input/output filtering, and audit logging before deployment.
- The included knowledge base is sample content. Replace it with approved, version-controlled policies.
- Streaming exposes partial output immediately; assess moderation and escalation requirements before a production release.
