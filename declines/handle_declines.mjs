// Show users a clear "can't verify" instead of a wrong number.   (Node 18+)
// Usage: node handle_declines.mjs "your question"
const RETRYABLE = new Set([429, 500, 503]);

async function ask(question, attempts = 3) {
  for (let i = 0; i < attempts; i++) {
    const resp = await fetch("https://api.factql.ai/query", {
      method: "POST",
      headers: { "X-API-Key": process.env.FACTQL_API_KEY, "Content-Type": "application/json" },
      body: JSON.stringify({ q: question }),
    });
    if (RETRYABLE.has(resp.status) && i < attempts - 1) {
      const wait = Number(resp.headers.get("Retry-After")) || 2 ** (i + 1);
      await new Promise((r) => setTimeout(r, wait * 1000));
      continue;
    }
    if (!resp.ok) throw new Error(`FactQL answered HTTP ${resp.status}`);
    return resp.json();
  }
}

function render(answer) {
  if (answer.result === "success") return answer.explanation;
  console.error(`[log] declined: ${answer.decline_reason ?? "unknown"} trace=${answer.trace_id}`);
  return `I can't verify that from your data. ${answer.explanation ?? ""}`.trim();
}

const q = process.argv.slice(2).join(" ") || "What was our ad spend last quarter?";
console.log(render(await ask(q)));
