// app/api/ask/route.ts — Next.js App Router
// Keeps FACTQL_API_KEY on the server. Add your own auth check before production.
import { NextResponse } from "next/server";

export async function POST(req: Request) {
  const { question } = await req.json().catch(() => ({ question: "" }));
  if (typeof question !== "string" || !question.trim() || question.length > 4096) {
    return NextResponse.json({ ok: false, explanation: "Ask a question." }, { status: 400 });
  }

  const resp = await fetch("https://api.factql.ai/query", {
    method: "POST",
    headers: {
      "X-API-Key": process.env.FACTQL_API_KEY ?? "",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ q: question }),
    cache: "no-store",
  });

  if (!resp.ok) {
    return NextResponse.json(
      { ok: false, explanation: "The data service is busy. Try again in a moment." },
      { status: resp.status === 429 ? 429 : 502 },
    );
  }

  const a = await resp.json();
  if (a.result !== "success") {
    // A decline: pass FactQL's explanation through, never a guessed number.
    return NextResponse.json({ ok: false, explanation: a.explanation });
  }
  return NextResponse.json({
    ok: true,
    explanation: a.explanation,
    columns: a.data?.columns ?? [],
    rows: a.data?.rows ?? [],
    sql: a.sql,
  });
}
