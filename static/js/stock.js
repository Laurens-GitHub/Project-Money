"use strict";

function generateStockLink(symbol) {
    return `<a href="http://localhost:5000/quote?search=${symbol}">${symbol}</a>`
}

function renderStockChart(symbol) {

fetch('/price_chart.json'+'?symbol='+symbol)
  .then(response => response.json())
  .then(responseJson => {

    let timestamps = []
    let unixStamps = responseJson['chart']['result'][0]['timestamp']
    for (const time of unixStamps) {
       const date = new Date(time*1000)
        timestamps.push(date)
    };

    const prevClose = responseJson['chart']['result'][0]['meta']['previousClose']
    let lineColor = "green"
    let closeLength = responseJson['chart']['result'][0]['indicators']['quote'][0]['close']
        if (closeLength[closeLength.length-1] < prevClose) {

            lineColor = "red"
        };

    const data = {
      x: timestamps,
    //   x: responseJson['chart']['result'][0]['timestamp'],
      y: responseJson['chart']['result'][0]['indicators']['quote'][0]['close'],
      close: prevClose
    };


    new Chart(document.querySelector('#line-time'), {
      type: 'line',
      data: {
          labels: data['x'],
          datasets: [{
            label: '',
            data: data['y'],
          },
          {
            label: '',
            data: data['close']
        }
        ],
      },
      options: {

        elements: {
            line:{
                borderColor: lineColor
            },
            point:{
                radius: 1
            }
        },
        scales: {
          x: {
            type: 'timeseries'
          },
          y: {
            stacked: true
          }
        },
      },

    });

    //horizontal line
})
};

// }    new Chart(document.querySelector('#line-time'), {
//         const horizontalLine = {
//             id: 'horizontalLine',
//             beforeDraw(chart, args, options) {
//                 const { ctx, chartArea: {top, right, bottom, left, width, height}, scales:
//             {x, y} } = chart;
//             ctx.save();
//             ctx.strokeStyle = 'blue';
//             ctx.strokeRect(left, data['close'], width, 0)
//             }
//         }
//   }