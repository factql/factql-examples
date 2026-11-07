# FactQL as a function-calling tool

Works with any OpenAI-compatible chat API (OpenAI, Azure OpenAI, Groq, Together, a local server...). The model decides when to call `ask_factql`; your code makes the call and hands the result back.

```bash
pip install -r requirements.txt
export FACTQL_API_KEY=fl_live_...
export OPENAI_API_KEY=...
# optional, for other providers:
export OPENAI_BASE_URL=https://your-provider/v1
export MODEL=gpt-4o-mini
python chat.py "How many orders did we ship last week, and which customer ordered most?"
```
