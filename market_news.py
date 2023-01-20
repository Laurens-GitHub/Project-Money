import os
import newsapi
from newsapi import NewsApiClient

NEWS_KEY = os.environ['NEWS_KEY']
HEADERS = {'X-API-KEY': NEWS_KEY}

def get_news():
    """Gets US business news"""
    newsapi = NewsApiClient(NEWS_KEY)
    top_headlines = newsapi.get_top_headlines(
                                          category='business',
                                          country='us',
                                          language='en',
                                          page_size=21)
    return top_headlines