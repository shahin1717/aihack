const API_BASE = "http://127.0.0.1:8000";

function getToken() {
    return localStorage.getItem("pg_token");
}

function headersAuth() {
    const token = getToken();
    return token ? { "Authorization": "Bearer " + token } : {};
}

document.getElementById("btn-reload-employees").onclick = loadEmployees;
document.getElementById("btn-create-employee").onclick = createEmployee;

// -------- LOAD EMPLOYEES ----------
async function loadEmployees() {
    const status = document.getElementById("emp-status");
    const tbody = document.getElementById("emp-table");
    tbody.innerHTML = "";

    if (!getToken()) {
        status.textContent = "You must login first.";
        return;
    }

    status.textContent = "Loading...";

    try {
        const res = await fetch(`${API_BASE}/employees/`, {
            method: "GET",
            headers: { ...headersAuth() }
        });

        const data = await res.json();
        if (!res.ok) {
            status.textContent = data.detail || "Error";
            return;
        }

        status.textContent = "";

        data.forEach(emp => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${emp.id}</td>
                <td>${emp.full_name}</td>
                <td>${emp.email}</td>
                <td>${emp.department || "-"}</td>
                <td>${emp.awareness_score}</td>
            `;
            tbody.appendChild(row);
        });

    } catch {
        status.textContent = "Network error";
    }
}

// -------- CREATE EMPLOYEE ----------
async function createEmployee() {
    const full_name = document.getElementById("emp-name").value;
    const email = document.getElementById("emp-email").value;
    const department = document.getElementById("emp-dept").value;
    const status = document.getElementById("emp-status");

    status.textContent = "Creating...";

    try {
        const res = await fetch(`${API_BASE}/employees/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...headersAuth()
            },
            body: JSON.stringify({ full_name, email, department })
        });

        const data = await res.json();
        if (!res.ok) {
            status.textContent = data.detail || "Error";
            return;
        }

        status.textContent = "Created!";
        loadEmployees();

    } catch {
        status.textContent = "Network error";
    }
}

// auto load on page enter
loadEmployees();
