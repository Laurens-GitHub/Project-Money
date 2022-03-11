"use strict";

fetch('/price_chart.json')
  .then(response => response.json())
  .then(responseJson => {
      // .map is another way to loop. It applies a function to every item in an iterable
      // In this case, we're creating a new JS object for every item in the list dailyTotal
    const data = responseJson.data.map(dailyTotal => ({
      x: dailyTotal.date,
      y: dailyTotal.melons_sold,
    }));

    new Chart(document.querySelector('#line-time'), {
      type: 'line',
      data: {
        datasets: [
          {
            label: 'All Melons',
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