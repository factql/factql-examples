"""OpenAI-compatible function calling with FactQL as the data tool.

Usage: python chat.py "your question"
"""
import json
import os
import sys

import requests
from openai import OpenAI

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "ask_factql",
            "description": (
                "Answer a question about the company's data. Returns a verified answer "
                "with the query and rows behind it, or a decline if the data can't support one."
            ),
            "parameters": {
                "type": "object",
                "properties": {"question": {"type": "string", "description": "The question, in plain English."}},
                "required": ["question"],
            },
        },
    }
]

SYSTEM = (
    "Answer data questions only with numbers returned by ask_factql. "
    "If it declines, say you can't verify that and pass on its explanation. Never estimate."
)


def ask_factql(question: str) -> dict:
    resp = requests.post(
        "https://api.factql.ai/query",
        headers={"X-API-Key": os.environ["FACTQL_API_KEY"]},
        json={"q": question},
        timeout=120,
    )
    resp.raise_for_status()
    a = resp.json()
    if a.get("result") != "success":
        return {"declined": True, "explanation": a.get("explanation")}
    data = a.get("data") or {}
    return {
        "answer": a.get("explanation"),
        "query": a.get("sql"),
        "columns": data.get("columns"),
        "rows": (data.get("rows") or [])[:10],
    }


def main(question: str) -> None:
    client = OpenAI()  # reads OPENAI_API_KEY and OPENAI_BASE_URL
    model = os.environ.get("MODEL", "gpt-4o-mini")
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": question}]

    for _ in range(5):  # a few tool rounds at most
        msg = client.chat.completions.create(model=model, messages=messages, tools=TOOLS).choices[0].message
        if not msg.tool_calls:
            print(msg.content)
            return
        messages.append(msg)
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)
            result = ask_factql(args["question"])
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
    print("Stopped after too many tool calls.")


if __name__ == "__main__":
    main(" ".join(sys.argv[1:]) or "How many orders did we ship last week?")
