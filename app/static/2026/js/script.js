/* ═══════════════════════════════════════════════
   PYCON TOGO 2026 — SCRIPT.JS
═══════════════════════════════════════════════ */

/* ── TRANSLATIONS ── */
let translations = {};

async function loadTranslations() {
  try {
    const response = await fetch("/static/2026/i18n/translations.json");
    translations = await response.json();
  } catch (error) {
    console.error("Failed to load translations:", error);
  }
}

function t(key, defaultValue = key) {
  const lang = currentLang || "en";
  const keys = key.split(".");
  let value = translations[lang] || {};

  for (const k of keys) {
    value = value[k];
    if (!value) return defaultValue;
  }

  return value;
}

/* ── TEAM DATA ── */
const teamData = [
  {
    name: "Waschiou Bouraima",
    role: "Président de la Conférence",
    bio: "Fondateur de Python Togo. Passionné par le développement de l'écosystème tech local et l'open source en Afrique.",
    flag: "🇹🇬",
    linkedin: "https://www.linkedin.com/in/waschioubouraima/",
    portfolio: "",
    colors: ["#0d3320", "#c52d2d"],
  },
  {
    name: "Geoffrey Logovi",
    role: "Directeur du Programme",
    bio: "Responsable de la sélection des speakers et de la conception du programme pour un maximum d'impact communautaire.",
    flag: "🇹🇬",
    linkedin: "https://www.linkedin.com/in/geoffrey-logovi/",
    portfolio: "",
    colors: ["#0d3320", "#c52d2d"],
  },
  {
    name: "Mawuli Dossou",
    role: "Responsable Partenariats",
    bio: "Construit les partenariats avec les entreprises tech pour financer et développer PyCon Togo année après année.",
    flag: "🇹🇬",
    linkedin: "https://www.linkedin.com/in/mawuli-dossou/",
    portfolio: "",
    colors: ["#0d3320", "#c8a400"],
  },
  {
    name: "Afi Kpodo",
    role: "Community Manager",
    bio: "Gère la communauté Python Togo, les événements locaux et la présence en ligne de l'organisation.",
    flag: "🇹🇬",
    linkedin: "https://www.linkedin.com/in/afi-kpodo/",
    portfolio: "",
    colors: ["#2d8a50", "#0d3320"],
  },
  {
    name: "Yinka Adewale",
    role: "Responsable Technique",
    bio: "Pilote l'infrastructure technique et le développement de la plateforme de la conférence.",
    flag: "🇳🇬",
    linkedin: "https://www.linkedin.com/in/yinka-adewale/",
    portfolio: "https://yinkatech.dev",
    colors: ["#1a5c35", "#0d3320"],
  },
  {
    name: "Nneji Gift",
    role: "Directrice Design de Frontend",
    bio: "Crée l'identité visuelle et le branding qui rendent PyCon Togo mémorable et reconnaissable.",
    flag: "🇳🇬",
    linkedin: "https://www.linkedin.com/in/nneji-gift/",
    portfolio: "https://nnejigift.design",
    colors: ["#1a5c35", "#0d3320"],
  },
];

/* ── SITE CREATORS ── */
const siteCreators = [
  {
    name: "Gift Chisom",
    linkedin: "https://www.linkedin.com/in/gift-nneji-128172348/",
    portfolio: "",
  },
  {
    name: "Tronka Diabate",
    linkedin: "https://www.linkedin.com/in/tronka-diabat%C3%A9/",
    portfolio: "",
  },
  {
    name: "Wachiou Bouraima (Wasiu Ibrahim)",
    linkedin: "",
    portfolio: "https://wasscodeur.github.io",
  },
];

/* ── HELPERS ── */
function initials(name) {
  return name.split(" ").map(n => n[0]).join("").slice(0, 2).toUpperCase();
}

/* ── LANGUAGE SWITCH ── */
let currentLang = "en";

