//////////  SUMMARY  \\\\\\\\\\\\\\

function getSummary() {

    fetch("/market_summary.json")
      .then((response) => response.json())
      //waits for a response, in json format
      .then((data) => insertSummaryData(data));
      //takes the json that is returned, and passes it into the insertCardData function
    //    console.log("function has run")
    //   debugger;
    };
  const insertSummaryData = (response) => {
    // Once the data has been provided by the server,
    // insert it into the page as an HTML string.
    const indexes = response['marketSummaryResponse']['result'];
    console.log("attempting insert")
    const container = document.querySelector("#summary");
    // empty the container so it has no content
    container.innerHTML = "";

    for (let i=0; i<indexes.length; i++) {
        if (indexes[i]['shortName'] == undefined) {
            market = indexes[i]['exchange']
        } else {
            market = indexes[i]['shortName']
        }
        createSummaryAndAddToContainer(
        market,
        price = indexes[i]['regularMarketPrice']['fmt'],
        change = indexes[i]['regularMarketChange']['fmt'],
        pct_change =  indexes[i]['regularMarketChangePercent']['fmt']
      );
    }
  };
  const createSummaryAndAddToContainer = (market, price, change, pct_change) => {
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

////////////  TRENDING  \\\\\\\\\\\\\\

function getTrending() {
    fetch("/trending_stocks.json")
      .then((response) => response.json())
      .then((data) => insertTrendData(data));

    };
  const insertTrendData = (response) => {

    const trending_stocks = response['finance']['result'][0]['quotes'];
    const container = document.querySelector("#trending");
    container.innerHTML = "";

    for (let i=0; i<trending_stocks.length; i++) {
      createTrendAndAddToContainer(
      trender = trending_stocks[i]['symbol']
      );
    }
  };
    const createTrendAndAddToContainer = (trender) => {
        const cardElement = document.createElement("div");
        cardElement.classList.add("card");
        cardElement.innerHTML = `
            <p>${trender}</p>

            `;
    document.querySelector("#trending").append(cardElement);
};

////////////  MAJOR TECH  \\\\\\\\\\\\\\

function getBigTech() {
    fetch("/big_tech.json")
      .then((response) => response.json())
      .then((data) => insertTechData(data));

    };
  const insertTechData = (response) => {

    const tech_stocks = response['quoteResponse']['result'];
    const container = document.querySelector("#big-tech");
    container.innerHTML = "";

    for (let i=0; i<tech_stocks.length; i++) {
        createStockAndAddToContainer(
        symbol = tech_stocks[i]['symbol'],
        price = tech_stocks[i]['regularMarketPrice'],
        change = tech_stocks[i]['regularMarketChange'],
        pct_change = tech_stocks[i]['regularMarketChangePercent']
        );
    }
    };
    const createStockAndAddToContainer = (symbol, price, change, pct_change) => {
        const cardElement = document.createElement("div");
        cardElement.classList.add("card");
        cardElement.innerHTML = `
            <p>${symbol}</p>
            <p>${price}</p>
            <p>${change}</p>
            <p>${pct_change}</p>
            `;
    document.querySelector("#big-tech").append(cardElement);
};

////////////  MARKET NEWS  \\\\\\\\\\\\\\

