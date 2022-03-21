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
    const container = document.querySelector("#summary-wrap");
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
    $('#summary').grouploop({forward:false});
  };
  const createSummaryAndAddToContainer = (market, price, change, pctChange) => {
    if (change > 0) {
        priceDirection = "+"
        colorState = "marqueeGreen"
    } else {
        colorState = "marqueeRed"
        priceDirection= ""
    }
    const cardElement = document.createElement("div");
    cardElement.classList.add("item");
    cardElement.innerHTML = `
            <span class="container-fluid justify-content-start"><b>${market}</b> ${price} <span class=${colorState}>${priceDirection}${change}</span><span> </span><span class=${colorState}>${priceDirection}${pctChange}</span>
    `;
    document.querySelector("#summary-wrap").append(cardElement);

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

    for (let i=0; i<10; i++) {
      createTrendAndAddToContainer(
      trender = trendingStocks[i]['symbol']
      );
    }
  };
    const createTrendAndAddToContainer = (trender) => {
        const cardElement = document.createElement("li");
        cardElement.classList.add("trend");
        cardElement.innerHTML = `${generateStockLink(trender)}`;

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
        symbol = generateStockLink(techStocks[i]['symbol']),
        company = techStocks[i]['shortName'],
        price = (Math.round(techStocks[i]['regularMarketPrice'] * 100) / 100).toFixed(2),
        change = (Math.round(techStocks[i]['regularMarketChange'] * 100) / 100).toFixed(2)
        // pct_change = techStocks[i]['regularMarketChangePercent']
        );
    }
    };
    const createStockAndAddToContainer = (symbol, company, price, change) => {
        if (change > 0) {
            priceDirection = "+"
            colorState = "green"
        } else {
            colorState = "red"
            priceDirection= ""
        }

        const cardElement = document.createElement("div");
        cardElement.classList.add("tech-card");
        cardElement.innerHTML = `
        <div class="hstack">
            <div>
                <strong>${symbol}</strong>
            </div>
            <span class="ms-auto">${price}</span>
        </div>

        <div class="hstack">
            <div class="card-subtitle mb-2 text-muted">${company}</div>
            <span class="ms-auto ${colorState}">${priceDirection}${change}</span>
        </div>

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
        cardElement.classList.add("col-md-4");
        cardElement.classList.add("news-card");
        cardElement.innerHTML = `
        <div class="col">
                <div class="card" style="width: 25rem;">
                    <a href="${link}" target="_blank" rel="noopener noreferrer">
                        <h5 class="card-title">${title}</h5>
                            <img class="card-img-top img-circle" src="${imageUrl}">
                        <div class="card-body">
                            <div class="article-source">${source}</div>
                                <p class="card-text">${description}</p>
                            </div>
                        </div>
                    </a>
                </div>
            </div>

            `;
    document.querySelector("#articles").append(cardElement);
};

