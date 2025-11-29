const API_BASE = "http://127.0.0.1:8000";

function getToken() {
    return localStorage.getItem("pg_token");
}

function headersAuth() {
    const t = getToken();
    return t ? { "Authorization": "Bearer " + t } : {};
}

document.getElementById("btn-reload-campaigns").onclick = loadCampaigns;
document.getElementById("btn-create-campaign").onclick = createCampaign;

// -------- LOAD CAMPAIGNS ----------
async function loadCampaigns() {
    const status = document.getElementById("camp-status");
    const tbody = document.getElementById("camp-table");
    tbody.innerHTML = "";

    status.textContent = "Loading...";

    try {
        const res = await fetch(`${API_BASE}/campaigns/`, {
            headers: { ...headersAuth() }
        });

        const data = await res.json();
        if (!res.ok) {
            status.textContent = data.detail || "Error";
            return;
        }

        status.textContent = "";

        data.forEach(c => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${c.id}</td>
                <td>${c.title}</td>
                <td>${c.sender_name} &lt;${c.sender_email}&gt;</td>
                <td>
                    <button class="btn-secondary" onclick="viewStats(${c.id})">Stats</button>
                </td>
            `;
            tbody.appendChild(row);
        });

    } catch {
        status.textContent = "Network error";
    }
}

// -------- CREATE CAMPAIGN ----------
async function createCampaign() {
    const title = document.getElementById("camp-title").value;
    const sender_name = document.getElementById("camp-sender-name").value;
    const sender_email = document.getElementById("camp-sender-email").value;
    const subject = document.getElementById("camp-subject").value;
    const body_html = document.getElementById("camp-body").value;

    const raw = document.getElementById("camp-employee-ids").value;
    const ids = raw.split(",").map(x => parseInt(x.trim())).filter(x => !isNaN(x));

    const status = document.getElementById("camp-status");
    status.textContent = "Sending...";

    try {
        const res = await fetch(`${API_BASE}/campaigns/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...headersAuth()
            },
            body: JSON.stringify({
                title,
                sender_name,
                sender_email,
                subject,
                body_html,
                employee_ids: ids
            })
        });

        const data = await res.json();
        if (!res.ok) {
            status.textContent = data.detail || "Error";
            return;
        }

        status.textContent = `Campaign created (ID ${data.id}).`;
        loadCampaigns();

    } catch {
        status.textContent = "Network error";
    }
}

// Go to dashboard
function viewStats(id) {
    window.location.href = `/dashboard.html?camp=${id}`;
}

// auto load
loadCampaigns();
