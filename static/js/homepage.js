function getSummary() {

    fetch("/market_summary.json")

      .then((response) => response.json())
      //waits for a response, in json format
      .then((data) => insertSummaryData(data));
      //takes the json that is returned, and passes it into the insertCardData function
  }
  const insertSummaryData = (response) => {
    // Once the data has been provided by the server,
    // insert it into the page as an HTML string.
    const indexes = response['marketSummaryResponse']['result'];

    const container = document.querySelector("#summary");

    // empty the container so it has no content
    container.innerHTML = "";

    for (const currentCard of listOfCards) {
      if (!currentCard.imgUrl) {
        currentCard.imgUrl = "/static/img/placeholder.png";
      }
      createCardAndAddToContainer(
        currentCard.name,
        currentCard.skill,
        currentCard.imgUrl
      );
    }
  };
  const createCardAndAddToContainer = (name, skill, imgUrl) => {
    const cardElement = document.createElement("div");
    cardElement.classList.add("card");
    cardElement.innerHTML = `
        <p>Name: ${name}</p>
        <img src='${imgUrl}'>
        <p>Skill: ${skill} </p>
    `;
    document.querySelector("#container").append(cardElement);
  };