"""Server for Ticker app."""

import os
from pprint import pformat
from flask import Flask, render_template, request, flash, session, redirect
import requests
from model import connect_to_db, db
import crud
import yhfapi
import parser
import market_news
from jinja2 import StrictUndefined
import datetime
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined
YHFAPI_KEY = os.environ['YHFAPI_KEY']
NEWS_KEY = os.environ['NEWS_KEY']

#TODO: remove in production
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

    summary_json = yhfapi.get_market_summary()

    return summary_json

@app.route('/trending_stocks.json')
def send_trending_stocks():
    """Sends data for trending stocks"""

    trends_json = yhfapi.get_trending()

    return trends_json

@app.route('/big_tech.json')
def send_tech_stocks():
    """Sends data for major tech stocks"""

    tech_json = yhfapi.get_big_tech()

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
        return format(num)
    else:
        return num

@app.route('/quote')
def get_stock_quote():
    """Show a stock quote data."""

    symbol = request.args.get('symbol')
    quote_data = parser.get_asset_dic(symbol)
    return render_template('stock.html',
                            quote_data=quote_data,
                            pformat=pformat)

                            # symbol=asset_quote.get('symbol'),
                            # company=asset_quote.get('company'),
                            # curr_price=asset_quote.get('curr_price'),
                            # dollar_chg=asset_quote.get('dollar_chg'),
                            # pct_chg=asset_quote.get('pct_chg'),
                            # prev_close=asset_quote.get('prev_close'),
                            # open_price=asset_quote.get('open_price'),
                            # ask_price=asset_quote.get('ask_price'),
                            # bid_price=asset_quote.get('bid_price'),
                            # day_high=asset_quote.get('day_high'),
                            # day_low=asset_quote.get('day_low'),
                            # year_high=asset_quote.get('year_high'),
                            # year_low=asset_quote.get('year_low'),
                            # volume=asset_quote.get('volume'),
                            # pe_ratio=asset_quote.get('pe_ratio'),
                            # eps=asset_quote.get('eps'),
                            # market_cap=asset_quote.get('market_cap'),
                            # curr_date=asset_quote.get('curr_date'),
                            # curr_time=asset_quote.get('curr_time'),



@app.route('/price_chart.json')
def send_chart_data():
    """Sends chart data by ticker"""
    symbol = request.args.get('symbol')
    chart = yhfapi.get_chart_data(symbol)
    return chart

@app.route('/stock_data.json')
def send_stock_data():
    """Sends stock data by ticker"""
    symbol = request.args.get('symbol')
    quote = yhfapi.get_stock_data(symbol)
    return quote

#=======================================#
###############   USERS   ###############
#=======================================#

@app.route('/users', methods=['POST'])
def register_user():
    """Register a new user."""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(first_name, last_name, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect('/')


@app.route('/saved')
def show_user():
    """Show the a user's saved stocks."""

    logged_in_user = session.get('user_id')
    user_stocks = crud.get_user_stocks(logged_in_user)

    return render_template('user-stocks.html', stocks=user_stocks)


@app.route('/login', methods=['POST'])
def process_login():
    """Process user login."""

    email = request.form.get('login-email')
    password = request.form.get('login-pass')

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session['user_email'] = user.email
        session['user_id'] = user.user_id
        flash(f'Welcome back, {user.first_name}!')

    return redirect('/')

@app.route('/logoff', methods=['POST'])
def process_logout():
    """Process user logout."""

    session['user_email'] = []
    session['user_id'] = []
    flash("You've been logged out")

    return redirect('/')


@app.route('/favorites', methods=['POST'])
def create_user_stock():
    """Create a new saved stock for the user."""

    logged_in_email = session.get('user_email')
    company = request.form.get('company')
    new_symbol = request.form.get('symbol')
    user = crud.get_user_by_email(logged_in_email)
    check_stock = crud.get_stock_by_symbol(new_symbol)

    if logged_in_email is None:
        flash('You must log in to save a stock.')

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
        flash(f'You saved {company} to your favorites.')

#check if this stock is already in our database:

    elif check_stock.symbol == new_symbol:

#if it is, just create the user stock:
        stock_id = check_stock.stock_id
        user_id = user.user_id
        fav_stock = crud.create_user_stock(user_id, stock_id)
        db.session.add(fav_stock)
        db.session.commit()
        flash(f'You saved {company} to your favorites.')

# TODO: Change this return statement so that the user stays on the same page, or change the flash to an alert box.
    return redirect('/')

@app.route('/user_profile', methods=['GET', 'POST'])
def show_user_favorites():
    """Return a user's favorite stocks"""
    logged_in_email = session.get('user_email')
    user = crud.get_user_by_email(logged_in_email)
    faves = crud.get_user_stocks(user.user_id)

#TODO: fix this conditional, the template is showing the wrong thing
    print(faves)
    if faves is None:

        return render_template('/user-profile.html', saved_stocks=None)

    else:
        user_stocks_by_id = []
        saved_stocks = {}
        our_user = user.first_name
        for count, value in enumerate(faves):
            user_stocks_by_id.append(faves[count].stock_id)
        for count, value in enumerate(user_stocks_by_id):
            stock = crud.get_stock_by_id(value)
            saved_stocks[stock.symbol] = stock.company, faves[count].date_saved

        return render_template('/user-profile.html', saved_stocks=saved_stocks, our_user=our_user)

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
