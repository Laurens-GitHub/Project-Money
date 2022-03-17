//////////  SUMMARY  \\\\\\\\\\\\\\

function getSummary() {

    fetch("/market_summary.json")
      .then((response) => response.json())
      //waits for a response, in json format
      .then((data) => insertSummaryData(data));
      //takes the json that is returned, and passes it into the insertCardData function
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
        pctChange =  indexes[i]['regularMarketChangePercent']['fmt']
      );
    }
  };
  const createSummaryAndAddToContainer = (market, price, change, pctChange) => {
    const cardElement = document.createElement("div");
    cardElement.classList.add("card");
    cardElement.innerHTML = `
        <p>${market}</p>
        <p>${price}</p>
        <p>${change}</p>
        <p>${pctChange}</p>
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

    const trendingStocks = response['finance']['result'][0]['quotes'];
    const container = document.querySelector("#trending");
    container.innerHTML = "";

    for (let i=0; i<trendingStocks.length; i++) {
      createTrendAndAddToContainer(
      trender = trendingStocks[i]['symbol']
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

    const techStocks = response['quoteResponse']['result'];
    const container = document.querySelector("#big-tech");
    container.innerHTML = "";

    for (let i=0; i<techStocks.length; i++) {
        createStockAndAddToContainer(
        symbol = techStocks[i]['symbol'],
        price = techStocks[i]['regularMarketPrice'],
        change = techStocks[i]['regularMarketChange'],
        pct_change = techStocks[i]['regularMarketChangePercent']
        );
    }
    };
    const createStockAndAddToContainer = (symbol, price, change, pctChange) => {
        const cardElement = document.createElement("div");
        cardElement.classList.add("card");
        cardElement.innerHTML = `
            <p>${symbol}</p>
            <p>${price}</p>
            <p>${change}</p>
            <p>${pctChange}</p>
            `;
    document.querySelector("#big-tech").append(cardElement);
};

////////////  MARKET NEWS  \\\\\\\\\\\\\\

function getNews() {
    fetch("/market_news.json")
    .then((response) => response.json())
    .then((data) => insertNewsData(data));

    };
    const insertNewsData = (response) => {

        const newsData = response['articles'];
        const container = document.querySelector("#articles");
        container.innerHTML = "";

        // trim the source name from the end of the title
        for (let i=0; i<newsData.length; i++) {
            if (newsData[i]['title'].indexOf(" - ")) {
                title = newsData[i]['title'].split(' - ')[0]
            } else {
                title = newsData[i]['title']
            }
            createArticleAndAddToContainer(
            title,
            description = newsData[i]['description'],
            link = newsData[i]['url'],
            imageUrl = newsData[i]['urlToImage'],
            source = newsData[i]['source']['name']
            );
        }
    };

    const createArticleAndAddToContainer = (title, description, link, imageUrl, source) => {
        const cardElement = document.createElement("div");
        cardElement.classList.add("card");
        cardElement.innerHTML = `
                <div class="col-xs-12 col-sm-6 col-md-6 col-lg-4 article-summary mt-3">
                    <div class="card text-center bg-light">
                    <a href="${link}" target="_blank" rel="noopener noreferrer">
                        <img class="card-img-top img-circle" src="${imageUrl}">
                    </a>
                    <div class="article-body">
                        <h5 class="article-title"><a href="${link}" target="_blank" rel="noopener noreferrer">${title}</a></h5>
                        <div class="article-source">${source}</div>
                        <a class="article-description" href="${link}" target="_blank" rel="noopener noreferrer">${description}</a>
                    </div>
                    </div>
                </div>
        </div>
            `;
    document.querySelector("#articles").append(cardElement);
};