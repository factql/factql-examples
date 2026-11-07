# Quickstart

Ask one question and print the answer, the rows and the query that ran.

```bash
export FACTQL_API_KEY=fl_live_...

# curl
./ask.sh "What were the top 5 products by revenue?"

# Python (pip install requests)
python ask.py "What were the top 5 products by revenue?"

# Node 18+
node ask.mjs "What were the top 5 products by revenue?"
```

Each call stands alone. For follow-up questions ("and last month?"), use the streaming Conversations endpoint in the [docs](https://docs.factql.ai/api/conversations/?ref=github).
