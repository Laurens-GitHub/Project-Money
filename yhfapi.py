import os
import requests

YHFAPI_KEY = os.environ['YHFAPI_KEY']

def get_stock_data(symbol):
    """Gets quote data by symbol from Rapid API"""
    url = "https://yh-finance.p.rapidapi.com/stock/v2/get-summary"
    query = {"symbol": symbol, "region": "US"}
    yhf_headers = {'x-rapidapi-host': "yh-finance.p.rapidapi.com", 'x-rapidapi-key': YHFAPI_KEY}
    stock_quote = requests.request("GET", url, headers=yhf_headers, params=query)

    if stock_quote.raise_for_status():
        return stock_quote.raise_for_status()
    else:
        return stock_quote

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
    url = "https://yh-finance.p.rapidapi.com/market/v2/get-quotes"
    tech_query = {"symbols":"^NDX,AAPL,MSFT,GOOGL,AMZN,NVDA,META", "region": "US"}
    yhf_headers = {'x-rapidapi-host': "yh-finance.p.rapidapi.com", 'x-rapidapi-key': YHFAPI_KEY}
    tech_json = requests.request("GET", url, headers=yhf_headers, params=tech_query)

    return tech_json.json()