function applyLanguage(lang) {
  currentLang = lang;

  document.documentElement.lang = lang;

  const titleByLang = {
    en: "PyCon Togo 2026 — The Python Conference of Togo",
    fr: "PyCon Togo 2026 — La Conférence Python du Togo",
  };
  const descriptionByLang = {
    en: "PyCon Togo 2026 — The national conference for the Python community in Togo. Lome, Togo.",
    fr: "PyCon Togo 2026 — La conférence nationale de la communauté Python du Togo. Lomé, Togo.",
  };

  document.title = titleByLang[lang] || titleByLang.en;
  const desc = document.querySelector('meta[name="description"]');
  if (desc) desc.setAttribute("content", descriptionByLang[lang] || descriptionByLang.en);

  // Update data-i18n-en/fr attributes
  document.querySelectorAll("[data-i18n-en]").forEach(el => {
    const next = lang === "fr" ? el.getAttribute("data-i18n-fr") : el.getAttribute("data-i18n-en");
    if (next !== null) el.textContent = next;
  });

  document.querySelectorAll("[data-i18n-html-en]").forEach(el => {
    const next = lang === "fr" ? el.getAttribute("data-i18n-html-fr") : el.getAttribute("data-i18n-html-en");
    if (next !== null) el.innerHTML = next;
  });

  // Update translatable placeholders.
  document.querySelectorAll("[data-i18n-placeholder-en]").forEach(el => {
    const next = lang === "fr"
      ? el.getAttribute("data-i18n-placeholder-fr")
      : el.getAttribute("data-i18n-placeholder-en");
    if (next !== null) el.setAttribute("placeholder", next);
  });

  // Update language buttons
  const enBtn = document.getElementById("lang-en");
  const frBtn = document.getElementById("lang-fr");
  const enMobileBtn = document.getElementById("lang-en-mobile");
  const frMobileBtn = document.getElementById("lang-fr-mobile");

  [enBtn, enMobileBtn].forEach(btn => btn && btn.classList.toggle("active", lang === "en"));
  [frBtn, frMobileBtn].forEach(btn => btn && btn.classList.toggle("active", lang === "fr"));

  // Update form labels and placeholders dynamically if contact page is loaded
  updateContactFormLabels(lang);

  // Show the right sponsorship prospectus links based on current language.
  updateProspectusLinks(lang);

  // Re-render footer creators so names/links stay correct after language switch.
  renderSiteCreators();

  // Notify page-specific scripts that language has changed.
  document.dispatchEvent(new CustomEvent("pycontg:language-changed", {
    detail: { lang }
  }));
}

function setLanguage(lang) {
  localStorage.setItem("pycontg_lang", lang);
  applyLanguage(lang);
}

/* ── UPDATE CONTACT FORM LABELS ── */
function updateContactFormLabels(lang) {
  const form = document.getElementById("contact-form");
  if (!form) return;

  const labels = {
    en: {
      form_name: "Full name",
      form_name_placeholder: "Kofi Mensah",
      form_email: "Email address",
      form_email_placeholder: "kofi@example.com",
      form_org: "Organization (optional)",
      form_org_placeholder: "Your company or university",
      form_subject: "Subject",
      form_message: "Message",
      form_message_placeholder: "Tell us how we can help you...",
      form_submit: "Send →",
      form_success: "Message sent!",
      form_success_desc: "We'll get back to you within 48 hours."
    },
    fr: {
      form_name: "Nom complet",
      form_name_placeholder: "Kofi Mensah",
      form_email: "Adresse email",
      form_email_placeholder: "kofi@exemple.com",
      form_org: "Organisation (optionnel)",
      form_org_placeholder: "Votre entreprise ou université",
      form_subject: "Sujet",
      form_message: "Message",
      form_message_placeholder: "Dites-nous comment nous pouvons vous aider...",
      form_submit: "Envoyer →",
      form_success: "Message envoyé !",
      form_success_desc: "Nous vous répondrons dans les 48h."
    }
  };

  // Use JSON translations if available
  if (translations[lang]) {
    const formLabels = {
      en: translations[lang].contact_page || labels.en,
      fr: translations[lang].contact_page || labels.fr
    };
    labels.en = formLabels.en;
    labels.fr = formLabels.fr;
  }

  const l = labels[lang] || labels.en;

  // Update visible labels and placeholders
  form.querySelectorAll("label").forEach(label => {
    const field = label.closest(".field");
    if (!field) return;
    const input = field.querySelector("input, textarea, select");
    if (!input) return;

    if (label.textContent.includes("Full name") || label.textContent.includes("Nom complet")) {
      label.textContent = l.form_name || "Full name";
    } else if (label.textContent.includes("Email") || label.textContent.includes("email")) {
      label.textContent = l.form_email || "Email address";
    } else if (label.textContent.includes("Organization") || label.textContent.includes("Organisation")) {
      label.textContent = l.form_org || "Organization (optional)";
    } else if (label.textContent.includes("Subject") || label.textContent.includes("Sujet")) {
      label.textContent = l.form_subject || "Subject";
    } else if (label.textContent.includes("Message")) {
      label.textContent = l.form_message || "Message";
    }
  });

  // Update placeholders
  const nameInput = form.querySelector("input[placeholder*='Kofi'], input[placeholder*='kofi']");
  if (nameInput) nameInput.placeholder = l.form_name_placeholder || "Kofi Mensah";

  const emailInput = form.querySelector("input[type='email']");
  if (emailInput) emailInput.placeholder = l.form_email_placeholder || "kofi@example.com";

  const orgInput = form.querySelector("input[placeholder*='company'], input[placeholder*='entreprise']");
  if (orgInput) orgInput.placeholder = l.form_org_placeholder || "Your company or university";

  const messageInput = form.querySelector("textarea");
  if (messageInput) messageInput.placeholder = l.form_message_placeholder || "Tell us how we can help you...";

  const submitBtn = form.querySelector("button[type='submit']");
  if (submitBtn && submitBtn.id === "submit-btn") {
    submitBtn.textContent = l.form_submit || "Send →";
  }

  // Update success message
  const successMsg = document.getElementById("form-success");
  if (successMsg) {
    const h3 = successMsg.querySelector("h3");
    const p = successMsg.querySelector("p");
    if (h3) h3.textContent = l.form_success || "Message sent!";
    if (p) p.textContent = l.form_success_desc || "We'll get back to you within 48 hours.";
  }
}

