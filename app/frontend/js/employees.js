// Employees page logic

document.addEventListener("DOMContentLoaded", () => {
    pgRequireAuth();
    pgInitLogout();
    pgUpdateAuthBadge();

    const btnReload = document.getElementById("btn-reload-employees");
    const btnCreate = document.getElementById("btn-create-employee");

    if (btnReload) btnReload.onclick = loadEmployees;
    if (btnCreate) btnCreate.onclick = createEmployee;

    // auto load on page open
    loadEmployees();
});

async function loadEmployees() {
    const status = document.getElementById("emp-status");
    const tbody = document.getElementById("emp-table");
    tbody.innerHTML = "";
    status.textContent = "Loading...";

    try {
        const res = await fetch(`${API_BASE}/employees/`, {
            headers: pgAuthHeaders()
        });

        const data = await res.json();
        if (!res.ok) {
            status.textContent = data.detail || "Error";
            return;
        }

        status.textContent = "";

        data.forEach(emp => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${emp.id}</td>
                <td>${emp.full_name}</td>
                <td>${emp.email}</td>
                <td>${emp.department || "-"}</td>
                <td>${emp.awareness_score}</td>
            `;
            tbody.appendChild(tr);
        });

    } catch (err) {
        status.textContent = "Network error";
    }
}

async function createEmployee() {
    const full_name = document.getElementById("emp-name").value;
    const email = document.getElementById("emp-email").value;
    const department = document.getElementById("emp-dept").value || null;
    const status = document.getElementById("emp-status");

    status.textContent = "Creating...";

    try {
        const res = await fetch(`${API_BASE}/employees/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...pgAuthHeaders()
            },
            body: JSON.stringify({ full_name, email, department })
        });

        const data = await res.json();
        if (!res.ok) {
            status.textContent = data.detail || "Error";
            return;
        }

        status.textContent = "Employee created.";
        loadEmployees();

    } catch (err) {
        status.textContent = "Network error";
    }
}
