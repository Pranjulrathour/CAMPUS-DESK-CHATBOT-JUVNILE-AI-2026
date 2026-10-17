# Sends a prompt to the Groq LLM and returns its JSON reply. The API key is read from the .env file.
import json
import os
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

URL = "https://api.groq.com/openai/v1/chat/completions"


def ask_json(system_prompt, user_prompt, retries=3):
    """Return (reply_dict, seconds_spent_waiting_for_rate_limits)."""
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise RuntimeError("GROQ_API_KEY is missing. Add it to the .env file.")
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    body = {
        "model": model,
        "temperature": 0,
        "max_completion_tokens": 500,
        "response_format": {"type": "json_object"},
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
    }
    if model.startswith("openai/gpt-oss"):
        body["reasoning_effort"] = "low"

    waited = 0.0
    for attempt in range(retries + 1):
        response = httpx.post(URL, headers={"Authorization": f"Bearer {key}"}, json=body, timeout=30)
        if response.status_code == 429 and attempt < retries:
            pause = min(float(response.headers.get("retry-after", "2")), 20)
            time.sleep(pause)
            waited += pause
            continue
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return json.loads(content), waited
    raise RuntimeError("LLM rate limit: too many retries")