/* ── PROSPECTUS LINKS BY LANGUAGE ── */
function updateProspectusLinks(lang) {
  const links = document.querySelectorAll("[data-prospectus-lang]");
  if (!links.length) return;

  const targetLang = lang === "fr" ? "fr" : "en";
  links.forEach(link => {
    link.hidden = link.getAttribute("data-prospectus-lang") !== targetLang;
  });
}

/* ── RENDER SITE CREATORS IN FOOTER ── */
function renderSiteCreators() {
  const footerBottom = document.getElementById("site-creators")
    || document.querySelector(".footer-bottom-inner span:last-child");
  if (!footerBottom) return;

  const lang = currentLang || "en";
  const madeWithText = translations[lang]?.footer?.made_with || "Made with ❤️ by";
  const andText = lang === "fr" ? " et " : " and ";

  let html = `${madeWithText} `;
  siteCreators.forEach((creator, i) => {
    const linkedin = (creator.linkedin || "").trim();
    const portfolio = (creator.portfolio || "").trim();
    const profileUrl = linkedin || portfolio;

    if (profileUrl) {
      html += `<a href="${profileUrl}" target="_blank" rel="noopener noreferrer">${creator.name}</a>`;
    } else {
      html += `<span>${creator.name}</span>`;
    }

    if (i < siteCreators.length - 1) {
      html += i === siteCreators.length - 2 ? andText : ", ";
    }
  });

  footerBottom.innerHTML = html;
}

/* ── RENDER TEAM ── */
function renderTeam() {
  const grid = document.getElementById("team-grid");
  if (!grid) return;

  grid.innerHTML = teamData.map((m, i) => `
    <div class="team-card reveal" style="transition-delay:${i * 80}ms">
      <div style="position:relative;width:fit-content">
        <div class="team-avatar" style="background:linear-gradient(135deg,${m.colors[0]},${m.colors[1]})">
          ${initials(m.name)}
          <span class="team-flag">${m.flag}</span>
        </div>
      </div>
      <div>
        <div class="team-name">${m.name}</div>
        <div class="team-role">${m.role}</div>
        <p class="team-bio">${m.bio}</p>
      </div>
      <a href="${m.linkedin}" target="_blank" rel="noreferrer" class="team-li">
        <svg width="13" height="13" fill="currentColor" viewBox="0 0 24 24">
          <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
        </svg>
        LinkedIn
      </a>
    </div>
  `).join("");

  // Re-observe newly created cards
  observeReveals();
}

/* ── NAVBAR SCROLL ── */
function initNavbarScroll() {
  const navbar = document.getElementById("navbar");
  const onScroll = () => navbar.classList.toggle("scrolled", window.scrollY > 24);
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
}

/* ── MOBILE MENU ── */
function toggleMenu() {
  const drawer = document.getElementById("drawer");
  const overlay = document.getElementById("drawer-overlay");
  const burger = document.getElementById("hamburger");
  drawer.classList.toggle("open");
  overlay.classList.toggle("open");
  burger.classList.toggle("open");
  document.body.style.overflow = drawer.classList.contains("open") ? "hidden" : "";
}

function closeMenu() {
  document.getElementById("drawer").classList.remove("open");
  document.getElementById("drawer-overlay").classList.remove("open");
  document.getElementById("hamburger").classList.remove("open");
  document.body.style.overflow = "";
}

/* ── SCROLL REVEAL ── */
let revealObserver = null;

function observeReveals() {
  if (revealObserver) revealObserver.disconnect();

  revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  document.querySelectorAll(".page.active .reveal").forEach(el => {
    revealObserver.observe(el);
  });
}

/* ── CONTACT FORM ── */
function handleSubmit(e) {
  e.preventDefault();
  const btn = document.getElementById("submit-btn");
  const form = document.getElementById("contact-form");
  const succ = document.getElementById("form-success");

  btn.textContent = currentLang === "fr" ? "Envoi en cours..." : "Sending...";
  console.log("Submitting contact form with data:", {
    name: nameInput.value,
    email: emailInput.value,
    subject: subjectInput.value,
    message: messageInput.value,
  });
  btn.disabled = true;

  setTimeout(() => {
    form.style.display = "none";
    succ.classList.add("show");
  }, 1400);
}

/* ── NEWSLETTER FORM ── */
function handleNewsletter(e) {
  e.preventDefault();
  const btn = e.target.querySelector("button");
  btn.textContent = currentLang === "fr" ? "✓ Inscrit !" : "✓ Subscribed!";
  btn.disabled = true;
  e.target.querySelector("input").value = "";
  setTimeout(() => {
    btn.textContent = currentLang === "fr" ? "M'avertir" : "Notify me";
    btn.disabled = false;
  }, 4000);
}

