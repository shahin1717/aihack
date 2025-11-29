// ======================
// CONFIG
// ======================
// API_BASE is imported from utils.js (loaded before this script)

// ======================
// BUTTON EVENT ATTACH
// ======================
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("btn-register").addEventListener("click", registerAdmin);
    document.getElementById("btn-login").addEventListener("click", login);
});

// ======================
// REGISTER ADMIN
// ======================
async function registerAdmin() {
    const email = document.getElementById("reg-email").value;
    const password = document.getElementById("reg-password").value;
    const statusEl = document.getElementById("reg-status");

    statusEl.textContent = "Registering...";

    try {
        const res = await fetch(`${API_BASE}/auth/register`, {     // 👈 correct endpoint
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (!res.ok) {
            statusEl.textContent = data.detail || "Error registering.";
            return;
        }

        // Save token
        localStorage.setItem("pg_token", data.access_token);
        localStorage.setItem("pg_email", email);

        statusEl.textContent = "Registered successfully. Redirecting...";
        setTimeout(() => window.location.href = "employees.html", 800);

    } catch (e) {
        statusEl.textContent = "Network error";
    }
}

// ======================
// LOGIN ADMIN
// ======================
async function login() {
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;
    const statusEl = document.getElementById("login-status");

    statusEl.textContent = "Logging in...";

    try {
        const res = await fetch(`${API_BASE}/auth/login`, {   // 👈 correct route
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (!res.ok) {
            statusEl.textContent = data.detail || "Invalid credentials.";
            return;
        }

        // Save token
        localStorage.setItem("pg_token", data.access_token);
        localStorage.setItem("pg_email", email);

        statusEl.textContent = "Login successful. Redirecting...";
        setTimeout(() => window.location.href = "employees.html", 800);

    } catch (e) {
        statusEl.textContent = "Network error";
    }
}
