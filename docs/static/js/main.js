/* DIVE Project Page — Interactions */

document.addEventListener('DOMContentLoaded', () => {

  // === Tab Switching ===
  document.querySelectorAll('.method-tabs .tabs li').forEach(tab => {
    tab.addEventListener('click', () => {
      const tabGroup = tab.closest('.method-tabs');
      const target = tab.dataset.tab;
      tabGroup.querySelectorAll('.tabs li').forEach(t => t.classList.remove('is-active'));
      tabGroup.querySelectorAll('.tab-content').forEach(c => c.classList.remove('is-active'));
      tab.classList.add('is-active');
      tabGroup.querySelector(`#${target}`).classList.add('is-active');
    });
  });

  // === Frontier Table Collapse/Expand ===
  document.querySelectorAll('.frontier-toggle').forEach(toggle => {
    toggle.addEventListener('click', () => {
      toggle.classList.toggle('is-open');
      const isOpen = toggle.classList.contains('is-open');
      document.querySelectorAll('.frontier-row').forEach(row => {
        row.style.display = isOpen ? '' : 'none';
      });
      toggle.querySelector('.toggle-label').textContent =
        isOpen ? 'Hide Frontier Models' : 'Show Frontier Models';
    });
  });

  // === Benchmark Card Expand/Collapse ===
  document.querySelectorAll('.bench-card-header').forEach(header => {
    header.addEventListener('click', () => {
      const card = header.closest('.bench-card');
      // Close other open cards (accordion behavior)
      document.querySelectorAll('.bench-card.is-open').forEach(c => {
        if (c !== card) c.classList.remove('is-open');
      });
      card.classList.toggle('is-open');
    });
  });

  // === BibTeX Copy ===
  document.querySelectorAll('.bibtex-copy-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const text = btn.closest('.bibtex-section').querySelector('.bibtex-content').textContent;
      navigator.clipboard.writeText(text).then(() => {
        btn.classList.add('copied');
        btn.textContent = 'Copied!';
        setTimeout(() => { btn.classList.remove('copied'); btn.textContent = 'Copy'; }, 2000);
      });
    });
  });

  // === Scroll Reveal ===
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) entry.target.classList.add('is-visible');
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

});
