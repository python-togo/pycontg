/* ═══════════════════════════════════════════════
   PyCon Togo 2026 - Admin Auth
   ═══════════════════════════════════════════════ */

const AdminAuth = (() => {
  const ACCESS_TOKEN_KEY = "admin_access_token";
  const REFRESH_TOKEN_KEY = "admin_refresh_token";
  const REFRESH_MARGIN_MS = 60 * 1000;

  function getAccessToken() {
    try {
      return localStorage.getItem(ACCESS_TOKEN_KEY) || "";
    } catch {
      return "";
    }
  }

  function getRefreshToken() {
    try {
      return localStorage.getItem(REFRESH_TOKEN_KEY) || "";
    } catch {
      return "";
    }
  }

  function isAuthenticated() {
    return Boolean(getAccessToken());
  }

  function clearTokens() {
    try {
      localStorage.removeItem(ACCESS_TOKEN_KEY);
      localStorage.removeItem(REFRESH_TOKEN_KEY);
    } catch {
      // ignore storage errors
    }
  }

  function setTokens({ access_token, refresh_token }) {
    try {
      localStorage.setItem(ACCESS_TOKEN_KEY, access_token || "");
      localStorage.setItem(REFRESH_TOKEN_KEY, refresh_token || "");
    } catch {
      // ignore storage errors
    }
  }

  async function refreshAccessToken() {
    const refresh_token = getRefreshToken();
    if (!refresh_token) {
      clearTokens();
      return null;
    }

    try {
      const res = await fetch("/api/v2/auth/refresh", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${refresh_token}`,
        },
        body: JSON.stringify({ refresh_token }),
      });

      if (!res.ok) {
        clearTokens();
        return null;
      }

      const data = await res.json();
      if (data?.access_token) {
        setTokens({
          access_token: data.access_token,
          refresh_token: data.refresh_token || refresh_token,
        });
        return data.access_token;
      }

      clearTokens();
      return null;
    } catch {
      clearTokens();
      return null;
    }
  }

  async function getValidAccessToken() {
    const token = getAccessToken();
    if (!token) return null;

    const decoded = parseJwt(token);
    if (!decoded || !decoded.exp) return await refreshAccessToken();

    const expiresInMs = decoded.exp * 1000 - Date.now();
    if (expiresInMs <= REFRESH_MARGIN_MS) {
      return await refreshAccessToken();
    }

    return token;
  }

  function parseJwt(token) {
    if (!token || typeof token !== "string") return null;
    const parts = token.split(".");
    if (parts.length !== 3) return null;
    try {
      const payload = parts[1].replace(/-/g, "+").replace(/_/g, "/");
      const json = decodeURIComponent(
        atob(payload)
          .split("")
          .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
          .join("")
      );
      return JSON.parse(json);
    } catch {
      return null;
    }
  }

  async function login({ email, password }) {
    const res = await fetch("/api/v2/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();
    if (!res.ok) {
      const message = data?.detail || data?.message || "Login failed";
      throw new Error(message);
    }

    setTokens({
      access_token: data.access_token || "",
      refresh_token: data.refresh_token || "",
    });

    return data;
  }

  async function logout() {
    const refresh_token = getRefreshToken();
    const access_token = getAccessToken();
    clearTokens();

    if (refresh_token && access_token) {
      try {
        await fetch("/api/v2/auth/logout", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${access_token}`,
          },
          body: JSON.stringify({ refresh_token }),
        });
      } catch {
        // ignore logout errors
      }
    }
  }

  async function authedFetch(url, options = {}) {
    const accessToken = await getValidAccessToken();
    if (!accessToken) {
      clearTokens();
      window.location.href = "/admin/login";
      return Promise.reject(new Error("Unauthorized"));
    }

    const headers = new Headers(options.headers || {});
    headers.set("Authorization", `Bearer ${accessToken}`);
    if (!headers.has("Accept")) {
      headers.set("Accept", "application/json");
    }

    const res = await fetch(url, { ...options, headers });

    if (res.status === 401) {
      const refreshed = await refreshAccessToken();
      if (!refreshed) {
        clearTokens();
        window.location.href = "/admin/login";
        return Promise.reject(new Error("Unauthorized"));
      }

      headers.set("Authorization", `Bearer ${refreshed}`);
      return fetch(url, { ...options, headers });
    }

    return res;
  }

  return {
    getAccessToken,
    getRefreshToken,
    isAuthenticated,
    clearTokens,
    setTokens,
    login,
    logout,
    authedFetch,
  };
})();