/* ── TICKETS PAGE ── */
const defaultTicketCatalog = [
  {
    id: "early-standard",
    name: { en: "Early Bird Standard", fr: "Standard Early Bird" },
    description: {
      en: "Full conference access for individual attendees.",
      fr: "Acces complet a la conference pour les participants individuels.",
    },
    earlyBirdPrice: 3000,
    regularPrice: 3500,
    earlyBirdEndDate: "2026-06-30T23:59:59+00:00",
    quantityAvailable: 220,
    maxPerUser: 4,
  },
  {
    id: "early-student",
    name: { en: "Early Bird Student", fr: "Etudiant Early Bird" },
    description: {
      en: "Discounted ticket for students with a valid ID.",
      fr: "Tarif reduit pour les etudiants avec carte valide.",
    },
    earlyBirdPrice: 2000,
    regularPrice: 2500,
    earlyBirdEndDate: "2026-06-30T23:59:59+00:00",
    quantityAvailable: 160,
    maxPerUser: 2,
  },
  {
    id: "regular-standard",
    name: { en: "Regular Standard", fr: "Standard" },
    description: {
      en: "Standard access once Early Bird ends.",
      fr: "Acces standard apres la fin de l'Early Bird.",
    },
    earlyBirdPrice: null,
    regularPrice: 3500,
    earlyBirdEndDate: null,
    quantityAvailable: 300,
    maxPerUser: 4,
  },
  {
    id: "vip",
    name: { en: "VIP Ticket", fr: "Ticket VIP" },
    description: {
      en: "Priority seating, VIP lounge access, and premium kit.",
      fr: "Places prioritaires, lounge VIP et kit premium.",
    },
    earlyBirdPrice: null,
    regularPrice: 10000,
    earlyBirdEndDate: null,
    quantityAvailable: 40,
    maxPerUser: 2,
  },
];

function ticketOrderPriority(ticket) {
  const label = `${ticket?.id || ""} ${ticket?.name?.en || ""} ${ticket?.name?.fr || ""} ${ticket?.description?.en || ""} ${ticket?.description?.fr || ""}`.toLowerCase();

  if (label.includes("student") || label.includes("etudiant") || label.includes("etudiante")) return 0;
  if (label.includes("professional") || label.includes("professionnel") || label.includes("pro")) return 1;
  if (label.includes("premium") || label.includes("vip")) return 2;
  if (label.includes("dina")) return 3;
  return 4;
}

function sortTicketCatalog(catalog) {
  return [...catalog].sort((a, b) => {
    const priorityDiff = ticketOrderPriority(a) - ticketOrderPriority(b);
    if (priorityDiff !== 0) return priorityDiff;

    const nameA = (a?.name?.[currentLang] || a?.name?.en || "").toLowerCase();
    const nameB = (b?.name?.[currentLang] || b?.name?.en || "").toLowerCase();
    return nameA.localeCompare(nameB);
  });
}

function readTicketCatalogFromBackend() {
  if (Array.isArray(window.pycontgTicketCatalog) && window.pycontgTicketCatalog.length) {
    return sortTicketCatalog(window.pycontgTicketCatalog);
  }

  const payload = document.getElementById("ticket-catalog-data");
  if (!payload) return defaultTicketCatalog;

  const normalizeCatalog = (value) => {
    if (Array.isArray(value)) {
      return value;
    }

    if (value && typeof value === "object") {
      if (Array.isArray(value.data)) return value.data;
      if (Array.isArray(value.items)) return value.items;
      if (Array.isArray(value.catalog)) return value.catalog;
    }

    return [];
  };

  try {
    const parsed = JSON.parse(payload.textContent || "[]");
    const catalog = normalizeCatalog(parsed);
    return catalog.length ? sortTicketCatalog(catalog) : sortTicketCatalog(defaultTicketCatalog);
  } catch (error) {
    return sortTicketCatalog(defaultTicketCatalog);
  }
}

const ticketCatalog = readTicketCatalogFromBackend();

const ticketState = {
  selectedTicketId: null,
  quantities: {},
};

function getTicketById(id) {
  return ticketCatalog.find(ticket => ticket.id === id);
}

function isEarlyBirdActive(ticket) {
  if (typeof ticket.isEarlyBirdActive === "boolean") return ticket.isEarlyBirdActive;
  if (!ticket.earlyBirdEndDate || !ticket.earlyBirdPrice) return false;
  const endDate = new Date(ticket.earlyBirdEndDate);
  return new Date() <= endDate;
}

function isTicketSalesOpen(ticket) {
  if (typeof ticket.isSalesOpen === "boolean") return ticket.isSalesOpen;
  if (typeof ticket.salesStatus === "string") return ticket.salesStatus === "open";
  return true;
}

