"""CRUD operations."""

from model import db, User, Stock, UserStock, connect_to_db
import datetime
import pytz
from pytz import timezone

#TODO: configure date into MM/DD/YY format
today = datetime.datetime.now(pytz.timezone('America/New_York'))

#=======================================#
###############   USERS   ###############
#=======================================#

def create_user(first_name, last_name, email, password):
    """Create and return a new user."""

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password
    )

    return user

def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


#=======================================#
###############   STOCKS   ##############
#=======================================#

def create_stock(symbol, company):
    """Create and return a new stock."""

    stock = Stock(
        symbol=symbol,
        company=company
    )

    return stock

def get_stocks():
    """Return all stocks."""

    return Stock.query.all()

def get_stock_by_id(stock_id):
    """Return a stock by its id."""

    return Stock.query.get(stock_id)

def get_stock_by_symbol(symbol):
    """Return a stock by its symbol."""

    stock_by_symbol = Stock.query.filter(Stock.symbol == symbol).first()
    if stock_by_symbol:
        return stock_by_symbol
    else:
        return None

#=======================================#
############   USER STOCKS   ############
#=======================================#

def create_user_stock(user_id, stock_id, date_saved=today):
    """Create and return a new user stock."""
    user_stock = UserStock(
            user_id=user_id,
            stock_id=stock_id,
            date_saved=date_saved
    )

    return user_stock

def get_user_stocks(user_id):
    """Return a user's saved stocks."""

    saved_stocks= UserStock.query.filter(UserStock.user_id == user_id).all()

    return saved_stocks

def delete_user_stock(user_id, stock_id):
    """Delete a user's saved stocks."""

    deleted_stock = UserStock.query.filter(user_id=user_id, stock_id=stock_id).first()

    return deleted_stock

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
