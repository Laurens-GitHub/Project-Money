"""Models for stock viewing app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"
    # users is a list of User objects

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)


    def __repr__(self):
        return f"""<User id={self.user_id},
    first name={self.first_name},
    last name={self.last_name},
    email={self.email}>"""


class Stock(db.Model):
    """A stock."""

    __tablename__ = "stocks"
    # stocks is a list of Stock objects

    stock_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    symbol = db.Column(db.String, unique=True)
    company = db.Column(db.String)


    def __repr__(self):
        return f"<Stock id={self.stock_id}, symbol={self.symbol}, company={self.company}>"


class User_stock(db.Model):
    """A stock saved by a user."""

    __tablename__ = "user_stocks"

    __table_args__ = (
    db.UniqueConstraint('user_id', 'stock_id', name='unique_user_stock'),)

    user_stock_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey("stocks.stock_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    date_saved = db.Column(db.String)

    stock = db.relationship("Stock", backref="user_stocks")
    user = db.relationship("User", backref="user_stocks")

    def __repr__(self):
        return f"""<User stock id={self.user_stock_id},
    stock id={self.stock_id},
    user={self.user_id},
    date saved={self.date_saved}>"""


def connect_to_db(flask_app, db_uri="postgresql:///market", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
