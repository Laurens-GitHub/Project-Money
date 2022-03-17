function getSummary() {

    fetch("/market_summary.json")

      .then((response) => response.json())
      //waits for a response, in json format
      .then((data) => insertSummaryData(data));
      //takes the json that is returned, and passes it into the insertCardData function
       console.log("function has run")
      debugger;
    }
  const insertSummaryData = (response) => {
    // Once the data has been provided by the server,
    // insert it into the page as an HTML string.
    const indexes = response['marketSummaryResponse']['result'];

    const container = document.querySelector("#summary");

    // empty the container so it has no content
    container.innerHTML = "";

    for (const index of indexes) {

      createCardAndAddToContainer(
      market = indexes[index]['shortName'],
      price = indexes[index]['regularMarketPrice']['fmt'],
      change =  indexes[index]['regularMarketChange']['fmt'],
      pct_change =  indexes[index]['regularMarketChangePercent']['fmt']
      );
    }
  };
  const createCardAndAddToContainer = (market, price, change, pct_change) => {
    const cardElement = document.createElement("div");
    cardElement.classList.add("card");
    cardElement.innerHTML = `
        <p>'${market}'</p>
        <p>'${price}'</p>
        <p>'${change}' </p>
        <p>'${pct_change}' </p>
    `;
    document.querySelector("#container").append(cardElement);
  };