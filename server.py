"""Server for Ticker app."""

import os
from pprint import pformat
from flask import Flask, render_template, request, flash, session, redirect
import requests
from model import connect_to_db, db
import crud
import yfapi
import market_news
from jinja2 import StrictUndefined
import datetime
from datetime import datetime

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
STOCKS_KEY = os.environ['YAHOO_KEY']
RAPID_KEY = os.environ['RAPID_KEY']
NEWS_KEY = os.environ['NEWS_KEY']

#remove in production
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True

#=======================================#
##############   HOMEPAGE   #############
#=======================================#
@app.route('/')
def show_stock_data():
    """Shows the homepage"""

    return render_template('homepage.html')

@app.route('/market_summary.json')
def send_market_summary():
    """Sends major index data"""

    summary_json = yfapi.get_market_summary()

    return summary_json

@app.route('/trending_stocks.json')
def send_trending_stocks():
    """Sends data for trending stocks"""

    trends_json = yfapi.get_trending()

    return trends_json

@app.route('/big_tech.json')
def send_tech_stocks():
    """Sends data for major tech stocks"""

    tech_json = yfapi.get_big_tech()

    return tech_json

@app.route('/market_news.json')
def send_market_news():
    """Sends data for latest US business news"""

    news_json = market_news.get_news()

    return news_json

#=======================================#
###############   QUOTES   ##############
#=======================================#
def two_decimal_formatter(num):
    """Formats numbers to two trailing decimal places"""
    if isinstance(num, (int, float)):
        result = format(num)
        return result
    else:
        return num

@app.route("/quote")
def get_stock_quote():
    """Show a stock quote data."""
    symbol = request.args.get("search")
    quote_response = yfapi.get_stock_data(symbol)
    date_time = datetime.now()

# if we don't get anything back, use the autocomplete route
    if quote_response == {'quoteResponse': {'error': None, 'result': []}}:
        quote_url = "https://yfapi.net/v6/finance/autocomplete"
        query = request.args.get("search")
        quote_query = {"query": query,
                        "lang": 'en' }
        headers = {'X-API-KEY': STOCKS_KEY}
        results = requests.request("GET", quote_url, headers=headers, params=quote_query)
        search_json = results.json()
        search_results = search_json['ResultSet'].get('Result')


        return render_template("search-results.html", search_results=search_results,
                            search_json=search_json, pformat=pformat,
                            user_query=query)

# if the symbol is a Future, quit early, send to later.html
    elif "." in symbol:
        return render_template("later.html")

