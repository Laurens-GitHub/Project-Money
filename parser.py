"""Parses the JSON responses from yhfapi.py"""

import datetime
from datetime import datetime
from yhfapi import get_stock_data

def get_asset_dic(symbol):
    """Returns a dictionary with asset attributes"""
    quote_response = get_stock_data(symbol)
    price_dic = quote_response.get('price', {})
    summ_dic = quote_response.get('summaryDetail', {})
    default_dic = quote_response.get('defaultKeyStatistics', {})
    fund_dic = quote_response.get('fundProfile', {})
    date_time = datetime.now()

# if we've reached our API limit, quit early
    # if quote_response == {'message': 'Limit Exceeded'}:
    #     return render_template('limit.html')

# if we don't get anything back, use the autocomplete route
# TODO: re-write with Alpha API
    # elif quote_response == {'quoteResponse': {'error': None, 'result': []}}:
    #     quote_url = 'https://yhfapi.net/v6/finance/autocomplete'
    #     query = request.args.get('search')
    #     quote_query = {'query': query,
    #                     'lang': 'en' }
    #     headers = {'X-API-KEY': YHFAPI_KEY}
    #     results = requests.request('GET', quote_url, headers=headers, params=quote_query)
    #     search_json = results.json()
    #     search_results = search_json['ResultSet', {}).get('Result')


        # return render_template('search-results.html', search_results=search_results,
        #                     search_json=search_json, pformat=pformat,
        #                     user_query=query)

# if the symbol is found, make the API call
    asset_quote = {
        'curr_date': date_time.strftime('%d/%m/%Y'),
        'curr_time': date_time.strftime('%H:%M:%S'),
        'quote_type': quote_response.get('quoteType', {}).get('quoteType', 'EQUITY'),
        # known values for quote_type: 'CRYPTOCURRENCY', 'EQUITY', 'ETF', 'FUTURE', 'MUTUTALFUND'

        #Equities/Universal
        'stock_symbol': quote_response.get('symbol', symbol),
        'company': price_dic.get('longName', '-'),
        'curr_price': quote_response.get('financialData', {}).get('currentPrice', {}).get('fmt', '-'),
        'dollar_chg': price_dic.get('regularMarketChange', {}).get('fmt', '-'),
        'pct_chg': price_dic.get('regularMarketChangePercent', {}).get('fmt', '-'),
        'prev_close': price_dic.get('regularMarketPreviousClose', {}).get('fmt', '-'),
        'open_price': price_dic.get('regularMarketOpen', {}).get('fmt', '-'),
        'ask_price': summ_dic.get('ask', {}).get('fmt', '-'),
        'bid_price': summ_dic.get('bid', {}).get('fmt', '-'),
        'day_high': price_dic.get('regularMarketDayHigh', {}).get('fmt', '-'),
        'day_low': price_dic.get('regularMarketDayLow', {}).get('fmt', '-'),
        'year_high': summ_dic.get('fiftyTwoWeekHigh', {}).get('fmt', '-'),
        'year_low': summ_dic.get('fiftyTwoWeekLow', {}).get('fmt', '-'),
        # 'pe_ratio': calculate in the template
        'eps': default_dic.get('trailingEps', {}).get('fmt', '-'),
        'market_cap': price_dic.get('marketCap', {}).get('fmt', '-'),
        'volume': price_dic.get('regularMarketVolume', {}).get('fmt', '-'),

        #ETFs (i.e. "QQQ")
        'ETF_curr_price': price_dic.get('regularMarketPrice', {}).get('fmt', '-'),
        'ETF_expense_ratio': fund_dic.get('feesExpensesInvestment', {}).get('annualReportExpenseRatio', {}).get('fmt', '-'),
        'fund_turnover': fund_dic.get('feesExpensesInvestment', {}).get('annualHoldingsTurnover', {}).get('fmt', '-'),
        'fund_style': fund_dic.get('categoryName', '-'),
        'ETF_market_cap': price_dic.get('marketCap', {}).get('fmt', '-'),
        'ETF_volume': price_dic.get('regularMarketVolume', {}).get('fmt', '-'),

# TODO: re-write with Alpha API
        # MUTUAL FUND (i.e. "VFIAX")
        # 'company_long': price_dic.get('longName', '-'),
        # 'MF_curr_price': price_dic.get('regularMarketPrice', {}).get('fmt', '-'),
        # 'MF_day_high': price_dic.get('regularMarketDayHigh', {}).get('fmt', '-'),
        # 'MF_day_low': price_dic.get('regularMarketDayLow', {}).get('fmt', '-'),
        # 'MF_dollar_chg': price_dic.get('regularMarketChange', {}).get('fmt', '-'),
        # 'expense_ratio': default_dic.get('annualReportExpenseRatio', {}).get('fmt', '-'),
        # 'holdings': quote_response.get('topHoldings', {}).get('holdings', '-'),
        # 'inception': default_dic.get('fundInceptionDate', {}).get('raw', '-'),
        # 'MF_pct_chg': price_dic.get('regularMarketChangePercent', {}).get('fmt', '-'),
        # 'MF_prev_close': price_dic.get('regularMarketPreviousClose', {}).get('fmt', '-'),
        # 'rating': default_dic.get('morningStarOverallRating', {}).get('raw', '-'),
        # 'return_yield': summ_dic.get('yield', {}).get('raw', '-'),
        # 'risk': default_dic.get('morningStarRiskRating', {}).get('raw', '-'),
        # 'MF_symbol': quote_response.get('symbol', symbol),
        # 'total_assets': default_dic.get('totalAssets', {}).get('raw', '-'),
        # 'turnover': default_dic.get('annualHoldingsTurnover', {}).get('fmt', '-'),
        # 'MF_year_high': summ_dic.get('fiftyTwoWeekHigh', {}).get('raw', '-'),
        # 'MF_year_low': summ_dic.get('fiftyTwoWeekLow', {}).get('raw', '-'),
        # 'ytd_return': summ_dic.get('ytdReturn', {}).get('raw', '-'),

        #Crypto and Futures (i.e. "BTC-USD" / "CLF23.NYM" - [Crude oil Jan-25, NY Mercantile exchange])
        'crypto_company': price_dic.get('shortName', '-'),
        'circulating': summ_dic.get('circulatingSupply', {}).get('longFmt', '-'),
        'crypto_curr_price': price_dic.get('regularMarketPrice', {}).get('fmt', '-'),
        }


    return asset_quote

# print(get_asset_dic("AAPL"))
