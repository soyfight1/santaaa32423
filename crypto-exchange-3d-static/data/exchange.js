function createEmitter() {
  const target = new EventTarget();
  return {
    target,
    emit(type, detail) { target.dispatchEvent(new CustomEvent(type, { detail })); },
    addEventListener(...args) { return target.addEventListener(...args); },
  };
}

function toKlineFromBinance(msg) {
  const k = msg.k;
  return {
    time: Math.floor(k.t / 1000),
    open: Number(k.o),
    high: Number(k.h),
    low: Number(k.l),
    close: Number(k.c),
  };
}

export function connectExchange(symbol) {
  const sym = symbol.toLowerCase();
  const streams = `${sym}@trade/${sym}@kline_1m/${sym}@depth5@100ms`;
  const url = `wss://stream.binance.com:9443/stream?streams=${streams}`;

  const emitter = createEmitter();
  let ws;
  let closed = false;
  let lastPrice = 0;

  try {
    ws = new WebSocket(url);
  } catch (e) {
    // Likely blocked environment; fallback to mock
    return mockFeed(emitter);
  }

  ws.onopen = () => {
    // ok
  };

  ws.onmessage = (ev) => {
    try {
      const data = JSON.parse(ev.data);
      if (!data || !data.stream || !data.data) return;
      const stream = data.stream;
      const payload = data.data;
      if (stream.endsWith('@trade')) {
        const price = Number(payload.p);
        lastPrice = price || lastPrice || 0;
        emitter.emit('price', { price: lastPrice });
        emitter.emit('trade', { time: payload.T, price, quantity: Number(payload.q), side: payload.m ? 'sell' : 'buy' });
      } else if (stream.includes('@kline')) {
        emitter.emit('kline', toKlineFromBinance(payload));
      } else if (stream.includes('@depth')) {
        const bids = payload.bids.slice(0, 10).map(([p,q]) => [Number(p), Number(q)]);
        const asks = payload.asks.slice(0, 10).map(([p,q]) => [Number(p), Number(q)]);
        emitter.emit('orderbook', { bids, asks });
      }
    } catch {}
  };

  ws.onerror = () => {
    // Fallback to mock on error
    try { ws.close(); } catch {}
    if (!closed) return mockFeed(emitter);
  };

  ws.onclose = () => {
    if (!closed) {
      // Try fallback when closed unexpectedly
      mockFeed(emitter);
    }
  };

  function close() {
    closed = true;
    try { ws && ws.close(); } catch {}
  }

  return { emitter, close };
}

function mockFeed(emitter) {
  let t = Date.now();
  let price = 50000 + Math.random() * 40000;
  let open = price, high = price, low = price, close = price;
  const interval = 1000; // 1s ticks
  const handlers = new Set();

  const timer = setInterval(() => {
    t += interval;
    const drift = (Math.random() - 0.5) * 100;
    price = Math.max(100, price + drift);
    high = Math.max(high, price);
    low = Math.min(low, price);
    close = price;
    emitter.emit('price', { price });
    emitter.emit('trade', { time: t, price, quantity: Math.random() * 0.5, side: drift >= 0 ? 'buy' : 'sell' });

    if (t % 60000 === 0) {
      const candle = { time: Math.floor(t / 1000), open, high, low, close };
      emitter.emit('kline', candle);
      open = close; high = close; low = close;
    }

    const bids = Array.from({ length: 10 }, (_, i) => [price - i * 15 - Math.random() * 5, Math.random() * 0.8 + 0.01]);
    const asks = Array.from({ length: 10 }, (_, i) => [price + i * 15 + Math.random() * 5, Math.random() * 0.8 + 0.01]);
    emitter.emit('orderbook', { bids, asks });
  }, interval);

  function close() { clearInterval(timer); }
  return { emitter, close };
}