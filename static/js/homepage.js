function getSummary() {

    fetch("/market_summary.json")

      .then((response) => response.json())
      //waits for a response, in json format
      .then((data) => insertSummaryData(data));
      //takes the json that is returned, and passes it into the insertCardData function
    //    console.log("function has run")
    //   debugger;
    };
  const insertTrendingData = (response) => {
    // Once the data has been provided by the server,
    // insert it into the page as an HTML string.
    const indexes = response['marketSummaryResponse']['result'];
    console.log("attempting insert")
    const container = document.querySelector("#summary");

    // empty the container so it has no content
    container.innerHTML = "";

    for (let i=0; i<indexes.length; i++) {

      createCardAndAddToContainer(
      market = indexes[i].get(['shortName'], '-'),
      price = indexes[i].get(['regularMarketPrice']['fmt'], '-'),
      change = indexes[i].get(['regularMarketChange']['fmt'], '-'),
      pct_change =  indexes[i].get(['regularMarketChangePercent']['fmt'], '-')
      );
    }
  };
  const createCardAndAddToContainer = (market, price, change, pct_change) => {
    const cardElement = document.createElement("div");
    cardElement.classList.add("card");
    cardElement.innerHTML = `
        <p>${market}</p>
        <p>${price}</p>
        <p>${change}</p>
        <p>${pct_change}</p>
    `;
    document.querySelector("#summary").append(cardElement);
  };


// TRENDING

function getTrending() {
    fetch("/trending_stocks.json")

      .then((response) => response.json())
      //waits for a response, in json format
      .then((data) => insertTrendData(data));
      //takes the json that is returned, and passes it into the insertCardData function
    //    console.log("function has run")
    //   debugger;
    };
  const insertTrendData = (response) => {
    // Once the data has been provided by the server,
    // insert it into the page as an HTML string.
    const trending_stocks = response['finance']['result']['quotes'];
    console.log("attempting insert")
    debugger;
    const container = document.querySelector("#trending");

    // empty the container so it has no content
    container.innerHTML = "";

    for (let i=0; i<indexes.length; i++) {

      createTrendAndAddToContainer(
      market = indexes[i].get(['shortName'], '-'),
      price = indexes[i].get(['regularMarketPrice']['fmt'], '-'),
      change = indexes[i].get(['regularMarketChange']['fmt'], '-'),
      pct_change =  indexes[i].get(['regularMarketChangePercent']['fmt'], '-')
      );
    }
  };
  const createTrendAndAddToContainer = (market, price, change, pct_change) => {
    const cardElement = document.createElement("div");
    cardElement.classList.add("card");
    cardElement.innerHTML = `
        <p>${market}</p>
        <p>${price}</p>
        <p>${change}</p>
        <p>${pct_change}</p>
    `;
    document.querySelector("#trending").append(cardElement);
};