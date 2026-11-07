"""A LangGraph agent that answers data questions through FactQL.

Usage: python agent.py "your question"
"""
import json
import os
import sys

import requests
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent


@tool
def ask_factql(question: str) -> str:
    """Answer a question about the company's data (sales, customers, orders...).
    Returns a verified answer with the query and rows behind it, or DECLINED
    if the data can't support an answer."""
    resp = requests.post(
        "https://api.factql.ai/query",
        headers={"X-API-Key": os.environ["FACTQL_API_KEY"]},
        json={"q": question},
        timeout=120,
    )
    resp.raise_for_status()
    answer = resp.json()
    if answer.get("result") != "success":
        return "DECLINED: " + answer.get("explanation", "FactQL could not verify an answer.")
    data = answer.get("data") or {}
    return json.dumps(
        {
            "answer": answer.get("explanation"),
            "query": answer.get("sql"),
            "columns": data.get("columns"),
            "rows": (data.get("rows") or [])[:10],
            "lineage": (answer.get("lineage") or {}).get("text"),
        }
    )


SYSTEM = (
    "You answer questions about the user's business data using the ask_factql tool. "
    "Only state numbers that come back from the tool. If the tool returns DECLINED, "
    "tell the user you can't verify that from their data and pass on the explanation. "
    "Never estimate or fill in a number yourself."
)

if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "Which region had the highest revenue last month?"
    agent = create_react_agent(ChatOpenAI(model="gpt-4o-mini"), [ask_factql], prompt=SYSTEM)
    result = agent.invoke({"messages": [("user", question)]})
    print(result["messages"][-1].content)
