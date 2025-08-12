import { initScene } from './3d/scene.js';
import { initChart } from './ui/chart.js';
import { initPanels } from './ui/panels.js';
import { connectExchange } from './data/exchange.js';

const symbolSelect = document.getElementById('symbol-select');
const livePriceEl = document.getElementById('live-price');
const threeRoot = document.getElementById('three-root');
const chartRoot = document.getElementById('chart-root');

let currentSymbol = symbolSelect.value;
let teardownData = null;

const scene = initScene(threeRoot);
const chart = initChart(chartRoot);
const panels = initPanels({ orderbookRoot: document.getElementById('orderbook'), tradesRoot: document.getElementById('trades'), ordersRoot: document.getElementById('orders') });

function startData(symbol) {
  if (teardownData) teardownData();
  const { emitter, close } = connectExchange(symbol);
  teardownData = close;

  const lastCandleByInterval = new Map();

  emitter.addEventListener('price', (e) => {
    const p = e.detail;
    livePriceEl.textContent = `${p.price.toLocaleString(undefined, {maximumFractionDigits: 2})} USDT`;
    scene.updatePrice(p.price);
  });

  emitter.addEventListener('kline', (e) => {
    const k = e.detail; // { time, open, high, low, close }
    chart.updateCandle(k);
  });

  emitter.addEventListener('orderbook', (e) => {
    panels.renderOrderbook(e.detail);
  });

  emitter.addEventListener('trade', (e) => {
    const t = e.detail;
    panels.appendTrade(t);
  });

  panels.onPlaceOrder((order) => {
    // Simulación de ejecución inmediata contra mejor precio
    const side = order.side;
    const qty = Number(order.quantity);
    const price = Number(order.price);
    const px = isFinite(price) && price > 0 ? price : scene.getLastPrice();
    panels.addOpenOrder({ id: crypto.randomUUID(), symbol: symbol.toUpperCase(), side, price: px, quantity: qty, status: 'filled' });
  });
}

// UI wiring
symbolSelect.addEventListener('change', () => {
  currentSymbol = symbolSelect.value;
  startData(currentSymbol);
});

document.getElementById('theme-toggle').addEventListener('click', () => {
  document.documentElement.style.setProperty('--bg', '#ffffff');
});

document.getElementById('quality-toggle').addEventListener('click', () => {
  scene.toggleQuality();
});

startData(currentSymbol);