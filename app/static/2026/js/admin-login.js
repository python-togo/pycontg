/* ═══════════════════════════════════════════════
   PyCon Togo 2026 - Admin Login Page
   ═══════════════════════════════════════════════ */

(function () {
  const form = document.getElementById("adminLoginForm");
  const emailInput = document.getElementById("adminEmail");
  const passwordInput = document.getElementById("adminPassword");
  const errorBox = document.getElementById("adminLoginError");

  if (!form) return;

  function showError(message) {
    if (!errorBox) return;
    errorBox.textContent = message;
    errorBox.style.display = "block";
  }

  function clearError() {
    if (!errorBox) return;
    errorBox.textContent = "";
    errorBox.style.display = "none";
  }

  async function onSubmit(e) {
    e.preventDefault();
    clearError();

    const email = (emailInput?.value || "").trim();
    const password = passwordInput?.value || "";

    if (!email || !password) {
      showError("Email and password are required.");
      return;
    }

    const submitBtn = form.querySelector(".admin-login-submit");
    if (submitBtn) submitBtn.disabled = true;

    try {
      await AdminAuth.login({ email, password });
      window.location.href = "/admin/registrations";
    } catch (err) {
      showError(err.message || "Login failed.");
      if (submitBtn) submitBtn.disabled = false;
    }
  }

  form.addEventListener("submit", onSubmit);
})();
