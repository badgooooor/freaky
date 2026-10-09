const MODES = ["freaky", "passive_aggressive", "wrong_occasion", "unhinged"];

const statusEl = document.getElementById("status");
const outputEl = document.getElementById("output");
const submitBtn = document.getElementById("submit");
const messageEl = document.getElementById("message");
const modeEl = document.getElementById("mode");

function setStatus(text, busy = false) {
  statusEl.textContent = text;
  submitBtn.disabled = busy;
}

submitBtn.addEventListener("click", async () => {
  if (submitBtn.disabled) return;
  const message = messageEl.value.trim();
  if (!message) return;

  const mode = modeEl.value;
  setStatus("Cursing…", true);
  outputEl.textContent = "";

  try {
    const res = await fetch("/label", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mode, message }),
    });
    if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
    const { emoji } = await res.json();
    outputEl.textContent = emoji;
    setStatus("", false);
  } catch (err) {
    setStatus(`Error: ${err.message}`, false);
  }
});