# if the symbol is found, make the API call
    elif quote_response:
        #create dictionary from
        yahoo_quote = {
            "curr_date": date_time.strftime("%d/%m/%Y"),
            "curr_time": date_time.strftime("%H:%M:%S"),
            "quote_type": quote_response['quoteResponse']['result'][0].get('quoteType'),
            "symbol": quote_response['quoteResponse']['result'][0].get('symbol'),
            "company": quote_response['quoteResponse']['result'][0].get('shortName'),
            "curr_price": two_decimal_formatter(quote_response['quoteResponse']['result'][0].get('regularMarketPrice')),
            "dollar_chg": two_decimal_formatter(quote_response['quoteResponse']['result'][0].get('regularMarketChange')),
            "pct_chg": two_decimal_formatter(quote_response['quoteResponse']['result'][0].get('regularMarketChangePercent')),
            "prev_close": two_decimal_formatter(quote_response['quoteResponse']['result'][0].get('regularMarketPreviousClose')),
            "open_price": two_decimal_formatter(quote_response['quoteResponse']['result'][0].get('regularMarketOpen')),
            "ask_price": two_decimal_formatter(quote_response['quoteResponse']['result'][0].get('ask')),
            "bid_price": two_decimal_formatter(quote_response['quoteResponse']['result'][0].get('bid')),
            "day_high": two_decimal_formatter(quote_response['quoteResponse']['result'][0].get('regularMarketDayHigh')),
            "day_low": two_decimal_formatter(quote_response['quoteResponse']['result'][0].get('regularMarketDayLow')),
            "year_high": two_decimal_formatter(quote_response['quoteResponse']['result'][0].get('fiftyTwoWeekHigh')),
            "year_low": two_decimal_formatter(quote_response['quoteResponse']['result'][0].get('fiftyTwoWeekLow')),
            "pe_ratio": two_decimal_formatter(quote_response['quoteResponse']['result'][0].get('trailingPE')),
            "eps": two_decimal_formatter(quote_response['quoteResponse']['result'][0].get('epsTrailingTwelveMonths'))
        }

        rapid_response = yfapi.get_rapid_api_data(symbol)

        if yahoo_quote['quote_type'] == "EQUITY":
            rapid_quote = {
                "market_cap": rapid_response['price']['marketCap'].get('fmt', '-'),
                "volume": rapid_response['price']['regularMarketVolume'].get('fmt'),
            }

        elif yahoo_quote['quote_type'] == "ETF":
            rapid_quote = {
                "fund_expense_ratio": rapid_response['fundProfile']['feesExpensesInvestment']['annualReportExpenseRatio'].get('fmt', '-'),
                "fund_style": rapid_response['fundProfile'].get('categoryName', '-'),
                "fund_turnover": rapid_response['fundProfile']['feesExpensesInvestment']['annualHoldingsTurnover'].get('fmt', '-'),
                "market_cap": rapid_response['price']['marketCap'].get('fmt', '-'),
                "volume": rapid_response['price']['regularMarketVolume'].get('fmt', '-'),
            }

        elif yahoo_quote['quote_type'] == "CRYPTOCURRENCY":
            rapid_quote = {
                "24_day_high": rapid_response['price']['regularMarketDayHigh'].get('fmt'), #24hour figure
                "24_day_low": rapid_response['price']['regularMarketDayLow'].get('fmt'), #24hour figure
                "circulating": rapid_response['summaryDetail']['circulatingSupply'].get('longFmt'),
                "company_short": rapid_response['price'].get('shortName'),
                "curr_price": rapid_response['price']['regularMarketPrice'].get('fmt'),
                "day_volume": rapid_response['price']['volume24Hr'].get('longFmt'), #24hour figure
                "dollar_chg": rapid_response['price']['regularMarketChange'].get('fmt'),
                "market_cap": rapid_response['price']['marketCap'].get('fmt', '-'),
                "pct_chg": rapid_response['price']['regularMarketChangePercent'].get('fmt'),
                "symbol": rapid_response['price'].get('symbol'),
                "year_high": rapid_response['summaryDetail']['fiftyTwoWeekHigh'].get('fmt'),
                "year_low": rapid_response['summaryDetail']['fiftyTwoWeekLow'].get('fmt'),
            }

        elif yahoo_quote['quote_type'] == "MUTUALFUND":
            rapid_quote = {
                "company_long": rapid_response['price'].get('longName'),
                "day_high": rapid_response['price']['regularMarketDayHigh'].get('fmt'),
                "day_low": rapid_response['price']['regularMarketDayLow'].get('fmt'),
                "expense_ratio": rapid_response['defaultKeyStatistics']['annualReportExpenseRatio'].get('fmt', '-'),
                "holdings": rapid_response['topHoldings'].get('holdings'),
                #"inception": rapid_response['defaultKeyStatistics']['fundInceptionDate'].get('fmt'),
                "prev_close": rapid_response['price']['regularMarketPreviousClose'].get('fmt'),
                "rating": rapid_response['defaultKeyStatistics']['morningStarOverallRating'].get('fmt'),
                "return_yield": rapid_response['summaryDetail']['yield'].get('fmt'),
                "risk": rapid_response['defaultKeyStatistics']['morningStarRiskRating'].get('fmt'),
                "symbol": rapid_response.get('symbol'),
                "total_assets": rapid_response['defaultKeyStatistics']['totalAssets'].get('fmt'),
                "turnover": rapid_response['defaultKeyStatistics']['annualHoldingsTurnover'].get('fmt', '-'),
                "ytd_return": rapid_response['summaryDetail']['ytdReturn'].get('fmt')
            }

        yahoo_quote.update(rapid_quote)

        return render_template("stock.html",
                                symbol=yahoo_quote.get('symbol'),
                                company=yahoo_quote.get('company'),
                                curr_price=yahoo_quote.get('curr_price'),
                                dollar_chg=yahoo_quote.get('dollar_chg'),
                                pct_chg=yahoo_quote.get('pct_chg'),
                                prev_close=yahoo_quote.get('prev_close'),
                                open_price=yahoo_quote.get('open_price'),
                                ask_price=yahoo_quote.get('ask_price'),
                                bid_price=yahoo_quote.get('bid_price'),
                                day_high=yahoo_quote.get('day_high'),
                                day_low=yahoo_quote.get('day_low'),
                                year_high=yahoo_quote.get('year_high'),
                                year_low=yahoo_quote.get('year_low'),
                                volume=yahoo_quote.get('volume'),
                                pe_ratio=yahoo_quote.get('pe_ratio'),
                                eps=yahoo_quote.get('eps'),
                                market_cap=yahoo_quote.get('market_cap'),
                                curr_date=yahoo_quote.get('curr_date'),
                                curr_time=yahoo_quote.get('curr_time'),
                                pformat=pformat,
                                stock_json=quote_response)


