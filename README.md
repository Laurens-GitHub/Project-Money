![](static/img/Ticker_Logo_Trans.png)
# Ticker
This application shows market news, major stock indexes, and trending stocks.

# Description
For staying updated on market news and popular stocks. You can search for domestic and international stocks, bonds, ETFs, mutual funds, cryptocurrencies, and FX rates. Users can save and track their favorite securites.

# Tech Stack
**Backend:** Python 3, PostgreSQL, Flask, SQLAlchemy, Jinja
**Frontend:** JavaScript, jQuery, HTML 5, CSS 3, Bootstrap
**APIs:** [Yahoo Finance API](https://www.yahoofinanceapi.com), [YH Finance AP](https://rapidapi.com/apidojo/api/yh-finance), [News API](https://newsapi.org/)

# Installation
**Prerequisites**
Python3 and pip3 should be installed on the target machine. API keys for [Yahoo Finance API](https://www.yahoofinanceapi.com), [YH Finance API](https://rapidapi.com/apidojo/api/yh-finance), and [News API](https://newsapi.org/) are required.

**How to run Ticker**
Clone this repo:
```git clone https://github.com/Laurens-GitHub/Ticker.git```

Create a virtual environment (Optional):
```
pip3 install virtualenv
virtualenv env
source env/bin/activate
```

Install all dependencies:
```
pip3 install -r requirements.txt
```

Place your API keys in a secrets.sh file:
```
export YAHOO_KEY="your Yahoo API key"
export RAPID_KEY="your YH Finance API key"
export NEWS_KEY="your News API key"
```

Create the database:
```
createdb markets
python3 seed_database.py
```

Initiate the server locally with `python3 server.py`

# About the Author
[Lauren Edwards](https://github.com/Laurens-GitHub) is a software engineer based in New York City. Her love of economics and personal finance led her to build Ticker as her capstonce project for Hackbright academy