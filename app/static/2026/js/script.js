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

  btn.textContent = "Envoi en cours...";
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
  btn.textContent = "✓ Inscrit !";
  btn.disabled = true;
  e.target.querySelector("input").value = "";
  setTimeout(() => {
    btn.textContent = "M'avertir";
    btn.disabled = false;
  }, 4000);
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
});