# #test template

#     else:
#         return render_template("test.html", pformat=pformat, quote_json=quote_response)#rapid_json=rapid_response)







#     quote_url = "https://yfapi.net/v6/finance/quote/"

#     symbol = request.args.get("search")
#     quote_query = {"symbols": symbol}
#     headers = {'X-API-KEY': STOCKS_KEY}
#     quote = requests.request("GET", quote_url, headers=headers, params=quote_query)
#     quote_response = quote.json()
#     date_time = datetime.now()
#     curr_date = date_time.strftime("%d/%m/%Y")
#     curr_time = date_time.strftime("%H:%M:%S")

# # known values for quote_type: "ECNQUOTE", "EQUITY", "ETF", "FUTURE", "INDEX", "MUTUALFUND", "CURRENCY", "CRYPTOCURRENCY"

#     if quote_response == {'quoteResponse': {'error': None, 'result': []}}:
#         quote_url = "https://yfapi.net/v6/finance/autocomplete"
#         query = request.args.get("search")
#         quote_query = {"query": query,
#                         "lang": 'en' }
#         headers = {'X-API-KEY': STOCKS_KEY}
#         results = requests.request("GET", quote_url, headers=headers, params=quote_query)
#         search_json = results.json()
#         search_results = search_json['ResultSet'].get('Result')


#         return render_template("search-results.html", search_results=search_results,
#                             search_json=search_json, pformat=pformat,
#                             user_query=query)

#     elif "." in symbol:
#         return render_template("later.html")


# #test template

#     # else:
#     #     return render_template("test.html", pformat=pformat, quote_json=quote_response)#rapid_json=rapid_response)

#     else:
#         quote_type = quote_response['quoteResponse']['result'][0].get('quoteType']
#         rapid_url = "https://yh-finance.p.rapidapi.com/stock/v2/get-summary"
#         rapid_query = {"symbol": symbol, "region": "US"}
#         rapid_headers = {'x-rapidapi-host': "yh-finance.p.rapidapi.com", 'x-rapidapi-key': RAPID_KEY}
#         rapid_quote = requests.request("GET", rapid_url, headers=rapid_headers, params=rapid_query)
#         rapid_response = rapid_quote.json()

#         if quote_type == 'ECNQUOTE':
#             quote_url = "https://yfapi.net/v6/finance/autocomplete"
#             query = request.args.get("search")
#             quote_query = {"query": query,
#                             "lang": 'en' }
#             headers = {'X-API-KEY': STOCKS_KEY}

#             results = requests.request("GET", quote_url, headers=headers, params=quote_query)
#             search_results = results.json()


