"""Script to seed database."""

import os
import json
from random import choice
import datetime

import crud
import model
import server

os.system("dropdb market")
os.system('createdb market')

model.connect_to_db(server.app)
model.db.create_all()

today = datetime.datetime.now()


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
    for _ in range (10):
        random_stock = choice(stocks_in_db)
        date_saved = today.strftime("%m/%d/%y")
        user_stock = crud.create_user_stock(user, random_stock, date_saved)
        model.db.session.add(user_stock)

model.db.session.commit()