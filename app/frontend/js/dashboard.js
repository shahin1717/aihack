// Dashboard page logic

document.addEventListener("DOMContentLoaded", () => {
    pgRequireAuth();
    pgInitLogout();
    pgUpdateAuthBadge();

    const btnLoad = document.getElementById("btn-load-stats");
    if (btnLoad) btnLoad.onclick = loadStats;

    // Autofill from ?camp=ID or ?campaign_id=ID
    const urlParams = new URLSearchParams(window.location.search);
    const campId = urlParams.get("camp") || urlParams.get("campaign_id");
    if (campId) {
        const input = document.getElementById("dash-camp-id");
        if (input) input.value = campId;
    }
});

async function loadStats() {
    const id = document.getElementById("dash-camp-id").value;
    const out = document.getElementById("dash-json");

    if (!id) {
        out.textContent = "Enter a campaign ID.";
        return;
    }

    out.textContent = "Loading...";

    try {
        const res = await fetch(`${API_BASE}/dashboard/campaign/${id}`, {
            headers: pgAuthHeaders()
        });

        const data = await res.json();
        if (!res.ok) {
            out.textContent = data.detail || "Error";
            return;
        }

        out.textContent = JSON.stringify(data, null, 2);

    } catch (err) {
        out.textContent = "Network error";
    }
}
