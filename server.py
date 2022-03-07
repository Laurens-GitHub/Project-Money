"""Server for stock market app."""

from flask import Flask, render_template, request, flash, session, redirect
from pprint import pformat
import os
import requests
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
import http.client, urllib.parse
from newsapi import NewsApiClient

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
STOCKS_KEY = os.environ['YAHOO_KEY']
RAPID_KEY = os.environ['RAPID_KEY']
NEWS_KEY = os.environ['NEWS_KEY']
NEWS_KEY2 = os.environ['NEWS_KEY2']


#remove in production
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True



# From anlu
# # Write a yfapi.py module that would make the following code work, and then
# # use this module in server.py in the appropriate places
# from yfapi import YFAPIClient

# yf_client = YFAPIClient(STOCKS_KEY)

# # for getting quotes
# quotes = yf_client.quotes(".INX,.DJI,NDAQ,AAPL,MSFT,GOOGL,AMZN,FB")

# # for getting trends
# trends = yf_client.trends()  # this can have a default region argument of "US"

# # for getting autocomplete
# quotes = yf_client.autocomplete("XXX")

#=======================================#
##############   HOMEPAGE   #############
#=======================================#

@app.route('/')
def show_stock_data():
    """Shows stock data"""

    # url = "https://yfapi.net/v6/finance/quote"
    #querystring = {"symbols":"AAPL"}

    quote_url = "https://yfapi.net/v6/finance/quote"
    trending_url = "https://yfapi.net/v1/finance/trending/US"
    summary_url = "https://yfapi.net/v6/finance/quote/marketSummary"

    trend_query = {"region":"US"}
    quote_query = {"symbols":".INX,NDAQ,AAPL,MSFT,GOOGL,AMZN,FB"}
    summary_query = {"lang":"en", "region":"US"}

    headers = {'X-API-KEY': STOCKS_KEY}

    trends = requests.request("GET", trending_url, headers=headers, params=trend_query)
    quotes = requests.request("GET", quote_url, headers=headers, params=quote_query)
    summary = requests.request("GET", summary_url, headers=headers, params=summary_query)
    trends_json = trends.json()
    quotes_json = quotes.json()
    summary_json = summary.json()

    # conn = http.client.HTTPSConnection('api.marketaux.com')

    # params = urllib.parse.urlencode({
    #     'api_token': NEWS_KEY2,
    #     'symbols': 'AAPL,TSLA',
    #     'limit': 3,
    #     })

    # conn.request('GET', '/v1/news/all?{}'.format(params))

    # res = conn.getresponse()
    # news = res.read()
    # print(type(news))

    # data = requests.request("GET", url, headers=headers, params=querystring)
    newsapi = NewsApiClient(NEWS_KEY)
    top_headlines = newsapi.get_top_headlines(
                                          category='business',
                                          country='us',
                                          language='en'
                                                                                    )

    return render_template('homepage.html',
                           pformat=pformat,
                           quote_data=quotes_json,
                           trend_data=trends_json,
                           summary_data=summary_json,
                           news_data=top_headlines)


#=======================================#
###############   QUOTES   ##############
#=======================================#

@app.route("/quote")
def get_stock_quote():
    """Show a stock quote data."""
    quote_url = "https://yfapi.net/v6/finance/quote/"
    rapid_url = "https://yh-finance.p.rapidapi.com/stock/v2/get-summary"
    price_url = "https://yfapi.net/v8/finance/spark" #gets price history

    symbol = request.args.get("search")
    quote_query = {"symbols": symbol}
    rapid_query = {"symbol": symbol, "region": "US"}
    price_query = {"symbols": symbol, "range": "1d", "interval": "15m"}
    rapid_headers = {'x-rapidapi-host': "yh-finance.p.rapidapi.com",
    'x-rapidapi-key': RAPID_KEY}
    headers = {'X-API-KEY': STOCKS_KEY}

    quote = requests.request("GET", quote_url, headers=headers, params=quote_query)
    price_hist = requests.request("GET", price_url, headers=headers, params=price_query)
    rapid_quote = requests.request("GET", rapid_url, headers=rapid_headers, params=rapid_query)

    quote_response = quote.json()
    price_response = price_hist.json()
    rapid_response = rapid_quote.json()
    quote_type = quote_response['quoteResponse']['result'][0]['quoteType']


    if quote_response == {'quoteResponse': {'error': None, 'result': []}}:
        quote_url = "https://yfapi.net/v6/finance/autocomplete"
        query = request.args.get("search")
        quote_query = {"query": query,
                        "lang": 'en' }
        headers = {'X-API-KEY': STOCKS_KEY}

        results = requests.request("GET", quote_url, headers=headers, params=quote_query)
        search_results = results.json()

        return render_template("search-results.html",
                            search_results=search_results, pformat=pformat,
                            user_query=query)


