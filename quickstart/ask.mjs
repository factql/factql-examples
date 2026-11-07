// Ask FactQL one question. Usage: node ask.mjs "your question"   (Node 18+)
const question = process.argv.slice(2).join(" ") || "What were the top 5 products by revenue?";

const resp = await fetch("https://api.factql.ai/query", {
  method: "POST",
  headers: { "X-API-Key": process.env.FACTQL_API_KEY, "Content-Type": "application/json" },
  body: JSON.stringify({ q: question }),
});
if (!resp.ok) throw new Error(`FactQL answered HTTP ${resp.status}`);
const answer = await resp.json();

if (answer.result !== "success") {
  console.log("FactQL couldn't verify an answer:", answer.explanation);
} else {
  console.log(answer.explanation, "\n");
  console.table(answer.data?.rows ?? []);
  console.log("Query that ran:\n" + answer.sql);
}
