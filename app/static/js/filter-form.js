const filterForm = document.getElementById('filter-form');
if (filterForm) {
  filterForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(filterForm);
    const payload = Object.fromEntries(formData.entries());
    payload.owner_only = formData.get('owner_only') === 'on';
    payload.min_price = payload.min_price ? Number(payload.min_price) : null;
    payload.max_price = payload.max_price ? Number(payload.max_price) : null;

    const response = await fetch('/api/filters', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    document.getElementById('result-box').textContent = JSON.stringify(data, null, 2);
  });
}
