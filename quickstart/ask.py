"""Ask FactQL one question. Usage: python ask.py "your question" """
import os
import sys

import requests

API = "https://api.factql.ai/query"


def ask(question: str) -> dict:
    resp = requests.post(
        API,
        headers={"X-API-Key": os.environ["FACTQL_API_KEY"]},
        json={"q": question},
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "What were the top 5 products by revenue?"
    answer = ask(question)

    if answer.get("result") != "success":
        print("FactQL couldn't verify an answer:", answer.get("explanation"))
        sys.exit(0)

    print(answer["explanation"], "\n")
    data = answer.get("data") or {}
    print(" | ".join(data.get("columns", [])))
    for row in data.get("rows", []):
        print(" | ".join(str(v) for v in row))
    print("\nQuery that ran:\n" + answer.get("sql", ""))
