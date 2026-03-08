document.addEventListener("DOMContentLoaded", function () {
    console.log("loading currency here!!!!!");

    function updateUSD(xofRate) {
        const usdToXof = xofRate; // 1 USD = XOF

        // --- Handle Dropdown Options (for contact.html) ---
        const sponsorshipLevelSelect = document.getElementById("sponsorship-level");
        if (sponsorshipLevelSelect) { // Check if the select element exists on this page
            Array.from(sponsorshipLevelSelect.options).forEach(option => {
                const cfa = parseFloat(option.dataset.cfa);
                if (!isNaN(cfa)) {
                    const usd = cfa / usdToXof;
                    // Retain original text (e.g., "Gold Sponsor") and append the currency info
                    const originalText = option.textContent.split('(')[0].trim();
                    option.textContent = `${originalText} (${cfa} CFA / ~$${usd.toFixed(2)} USD)`;
                }
            });
        }

        const usdElements = document.querySelectorAll(".usd-value"); // Selects all elements with class 'usd-value'
        usdElements.forEach(el => {
            const cfa = parseFloat(el.dataset.cfa);
            if (!isNaN(cfa)) {
                const usd = cfa / usdToXof;
                el.textContent = `~$${usd.toFixed(2)} USD`;
            }
        });
    }

    function loadFallback() {
        const cached = localStorage.getItem("usd_to_xof_rate");
        if (cached) {
            const rate = parseFloat(cached);
            if (!isNaN(rate)) updateUSD(rate);
        } else {
            // Fallback for dropdown options
            const sponsorshipLevelSelect = document.getElementById("sponsorship-level");
            if (sponsorshipLevelSelect) {
                Array.from(sponsorshipLevelSelect.options).forEach(option => {
                    if (option.dataset.cfa) {
                        const originalText = option.textContent.split('(')[0].trim();
                        option.textContent = `${originalText} (~Unavailable USD)`;
                    }
                });
            }

            // Fallback for general text elements
            const usdElements = document.querySelectorAll(".usd-value");
            usdElements.forEach(el => {
                el.textContent = "~Unavailable USD";
            });
        }
    }

    fetch("https://raw.githubusercontent.com/ismartcoding/currency-api/main/latest/data.json")
        .then(res => {
            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }
            return res.json();
        })
        .then(data => {
            const xofValue = data.quotes.XOF;
            if (typeof xofValue === 'number' && !isNaN(xofValue)) {
                localStorage.setItem("usd_to_xof_rate", xofValue);
                updateUSD(xofValue);
            } else {
                throw new Error("Invalid XOF rate received from API.");
            }
        })
        .catch(err => {
            console.error("Could not fetch rate from ismartcoding API. Using fallback.", err);
            loadFallback();
        });
});