#             return render_template("search-results.html",
#                                 search_results=search_results, pformat=pformat,
#                                 user_query=query)

#         elif quote_type == "EQUITY":

#             symbol = quote_response['quoteResponse']['result'][0].get('symbol']
#             company = quote_response['quoteResponse']['result'][0].get('shortName']
#             curr_price = format(quote_response['quoteResponse']['result'][0].get('regularMarketPrice'))
#             dollar_chg = format(quote_response['quoteResponse']['result'][0].get('regularMarketChange'))
#             pct_chg = format(quote_response['quoteResponse']['result'][0].get('regularMarketChangePercent'))
#             prev_close = format(quote_response['quoteResponse']['result'][0].get('regularMarketPreviousClose'))
#             open_price = format(quote_response['quoteResponse']['result'][0].get('regularMarketOpen'))
#             ask_price = format(quote_response['quoteResponse']['result'][0].get('ask'))
#             bid_price = format(quote_response['quoteResponse']['result'][0].get('bid'))
#             day_high = format(quote_response['quoteResponse']['result'][0].get('regularMarketDayHigh'))
#             day_low = format(quote_response['quoteResponse']['result'][0].get('regularMarketDayLow'))
#             year_high = format(quote_response['quoteResponse']['result'][0].get('fiftyTwoWeekHigh'))
#             year_low = format(quote_response['quoteResponse']['result'][0].get('fiftyTwoWeekLow'))
#             volume = rapid_response['price']['regularMarketVolume']['fmt']
#             pe_ratio = quote_response['quoteResponse']['result'][0].get('trailingPE', '-')
#             pe_ratio = two_decimal_formatter(pe_ratio)
#             eps = quote_response['quoteResponse']['result'][0].get('epsTrailingTwelveMonths', '-')
#             eps = two_decimal_formatter(eps)
#             market_cap = rapid_response['price']['marketCap'].get('fmt', '-')
#             market_cap = two_decimal_formatter(market_cap)
#             return render_template("stock.html",
#                                     symbol=symbol,
#                                     company=company,
#                                     curr_price=curr_price,
#                                     dollar_chg=dollar_chg,
#                                     pct_chg=pct_chg,
#                                     prev_close=prev_close,
#                                     open_price=open_price,
#                                     ask_price=ask_price,
#                                     bid_price=bid_price,
#                                     day_high=day_high,
#                                     day_low=day_low,
#                                     year_high=year_high,
#                                     year_low=year_low,
#                                     volume=volume,
#                                     pe_ratio=pe_ratio,
#                                     eps=eps,
#                                     market_cap=market_cap,
#                                     curr_date=curr_date,
#                                     curr_time=curr_time,
#                                     pformat=pformat,
#                                     stock_json=quote_response)

