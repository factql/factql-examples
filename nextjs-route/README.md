# Next.js route

A server route that forwards questions to FactQL, so your full-access key never reaches the browser.

1. Copy `app/api/ask/route.ts` into your Next.js (App Router) project.
2. Set `FACTQL_API_KEY` in `.env.local` (server-side only, no `NEXT_PUBLIC_` prefix).
3. From your UI:

```ts
const res = await fetch("/api/ask", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ question: "Top 5 customers by spend" }),
});
const answer = await res.json(); // { ok, explanation, columns, rows, sql } or { ok: false, explanation }
```

Add your own auth check at the top of the route before going to production: anyone who can reach the route can spend your FactQL usage.
