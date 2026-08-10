/* Shared chrome: nav injection, active-page marking, mobile menu, footer year.
   Kept dependency-free and tiny so every page except the simulator stays instant. */

const NAV_LINKS = [
  { href: 'index.html',      label: 'Home' },
  { href: 'simulator.html',  label: 'Simulator' },
  { href: 'validation.html', label: 'Validation' },
  { href: 'docs.html',       label: 'Docs' },
  { href: 'research.html',   label: 'Research' },
  { href: 'about.html',      label: 'About' },
];

const REPO = 'https://github.com/ayushsankar12/Velocity-X';

function currentPage() {
  const file = window.location.pathname.split('/').pop();
  return !file || file === '' ? 'index.html' : file;
}

function buildNav() {
  const here = currentPage();
  const links = NAV_LINKS.map(l => {
    const active = l.href === here ? ' class="active" aria-current="page"' : '';
    return `<a href="${l.href}"${active}>${l.label}</a>`;
  }).join('');

  return `
<a class="skip-link" href="#main">Skip to content</a>
<nav class="nav">
  <div class="nav-inner">
    <a class="brand" href="index.html">
      <span class="brand-mark" aria-hidden="true">V</span>
      <span>Velocity&nbsp;X</span>
    </a>
    <button class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="navLinks" aria-label="Toggle navigation">☰</button>
    <div class="nav-links" id="navLinks">
      ${links}
      <a href="${REPO}" target="_blank" rel="noopener">GitHub&nbsp;↗</a>
    </div>
  </div>
</nav>`;
}

function buildFooter() {
  return `
<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <div class="brand" style="margin-bottom:10px">
          <span class="brand-mark" aria-hidden="true">V</span>
          <span>Velocity&nbsp;X</span>
        </div>
        <p class="small" style="max-width:42ch">
          An open simulator for visual-inertial odometry under aggressive flight —
          with analytic ground truth that is exact by construction.
        </p>
      </div>
      <div>
        <h4>Explore</h4>
        <a href="simulator.html">Run the simulator</a>
        <a href="validation.html">Validation</a>
        <a href="docs.html">Documentation</a>
        <a href="research.html">Research</a>
      </div>
      <div>
        <h4>Project</h4>
        <a href="about.html">About the author</a>
        <a href="${REPO}" target="_blank" rel="noopener">Source on GitHub ↗</a>
        <a href="${REPO}/issues" target="_blank" rel="noopener">Report an issue ↗</a>
      </div>
    </div>
    <div class="footer-base">
      <span>© <span id="year"></span> Ayush Sankar · MIT licensed</span>
    </div>
  </div>
</footer>`;
}

function mount() {
  const navHost = document.getElementById('site-nav');
  if (navHost) navHost.innerHTML = buildNav();

  const footHost = document.getElementById('site-footer');
  if (footHost) footHost.innerHTML = buildFooter();

  const y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  const toggle = document.getElementById('navToggle');
  const links = document.getElementById('navLinks');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      const open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    });
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', mount);
} else {
  mount();
}
