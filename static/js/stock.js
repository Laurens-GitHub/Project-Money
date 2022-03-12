"use strict";

function renderStockChart(symbol) {

fetch('/price_chart.json'+'?symbol='+symbol)
  .then(response => response.json())
  .then(responseJson => {
    const data = {
      x: responseJson['chart']['result'][0]['timestamp'],
      y: responseJson['chart']['result'][0]['indicators']['quote'][0]['close']
    };

    new Chart(document.querySelector('#line-time'), {
      type: 'line',
      data: {
        datasets: [
          {
            label: 'Price',
            data,
          },
        ],
      },
      options: {
        scales: {
          x: {
            type: 'time',
            time: {
              tooltipFormat: 'LLLL dd', // Luxon format string
              unit: 'day',
            },
          },
        },
      },
    });
  });

}