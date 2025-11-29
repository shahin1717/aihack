// ---------------- CONFIG ----------------
const API_BASE = "http://localhost:8000";

// ---------------- TOKEN MANAGEMENT ----------------
let accessToken = localStorage.getItem("pg_token") || null;
let authEmail = localStorage.getItem("pg_email") || null;

function authHeaders() {
  if (!accessToken) return {};
  return {
    "Authorization": `Bearer ${accessToken}`
  };
}

// ---------------- UI UPDATE ----------------
function updateAuthUI() {
  const emailSpan = document.getElementById("auth-email-pill");
  const logoutBtn = document.getElementById("logout-btn");

  if (!emailSpan) return; // some pages may not have this

  if (accessToken) {
    emailSpan.textContent = authEmail;
    logoutBtn.style.display = "inline-block";
  } else {
    emailSpan.textContent = "Not logged in";
    logoutBtn.style.display = "none";
  }
}

// ---------------- LOGOUT ----------------
function logout() {
  accessToken = null;
  authEmail = null;
  localStorage.removeItem("pg_token");
  localStorage.removeItem("pg_email");
  window.location.href = "auth.html";
}

// ---------------- PROTECTED PAGE CHECK ----------------
function requireAuth() {
  if (!accessToken) {
    window.location.href = "auth.html";
  }
}

// Run on every page
updateAuthUI();
