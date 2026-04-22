const listingForm = document.getElementById('listing-form');
if (listingForm) {
  listingForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(listingForm);
    const payload = Object.fromEntries(formData.entries());
    payload.price = payload.price ? Number(payload.price) : null;

    const response = await fetch('/api/listings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    document.getElementById('result-box').textContent = JSON.stringify(data, null, 2);
  });
}
