"""Show users a clear "can't verify" instead of a wrong number.

Usage: python handle_declines.py "your question"
"""
import os
import sys
import time

import requests

API = "https://api.factql.ai/query"
RETRYABLE = {429, 500, 503}


def ask(question: str, attempts: int = 3) -> dict:
    for attempt in range(attempts):
        resp = requests.post(
            API,
            headers={"X-API-Key": os.environ["FACTQL_API_KEY"]},
            json={"q": question},
            timeout=120,
        )
        if resp.status_code in RETRYABLE and attempt < attempts - 1:
            time.sleep(int(resp.headers.get("Retry-After", 2 ** (attempt + 1))))
            continue
        resp.raise_for_status()
        return resp.json()
    raise RuntimeError("unreachable")


def render(answer: dict) -> str:
    """What your UI shows. Never a number FactQL couldn't back."""
    if answer.get("result") == "success":
        return answer["explanation"]
    # A decline: show FactQL's explanation, keep the reason for your logs.
    reason = answer.get("decline_reason", "unknown")
    print(f"[log] declined: {reason} trace={answer.get('trace_id')}", file=sys.stderr)
    return f"I can't verify that from your data. {answer.get('explanation', '')}".strip()


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "What was our ad spend last quarter?"
    print(render(ask(q)))
