pgRequireAuth();
pgInitLogout();
pgUpdateAuthBadge();

// DOM elements
const depNameInput = document.getElementById("dep-name");
const btnCreateDep = document.getElementById("btn-create-department");
const depStatus = document.getElementById("dep-status");

const empNameInput = document.getElementById("emp-name");
const empEmailInput = document.getElementById("emp-email");
const depSelect = document.getElementById("department");
const btnCreateEmployee = document.getElementById("btn-create-employee");
const empStatus = document.getElementById("emp-status");

const btnReloadEmployees = document.getElementById("btn-reload-employees");
const empTableBody = document.getElementById("emp-table");


// ------------------------------------------------------
// LOAD DEPARTMENTS INTO DROPDOWN
// ------------------------------------------------------
async function loadDepartments() {
    const select = document.getElementById("department");
    if (!select) return;

    select.innerHTML = `<option value="">-- Select department --</option>`;

    try {
        const res = await fetch(`${API_BASE}/departments/`, {
            method: "GET",
            headers: pgAuthHeaders()
        });

        if (!res.ok) {
            console.error("Failed to load departments");
            return;
        }

        const deps = await res.json();

        deps.forEach(dep => {
            const opt = document.createElement("option");
            opt.value = dep.id;
            opt.textContent = dep.name;
            select.appendChild(opt);
        });

    } catch (err) {
        console.error("Error loading departments", err);
    }
}



// ------------------------------------------------------
// CREATE A DEPARTMENT
// ------------------------------------------------------
async function createDepartment() {
    const name = depNameInput.value.trim();
    if (!name) {
        depStatus.textContent = "Enter department name.";
        return;
    }

    depStatus.textContent = "Creating...";

    try {
        const res = await fetch(`${API_BASE}/departments/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...pgAuthHeaders()
            },
            body: JSON.stringify({ name })
        });

        const data = await res.json();

        if (!res.ok) {
            depStatus.textContent = data.detail || "Failed.";
            return;
        }

        depStatus.textContent = `Department '${data.name}' created.`;
        depNameInput.value = "";
        loadDepartments(); // refresh dropdown

    } catch {
        depStatus.textContent = "Network error.";
    }
}


// ------------------------------------------------------
// CREATE EMPLOYEE
// ------------------------------------------------------
async function createEmployee() {
    const full_name = empNameInput.value.trim();
    const email = empEmailInput.value.trim();
    const department_id = parseInt(depSelect.value);

    if (!full_name || !email || !department_id) {
        empStatus.textContent = "Fill name, email and department.";
        return;
    }

    empStatus.textContent = "Creating employee...";

    try {
        const res = await fetch(`${API_BASE}/employees/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...pgAuthHeaders()
            },
            body: JSON.stringify({
                full_name,
                email,
                department_id
            })
        });

        const data = await res.json();

        if (!res.ok) {
            empStatus.textContent = data.detail || "Error creating employee.";
            return;
        }

        empStatus.textContent = `Employee '${data.full_name}' added.`;
        empNameInput.value = "";
        empEmailInput.value = "";
        depSelect.value = "";

        loadEmployees();

    } catch {
        empStatus.textContent = "Network error.";
    }
}


// ------------------------------------------------------
// LOAD EMPLOYEES TABLE
// ------------------------------------------------------
async function loadEmployees() {
    empTableBody.innerHTML = "";

    try {
        const res = await fetch(`${API_BASE}/employees/`, {
            headers: pgAuthHeaders()
        });

        const data = await res.json();

        if (!res.ok) {
            empTableBody.innerHTML = "<tr><td colspan='5'>Failed to load.</td></tr>";
            return;
        }

        data.forEach(emp => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${emp.id}</td>
                <td>${emp.full_name}</td>
                <td>${emp.email}</td>
                <td>${emp.department_name || "-"}</td>
                <td>${emp.awareness_score}</td>
            `;
            empTableBody.appendChild(tr);
        });

    } catch (err) {
        empTableBody.innerHTML = "<tr><td colspan='5'>Error.</td></tr>";
    }
}


// ------------------------------------------------------
// EVENT BINDINGS
// ------------------------------------------------------
if (btnCreateDep) btnCreateDep.addEventListener("click", createDepartment);
if (btnCreateEmployee) btnCreateEmployee.addEventListener("click", createEmployee);
if (btnReloadEmployees) btnReloadEmployees.addEventListener("click", loadEmployees);


// ------------------------------------------------------
// INIT
// ------------------------------------------------------
loadDepartments();
loadEmployees();
