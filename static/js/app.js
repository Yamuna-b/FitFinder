console.log('Fitfinder loaded');

// Simple placeholder gallery rendering
window.addEventListener('DOMContentLoaded', () => {
  const grid = document.getElementById('gallery-grid');
  if (!grid) return;

  const state = { all: [], filtered: [] };
  const searchEl = document.getElementById('filter-search');
  const categoryEl = document.getElementById('filter-category');
  const colorEl = document.getElementById('filter-color');
  const resetBtn = document.getElementById('filter-reset');

  function loadProducts() {
    fetch('/static/data/products.json').then(r => r.json()).then(data => {
      state.all = data.products || [];
      state.filtered = state.all;
      render();
    }).catch(() => {
      state.all = [];
      state.filtered = [];
      render();
    });
  }

  function matchesFilters(item) {
    const q = (searchEl?.value || '').toLowerCase();
    const cat = (categoryEl?.value || '').toLowerCase();
    const color = (colorEl?.value || '').toLowerCase();
    const inQ = !q || (item.name?.toLowerCase().includes(q) || item.description?.toLowerCase().includes(q));
    const inCat = !cat || item.category?.toLowerCase() === cat;
    const inColor = !color || (item.color || '').toLowerCase().includes(color);
    return inQ && inCat && inColor;
  }

  function openModal(item) {
    const modalEl = document.getElementById('itemModal');
    if (!modalEl) return;
    document.getElementById('itemModalLabel').textContent = item.name;
    const img = document.getElementById('modal-image');
    img.src = item.image || '';
    img.alt = item.name;
    document.getElementById('modal-desc').textContent = item.description || '';
    const modal = new bootstrap.Modal(modalEl);
    modal.show();
  }

  function render() {
    grid.innerHTML = '';
    grid.classList.add('row', 'g-3');
    state.filtered.forEach(item => {
      const col = document.createElement('div');
      col.className = 'col-6 col-md-4 col-lg-3';
      col.innerHTML = `
        <div class="card bg-dark border-secondary h-100">
          <img src="${item.thumb || item.image || ''}" class="card-img-top" alt="${item.name}">
          <div class="card-body">
            <h6 class="card-title">${item.name}</h6>
            <p class="card-text text-muted mb-2">${item.category || ''}</p>
            <div class="d-flex gap-2">
              <button class="btn btn-outline-primary btn-sm" data-action="modal">Details</button>
              <a class="btn btn-outline-light btn-sm" href="/try-on">Add to Try-On</a>
            </div>
          </div>
        </div>`;
      col.querySelector('[data-action="modal"]').addEventListener('click', () => openModal(item));
      grid.appendChild(col);
    });
  }

  function applyFilters() {
    state.filtered = state.all.filter(matchesFilters);
    render();
  }

  [searchEl, categoryEl, colorEl].forEach(el => el && el.addEventListener('input', applyFilters));
  resetBtn?.addEventListener('click', () => {
    if (searchEl) searchEl.value = '';
    if (categoryEl) categoryEl.value = '';
    if (colorEl) colorEl.value = '';
    applyFilters();
  });

  loadProducts();
});


