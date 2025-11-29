// ========== GLOBAL CONFIG ==========
// NOTE: This file is deprecated. Use utils.js instead.
// API_BASE is imported from utils.js (loaded before this script)

// ========== TOKEN ==========
let accessToken = localStorage.getItem("pg_token") || null;
let authEmail = localStorage.getItem("pg_email") || null;

function authHeaders() {
  if (!accessToken) return {};
  return {
    "Authorization": `Bearer ${accessToken}`
  };
}

// ========== AUTH UI ==========
function updateAuthUI() {
  const emailSpan = document.getElementById("auth-email-pill");
  const logoutBtn = document.getElementById("logout-btn");

  if (!emailSpan) return; // Page does not have auth UI

  if (accessToken) {
    emailSpan.textContent = authEmail || "Admin";
    if (logoutBtn) logoutBtn.style.display = "inline-block";
  } else {
    emailSpan.textContent = "Not logged in";
    if (logoutBtn) logoutBtn.style.display = "none";
  }
}

// ========== LOGOUT ==========
function logout() {
  accessToken = null;
  authEmail = null;

  localStorage.removeItem("pg_token");
  localStorage.removeItem("pg_email");

  window.location.href = "auth.html";
}

// ========== PROTECTED PAGE GUARD ==========
function requireAuth() {
  if (!accessToken) {
    window.location.href = "auth.html";
  }
}

// Run on all pages automatically
updateAuthUI();