#         elif quote_type == "ETF":
#             symbol = quote_response['quoteResponse']['result'][0].get('symbol']
#             company = quote_response['quoteResponse']['result'][0].get('shortName']
#             curr_price = format(quote_response['quoteResponse']['result'][0].get('regularMarketPrice'))
#             dollar_chg = format(quote_response['quoteResponse']['result'][0].get('regularMarketChange'))
#             pct_chg = format(quote_response['quoteResponse']['result'][0].get('regularMarketChangePercent'))
#             prev_close = format(quote_response['quoteResponse']['result'][0].get('regularMarketPreviousClose'))
#             open_price = format(quote_response['quoteResponse']['result'][0].get('regularMarketOpen'))
#             ask_price = format(quote_response['quoteResponse']['result'][0].get('ask'))
#             bid_price = format(quote_response['quoteResponse']['result'][0].get('bid'))
#             day_high = format(quote_response['quoteResponse']['result'][0].get('regularMarketDayHigh'))
#             day_low = format(quote_response['quoteResponse']['result'][0].get('regularMarketDayLow'))
#             year_high = format(quote_response['quoteResponse']['result'][0].get('fiftyTwoWeekHigh'))
#             year_low = format(quote_response['quoteResponse']['result'][0].get('fiftyTwoWeekLow'))
# #TODO: format values to 2 decimal places
#             pe_ratio = quote_response['quoteResponse']['result'][0].get('trailingPE', '-')
#             eps = quote_response['quoteResponse']['result'][0].get('epsTrailingTwelveMonths', '-')
#             volume = rapid_response['price']['regularMarketVolume'].get('fmt', '-')
#             market_cap = rapid_response['price']['marketCap'].get('fmt', '-')
#             expense_ratio = rapid_response['fundProfile']['feesExpensesInvestment']['annualReportExpenseRatio'].get('fmt', '-')
#             turnover = rapid_response['fundProfile']['feesExpensesInvestment']['annualHoldingsTurnover'].get('fmt', '-')
#             fund_style = rapid_response['fundProfile'].get('categoryName', '-')
#             return render_template("ETF.html",
#                                     symbol=symbol,
#                                     company=company,
#                                     curr_price=curr_price,
#                                     dollar_chg=dollar_chg,
#                                     pct_chg=pct_chg,
#                                     prev_close=prev_close,
#                                     open_price=open_price,
#                                     ask_price=ask_price,
#                                     bid_price=bid_price,
#                                     day_high=day_high,
#                                     day_low=day_low,
#                                     year_high=year_high,
#                                     year_low=year_low,
#                                     volume=volume,
#                                     pe_ratio=pe_ratio,
#                                     eps=eps,
#                                     market_cap=market_cap,
#                                     expense_ratio=expense_ratio,
#                                     turnover=turnover,
#                                     fund_style=fund_style,
#                                     pformat=pformat,
#                                     ETF_json=quote_response, rapid_json=rapid_response)

#         elif quote_type == "INDEX":
#             symbol = quote_response['quoteResponse']['result'][0].get('symbol']
#             company = quote_response['quoteResponse']['result'][0].get('shortName']
#             curr_price = format(quote_response['quoteResponse']['result'][0].get('regularMarketPrice'))
#             dollar_chg = format(quote_response['quoteResponse']['result'][0].get('regularMarketChange'))
#             pct_chg = format(quote_response['quoteResponse']['result'][0].get('regularMarketChangePercent'))
#             open_price = format(quote_response['quoteResponse']['result'][0].get('regularMarketOpen'))
#             prev_close = format(quote_response['quoteResponse']['result'][0].get('regularMarketPreviousClose'))
#             day_high = format(quote_response['quoteResponse']['result'][0].get('regularMarketDayHigh'))
#             day_low = format(quote_response['quoteResponse']['result'][0].get('regularMarketDayLow'))
#             year_high = format(quote_response['quoteResponse']['result'][0].get('fiftyTwoWeekHigh'))
#             year_low = format(quote_response['quoteResponse']['result'][0].get('fiftyTwoWeekLow'))
#             return render_template("index.html",
#                                     symbol=symbol,
#                                     company=company,
#                                     curr_price=curr_price,
#                                     dollar_chg=dollar_chg,
#                                     pct_chg=pct_chg,
#                                     open_price=open_price,
#                                     prev_close=prev_close,
#                                     day_high=day_high,
#                                     day_low=day_low,
#                                     year_high=year_high,
#                                     year_low=year_low,
#         pformat=pformat, index_json=quote_response)