function isStudentTicket(ticket) {
  if (!ticket) return false;
  if (typeof ticket.isStudent === "boolean") return ticket.isStudent;
  const label = `${ticket.id || ""} ${ticket.name?.en || ""} ${ticket.name?.fr || ""} ${ticket.description?.en || ""} ${ticket.description?.fr || ""}`.toLowerCase();
  return label.includes("student") || label.includes("etudiant") || label.includes("etudiante");
}

function getTicketPrice(ticket) {
  if (isEarlyBirdActive(ticket)) return ticket.earlyBirdPrice;
  return ticket.regularPrice;
}

function formatCfa(value) {
  if (value === null || value === undefined) return "-";
  const locale = currentLang === "fr" ? "fr-FR" : "en-US";
  return `${value.toLocaleString(locale)} F CFA`;
}

function maxSelectable(ticket) {
  const available = Math.max(ticket.quantityAvailable, 0);
  return Math.max(0, Math.min(ticket.maxPerUser, available));
}

function ensureQuantity(ticket) {
  const max = maxSelectable(ticket);
  if (max === 0) {
    ticketState.quantities[ticket.id] = 0;
    return 0;
  }
  const current = ticketState.quantities[ticket.id] || 1;
  const next = Math.min(Math.max(current, 1), max);
  ticketState.quantities[ticket.id] = next;
  return next;
}

function renderTicketList() {
  const container = document.getElementById("ticket-list");
  if (!container) return;

  container.innerHTML = ticketCatalog.map(ticket => {
    const earlyActive = isEarlyBirdActive(ticket);
    const salesOpen = isTicketSalesOpen(ticket);
    const qty = ensureQuantity(ticket);
    const soldOut = maxSelectable(ticket) === 0;
    const buyDisabled = !salesOpen || soldOut;
    const badge = earlyActive
      ? `<span class="ticket-badge">${currentLang === "fr" ? "Early Bird" : "Early Bird"}</span>`
      : "";

    const priceBlock = earlyActive
      ? `<div class="ticket-price"><del>${formatCfa(ticket.regularPrice)}</del><span class="price-main">${formatCfa(ticket.earlyBirdPrice)}</span></div>`
      : `<div class="ticket-price"><span class="price-main">${formatCfa(ticket.regularPrice)}</span></div>`;

    const availabilityLabel = !salesOpen
      ? (ticket.salesStatus === "upcoming"
        ? (currentLang === "fr" ? "Bientot disponible" : "Coming soon")
        : (currentLang === "fr" ? "Ferme" : "Closed"))
      : soldOut
        ? (currentLang === "fr" ? "Epuise" : "Sold out")
        : `${ticket.quantityAvailable} ${currentLang === "fr" ? "places" : "spots"}`;

    const buyLabel = !salesOpen
      ? (ticket.salesStatus === "upcoming"
        ? (currentLang === "fr" ? "Bientot disponible" : "Coming soon")
        : (currentLang === "fr" ? "Ferme" : "Closed"))
      : soldOut
        ? (currentLang === "fr" ? "Epuise" : "Sold out")
        : (currentLang === "fr" ? "Acheter" : "Buy");

    return `
      <article class="ticket-card ${buyDisabled ? "is-sold-out" : ""}" data-ticket-id="${ticket.id}" data-sales-status="${ticket.salesStatus || (salesOpen ? "open" : "closed")}">
        <div class="ticket-card-header">
          <div>
            <h3 class="ticket-card-title">${ticket.name[currentLang] || ticket.name.en}</h3>
            <p class="ticket-card-desc">${ticket.description[currentLang] || ticket.description.en}</p>
          </div>
          ${badge}
        </div>
        ${priceBlock}
        <div class="ticket-meta-row">
          <span>${availabilityLabel}</span>
          <span>${currentLang === "fr" ? `Max ${ticket.maxPerUser} par personne` : `Max ${ticket.maxPerUser} per attendee`}</span>
        </div>
        <div class="ticket-actions">
          <div class="qty-selector" role="group" aria-label="${currentLang === "fr" ? "Quantite" : "Quantity"}">
            <button type="button" aria-label="${currentLang === "fr" ? "Diminuer" : "Decrease"}" data-qty-btn="minus" data-ticket-id="${ticket.id}" ${buyDisabled ? "disabled" : ""}>-</button>
            <input type="number" aria-label="${currentLang === "fr" ? "Quantite" : "Quantity"}" min="${buyDisabled ? 0 : 1}" max="${maxSelectable(ticket)}" value="${qty}" inputmode="numeric" data-qty-input="${ticket.id}" ${buyDisabled ? "disabled" : ""} />
            <button type="button" aria-label="${currentLang === "fr" ? "Augmenter" : "Increase"}" data-qty-btn="plus" data-ticket-id="${ticket.id}" ${buyDisabled ? "disabled" : ""}>+</button>
          </div>
          <button type="button" class="btn ${buyDisabled ? "btn-ghost" : "btn-primary"}" data-buy-ticket="${ticket.id}" ${buyDisabled ? "disabled" : ""}>
            ${buyLabel}
          </button>
        </div>
      </article>
    `;
  }).join("");

  container.querySelectorAll("[data-qty-btn]").forEach(btn => {
    btn.addEventListener("click", () => {
      const ticketId = btn.getAttribute("data-ticket-id");
      const ticket = getTicketById(ticketId);
      if (!ticket) return;
      const max = maxSelectable(ticket);
      const current = ensureQuantity(ticket);
      const direction = btn.getAttribute("data-qty-btn");
      const next = direction === "plus" ? Math.min(current + 1, max) : Math.max(current - 1, 1);
      ticketState.quantities[ticketId] = next;
      const input = container.querySelector(`[data-qty-input='${ticketId}']`);
      if (input) input.value = next;
      updateSummary(ticketId);
    });
  });

  container.querySelectorAll("[data-qty-input]").forEach(input => {
    input.addEventListener("change", () => {
      const ticketId = input.getAttribute("data-qty-input");
      const ticket = getTicketById(ticketId);
      if (!ticket) return;
      const max = maxSelectable(ticket);
      const value = Math.min(Math.max(parseInt(input.value || "1", 10), 1), max);
      ticketState.quantities[ticketId] = value;
      input.value = value;
      updateSummary(ticketId);
    });
  });

  container.querySelectorAll("[data-buy-ticket]").forEach(btn => {
    btn.addEventListener("click", () => {
      const ticketId = btn.getAttribute("data-buy-ticket");
      if (!ticketId) return;
      ticketState.selectedTicketId = ticketId;
      updateSummary(ticketId);
      openTicketModal();
    });
  });
}

