const root = document.getElementById("root");
const smaLegend = document.getElementById("smaLegend");
const realtimeButton = document.getElementById("go-to-realtime-button");


var candle = require('./candle.json'); 
var volumes = require('./vol.json'); 

/////////////////////////////////////// CHART CONFIGURATION
const chartConfig = {
  width: 1900,
  height: 870,
  timeScale: {
    timeVisible: true,
    secondsVisible: false,
    borderColor: "#D1D4DC",
  },
  rightpriceScale: {
    scaleMargins: {
      top: 0.2,
      bottom: 0.25,
    },
    mode: 1,
	  borderColor: 'rgba(197, 203, 206, 0.8)',
    borderVisible: false,
  },
  leftPriceScale: {
		visible: false,
    borderColor: 'rgba(197, 203, 206, 1)',
	},
  handleScale: {
    axisPressedMouseMove: {
      time: true,
      price: true,
    }
  },
  layout: {
    backgroundColor: "#131722",
    textColor: "#d1d4dc",
  },
  grid: {
    vertLines: {
      color: "rgba(42, 46, 57, 0)",
      style: LightweightCharts.LineStyle.Dotted,
    },
    horzLines: {
      color: "rgba(42, 46, 57, 0.6)",
      style: LightweightCharts.LineStyle.Dotted,
    },
  },
  crosshair: {
    mode: LightweightCharts.CrosshairMode.Normal,
},
};

/////////////////////////////////////// CHART CREATION
const chart = LightweightCharts.createChart(root, chartConfig);

/////////////////////////////////////// CANDLES
//let candlestickSeries = null;
candlestickSeries = chart.addCandlestickSeries({ priceScaleId: 'right' });
candlestickSeries.setData(candle)

/////////////////////////////////////// ADD VOLUME
const volumeStudiesVolumeSeries = chart.addHistogramSeries({
  color: "#26a69a",
  priceFormat: {
    type: "volume",
  },
  priceScaleId: "",
  scaleMargins: {
    top: 0.8,
    bottom: 0,
  },
});

const toggleVolumeBars = toggleShow(volumeStudiesVolumeSeries, volumes);
toggleVolumeBars();

/////////////////////////////////////// SMA
const smaLine = chart.addLineSeries({
	color: 'rgba(4, 111, 232, 1)',
	lineWidth: 2,
});

// const toggleSMALegend = () => smaLegend.classList.toggle("--hidden");
// let toggleSMA = toggleShow(SMAData, [], false, toggleSMALegend);

// toggleSMA = toggleShow(SMAData, json, false, toggleSMALegend);
// toggleSMA();

// setLegendText(smaLegend, json[json.length - 1].value);

// chart.subscribeCrosshairMove((param) => {
//   setLegendText(smaLegend, param.seriesPrices.get(SMAData));
// });


/////////////////////////////////////// GOTO REAL-TIME BUTTON
chart.timeScale().scrollToPosition(-200000, false);
const timeScale = chart.timeScale();
timeScale.subscribeVisibleTimeRangeChange(() => {
	const buttonVisible = timeScale.scrollPosition() < 0;
	realtimeButton.style.display = buttonVisible ? 'block' : 'none';
});

/////////////////////////////////////// LISTENERS FOR BUTTONS

realtimeButton.addEventListener('click', () => {
	timeScale.scrollToRealTime();
}); 

realtimeButton.addEventListener('mouseover', () => {
	realtimeButton.style.background = 'rgba(250, 250, 250, 1)';
	realtimeButton.style.color = '#000';
});

realtimeButton.addEventListener('mouseout', () => {
	realtimeButton.style.background = 'rgba(250, 250, 250, 0.6)';
	realtimeButton.style.color = '#4c525e';
});

const toggleYAxisFormat = changeYAxisFormat(chart);
document.getElementById("y-axis").addEventListener("click", () => {
    toggleYAxisFormat();
});
document.getElementById("toggle-volume-bars").addEventListener("click", () => {
  toggleVolumeBars();
});

document.getElementById("toggle-sma-1").addEventListener("click", () => {
  toggleSMA();
});



