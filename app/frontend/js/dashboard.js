requireAuth();

async function loadStats() {
  const idField = document.getElementById("dash-camp-id");
  const id = idField.value;
  const out = document.getElementById("dash-json");
  const statusEl = document.getElementById("dash-status");

  if (!id) {
    statusEl.textContent = "Enter ID.";
    return;
  }

  statusEl.textContent = "Loading...";

  try {
    const res = await fetch(`${API_BASE}/dashboard/campaign/${id}`, {
      headers: authHeaders()
    });

    const data = await res.json();

    if (!res.ok) {
      statusEl.textContent = data.detail || "Error";
      return;
    }

    statusEl.textContent = "";
    out.textContent = JSON.stringify(data, null, 2);

    // Summary boxes in future (optional)
  } catch {
    statusEl.textContent = "Network error";
  }
}

document.getElementById("dash-load-btn").onclick = loadStats;


// auto-fill from ?campaign=ID
const params = new URLSearchParams(window.location.search);
if (params.has("campaign")) {
  document.getElementById("dash-camp-id").value = params.get("campaign");
  loadStats();
}