#         elif quote_type == "MUTUALFUND":
#             symbol = rapid_response['symbol']
#             company = rapid_response['price']['longName']
#             curr_price = rapid_response['price']['regularMarketPrice']['fmt']
#             dollar_chg = rapid_response['price']['regularMarketChange']['fmt']
#             pct_chg = rapid_response['price']['regularMarketChangePercent']['fmt']
#             prev_close = rapid_response['price']['regularMarketPreviousClose']['fmt']
#             year_high = rapid_response['summaryDetail']['fiftyTwoWeekHigh']['fmt']
#             year_low = rapid_response['summaryDetail']['fiftyTwoWeekLow']['fmt']
#             ytd_return = rapid_response['summaryDetail']['ytdReturn']['fmt']
#             expense_ratio = rapid_response['defaultKeyStatistics']['annualReportExpenseRatio'].get('fmt', '-')
#             total_assets = rapid_response['defaultKeyStatistics']['totalAssets']['fmt']
#             fund_style = rapid_response['fundProfile'].get('categoryName', '-')
#             return_yield = rapid_response['summaryDetail']['yield']['fmt']
#             turnover = rapid_response['defaultKeyStatistics']['annualHoldingsTurnover'].get('fmt', '-')
#             rating = rapid_response['defaultKeyStatistics']['morningStarOverallRating']['fmt']
#             risk = rapid_response['defaultKeyStatistics']['morningStarRiskRating']['fmt']
#             inception = rapid_response['defaultKeyStatistics']['fundInceptionDate']['fmt']
#             holdings = rapid_response['topHoldings']['holdings']
#             return render_template("fund.html",
#                                     symbol=symbol,
#                                     company=company,
#                                     curr_price=curr_price,
#                                     dollar_chg=dollar_chg,
#                                     pct_chg=pct_chg,
#                                     prev_close=prev_close,
#                                     year_high=year_high,
#                                     year_low=year_low,
#                                     ytd_return=ytd_return,
#                                     expense_ratio=expense_ratio,
#                                     total_assets=total_assets,
#                                     fund_style=fund_style,
#                                     return_yield=return_yield,
#                                     turnover=turnover,
#                                     rating=rating,
#                                     risk=risk,
#                                     inception=inception,
#                                     holdings=holdings,
#                                     pformat=pformat,
#                                     fund_json=rapid_response)

#         elif quote_type == "CURRENCY":
#             symbol = quote_response['quoteResponse']['result'][0].get('symbol']
#             company = quote_response['quoteResponse']['result'][0].get('shortName']
#             curr_price = format(quote_response['quoteResponse']['result'][0].get('regularMarketPrice'))
#             dollar_chg = format(quote_response['quoteResponse']['result'][0].get('regularMarketChange'))
#             pct_chg = format(quote_response['quoteResponse']['result'][0].get('regularMarketChangePercent'))
#             prev_close = format(quote_response['quoteResponse']['result'][0].get('regularMarketPreviousClose'))
#             open_price = format(quote_response['quoteResponse']['result'][0].get('regularMarketOpen'))
#             ask_price = format(quote_response['quoteResponse']['result'][0].get('ask'))
#             bid_price = format(quote_response['quoteResponse']['result'][0].get('bid'))
#             day_high = format(quote_response['quoteResponse']['result'][0].get('regularMarketDayHigh'))
#             day_low = format(quote_response['quoteResponse']['result'][0].get('regularMarketDayLow'))
#             year_high = format(quote_response['quoteResponse']['result'][0].get('fiftyTwoWeekHigh'))
#             year_low = format(quote_response['quoteResponse']['result'][0].get('fiftyTwoWeekLow'))
#             return render_template("currency.html",
#                                     symbol=symbol,
#                                     company=company,
#                                     curr_price=curr_price,
#                                     dollar_chg=dollar_chg,
#                                     pct_chg=pct_chg,
#                                     prev_close=prev_close,
#                                     open_price=open_price,
#                                     ask_price=ask_price,
#                                     bid_price=bid_price,
#                                     day_high=day_high,
#                                     day_low=day_low,
#                                     year_high=year_high,
#                                     year_low=year_low,
#                                     pformat=pformat,
#                                     currency_json=quote_response)

