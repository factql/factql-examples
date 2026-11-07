# FactQL examples

**The model writes a plausible answer. FactQL makes it true.**

FactQL runs the query before it answers. Every answer comes back with the query that ran, the rows it returned, and a short explanation of only those rows. When it can't back an answer, it declines instead of guessing.

These are small, runnable examples of putting FactQL behind an AI app or agent.

| Folder | What it shows | Language |
|---|---|---|
| [`quickstart/`](quickstart) | Ask one question, print the answer, the rows and the query | curl, Python, Node |
| [`declines/`](declines) | Show "can't verify" to your user instead of a wrong number | Python, Node |
| [`langchain-tool/`](langchain-tool) | FactQL as a tool for a LangChain or LangGraph agent | Python |
| [`function-calling/`](function-calling) | FactQL as a tool for OpenAI-compatible function calling | Python |
| [`nextjs-route/`](nextjs-route) | A server route that keeps your key off the browser | TypeScript |
| [`embed-chat/`](embed-chat) | A ready-made chat on any web page with one tag | HTML |

## Before you start

1. Get a free key at [factql.ai](https://factql.ai/?ref=github): free tier, no card. Want to look first? The [docs](https://docs.factql.ai/?ref=github) have a Try it panel on sample data, no signup needed.
2. Add data: upload a CSV or connect PostgreSQL or MySQL in the app.
3. `cp .env.example .env` and put your key in it, or `export FACTQL_API_KEY=fl_live_...`.

Keep full-access keys on your server. Use an ask-only key for anything a browser loads.

## What an answer looks like

```json
{
  "result": "success",
  "sql": "SELECT region, SUM(revenue) AS total_revenue FROM orders GROUP BY region ORDER BY total_revenue DESC",
  "data": {
    "columns": ["region", "total_revenue"],
    "rows": [["North", 43148.0], ["South", 41223.0], ["West", 41113.0], ["East", 40823.0]]
  },
  "explanation": "North leads with 43,148, followed by South (41,223), West (41,113) and East (40,823).",
  "lineage": { "text": "Computed SUM(revenue); from orders; broken down by region." },
  "trace_id": "c5f50cff-..."
}
```

And when it can't answer:

```json
{
  "result": "error",
  "decline_reason": "no_safe_sql",
  "explanation": "I couldn't find data that answers this. Try naming the table or column you mean.",
  "trace_id": "c5f50cff-..."
}
```

A decline is still HTTP 200. Show the `explanation` to your user and don't retry the same question. See [`declines/`](declines).

## Links

- Docs: https://docs.factql.ai/?ref=github
- Website: https://factql.ai/?ref=github
- Questions and ideas: open a Discussion in this repo

MIT licensed. Examples only: they call the public FactQL API.
