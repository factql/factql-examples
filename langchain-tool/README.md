# FactQL as a LangChain / LangGraph tool

Give your agent one tool for questions about your data. The agent gets back the answer with its evidence, or a decline it can pass on, never a number FactQL couldn't back.

```bash
pip install -r requirements.txt
export FACTQL_API_KEY=fl_live_...
export OPENAI_API_KEY=...        # or swap in any chat model LangChain supports
python agent.py "Which region had the highest revenue last month?"
```

The tool returns the explanation plus the query and a few rows, so the agent can cite them. On a decline it returns the explanation prefixed with `DECLINED:`, and the system prompt tells the agent to say it can't verify rather than estimate.
