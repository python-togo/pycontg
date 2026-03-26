/* ═══════════════════════════════════════════════
   PYCON TOGO 2026 — SCRIPT.JS
═══════════════════════════════════════════════ */

/* ── TEAM DATA ── */
const teamData = [
  {
    name:    "Waschiou Bouraima",
    role:    "Président de la Conférence",
    bio:     "Fondateur de Python Togo. Passionné par le développement de l'écosystème tech local et l'open source en Afrique.",
    flag:    "🇹🇬",
    linkedin: "https://linkedin.com",
    colors:  ["#0d3320", "#c52d2d"],
  },
  {
    name:    "Geoffrey Logovi",
    role:    "Directeur du Programme",
    bio:     "Responsable de la sélection des speakers et de la conception du programme pour un maximum d'impact communautaire.",
    flag:    "TG",
    linkedin: "https://linkedin.com",
    colors:  ["#0d3320", "#c52d2d"],
  },
  {
    name:    "Mawuli Dossou",
    role:    "Responsable Partenariats",
    bio:     "Construit les partenariats avec les entreprises tech pour financer et développer PyCon Togo année après année.",
    flag:    "🇹🇬",
    linkedin: "https://linkedin.com",
    colors:  ["#0d3320", "#c8a400"],
  },
  {
    name:    "Afi Kpodo",
    role:    "Community Manager",
    bio:     "Gère la communauté Python Togo, les événements locaux et la présence en ligne de l'organisation.",
    flag:    "🇹🇬",
    linkedin: "https://linkedin.com",
    colors:  ["#2d8a50", "#0d3320"],
  },
  {
    name:    "Yinka Adewale",
    role:    "Responsable Technique",
    bio:     "Pilote l'infrastructure technique et le développement de la plateforme de la conférence.",
    flag:    "🇳🇬",
    linkedin: "https://linkedin.com",
    colors:  ["#1a5c35", "#0d3320"],
  },
  {
    name:    "Nneji Gift",
    role:    "Directrice Design de Frontend ",
    bio:     "Crée l'identité visuelle et le branding qui rendent PyCon Togo mémorable et reconnaissable.",
    flag:    "NG",
    linkedin: "https://linkedin.com",
    colors:  ["#1a5c35", "#0d3320"],
  },
];

/* ── HELPERS ── */
function initials(name) {
  return name.split(" ").map(n => n[0]).join("").slice(0, 2).toUpperCase();
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

/* ── NAVIGATION ── */
let currentPage = "home";

function navigate(page) {
  // Hide all pages
  document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));

  // Show target
  const target = document.getElementById("page-" + page);
  if (target) target.classList.add("active");

  // Update nav links
  document.querySelectorAll(".nav-link").forEach(l => {
    l.classList.toggle("active", l.dataset.page === page);
  });

  currentPage = page;
  window.scrollTo({ top: 0, behavior: "smooth" });

  // Re-trigger reveals for the new page
  setTimeout(observeReveals, 50);
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
  const drawer  = document.getElementById("drawer");
  const overlay = document.getElementById("drawer-overlay");
  const burger  = document.getElementById("hamburger");
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
  const btn  = document.getElementById("submit-btn");
  const form = document.getElementById("contact-form");
  const succ = document.getElementById("form-success");

  btn.textContent = "Envoi en cours...";
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
    const cx = (e.clientX - rect.left) / rect.width  - 0.5;
    const cy = (e.clientY - rect.top)  / rect.height - 0.5;
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
    dot.style.top  = oy + "px";
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
document.addEventListener("DOMContentLoaded", () => {
  renderTeam();
  initNavbarScroll();
  initCollageParallax();
  initCursorDot();

  // Hero entrance on load
  heroEntrance();

  // Observe sections that are visible on load
  setTimeout(observeReveals, 80);
});
