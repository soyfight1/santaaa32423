export function initChart(root) {
  const chart = LightweightCharts.createChart(root, {
    layout: { background: { type: 'solid', color: 'transparent' }, textColor: '#d8e1ea' },
    rightPriceScale: { borderVisible: false },
    timeScale: { borderVisible: false },
    grid: { vertLines: { color: 'rgba(255,255,255,0.06)' }, horzLines: { color: 'rgba(255,255,255,0.06)' } },
    width: root.clientWidth,
    height: root.clientHeight,
    autoSize: true,
  });

  const series = chart.addCandlestickSeries({
    upColor: '#7cf08a', downColor: '#ff7f7f', borderVisible: false, wickUpColor: '#7cf08a', wickDownColor: '#ff7f7f'
  });

  const candles = new Map();

  function updateCandle(k) {
    candles.set(k.time, k);
    series.update(k);
  }

  function setData(arr) { series.setData(arr); }

  return { updateCandle, setData };
}