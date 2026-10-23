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
