"""Script to seed database."""

import os
import json
from copy import deepcopy
from random import choice
import datetime
import pytz
from pytz import timezone

import crud
import model
from model import Stock
import server

os.system('dropdb market')
os.system('createdb market')

model.connect_to_db(server.app)
model.db.create_all()

today = datetime.datetime.now(pytz.timezone('America/New_York'))


# Load stock data from txt file
stock_data = open('data/Sample_stocks.txt')

stocks_in_db = []
for line in stock_data:
    line = line.rstrip()
    data = line.split(',')

    symbol, company = (
        data[0],
        data[1]
    )
    db_stock = crud.create_stock(symbol, company)
    stocks_in_db.append(db_stock)

model.db.session.add_all(stocks_in_db)
model.db.session.commit()


for n in range(5):
    first_name = f'John'
    last_name = f'Doe {n}'
    email = f'user{n}@test.com'
    password = 'test'

#create a user
    user = crud.create_user(first_name, last_name, email, password)
    model.db.session.add(user)

    # save 10 stocks for the user
    unique_stocks = Stock.query.all()

    for _ in range (10):
        print(user)
        random_stock = choice(unique_stocks)
        date_saved = today.strftime("%m/%d/%y")
        print(random_stock)
        print(unique_stocks)
        print(model.db.session)

        user_stock = crud.create_user_stock(user.user_id, random_stock.stock_id, date_saved)
        model.db.session.add(user_stock)
        unique_stocks.remove(random_stock)


model.db.session.commit()