"""CRUD operations."""

from model import db, User, Stock, User_stock, connect_to_db

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

    return Stock.query.filter(Stock.symbol == symbol).first()

#=======================================#
############   USER STOCKS   ############
#=======================================#

def create_user_stock(user, stock, date_saved):
    """Create and return a new user stock."""

    user_stock = User_stock(
            user=user,
            stock=stock,
            date_saved=date_saved
    )

    return user_stock

def get_user_stocks(user_id):
    """Return a user's saved stocks."""

    return User_stock.query.filter(User_stock.user_id == user_id).all()


# def get_movie_by_id(movie_id):
#     """Return a movie by primary key."""

#     return Movie.query.get(movie_id)

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
