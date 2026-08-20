(function() {
    "use strict";

    var form = document.getElementById("feedbackForm");
    if (!form) return;

    var apiUrl = "https://api.pycontg.pytogo.org/api/feedback/";
    var submitBtn = document.getElementById("submitBtn");
    var resetBtn = document.getElementById("resetBtn");
    var statusEl = document.getElementById("formStatus");
    var statusMsg = statusEl.querySelector(".feedback-status-msg");
    var feedbackIsOpen = form.dataset.feedbackOpen === "true";

    var i18n = {
        fr: {
            required: "Veuillez remplir les champs requis.",
            days_required: "Veuillez sélectionner au moins un jour.",
            not_open: "Le formulaire n'est pas encore ouvert.",
            sending: "Envoi…",
            success: "Merci ! Votre retour a été envoyé.",
            error: "Une erreur est survenue. Veuillez réessayer plus tard.",
            network: "Erreur réseau. Veuillez vérifier votre connexion."
        },
        en: {
            required: "Please fill in the required fields.",
            days_required: "Please select at least one day.",
            not_open: "The feedback form is not yet open.",
            sending: "Sending…",
            success: "Thank you! Your feedback has been sent.",
            error: "An error occurred. Please try again later.",
            network: "Network error. Please check your connection."
        }
    };

    function getLang() {
        var docLang = (document.documentElement.lang || "fr").toLowerCase();
        return docLang.startsWith("en") ? "en" : (docLang.startsWith("fr") ? "fr" : "fr");
    }

    function showStatus(success, text) {
        statusEl.className = "feedback-status " + (success ? "success" : "error");
        statusMsg.textContent = text;
        statusEl.style.display = "flex";
    }

    function hideStatus() {
        statusEl.style.display = "none";
        statusMsg.textContent = "";
    }

    function setDaysError(show) {
        var daysError = document.querySelector(".feedback-checkbox-error");
        if (!daysError) return;
        daysError.style.display = show ? "block" : "none";
    }

    function daysSelected(fd) {
        return fd.getAll("days").length > 0;
    }

    var dayCheckboxes = document.querySelectorAll('input[type="checkbox"][name="days"]');
    dayCheckboxes.forEach(function(cb) {
        cb.addEventListener("change", function() {
            if (daysSelected(new FormData(form))) setDaysError(false);
        });
    });

    if (resetBtn) {
        resetBtn.addEventListener("click", function() {
            form.reset();
            setDaysError(false);
            hideStatus();
        });
    }

    form.addEventListener("submit", async function(e) {
        e.preventDefault();
        hideStatus();

        var lang = getLang();
        var t = i18n[lang] || i18n.en;

        if (!feedbackIsOpen) {
            showStatus(false, t.not_open);
            return;
        }

        var fd = new FormData(form);

        var payload = {
            sex: fd.get("sex") || null,
            age: fd.get("age") || null,
            profession: (fd.get("profession") || "").trim() || null,
            country: (fd.get("country") || "").trim() || null,
            python_level: fd.get("python_level") || null,
            days: fd.getAll("days"),
            heard: fd.get("heard") || null,
            rating: fd.get("rating") ? Number(fd.get("rating")) : null,
            overall: (fd.get("overall") || "").trim() || null,
            favorite: (fd.get("favorite") || "").trim() || null,
            improvements: (fd.get("improvements") || "").trim() || null,
            comments: (fd.get("comments") || "").trim() || null
        };

        if (!payload.days || payload.days.length === 0) {
            setDaysError(true);
            showStatus(false, t.days_required || t.required);
            return;
        } else {
            setDaysError(false);
        }

        if (!payload.sex && !payload.age && !payload.profession && !payload.heard && !payload.overall && !payload.favorite) {
            showStatus(false, t.required);
            return;
        }

        submitBtn.disabled = true;
        var originalText = submitBtn.textContent;
        submitBtn.textContent = t.sending;

        try {
            var res = await fetch(apiUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (res.ok) {
                showStatus(true, t.success);
                form.reset();
                setDaysError(false);
            } else {
                var msg = t.error;
                try {
                    var data = await res.json();
                    if (data && data.message) msg = data.message + " - " + msg;
                } catch (err) {}
                showStatus(false, msg);
            }
        } catch (err) {
            showStatus(false, t.network);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    });
})();
