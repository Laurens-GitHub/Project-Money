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

import requests
import os

STOCKS_KEY = os.environ['YAHOO_KEY']
HEADERS = {'X-API-KEY': STOCKS_KEY}

def get_stock_data(symbol):
    """Gets quote data by symbol"""
    quote_url = 'https://yfapi.net/v6/finance/quote/'
    quote_query = {"symbols": symbol}
    quote = requests.request("GET", quote_url, headers=HEADERS, params=quote_query)
    quote_json = quote.json()

    return quote_json

def get_chart_data(symbol):
    """Gets stock chart data by symbol"""
    price_url = f'https://yfapi.net/v8/finance/chart/{symbol}'
    price_query = {"range": "1d", "interval": "1m"}
    price_hist = requests.request("GET", price_url, headers=HEADERS, params=price_query)
    price_json = price_hist.json()

    return price_json

def get_market_summary():
    """Gets major index data"""
    summary_url = "https://yfapi.net/v6/finance/quote/marketSummary"
    summary_query = {"lang":"en", "region":"US"}
    summary = requests.request("GET", summary_url, headers=HEADERS, params=summary_query)
    summary_json = summary.json()

    return summary_json

def get_trending():
    """Gets major index data"""
    trending_url = "https://yfapi.net/v1/finance/trending/US"
    trend_query = {"region":"US"}
    trends = requests.request("GET", trending_url, headers=HEADERS, params=trend_query)
    trends_json = trends.json()

    return trends_json

def get_big_tech():
    """Gets major tech stocks"""
    quote_url = "https://yfapi.net/v6/finance/quote"
    tech_query = {"symbols":"^NDX,AAPL,MSFT,GOOGL,AMZN,NVDA,FB"}
    headers = {'X-API-KEY': STOCKS_KEY}
    quotes = requests.request("GET", quote_url, headers=headers, params=tech_query)
    tech_json = quotes.json()

    return tech_json
