"use strict";

document.querySelector("#favorite-button").addEventListener("click", function(event) {
    document.getElementById("favorite-button").innerHTML = `<i class="bi bi-star-fill"></i>`;
    event.preventDefault();
    alert(`You've saved this to your watchlist`);
}, false);

function generateStockLink(symbol) {
    return `<a href="http://localhost:5000/quote?search=${symbol}" target="_blank" rel="noopener noreferrer">${symbol}</a>`
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

    // var canvas = document.getElementById('line-time');
    // var ctx = canvas.getContext("2d");
    // var gradient = ctx.createLinearGradient(0, 0, 0, 400);
    // gradient.addColorStop(0, 'rgba(250,174,50,1)');
    // gradient.addColorStop(1, 'rgba(250,174,50,0)');

    new Chart(document.querySelector('#line-time'), {
        type: 'line',
        data: {
            labels: data['x'],
            datasets: [{
            label: '',
            data: data['y'],
            fill: 1
            }],
        },

        options: {
            plugins: {
                legend: {
                    labels: {
                        boxWidth: 0
                    }
                }
            },
            elements: {
                line:{
                    borderColor: lineColor,
                    borderWidth: 4
                },
                point:{
                    borderColor: lineColor,
                    backgroundColor: lineColor,
                    pointStyle: 'cross',
                    radius: 4
                }
            },
            scales: {
                gridlines: {
                    display: false
                },
                x: {
                    type: 'timeseries',
                    gridlines: {
                        display: true
                    },
                    legend: {
                        labels: {
                            boxWidth: 0,
                        }
                    }
                },

                y: {
                    legend: {
                        labels: {
                            boxWidth: 0,
                        }
                    },

                }
            },
        },

    });

})
};
    //horizontal line

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