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
NEWS_KEY = os.environ['NEWS_KEY']
NEWS_KEY2 = os.environ['NEWS_KEY2']


#remove in production
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True



# From anlu to Everyone 12:16 PM
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

@app.route('/')
def show_stock_data():
    """Shows stock data"""

    # url = "https://yfapi.net/v6/finance/quote"
    #querystring = {"symbols":"AAPL"}

    quote_url = "https://yfapi.net/v6/finance/quote"
    trending_url = "https://yfapi.net/v1/finance/trending/US"


    trend_query = {"region":"US"}
    quote_query = {"symbols":".INX,.DJI,NDAQ,AAPL,MSFT,GOOGL,AMZN,FB"}

    headers = {'X-API-KEY': STOCKS_KEY}

    trends = requests.request("GET", trending_url, headers=headers, params=trend_query)
    quotes = requests.request("GET", quote_url, headers=headers, params=quote_query)
    trends_json = trends.json()
    quotes_json = quotes.json()

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
                           news_data=top_headlines)

@app.route("/quote")
def get_stock_quote():
    """Show a stock quote data."""
    quote_url = "https://yfapi.net/v6/finance/quote/"
    symbol = request.args.get("search")
    quote_query = {"symbols": symbol }
    headers = {'X-API-KEY': STOCKS_KEY}

    quote = requests.request("GET", quote_url, headers=headers, params=quote_query)
    quote_response = quote.json()
    # AAPL_quote = json_data['quoteResponse']['result'][0]
    # ticker = json_data['quoteResponse']['result'][0]['symbol']
    # stocks = data[symbol]
    # print(data.text)

    if quote_response == {'quoteResponse': {'error': None, 'result': []}}:
        quote_url = "https://yfapi.net/v6/finance/autocomplete"
        query = request.args.get("search")
        quote_query = {"query": query,
                        "lang": 'en' }
        headers = {'X-API-KEY': STOCKS_KEY}

        results = requests.request("GET", quote_url, headers=headers, params=quote_query)
        results_json = results.json()


        return render_template("search-results.html",
                            pformat=pformat,
                            search_results=results_json)


    else:
        return render_template("quote.html",
                                pformat=pformat,
                                quote=quote_response)


# @app.route("/search")
# def show_search_results():
#     """Show stock search results"""





# @app.route("/movies/<movie_id>")
# def show_movie(movie_id):
#     """Show details on a particular movie."""

#     movie = crud.get_movie_by_id(movie_id)

#     return render_template("movie_details.html", movie=movie)


# @app.route("/users")
# def all_users():
#     """View all users."""

#     users = crud.get_users()

#     return render_template("all_users.html", users=users)


@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

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


@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""

    user = crud.get_user_by_id(user_id)

    return render_template("user_stocks.html", user=user)


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
        flash(f"Welcome back, {user.email}!")

    return redirect("/")


# @app.route("/movies/<movie_id>/ratings", methods=["POST"])
# def create_rating(movie_id):
#     """Create a new rating for the movie."""

#     logged_in_email = session.get("user_email")
#     rating_score = request.form.get("rating")

#     if logged_in_email is None:
#         flash("You must log in to rate a movie.")
#     elif not rating_score:
#         flash("Error: you didn't select a score for your rating.")
#     else:
#         user = crud.get_user_by_email(logged_in_email)
#         movie = crud.get_movie_by_id(movie_id)

#         rating = crud.create_rating(user, movie, int(rating_score))
#         db.session.add(rating)
#         db.session.commit()

#         flash(f"You rated this movie {rating_score} out of 5.")

#     return redirect(f"/movies/{movie_id}")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)