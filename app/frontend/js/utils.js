// Shared utilities for all PhishGuard pages
// API_BASE is the single source of truth for all API calls

const API_BASE = "http://127.0.0.1:8000";

// ----- Auth token helpers -----

function pgGetToken() {
    return localStorage.getItem("pg_token");
}

function pgGetEmail() {
    return localStorage.getItem("pg_email");
}

function pgSetAuth(token, email) {
    localStorage.setItem("pg_token", token);
    localStorage.setItem("pg_email", email);
}

function pgClearAuth() {
    localStorage.removeItem("pg_token");
    localStorage.removeItem("pg_email");
}

function pgAuthHeaders() {
    const token = pgGetToken();
    if (!token) return {};
    return { "Authorization": "Bearer " + token };
}

// ----- UI helpers -----

function pgUpdateAuthBadge() {
    const span = document.getElementById("auth-email");
    const logoutBtn = document.getElementById("btn-logout");

    if (!span || !logoutBtn) return;

    const email = pgGetEmail();
    const token = pgGetToken();

    if (token && email) {
        span.textContent = email;
        logoutBtn.style.display = "inline-block";
    } else {
        span.textContent = "Not logged in";
        logoutBtn.style.display = "none";
    }
}

function pgRequireAuth() {
    const token = pgGetToken();
    if (!token) {
        window.location.href = "/auth.html";
    }
}

function pgInitLogout() {
    const logoutBtn = document.getElementById("btn-logout");
    if (logoutBtn) {
        logoutBtn.onclick = () => {
            pgClearAuth();
            window.location.href = "/auth.html";
        };
    }
}

// Hide/show navbar items based on login state
function pgUpdateNavbar() {
    const token = pgGetToken();

    const linkAuth = document.getElementById("nav-auth");
    const linkEmployees = document.getElementById("nav-employees");
    const linkCampaigns = document.getElementById("nav-campaigns");
    const linkDashboard = document.getElementById("nav-dashboard");

    if (!linkAuth) return; // navbar not loaded on this page

    if (token) {
        // Logged in → hide Auth, show other pages
        linkAuth.style.display = "none";
        if (linkEmployees) linkEmployees.style.display = "inline-block";
        if (linkCampaigns) linkCampaigns.style.display = "inline-block";
        if (linkDashboard) linkDashboard.style.display = "inline-block";
    } else {
        // Logged out → show only Auth
        linkAuth.style.display = "inline-block";
        if (linkEmployees) linkEmployees.style.display = "none";
        if (linkCampaigns) linkCampaigns.style.display = "none";
        if (linkDashboard) linkDashboard.style.display = "none";
    }
}

// Auto-run on every page
document.addEventListener("DOMContentLoaded", () => {
    pgUpdateNavbar();
    pgUpdateAuthBadge();
    pgInitLogout();
});
