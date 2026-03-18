document.addEventListener('DOMContentLoaded', () => {
    const typeSelect = document.getElementById('type');
    const priceGroup = document.getElementById('price-group');
    const stopPriceGroup = document.getElementById('stop-price-group');
    
    // Toggle input fields based on order type
    typeSelect.addEventListener('change', (e) => {
        const type = e.target.value;
        if (type === 'LIMIT') {
            priceGroup.style.display = 'block';
            stopPriceGroup.style.display = 'none';
        } else if (type === 'STOP_MARKET') {
            priceGroup.style.display = 'none';
            stopPriceGroup.style.display = 'block';
        } else {
            priceGroup.style.display = 'none';
            stopPriceGroup.style.display = 'none';
        }
    });

    const form = document.getElementById('orderForm');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const loader = submitBtn.querySelector('.loader');
    const responseArea = document.getElementById('responseArea');
    const responseContent = document.getElementById('responseContent');
    const closeResponse = document.getElementById('closeResponse');

    closeResponse.addEventListener('click', () => {
        responseArea.classList.add('hidden');
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // UI Loading state
        btnText.style.display = 'none';
        loader.style.display = 'block';
        submitBtn.disabled = true;
        responseArea.classList.add('hidden');

        try {
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            // Clean up empty fields
            if (!data.price) delete data.price;
            if (!data.stop_price) delete data.stop_price;

            const response = await fetch('/api/order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            
            let html = '';
            if (result.success && result.data) {
                const d = result.data;
                html = `
                    <div class="status-row">
                        <span class="status-label">Status</span>
                        <span class="status-value success-badge">EXECUTED SUCCESS</span>
                    </div>
                    <div class="status-row">
                        <span class="status-label">Order ID</span>
                        <span class="status-value">${d.orderId}</span>
                    </div>
                    <div class="status-row">
                        <span class="status-label">Symbol / Type</span>
                        <span class="status-value">${d.symbol} / ${d.type}</span>
                    </div>
                    <div class="status-row">
                        <span class="status-label">Executed Qty</span>
                        <span class="status-value">${d.executedQty}</span>
                    </div>
                `;
            } else {
                html = `
                    <div class="status-row">
                        <span class="status-label">Status</span>
                        <span class="status-value error-badge">FAILED</span>
                    </div>
                    <div class="status-row" style="flex-direction: column; gap: 0.5rem;">
                        <span class="status-label">Reason</span>
                        <span class="status-value" style="color: var(--error); font-size: 0.8rem; white-space: pre-wrap;">${result.error || 'Unknown network error occurred.'}</span>
                    </div>
                `;
            }

            responseContent.innerHTML = html;
            responseArea.classList.remove('hidden');

        } catch (err) {
            responseContent.innerHTML = `
                <div class="status-row">
                    <span class="status-label">System Error</span>
                    <span class="status-value error-badge">Fetch Failed: ${err.message}</span>
                </div>
            `;
            responseArea.classList.remove('hidden');
        } finally {
            // Restore UI
            btnText.style.display = 'block';
            loader.style.display = 'none';
            submitBtn.disabled = false;
        }
    });
});