function updateSummary(selectedId = ticketState.selectedTicketId) {
  const summaryTicket = document.getElementById("summary-ticket");
  const summaryQty = document.getElementById("summary-qty");
  const summarySubtotal = document.getElementById("summary-subtotal");
  const summaryTotal = document.getElementById("summary-total");
  const continueBtn = document.getElementById("continue-to-payment");

  if (!summaryTicket || !summaryQty || !summarySubtotal || !summaryTotal || !continueBtn) return;

  if (!selectedId) {
    summaryTicket.textContent = currentLang === "fr" ? "Choisissez un ticket" : "Select a ticket";
    summaryQty.textContent = "0";
    summarySubtotal.textContent = formatCfa(0);
    summaryTotal.textContent = formatCfa(0);
    continueBtn.disabled = true;
    return;
  }

  ticketState.selectedTicketId = selectedId;

  const ticket = getTicketById(selectedId);
  if (!ticket) return;
  const qty = ensureQuantity(ticket);
  const price = getTicketPrice(ticket);
  const total = price * qty;
  const salesOpen = isTicketSalesOpen(ticket);

  syncStudentProofField(ticket);

  summaryTicket.textContent = ticket.name[currentLang] || ticket.name.en;
  summaryQty.textContent = qty;
  summarySubtotal.textContent = formatCfa(total);
  summaryTotal.textContent = formatCfa(total);
  continueBtn.disabled = !salesOpen || maxSelectable(ticket) === 0;

  updateModalSummary(ticket, qty, total);
}

function updateModalSummary(ticket, qty, total) {
  const modalTicket = document.getElementById("modal-summary-ticket");
  const modalQty = document.getElementById("modal-summary-qty");
  const modalTotal = document.getElementById("modal-summary-total");
  if (!modalTicket || !modalQty || !modalTotal) return;
  modalTicket.textContent = ticket ? (ticket.name[currentLang] || ticket.name.en) : "-";
  modalQty.textContent = qty || 0;
  modalTotal.textContent = formatCfa(total || 0);
}

function syncStudentProofField(ticket) {
  const field = document.getElementById("student-proof-field");
  const input = document.getElementById("student-proof");
  if (!field || !input) return;

  const studentMode = isStudentTicket(ticket);
  field.hidden = !ticket;
  field.classList.toggle("is-active", studentMode);
  field.classList.toggle("is-muted", !studentMode);
  input.required = studentMode;
  input.disabled = !studentMode;

  if (!studentMode) {
    input.value = "";
    showFieldError("student-proof", "");
  }
}

function openTicketModal() {
  const modal = document.getElementById("ticket-modal");
  if (!modal) return;
  syncStudentProofField(getTicketById(ticketState.selectedTicketId));
  const form = document.getElementById("ticket-form");
  if (form) setTicketFormSubmitting(form, false);
  modal.classList.add("open");
  modal.setAttribute("aria-hidden", "false");
  document.body.style.overflow = "hidden";
  const firstInput = modal.querySelector("input, textarea");
  if (firstInput) firstInput.focus();
}

function closeTicketModal() {
  const modal = document.getElementById("ticket-modal");
  if (!modal) return;
  modal.classList.remove("open");
  modal.setAttribute("aria-hidden", "true");
  document.body.style.overflow = "";
  const form = document.getElementById("ticket-form");
  if (form) setTicketFormSubmitting(form, false);
}

