// -------- CONFIG ----------
const API_BASE = "http://127.0.0.1:8000";

function saveAuth(token, email) {
    localStorage.setItem("pg_token", token);
    localStorage.setItem("pg_email", email);
}

function clearAuth() {
    localStorage.removeItem("pg_token");
    localStorage.removeItem("pg_email");
}

function getToken() {
    return localStorage.getItem("pg_token");
}

function headersAuth() {
    const token = getToken();
    return token ? { "Authorization": "Bearer " + token } : {};
}

// ---------- REGISTER ----------
document.getElementById("btn-register").onclick = async () => {
    const email = document.getElementById("reg-email").value;
    const password = document.getElementById("reg-password").value;
    const status = document.getElementById("reg-status");
    status.textContent = "Registering...";

    try {
        const res = await fetch(`${API_BASE}/auth/register`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (!res.ok) {
            status.textContent = data.detail || "Error";
            return;
        }

        saveAuth(data.access_token, email);
        status.textContent = "Registered. Logged in!";
        window.location.href = "/employees.html";

    } catch (e) {
        status.textContent = "Network error";
    }
};

// ---------- LOGIN ----------
document.getElementById("btn-login").onclick = async () => {
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;
    const status = document.getElementById("login-status");

    status.textContent = "Logging in...";

    try {
        const res = await fetch(`${API_BASE}/auth/login`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (!res.ok) {
            status.textContent = data.detail || "Invalid credentials";
            return;
        }

        saveAuth(data.access_token, email);
        status.textContent = "Success!";
        window.location.href = "/employees.html";

    } catch {
        status.textContent = "Network error";
    }
};
