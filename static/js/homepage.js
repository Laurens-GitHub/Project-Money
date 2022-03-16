function getSummary() {

    fetch("/market_summary.json")
    //requests "/cards.json" from our server, which returns
    // the cards as a json object
      .then((response) => response.json())
      //waits for a response, in json format
      .then((data) => insertCardData(data));
      //takes the json that is returned, and passes it into the insertCardData function
  }

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