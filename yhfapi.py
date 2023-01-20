"""Functions for handling requests to the YH Finance API"""
import os
import time
import requests
from requests.exceptions import HTTPError

YHFAPI_KEY = os.environ['YHFAPI_KEY']
YHF_HEADERS = {'x-rapidapi-host': 'yh-finance.p.rapidapi.com', 'x-rapidapi-key': YHFAPI_KEY}

def get_stock_data(symbol, endpoint, key='symbol', retries=2):
    """Gets quote data by symbol from Rapid API

    symbol (str): the symbol to search for, input by the user
    endpoint (str): The Rapid API endpoint to be used
    key (str): the first required parameter for the query string. Commonly "symbol" or "q".
    """

    base = 'https://yh-finance.p.rapidapi.com'
    url = base + endpoint
    query = {key: symbol, 'region': 'US'}

    for i in range(retries):
        try:
            response = requests.request('GET', url, headers=YHF_HEADERS, params=query)
            response.raise_for_status()
        except HTTPError as exc:
            code = exc.response.status_code
            print(f'HTTP CODE {code}. executing retry')
            time.sleep(3)
            continue

            raise

        return response

# def get_chart_data(symbol):
#     """Gets stock chart data by symbol"""
#     price_url = f'https://yhfapi.net/v8/finance/chart/{symbol}'
#     price_query = {"range": "1d", "interval": "1m"}
#     price_hist = requests.request("GET", price_url, headers=HEADERS, params=price_query)
#     price_json = price_hist.json()

#     return price_json

# def get_market_summary():
#     """Gets major index data"""
#     summary_url = "https://yhfapi.net/v6/finance/quote/marketSummary"
#     summary_query = {"lang":"en", "region":"US"}
#     summary = requests.request("GET", summary_url, headers=HEADERS, params=summary_query)
#     summary_json = summary.json()

#     return summary_json

# def get_trending():
#     """Gets major index data"""
#     trending_url = "https://yhfapi.net/v1/finance/trending/US"
#     trend_query = {"region":"US"}
#     trends = requests.request("GET", trending_url, headers=HEADERS, params=trend_query)
#     trends_json = trends.json()

#     return trends_json

def get_big_tech():
    """Gets major tech stocks"""
    url = 'https://yh-finance.p.rapidapi.com/market/v2/get-quotes'
    tech_query = {'symbols':'^NDX,AAPL,MSFT,GOOGL,AMZN,NVDA,META', 'region': 'US'}
    tech_json = requests.request('GET', url, headers=YHF_HEADERS, params=tech_query)

    return tech_json.json()