function showFieldError(fieldId, message) {
  const error = document.querySelector(`[data-error-for='${fieldId}']`);
  if (error) error.textContent = message || "";
}

function clearFieldErrors() {
  document.querySelectorAll(".field-error").forEach(el => { el.textContent = ""; });
  const formError = document.getElementById("ticket-form-error");
  if (formError) formError.textContent = "";
}

function setTicketFormSubmitting(form, isSubmitting) {
  const submitBtn = form.querySelector("button[type='submit']");
  if (!submitBtn) return;

  if (isSubmitting) {
    if (!submitBtn.dataset.defaultLabel) {
      submitBtn.dataset.defaultLabel = submitBtn.textContent || "";
    }
    submitBtn.disabled = true;
    submitBtn.textContent = currentLang === "fr"
      ? (submitBtn.getAttribute("data-loading-fr") || "Envoi en cours...")
      : (submitBtn.getAttribute("data-loading-en") || "Sending...");
    form.dataset.submitting = "true";
    return;
  }

  submitBtn.disabled = false;
  submitBtn.textContent = submitBtn.dataset.defaultLabel || (currentLang === "fr" ? "Continuer vers le paiement" : "Continue to payment");
  delete form.dataset.submitting;
}

function validateTicketForm(form) {
  clearFieldErrors();
  let valid = true;

  const fullName = form.querySelector("#full-name");
  const email = form.querySelector("#email");
  const consentCoc = form.querySelector("#consent-coc");
  const ticket = getTicketById(ticketState.selectedTicketId);
  const studentProof = form.querySelector("#student-proof");

  if (!fullName.value.trim()) {
    showFieldError("full-name", currentLang === "fr" ? "Champ obligatoire." : "Required field.");
    valid = false;
  }
  if (!email.value.trim()) {
    showFieldError("email", currentLang === "fr" ? "Email requis." : "Email is required.");
    valid = false;
  } else {
    const emailPattern = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
    if (!emailPattern.test(email.value.trim())) {
      showFieldError("email", currentLang === "fr" ? "Email invalide." : "Invalid email.");
      valid = false;
    }
  }

  if (!consentCoc.checked) {
    showFieldError("consent", currentLang === "fr" ? "Veuillez accepter les conditions obligatoires." : "Please accept the required policies.");
    valid = false;
  }

  if (isStudentTicket(ticket)) {
    if (!studentProof || !studentProof.files || studentProof.files.length === 0) {
      showFieldError("student-proof", currentLang === "fr" ? "Veuillez joindre une preuve etudiante." : "Please upload student proof.");
      valid = false;
    }
  }

  return valid;
}

function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const result = typeof reader.result === "string" ? reader.result : "";
      const base64 = result.includes(",") ? result.split(",")[1] : "";
      resolve(base64);
    };
    reader.onerror = () => reject(reader.error || new Error("Failed to read file."));
    reader.readAsDataURL(file);
  });
}

async function buildTicketSubmissionPayload(form, ticket) {
  const fullName = form.querySelector("#full-name").value.trim();
  const nameParts = fullName.split(/\s+/).filter(Boolean);
  const firstName = nameParts.shift() || "";
  const lastName = nameParts.join(" ");
  const studentFile = form.querySelector("#student-proof")?.files?.[0] || null;
  const quantity = ensureQuantity(ticket);
  const unitPrice = getTicketPrice(ticket);
  const consentCoc = form.querySelector("#consent-coc").checked;

  const payload = {
    ticket: {
      id: ticket.id,
      name: ticket.name[currentLang] || ticket.name.en,
      unitPrice,
      currency: "XOF",
      isStudent: isStudentTicket(ticket),
    },
    quantity,
    total: unitPrice * quantity,
    buyer: {
      fullName,
      firstName,
      lastName,
      email: form.querySelector("#email").value.trim(),
      whatsapp: form.querySelector("#whatsapp").value.trim(),
      dietaryRestrictions: (form.querySelector("#dietary-restrictions")?.value || "").trim() || null,
    },
    consent: {
      codeOfConduct: consentCoc,
      privacyPolicy: consentCoc,
      terms: consentCoc,
      partnerSharing: !!form.querySelector("#consent-partners")?.checked,
    },
    coupon: (document.getElementById("coupon")?.value || "").trim() || null,
    studentProof: null,
  };

  if (isStudentTicket(ticket) && studentFile) {
    payload.studentProof = {
      fileName: studentFile.name,
      mimeType: studentFile.type || "application/octet-stream",
      base64: await fileToBase64(studentFile),
    };
  }

  return payload;
}

async function submitTicketPurchase(payload) {
  const response = await fetch("/tickets/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.detail || data.message || "Unable to submit ticket data.");
  }

  return data;
}

