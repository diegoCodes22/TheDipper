from DbManager import *


db = DbManager("../TWS1/watchlist.db")
ticker_list = db.select_all()
for ticker in ticker_list:
    print(ticker[''])
