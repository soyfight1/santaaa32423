export function initPanels({ orderbookRoot, tradesRoot, ordersRoot }) {
  // Orderbook
  const obTitle = document.createElement('h3');
  obTitle.textContent = 'Orderbook';
  const obGrid = document.createElement('div');
  obGrid.className = 'orderbook-grid';
  orderbookRoot.append(obTitle, obGrid);

  function renderOrderbook({ bids, asks }) {
    obGrid.innerHTML = '';
    const header = ['Precio', 'Cantidad', 'Total'];
    header.forEach(h => {
      const el = document.createElement('div'); el.textContent = h; el.style.opacity = '0.6'; obGrid.appendChild(el);
    });
    const max = Math.max(
      ...bids.map(b => b[1]),
      ...asks.map(a => a[1]),
      1
    );
    const row = (arr, cls) => {
      arr.forEach(([price, qty]) => {
        const total = qty * price;
        const p = document.createElement('div'); p.textContent = price.toLocaleString(); p.className = cls;
        const q = document.createElement('div'); q.textContent = qty.toFixed(4);
        const t = document.createElement('div'); t.textContent = total.toLocaleString();
        obGrid.append(p, q, t);
      });
    };
    row(asks.slice().reverse(), 'ask');
    row(bids, 'bid');
  }

  // Trades tape
  const trTitle = document.createElement('h3');
  trTitle.textContent = 'Trades';
  const trList = document.createElement('div');
  tradesRoot.append(trTitle, trList);

  function appendTrade(t) {
    const el = document.createElement('div');
    el.className = 'trade-item';
    el.innerHTML = `
      <div style="opacity:.6">${new Date(t.time).toLocaleTimeString()}</div>
      <div class="${t.side === 'buy' ? 'bid' : 'ask'}">${t.price.toLocaleString()}</div>
      <div>${Number(t.quantity).toFixed(4)}</div>
    `;
    trList.prepend(el);
    while (trList.children.length > 120) trList.removeChild(trList.lastChild);
  }

  // Orders panel with simple form
  const odTitle = document.createElement('h3'); odTitle.textContent = 'Order Entry';
  const form = document.createElement('div'); form.className = 'orders-form';
  const side = document.createElement('select'); side.innerHTML = '<option value="buy">Buy</option><option value="sell">Sell</option>';
  const price = document.createElement('input'); price.type = 'number'; price.placeholder = 'Precio';
  const qty = document.createElement('input'); qty.type = 'number'; qty.placeholder = 'Cantidad';
  const submit = document.createElement('button'); submit.textContent = 'Place Order';
  const openList = document.createElement('div'); openList.style.marginTop = '8px';
  ordersRoot.append(odTitle, form, openList);
  form.append(side, price, qty, submit);

  let onPlaceOrderCb = () => {};
  submit.addEventListener('click', () => {
    onPlaceOrderCb({ side: side.value, price: Number(price.value), quantity: Number(qty.value) });
  });

  function onPlaceOrder(cb) { onPlaceOrderCb = cb; }

  function addOpenOrder(o) {
    const el = document.createElement('div');
    el.style.padding = '6px 0';
    el.style.display = 'grid';
    el.style.gridTemplateColumns = '1fr 1fr 1fr 1fr';
    el.style.borderBottom = '1px dashed rgba(255,255,255,0.06)';
    el.innerHTML = `
      <div>${o.symbol}</div>
      <div class="${o.side === 'buy' ? 'bid' : 'ask'}">${o.side.toUpperCase()}</div>
      <div>${o.price.toLocaleString()}</div>
      <div>${o.quantity}</div>
    `;
    openList.prepend(el);
  }

  return { renderOrderbook, appendTrade, onPlaceOrder, addOpenOrder };
}