#         elif quote_type == "CRYPTOCURRENCY":
#             rapid_quote = requests.request("GET", rapid_url, headers=rapid_headers, params=rapid_query)
#             rapid_response = rapid_quote.json()
#             symbol = rapid_response['price']['symbol']
#             company = rapid_response['price']['shortName']
#             curr_price = rapid_response['price']['regularMarketPrice']['fmt']
#             dollar_chg = rapid_response['price']['regularMarketChange']['fmt']
#             pct_chg = rapid_response['price']['regularMarketChangePercent']['fmt']
#             day_high = rapid_response['price']['regularMarketDayHigh']['fmt'] #24hour figure
#             day_low = rapid_response['price']['regularMarketDayLow']['fmt']  #24hour figure
#             year_high = rapid_response['summaryDetail']['fiftyTwoWeekHigh']['fmt']
#             year_low = rapid_response['summaryDetail']['fiftyTwoWeekLow']['fmt']
#             market_cap = rapid_response['price']['marketCap'].get('fmt', '-')
#             day_volume = rapid_response['price']['volume24Hr']['longFmt'] #24hour figure
#             circulating = rapid_response['summaryDetail']['circulatingSupply']['longFmt']
#             return render_template("crypto.html",
#                                     symbol=symbol,
#                                     company=company,
#                                     curr_price=curr_price,
#                                     dollar_chg=dollar_chg,
#                                     pct_chg=pct_chg,
#                                     day_high=day_high,
#                                     day_low=day_low,
#                                     year_high=year_high,
#                                     year_low=year_low,
#                                     market_cap=market_cap,
#                                     day_volume=day_volume,
#                                     circulating=circulating,
#                                     pformat=pformat,
#                                     crypto_json=rapid_response)

#         elif quote_type == "FUTURE":
#                     rapid_quote = requests.request("GET", rapid_url, headers=rapid_headers, params=rapid_query)
#                     rapid_response = rapid_quote.json()
#                     symbol = rapid_response['price']['symbol']
#                     company = rapid_response['price']['shortName']
#                     curr_price = rapid_response['price']['regularMarketPrice']['fmt']
#                     dollar_chg = rapid_response['price']['regularMarketChange']['fmt']
#                     pct_chg = rapid_response['price']['regularMarketChangePercent']['fmt']
#                     day_high = rapid_response['price']['regularMarketDayHigh']['fmt'] #24hour figure
#                     day_low = rapid_response['price']['regularMarketDayLow']['fmt']  #24hour figure
#                     year_high = rapid_response['summaryDetail']['fiftyTwoWeekHigh']['fmt']
#                     year_low = rapid_response['summaryDetail']['fiftyTwoWeekLow']['fmt']
#                     return render_template("future.html",
#                                             symbol=symbol,
#                                             company=company,
#                                             curr_price=curr_price,
#                                             dollar_chg=dollar_chg,
#                                             pct_chg=pct_chg,
#                                             day_high=day_high,
#                                             day_low=day_low,
#                                             year_high=year_high,
#                                             year_low=year_low,
#                                             pformat=pformat,
#                                             future_json=rapid_response)

#         # else:
#         #     # quote_response == {'message': 'Limit Exceeded'}:
#         #     return render_template("limit.html")

@app.route("/price_chart.json")
def send_chart_data():
    """Sends chart data by ticker"""
    symbol = request.args.get("symbol")
    chart = yfapi.get_chart_data(symbol)
    return chart

@app.route("/stock_data.json")
def send_stock_data():
    """Sends stock data by ticker"""
    symbol = request.args.get("symbol")
    quote = yfapi.get_stock_data(symbol)
    return quote



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
    flash("You've been logged out")

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

# TODO: Change this return statement so that the user stays on the same page, or change the flash to an alert box.
    return redirect("/")

@app.route("/user_profile", methods=["GET", "POST"])
def show_user_favorites():
    """Return a user's favorite stocks"""
    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email)
    faves = crud.get_user_stocks(user.user_id)

#TODO: fix this conditional, the template is showing the wrong thing
    print(faves)
    if faves is None:

        return render_template("/user-profile.html", saved_stocks=None)

    else:
        user_stocks_by_id = []
        saved_stocks = {}
        our_user = user.first_name
        for count, value in enumerate(faves):
            user_stocks_by_id.append(faves[count].stock_id)
        for count, value in enumerate(user_stocks_by_id):
           stock = crud.get_stock_by_id(value)
           saved_stocks[stock.symbol] = stock.company, faves[count].date_saved

        return render_template("/user-profile.html", saved_stocks=saved_stocks, our_user=our_user)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)