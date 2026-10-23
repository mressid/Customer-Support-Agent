// Shared reveal.js setup for all decks.
(function () {
  var label = document.createElement('div'); label.id = 'chapter-label'; document.body.appendChild(label);
  var brand = document.createElement('div'); brand.id = 'brand-label'; brand.textContent = 'AI Customer Support Platform';
  document.body.appendChild(brand);

  function updateLabel(slide) {
    if (!slide) return;
    var sec = slide.closest('section[data-chapter]') || slide;
    var text = sec.getAttribute('data-chapter') || '';
    var dark = slide.classList.contains('on-dark') || (slide.parentElement && slide.parentElement.classList.contains('on-dark'));
    document.body.classList.toggle('on-dark', !!dark);
    label.textContent = text;
    label.classList.toggle('hidden', !text || dark);
  }

  Reveal.initialize({
    hash: true, width: 1280, height: 720, margin: 0.04, minScale: 0.2, maxScale: 2.0,
    transition: 'slide', transitionSpeed: 'default', backgroundTransition: 'fade',
    controls: true, controlsTutorial: false, progress: true, slideNumber: 'c/t',
    center: true, pdfSeparateFragments: false, autoAnimateDuration: 0.7, autoAnimateEasing: 'ease-in-out',
    plugins: [RevealNotes, RevealZoom, RevealHighlight]
  }).then(function () { updateLabel(Reveal.getCurrentSlide()); });

  Reveal.on('slidechanged', function (e) { updateLabel(e.currentSlide); });
  Reveal.on('ready', function (e) { updateLabel(e.currentSlide); });
})();

// Click a diagram to enlarge it; click again or press Esc to close.
(function () {
  var overlay = null;
  function close() { if (overlay) { overlay.remove(); overlay = null; } }
  document.addEventListener('click', function (e) {
    var img = e.target.closest && e.target.closest('.diagram img');
    if (overlay) { close(); return; }
    if (!img) return;
    overlay = document.createElement('div');
    overlay.style.cssText = 'position:fixed;inset:0;z-index:1000;background:rgba(10,20,30,.93);display:flex;align-items:center;justify-content:center;cursor:zoom-out;';
    var big = document.createElement('img');
    big.src = img.src; big.alt = img.alt;
    big.style.cssText = 'max-width:96vw;max-height:94vh;background:#fff;border-radius:10px;padding:14px;';
    if (document.documentElement.getAttribute('data-theme') === 'dark') big.style.filter = 'invert(.9) hue-rotate(180deg)';
    overlay.appendChild(big); document.body.appendChild(overlay);
  });
  document.addEventListener('keydown', function (e) {
    if (overlay && e.key === 'Escape') { e.stopPropagation(); e.preventDefault(); close(); }
  }, true);
})();

// Back to the presentations list: visible button + "I" key (listed in the ? help overlay).
(function () {
  var a = document.createElement('a');
  a.id = 'home-link'; a.href = 'index.html'; a.title = 'Back to the presentations list (I)';
  a.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/></svg>' +
    '<span>All decks</span><kbd>I</kbd>';
  document.body.appendChild(a);
  function goHome() { window.location.href = 'index.html'; }
  var register = function () {
    if (window.Reveal && Reveal.addKeyBinding) {
      Reveal.addKeyBinding({ keyCode: 73, key: 'I', description: 'Back to the presentations list' }, goHome);
    }
  };
  if (window.Reveal && Reveal.isReady && Reveal.isReady()) register(); else Reveal.on('ready', register);
})();

// Link to the full report (PDF) on every slide, next to the "All decks" button.
(function () {
  var r = document.createElement('a');
  r.id = 'report-link'; r.href = 'assets/rapport.pdf'; r.target = '_blank'; r.rel = 'noopener';
  r.title = 'Open the full report (PDF)';
  r.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>' +
    '<span>Report</span>';
  document.body.appendChild(r);
})();

// Link to the functional specification (PDF), left of the "Report" button.
(function () {
  var r = document.createElement('a');
  r.id = 'spec-link'; r.href = 'assets/functional-specification.pdf'; r.target = '_blank'; r.rel = 'noopener';
  r.title = 'Open the functional specification (PDF)';
  r.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="m9 15 2 2 4-4"/></svg>' +
    '<span>Spec</span>';
  document.body.appendChild(r);
})();

// Light / dark theme: toggle button, "D" key, follows the system until the user chooses.
(function () {
  var KEY = 'deck-theme', root = document.documentElement;
  function stored() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function current() { return root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light'; }
  var MOON = '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>';
  var SUN = '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>';
  var btn = document.createElement('button');
  btn.id = 'theme-toggle'; btn.type = 'button';
  function render() {
    var dark = current() === 'dark';
    btn.title = 'Switch to the ' + (dark ? 'light' : 'dark') + ' theme (D)';
    btn.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      (dark ? SUN : MOON) + '</svg><span>' + (dark ? 'Light' : 'Dark') + '</span><kbd>D</kbd>';
  }
  function apply(theme, save) {
    root.setAttribute('data-theme', theme);
    if (save) { try { localStorage.setItem(KEY, theme); } catch (e) {} }
    render();
  }
  function toggle() { apply(current() === 'dark' ? 'light' : 'dark', true); }
  if (!root.getAttribute('data-theme')) {
    apply(stored() || (window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'), false);
  }
  if (/print-pdf/.test(location.search)) root.setAttribute('data-theme', 'light'); // handouts are always light
  btn.addEventListener('click', function () { toggle(); btn.blur(); });
  var nav = document.createElement('div'); nav.id = 'deck-nav';
  nav.appendChild(btn);
  ['report-link', 'home-link'].forEach(function (id) { var el = document.getElementById(id); if (el) nav.appendChild(el); });
  document.body.appendChild(nav);
  render();
  function register() { Reveal.addKeyBinding({ keyCode: 68, key: 'D', description: 'Switch between light and dark theme' }, toggle); }
  if (Reveal.isReady && Reveal.isReady()) register(); else Reveal.on('ready', register);
  if (window.matchMedia) {
    matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) { if (!stored()) apply(e.matches ? 'dark' : 'light', false); });
  }
})();