# known values for quote_type: "EQUITY", "ETF", "INDEX", "MUTUALFUND", "CURRENCY", "CRYPTOCURRENCY"

#test template

    else:
        return render_template("test.html", pformat=pformat, rapid_json=rapid_response)#quote_json=quote_response)

    # else:

#TODO: add the current price to these asset classes
    # elif quote_type == "EQUITY":

    #     rapid_quote = requests.request("GET", rapid_url, headers=rapid_headers, params=rapid_query)
    #     rapid_response = rapid_quote.json()
    #     symbol = quote_response['quoteResponse']['result'][0]['symbol']
    #     company = quote_response['quoteResponse']['result'][0]['shortName']
    #     dollar_chg = format(quote_response['quoteResponse']['result'][0]['regularMarketChange'], ".2f")
    #     pct_chg = format(quote_response['quoteResponse']['result'][0]['regularMarketChangePercent'], ".2f")
    #     prev_close = format(quote_response['quoteResponse']['result'][0]['regularMarketPreviousClose'], ".2f")
    #     open_price = format(quote_response['quoteResponse']['result'][0]['regularMarketOpen'], ".2f")
    #     ask_price = format(quote_response['quoteResponse']['result'][0]['ask'], ".2f")
    #     bid_price = format(quote_response['quoteResponse']['result'][0]['bid'], ".2f")
    #     day_high = format(quote_response['quoteResponse']['result'][0]['regularMarketDayHigh'], ".2f")
    #     day_low = format(quote_response['quoteResponse']['result'][0]['regularMarketDayLow'], ".2f")
    #     year_high = format(quote_response['quoteResponse']['result'][0]['fiftyTwoWeekHigh'], ".2f")
    #     year_low = format(quote_response['quoteResponse']['result'][0]['fiftyTwoWeekLow'], ".2f")
    #     volume = rapid_response['price']['regularMarketVolume']['fmt']
    #     pe_ratio = format(quote_response['quoteResponse']['result'][0]['trailingPE'], ".2f")
    #     eps = format(quote_response['quoteResponse']['result'][0]['epsTrailingTwelveMonths'], ".2f")
    #     market_cap = rapid_response['price']['marketCap']['fmt']
    #     return render_template("stock.html",
    #                             symbol=symbol,
    #                             company=company,
    #                             dollar_chg=dollar_chg,
    #                             pct_chg=pct_chg,
    #                             prev_close=prev_close,
    #                             open_price=open_price,
    #                             ask_price=ask_price,
    #                             bid_price=bid_price,
    #                             day_high=day_high,
    #                             day_low=day_low,
    #                             year_high=year_high,
    #                             year_low=year_low,
    #                             volume=volume,
    #                             pe_ratio=pe_ratio,
    #                             eps=eps,
    #                             market_cap=market_cap,
    #                             pformat=pformat,
    #                             stock_json=quote_response,
    #                             price_json=price_response
    #                             )

    # elif quote_type == "ETF":
    #     rapid_quote = requests.request("GET", rapid_url, headers=rapid_headers, params=rapid_query)
    #     rapid_response = rapid_quote.json()
    #     symbol = quote_response['quoteResponse']['result'][0]['symbol']
    #     company = quote_response['quoteResponse']['result'][0]['shortName']
    #     dollar_chg = format(quote_response['quoteResponse']['result'][0]['regularMarketChange'], ".2f")
    #     pct_chg = format(quote_response['quoteResponse']['result'][0]['regularMarketChangePercent'], ".2f")
    #     prev_close = format(quote_response['quoteResponse']['result'][0]['regularMarketPreviousClose'], ".2f")
    #     open_price = format(quote_response['quoteResponse']['result'][0]['regularMarketOpen'], ".2f")
    #     ask_price = format(quote_response['quoteResponse']['result'][0]['ask'], ".2f")
    #     bid_price = format(quote_response['quoteResponse']['result'][0]['bid'], ".2f")
    #     day_high = format(quote_response['quoteResponse']['result'][0]['regularMarketDayHigh'], ".2f")
    #     day_low = format(quote_response['quoteResponse']['result'][0]['regularMarketDayLow'], ".2f")
    #     year_high = format(quote_response['quoteResponse']['result'][0]['fiftyTwoWeekHigh'], ".2f")
    #     year_low = format(quote_response['quoteResponse']['result'][0]['fiftyTwoWeekLow'], ".2f")
    #     pe_ratio = format(quote_response['quoteResponse']['result'][0]['trailingPE'], ".2f")
    #     eps = format(quote_response['quoteResponse']['result'][0]['epsTrailingTwelveMonths'], ".2f")
    #     volume = rapid_response['price']['regularMarketVolume']['fmt']
    #     market_cap = rapid_response['price']['marketCap']['fmt']
    #     expense_ratio = rapid_response['fundProfile']['feesExpensesInvestment']['annualReportExpenseRatio']['fmt']
    #     turnover = rapid_response['fundProfile']['feesExpensesInvestment']['annualHoldingsTurnover']['fmt']
    #     fund_style = rapid_response['fundProfile']['categoryName']
    #     return render_template("ETF.html",
    #                             symbol=symbol,
    #                             company=company,
    #                             dollar_chg=dollar_chg,
    #                             pct_chg=pct_chg,
    #                             prev_close=prev_close,
    #                             open_price=open_price,
    #                             ask_price=ask_price,
    #                             bid_price=bid_price,
    #                             day_high=day_high,
    #                             day_low=day_low,
    #                             year_high=year_high,
    #                             year_low=year_low,
    #                             volume=volume,
    #                             pe_ratio=pe_ratio,
    #                             eps=eps,
    #                             market_cap=market_cap,
    #                             expense_ratio=expense_ratio,
    #                             turnover=turnover,
    #                             fund_style=fund_style,
    #                             pformat=pformat,
    #                             ETF_json=quote_response,
    #                             price_json=price_response
    #                             )

    # elif quote_type == "INDEX":
    #     return render_template("index.html", pformat=pformat, index_json=quote_response, price_json=price_response)

    # elif quote_type == "MUTUALFUND":
    #     return render_template("fund.html", pformat=pformat, fund_json=quote_response, price_json=price_response)

    # elif quote_type == "CURRENCY":
    #     symbol = quote_response['quoteResponse']['result'][0]['symbol']
    #     company = quote_response['quoteResponse']['result'][0]['shortName']
    #     dollar_chg = format(quote_response['quoteResponse']['result'][0]['regularMarketChange'], ".2f")
    #     pct_chg = format(quote_response['quoteResponse']['result'][0]['regularMarketChangePercent'], ".2f")
    #     prev_close = format(quote_response['quoteResponse']['result'][0]['regularMarketPreviousClose'], ".2f")
    #     open_price = format(quote_response['quoteResponse']['result'][0]['regularMarketOpen'], ".2f")
    #     ask_price = format(quote_response['quoteResponse']['result'][0]['ask'], ".2f")
    #     bid_price = format(quote_response['quoteResponse']['result'][0]['bid'], ".2f")
    #     day_high = format(quote_response['quoteResponse']['result'][0]['regularMarketDayHigh'], ".2f")
    #     day_low = format(quote_response['quoteResponse']['result'][0]['regularMarketDayLow'], ".2f")
    #     year_high = format(quote_response['quoteResponse']['result'][0]['fiftyTwoWeekHigh'], ".2f")
    #     year_low = format(quote_response['quoteResponse']['result'][0]['fiftyTwoWeekLow'], ".2f")
    #     return render_template("currency.html",
    #                             symbol=symbol,
    #                             company=company,
    #                             dollar_chg=dollar_chg,
    #                             pct_chg=pct_chg,
    #                             prev_close=prev_close,
    #                             open_price=open_price,
    #                             ask_price=ask_price,
    #                             bid_price=bid_price,
    #                             day_high=day_high,
    #                             day_low=day_low,
    #                             year_high=year_high,
    #                             year_low=year_low,
    #                             pformat=pformat,
    #                             currency_json=quote_response,
    #                             price_json=price_response)

    # elif quote_type == "CRYPTOCURRENCY":
    #     rapid_quote = requests.request("GET", rapid_url, headers=rapid_headers, params=rapid_query)
    #     rapid_response = rapid_quote.json()
    #     symbol = rapid_response['assetProfile']['price']['symbol']
    #     company = rapid_response['assetProfile']['price']['shortName']
    #     curr_price = rapid_response['assetProfile']['price']['regularMarketPrice']['fmt']
    #     dollar_chg = rapid_response['assetProfile']['price']['regularMarketChange']['fmt']
    #     pct_chg = rapid_response['assetProfile']['price']['regularMarketChangePercent']['fmt']
    #     24hr_high = rapid_response['assetProfile']['price']['dayHigh']['fmt']
    #     24hr_low = rapid_response['assetProfile']['price']['dayLow']['fmt']
    #     year_high = rapid_response['assetProfile']['price']['fiftyTwoWeekHigh']['fmt']
    #     year_low = rapid_response['assetProfile']['price']['fiftyTwoWeekLow']['fmt']
    #     market_cap = format(rapid_response['assetProfile']['price']['marketCap']['fmt']:g)
    #     24hr_volume = format(rapid_response['assetProfile']['price']['volume24Hr']['longFmt']:g)
    #     circulating = format(rapid_response['assetProfile']['summaryDetail']['circulatingSupply']['longFmt']:g)
    #     return render_template("crypto.html",
    #                             symbol=symbol,
    #                             company=company,
    #                             curr_price=curr_price,
    #                             dollar_chg=dollar_chg,
    #                             pct_chg=pct_chg,
    #                             24hr_high=24hr_high,
    #                             24hr_low=24hr_low,
    #                             year_high=year_high,
    #                             year_low=year_low,
    #                             market_cap=market_cap,
    #                             24hr_volume=24hr_volume,
    #                             circulating=circulating,
    #                             pformat=pformat,
    #                             crypto_json=rapid_response,
    #                             price_json=price_response)



