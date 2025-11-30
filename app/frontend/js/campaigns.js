// campaigns.js

// Require login and set navbar badges
pgRequireAuth();
pgInitLogout();
pgUpdateAuthBadge();

// -------- DOM refs --------
const campTitleInput   = document.getElementById("camp-title");
const scenarioSelect   = document.getElementById("camp-scenario");
const employeeIdsInput = document.getElementById("camp-ids");

const senderNameInput  = document.getElementById("ai-sender-name");
const senderEmailInput = document.getElementById("ai-sender-email");
const subjectInput     = document.getElementById("ai-subject");
const bodyTextarea     = document.getElementById("ai-body");

const aiStatusSpan        = document.getElementById("gen-status");
const campStatusSpan      = document.getElementById("camp-status");
const campListStatusSpan  = document.getElementById("camp-list-status");

const btnGenerateAI      = document.getElementById("btn-generate-ai");
const btnSendCampaign    = document.getElementById("btn-send-campaign");
const btnReloadCampaigns = document.getElementById("btn-reload-campaigns");
const btnUseAll          = document.getElementById("btn-use-all");

const tableBody          = document.querySelector("#camp-table tbody");
const deptSelect = document.getElementById("camp-dept");
const btnUseDept = document.getElementById("btn-use-dept");
// -------- helpers --------
function parseEmployeeIds(raw) {
    return raw
        .split(",")
        .map(s => parseInt(s.trim(), 10))
        .filter(n => !Number.isNaN(n));
}

function setButtonState(button, disabled) {
    if (button) button.disabled = disabled;
}

async function loadDepartments() {
    if (!deptSelect) return;

    try {
        const res = await fetch(`${API_BASE}/departments/`, {
            headers: pgAuthHeaders()
        });
        const data = await res.json();

        deptSelect.innerHTML = '<option value="">-- Select department --</option>';

        data.forEach(dep => {
            deptSelect.innerHTML += `<option value="${dep.id}">${dep.name}</option>`;
        });
    } catch (e) {
        console.error("Failed to load departments", e);
    }
}

loadDepartments();
loadCampaigns();

async function useDepartmentEmployees() {
    if (!deptSelect || !deptSelect.value) {
        campStatusSpan.textContent = "Select a department first.";
        return;
    }

    const depId = deptSelect.value;
    campStatusSpan.textContent = "Loading department employees...";

    try {
        const res = await fetch(`${API_BASE}/employees/?department_id=${depId}`, {
            headers: pgAuthHeaders()
        });

        const data = await res.json();
        const ids = data.map(emp => emp.id);

        employeeIdsInput.value = ids.join(", ");
        campStatusSpan.textContent = `Selected ${ids.length} employees from department "${deptSelect.options[deptSelect.selectedIndex].text}".`;

    } catch (e) {
        campStatusSpan.textContent = "Failed to load employees for this department.";
    }
}


if (btnUseDept) {
    btnUseDept.addEventListener("click", useDepartmentEmployees);
}

// Prefill sender defaults if empty
function ensureSenderDefaults() {
    if (senderNameInput && !senderNameInput.value.trim()) {
        senderNameInput.value = "IT Security Team";
    }
    if (senderEmailInput && !senderEmailInput.value.trim()) {
        senderEmailInput.value = "secure.alert.notice@gmail.com";
    }
}

// -------- AI generation (uses /ai/generate) --------
async function generateEmailWithAI() {
    if (!scenarioSelect) return;

    const scenario = scenarioSelect.value;
    const title = campTitleInput ? campTitleInput.value.trim() : "";

    ensureSenderDefaults();

    if (aiStatusSpan) aiStatusSpan.textContent = "Generating with AI...";
    setButtonState(btnGenerateAI, true);

    try {
        const res = await fetch(`${API_BASE}/ai/generate`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...pgAuthHeaders()
            },
            body: JSON.stringify({
                topic: `${scenario} phishing email for employees. Internal campaign: ${title || "Unnamed"}.`,
                tone: "professional and slightly urgent, corporate security style",
                difficulty: "medium"
            })
        });

        const data = await res.json();

        if (!res.ok) {
            if (aiStatusSpan) aiStatusSpan.textContent = data.detail || "AI generation failed.";
            return;
        }

        if (subjectInput)  subjectInput.value  = data.subject || "";
        if (bodyTextarea)  bodyTextarea.value  = data.body_html || "";
        if (aiStatusSpan)  aiStatusSpan.textContent = "AI email generated. You can edit it before sending.";

    } catch (err) {
        if (aiStatusSpan) aiStatusSpan.textContent = "Network error during AI generation.";
    } finally {
        setButtonState(btnGenerateAI, false);
    }
}

// Option B – auto generate when scenario changes
if (scenarioSelect) {
    scenarioSelect.addEventListener("change", generateEmailWithAI);
}

