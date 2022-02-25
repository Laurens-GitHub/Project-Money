"use strict";

const quoteData = document.querySelector("pre").innerHTML

(async () => {
    const rawResponse = await fetch('/favorites', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(quote_data)
    });
    const content = await rawResponse.json();

    console.log(content);
  })();
