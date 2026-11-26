const form = document.getElementById("expense-form");
const list = document.getElementById("list");
document.getElementById("spent_on").valueAsDate = new Date();

const money = (n) => Number(n).toFixed(2);

async function load() {
  const [expenses, summary] = await Promise.all([
    fetch("/api/expenses").then((r) => r.json()),
    fetch("/api/summary").then((r) => r.json()),
  ]);

  list.innerHTML = "";
  for (const e of expenses) {
    const li = document.createElement("li");
    li.innerHTML = `<div><strong></strong><br><small></small></div>
      <div><strong>₹${money(e.amount)}</strong> <button class="del" title="Delete">✕</button></div>`;
    li.querySelector("strong").textContent = e.title;
    li.querySelector("small").textContent = `${e.category} · ${e.spent_on}`;
    li.querySelector(".del").onclick = async () => {
      await fetch(`/api/expenses/${e.id}`, { method: "DELETE" });
      load();
    };
    list.appendChild(li);
  }

  document.getElementById("total").textContent = money(summary.total);
  const cats = document.getElementById("categories");
  cats.innerHTML = "";
  for (const [cat, total] of Object.entries(summary.by_category)) {
    const span = document.createElement("span");
    span.className = "chip";
    span.textContent = `${cat}: ₹${money(total)}`;
    cats.appendChild(span);
  }
}

form.addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const body = {
    title: document.getElementById("title").value.trim(),
    amount: parseFloat(document.getElementById("amount").value),
    category: document.getElementById("category").value,
  };
  const date = document.getElementById("spent_on").value;
  if (date) body.spent_on = date;

  const res = await fetch("/api/expenses", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) return alert("Could not add expense");
  form.reset();
  document.getElementById("spent_on").valueAsDate = new Date();
  load();
});

load();
