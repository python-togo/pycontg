/* ═══════════════════════════════════════════════
   PyCon Togo 2026 - Admin Registrations
   ═══════════════════════════════════════════════ */

(function () {
  const API_URL = "/api/v2/registrations";
  let allRegistrations = [];
  let currentFilter = "";

  function t(key, fallback) {
    if (typeof translations !== "undefined" && translations[currentLang || "en"]) {
      const keys = key.split(".");
      let value = translations[currentLang || "en"];
      for (const k of keys) {
        value = value && value[k];
        if (!value) return fallback;
      }
      return value;
    }
    return fallback;
  }

  async function loadRegistrations() {
    const loadingRow = document.getElementById("registrationsLoading");
    const errorRow = document.getElementById("registrationsError");
    const emptyRow = document.getElementById("registrationsEmpty");
    const errorText = document.getElementById("registrationsErrorText");

    if (loadingRow) loadingRow.style.display = "";
    if (errorRow) errorRow.style.display = "none";
    if (emptyRow) emptyRow.style.display = "none";

    try {
      const res = await AdminAuth.authedFetch(API_URL, {
        headers: { "Accept": "application/json" },
      });

      if (res.status === 403) {
        throw new Error(t("errors.adminRequired", "Admin access required"));
      }
      if (res.status === 500) {
        throw new Error(t("errors.retrieving", "Error retrieving registrations"));
      }
      if (!res.ok) {
        throw new Error(t("errors.unexpected", "Unexpected error"));
      }

      allRegistrations = await res.json();
      renderRegistrations(allRegistrations);
    } catch (err) {
      console.error("Failed to load registrations:", err);
      if (loadingRow) loadingRow.style.display = "none";
      if (errorRow) {
        errorRow.style.display = "";
        errorText.textContent = err.message || t("errors.loadFailed", "Failed to load registrations.");
      }
    }
  }

  function formatDate(iso) {
    if (!iso) return "";
    try {
      const d = new Date(iso);
      if (isNaN(d.getTime())) return iso;
      return d.toLocaleString(currentLang === "fr" ? "fr-FR" : "en-US", {
        year: "numeric",
        month: "short",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch {
      return iso;
    }
  }

  function renderRegistrations(list) {
    const tbody = document.getElementById("registrationsBody");
    const loadingRow = document.getElementById("registrationsLoading");
    const errorRow = document.getElementById("registrationsError");
    const emptyRow = document.getElementById("registrationsEmpty");
    const countEl = document.getElementById("registrationsCount");

    if (!tbody) return;

    if (loadingRow) loadingRow.style.display = "none";
    if (errorRow) errorRow.style.display = "none";

    const filtered = currentFilter
      ? list.filter((r) => (r.ticket_type || "") === currentFilter)
      : list;

    if (countEl) {
      const total = filtered.length;
      const label =
        total === 1
          ? t("admin.registrationSingular", "1 registration")
          : t("admin.registrationPlural", "{count} registrations");
      countEl.textContent = label.replace("{count}", String(total));
    }

    tbody.innerHTML = "";

    if (filtered.length === 0) {
      const tr = document.createElement("tr");
      tr.innerHTML =
        `<td colspan="7" class="admin-empty">${t("admin.noRegistrations", "No registrations found.")}</td>`;
      tbody.appendChild(tr);
      return;
    }

    filtered.forEach((r) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td data-label="Participant">
          <div class="admin-cell-primary">${escapeHtml(r.full_name || "")}</div>
          <div class="admin-cell-secondary">${escapeHtml(r.email || "")}</div>
        </td>
        <td data-label="Accès"><span class="badge badge-status">${escapeHtml(r.attendance_status || "")}</span></td>
        <td data-label="Type de billet"><span class="badge ${ticketTypeClass(r.ticket_type)}">${escapeHtml(ticketTypeLabel(r.ticket_type))}</span></td>
        <td data-label="Quantité">${escapeHtml(String(r.ticket_quantity ?? ""))}</td>
        <td data-label="Statut paiement"><span class="badge badge-payment">${escapeHtml(r.payment_status || "")}</span></td>
        <td data-label="Réf. paiement">${escapeHtml(r.payment_reference || "")}</td>
        <td data-label="Créé le">${escapeHtml(formatDate(r.created_at))}</td>
      `;
      tbody.appendChild(tr);
    });
  }

  function escapeHtml(str) {
    if (str == null) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function ticketTypeClass(type) {
    const normalized = (type || "").toLowerCase();
    if (normalized.includes("student")) return "badge-ticket-student";
    if (normalized.includes("standard")) return "badge-ticket-standard";
    if (normalized.includes("premium")) return "badge-ticket-premium";
    if (normalized.includes("dinner")) return "badge-ticket-dinner";
    return "badge-ticket";
  }

  function ticketTypeLabel(type) {
    const normalized = (type || "").toLowerCase();
    if (normalized.includes("student")) return t("admin.ticketStudent", "Student");
    if (normalized.includes("standard")) return t("admin.ticketStandard", "Standard");
    if (normalized.includes("premium")) return t("admin.ticketPremium", "Premium");
    if (normalized.includes("dinner")) return t("admin.ticketDinner", "Dinner");
    return type;
  }

  function populateTicketTypeFilter(list) {
    const select = document.getElementById("ticketTypeFilter");
    if (!select) return;

    const types = Array.from(
      new Set(list.map((r) => r.ticket_type).filter(Boolean))
    ).sort();

    const fallbackTypes = ["dinner", "premium", "standard", "student"];
    const orderedTypes = [
      ...types,
      ...fallbackTypes.filter((t) => !types.includes(t)),
    ];

    orderedTypes.forEach((type) => {
      const opt = document.createElement("option");
      opt.value = type;
      opt.textContent = ticketTypeLabel(type);
      select.appendChild(opt);
    });

    select.addEventListener("change", () => {
      currentFilter = select.value;
      renderRegistrations(allRegistrations);
    });
  }

  function init() {
    if (!AdminAuth.isAuthenticated()) {
      window.location.href = "/admin/login";
      return;
    }

    loadRegistrations().then(() => {
      populateTicketTypeFilter(allRegistrations);
    });

    const logoutBtn = document.getElementById("adminLogoutBtn");
    if (logoutBtn) {
      logoutBtn.addEventListener("click", async () => {
        await AdminAuth.logout();
        window.location.href = "/admin/login";
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
