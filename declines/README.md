# Handling declines

When FactQL can't back an answer, it says so instead of guessing. The response is still HTTP 200, with `"result": "error"`, a `decline_reason` and an `explanation` written for your user.

What your app should do:

1. Check `result` before you show any number.
2. On a decline, show the `explanation`. It tells the user what to change ("try naming the table or column you mean").
3. Don't retry the same question. It gets the same answer.
4. Retry only on HTTP 429, 500 and 503, after `Retry-After`.

```bash
python handle_declines.py "What was our ad spend last quarter?"
node handle_declines.mjs "What was our ad spend last quarter?"
```

A question the data can't answer, like ad spend on a sales-only database, is the easiest way to see a decline.