// -------- Use all employees button --------
async function useAllEmployees() {
    if (!employeeIdsInput) return;
    if (campStatusSpan) campStatusSpan.textContent = "Loading employees...";

    try {
        const res = await fetch(`${API_BASE}/employees/`, {
            headers: pgAuthHeaders()
        });

        const data = await res.json();
        if (!res.ok) {
            if (campStatusSpan) campStatusSpan.textContent = data.detail || "Failed to load employees.";
            return;
        }

        const ids = data.map(emp => emp.id);
        employeeIdsInput.value = ids.join(", ");
        if (campStatusSpan) campStatusSpan.textContent = `Selected all employees (${ids.length}).`;
    } catch (err) {
        if (campStatusSpan) campStatusSpan.textContent = "Network error while loading employees.";
    }
}

// -------- Send campaign --------
async function sendCampaign() {
    if (!campTitleInput || !scenarioSelect || !employeeIdsInput ||
        !senderNameInput || !senderEmailInput || !subjectInput || !bodyTextarea) {
        return;
    }

    const title        = campTitleInput.value.trim() || "AI phishing simulation";
    const scenario     = scenarioSelect.value;
    const employeeIds  = parseEmployeeIds(employeeIdsInput.value);

    const senderName   = senderNameInput.value.trim();
    const senderEmail  = senderEmailInput.value.trim();
    const subject      = subjectInput.value.trim();
    const bodyHtml     = bodyTextarea.value.trim();

    if (!employeeIds.length) {
        if (campStatusSpan) campStatusSpan.textContent = "Add at least one employee ID (or use all employees).";
        return;
    }
    if (!subject || !bodyHtml) {
        if (campStatusSpan) campStatusSpan.textContent = "Generate the email with AI first (or type it manually).";
        return;
    }

    if (campStatusSpan) campStatusSpan.textContent = "Creating campaign and sending emails...";
    setButtonState(btnSendCampaign, true);

    try {
        const res = await fetch(`${API_BASE}/campaigns/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...pgAuthHeaders()
            },
            body: JSON.stringify({
                title: title,
                sender_name: senderName,
                sender_email: senderEmail,
                subject: subject,
                body_html: bodyHtml,
                employee_ids: employeeIds
            })
        });

        const data = await res.json();

        if (!res.ok) {
            if (campStatusSpan) campStatusSpan.textContent = data.detail || "Sending failed.";
            return;
        }

        if (campStatusSpan) campStatusSpan.textContent = `Campaign ${data.id} created and emails sent.`;
        loadCampaigns();
    } catch (err) {
        if (campStatusSpan) campStatusSpan.textContent = "Network error while sending campaign.";
    } finally {
        setButtonState(btnSendCampaign, false);
    }
}

// -------- Load campaigns list --------
async function loadCampaigns() {
    if (!tableBody) return;

    tableBody.innerHTML = "";
    if (campListStatusSpan) campListStatusSpan.textContent = "Loading campaigns...";

    try {
        const res = await fetch(`${API_BASE}/campaigns/`, {
            headers: pgAuthHeaders()
        });

        const data = await res.json();

        if (!res.ok) {
            if (campListStatusSpan) campListStatusSpan.textContent = data.detail || "Failed to load campaigns.";
            return;
        }

        if (!data.length) {
            if (campListStatusSpan) campListStatusSpan.textContent = "No campaigns yet.";
            return;
        }

        if (campListStatusSpan) campListStatusSpan.textContent = "";

        data.forEach(c => {
            const tr = document.createElement("tr");
            const scenarioLabel = c.scenario || "Custom";

            tr.innerHTML = `
                <td>${c.id}</td>
                <td>${c.title}</td>
                <td>${scenarioLabel}</td>
                <td>${c.sender_name} &lt;${c.sender_email}&gt;</td>
                <td>
                  <button class="btn-small" type="button"
                          onclick="pgOpenCampaignDashboard(${c.id})">
                    View stats
                  </button>
                </td>
            `;
            tableBody.appendChild(tr);
        });
    } catch (err) {
        if (campListStatusSpan) campListStatusSpan.textContent = "Network error while loading campaigns.";
    }
}

// Allow inline handler from table
window.pgOpenCampaignDashboard = function (id) {
    window.location.href = `/dashboard.html?campaign_id=${id}`;
};

// -------- wire buttons --------
if (btnGenerateAI) {
    btnGenerateAI.addEventListener("click", generateEmailWithAI);
}
if (btnSendCampaign) {
    btnSendCampaign.addEventListener("click", sendCampaign);
}
if (btnReloadCampaigns) {
    btnReloadCampaigns.addEventListener("click", loadCampaigns);
}
if (btnUseAll) {
    btnUseAll.addEventListener("click", useAllEmployees);
}

// initial load
if (tableBody) {
    loadCampaigns();
}
