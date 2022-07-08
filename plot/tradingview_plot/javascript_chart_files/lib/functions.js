// switcher functions
function createSimpleSwitcher(items, activeItem, activeItemChangedCallback) {
	var switcherElement = document.createElement('div');
	switcherElement.classList.add('switcher');

	var intervalElements = items.map(function(item) {
		var itemEl = document.createElement('button');
		itemEl.innerText = item;
		itemEl.classList.add('switcher-item');
		itemEl.classList.toggle('switcher-active-item', item === activeItem);
		itemEl.addEventListener('click', function() {
			onItemClicked(item);
		});
		switcherElement.appendChild(itemEl);
		return itemEl;
	});

	function onItemClicked(item) {
		if (item === activeItem) {
			return;
		}
		intervalElements.forEach(function(element, index) {
			element.classList.toggle('switcher-active-item', items[index] === item);
		});
		activeItem = item;
		activeItemChangedCallback(item);
	}
	return switcherElement;
}

function setLegendText(legend, priceValue) {
  let val = "n/a";
  if (priceValue !== undefined) {
    val = (Math.round(priceValue * 100) / 100).toFixed(2);
  }
  legend.innerHTML = 'MA10 <span style="color:rgba(4, 111, 232, 1)">' + val + "</span>";
}












// custom functions
function changeYAxisFormat(chart) {
  let flag = 2;
  return () => {
    flag = flag === 1 ? 2 : 1;
    chart.applyOptions({
      priceScale: {
          mode: flag,
      },
    });
  }
}






function toggleShow(series, data, initialState, callback = () => null){
  let state = false;
  if (initialState !== undefined) state = !initialState;
  return () => {
    state = !state;
    if (!state) {
      series.setData([]);
    } else {
      series.setData(data);
    }
    callback();
  }
}