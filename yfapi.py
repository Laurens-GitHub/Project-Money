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
RAPID_KEY = os.environ['RAPID_KEY']
NEWS_KEY = os.environ['NEWS_KEY']
NEWS_KEY2 = os.environ['NEWS_KEY2']

def get_chart_data(symbol):
    """Gets stock chart data by symbol"""
    price_url = f'https://yfapi.net/v8/finance/chart/{symbol}'
    price_query = {"range": "1d", "interval": "1m"}
    headers = {'X-API-KEY': STOCKS_KEY}
    price_hist = requests.request("GET", price_url, headers=headers, params=price_query)
    price_json = price_hist.json()

    return price_json