#=======================================#
###############   USERS   ###############
#=======================================#

@app.route("/users", methods=["POST"])
def register_user():
    """Register a new user."""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(first_name, last_name, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")


@app.route("/saved")
def show_user():
    """Show the a user's saved stocks."""

    logged_in_user = session.get("user_id")
    user_stocks = crud.get_user_stocks(logged_in_user)

    return render_template("user-stocks.html", stocks=user_stocks)


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("login-email")
    password = request.form.get("login-pass")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        session["user_id"] = user.user_id
        flash(f"Welcome back, {user.first_name}!")

    return redirect("/")

@app.route("/logoff", methods=["POST"])
def process_logout():
    """Process user logout."""

    session["user_email"] = []
    session["user_id"] = []
    flash(f"You've been logged out")

    return redirect("/")


@app.route("/favorites", methods=["POST"])
def create_user_stock():
    """Create a new saved stock for the user."""

    logged_in_email = session.get("user_email")
    company = request.form.get("company")
    new_symbol = request.form.get("symbol")
    user = crud.get_user_by_email(logged_in_email)
    check_stock = crud.get_stock_by_symbol(new_symbol)

    if logged_in_email is None:
        flash("You must log in to save a stock.")

#if this stock doesn't already exist in our database,
#add it using the quote info:
    elif check_stock is None:
        symbol = new_symbol
        new_stock = crud.create_stock(symbol, company)
        db.session.add(new_stock)
        db.session.commit()
#and add the user stock:
        created_stock = crud.get_stock_by_symbol(symbol)
        stock_id = created_stock.stock_id
        user_id = user.user_id
        fav_stock = crud.create_user_stock(user_id, stock_id)
        db.session.add(fav_stock)
        db.session.commit()
        flash(f"You saved {company} to your favorites.")

#check if this stock is already in our database:

    elif check_stock.symbol == new_symbol:

#if it is, just create the user stock:
        stock_id = check_stock.stock_id
        user_id = user.user_id
        fav_stock = crud.create_user_stock(user_id, stock_id)
        db.session.add(fav_stock)
        db.session.commit()
        flash(f"You saved {company} to your favorites.")



    return redirect("/")



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)