function initTicketsPage() {
  const page = document.getElementById("page-tickets");
  if (!page) return;

  const modal = document.getElementById("ticket-modal");
  if (modal && modal.parentElement !== document.body) {
    document.body.appendChild(modal);
  }

  renderTicketList();
  updateSummary();

  const continueBtn = document.getElementById("continue-to-payment");
  if (continueBtn) {
    continueBtn.addEventListener("click", () => {
      if (!ticketState.selectedTicketId) return;
      openTicketModal();
    });
  }

  document.querySelectorAll("[data-close-modal]").forEach(btn => {
    btn.addEventListener("click", closeTicketModal);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeTicketModal();
  });

  const form = document.getElementById("ticket-form");
  if (form) {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (form.dataset.submitting === "true") return;
      if (!validateTicketForm(form)) return;

      const ticket = getTicketById(ticketState.selectedTicketId);
      if (!ticket) return;
      if (!isTicketSalesOpen(ticket) || maxSelectable(ticket) === 0) return;
      try {
        setTicketFormSubmitting(form, true);
        const payload = await buildTicketSubmissionPayload(form, ticket);
        const submission = await submitTicketPurchase(payload);
        const paymentUrl = submission.payment_url || submission.paymentUrl;
        if (!paymentUrl) {
          throw new Error(currentLang === "fr"
            ? "Le lien de paiement est manquant."
            : "The payment link is missing.");
        }

        closeTicketModal();
        window.location.assign(paymentUrl);
      } catch (error) {
        setTicketFormSubmitting(form, false);
        const formError = document.getElementById("ticket-form-error");
        if (formError) {
          formError.textContent = error instanceof Error ? error.message : "Unable to submit ticket data.";
        }
      }
    });
  }

  document.addEventListener("pycontg:language-changed", () => {
    renderTicketList();
    updateSummary(ticketState.selectedTicketId);
  });
}

/* ── HERO ENTRANCE (staggered) ── */
function heroEntrance() {
  const items = document.querySelectorAll("#page-home .hero .reveal");
  items.forEach((el, i) => {
    setTimeout(() => el.classList.add("visible"), 120 + i * 110);
  });
}

/* ── COLLAGE HOVER PARALLAX ── */
function initCollageParallax() {
  const hero = document.querySelector(".hero");
  if (!hero) return;
  const collage = hero.querySelector(".collage");
  if (!collage) return;

  hero.addEventListener("mousemove", (e) => {
    const rect = hero.getBoundingClientRect();
    const cx = (e.clientX - rect.left) / rect.width - 0.5;
    const cy = (e.clientY - rect.top) / rect.height - 0.5;
    collage.style.transform = `perspective(800px) rotateY(${cx * 4}deg) rotateX(${-cy * 4}deg)`;
  });
  hero.addEventListener("mouseleave", () => {
    collage.style.transform = "perspective(800px) rotateY(0deg) rotateX(0deg)";
    collage.style.transition = "transform .6s ease";
  });
  hero.addEventListener("mouseenter", () => {
    collage.style.transition = "transform .1s ease";
  });
}

/* ── CURSOR DOT (subtle) ── */
function initCursorDot() {
  // Only on large screens
  if (window.innerWidth < 1024) return;
  const dot = document.createElement("div");
  dot.style.cssText = `
    position:fixed;width:8px;height:8px;border-radius:50%;
    background:var(--gold);pointer-events:none;z-index:9999;
    transform:translate(-50%,-50%);transition:transform .1s ease,opacity .2s;
    mix-blend-mode:multiply;opacity:0;
  `;
  document.body.appendChild(dot);

  let mx = 0, my = 0, ox = 0, oy = 0;
  document.addEventListener("mousemove", e => {
    mx = e.clientX; my = e.clientY;
    dot.style.opacity = "1";
  });
  document.addEventListener("mouseleave", () => { dot.style.opacity = "0"; });

  function animDot() {
    ox += (mx - ox) * 0.15;
    oy += (my - oy) * 0.15;
    dot.style.left = ox + "px";
    dot.style.top = oy + "px";
    requestAnimationFrame(animDot);
  }
  animDot();

  // Scale on hover over clickables
  document.querySelectorAll("a,button,.btn,.nav-link,.drawer-link").forEach(el => {
    el.addEventListener("mouseenter", () => { dot.style.transform = "translate(-50%,-50%) scale(3)"; dot.style.opacity = ".4"; });
    el.addEventListener("mouseleave", () => { dot.style.transform = "translate(-50%,-50%) scale(1)"; dot.style.opacity = "1"; });
  });
}

/* ── INIT ── */
document.addEventListener("DOMContentLoaded", async () => {
  // Load translations first
  await loadTranslations();

  const savedLang = localStorage.getItem("pycontg_lang") || "en";
  applyLanguage(savedLang);

  renderTeam();
  initNavbarScroll();
  // Intentionally disabled for a calmer, less flashy visual style.
  // initCollageParallax();
  // initCursorDot();

  // Hero entrance on load
  heroEntrance();

  // Observe sections that are visible on load
  setTimeout(observeReveals, 80);

  initTicketsPage();
});
