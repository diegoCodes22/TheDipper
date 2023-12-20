import sqlite3

from TWSIBAPI_MODULES.DataStreams import reqCurrentPrice
from TWSIBAPI_MODULES.Contracts import stock
from TWSIBAPI_MODULES.Orders import place_order
from functions import *
from time import sleep


def dipper(config: AlgoConfig):
    stk = stock(config.SYMBOL)
    current_price = reqCurrentPrice(config.CONN_VARS, stk)
    da = dipper_algo(config, stk, current_price)
    if 0 < da != config.db.select_status(config.SYMBOL):
        if config.RUN_AUTO:
            place_order(config.CONN_VARS, stk, buy(current_price))
            config.db.update_status(config.SYMBOL, da)
            if config.DIP_CALC == "Relative":
                config.db.update_rh(config.SYMBOL, current_price)
            config.db.commit_operation()
        else:
            print(f"Buy {config.SYMBOL} at {current_price}. Dipper algo {da}.")


def dipper_start(config: AlgoConfig):
    if config.SYMTYPE == "Watchlist":
        while True:
            ticker_list = config.db.select_all()
            for ticker in ticker_list:
                config.SYMBOL = ticker['ticker']
                dipper(config)
            print([(ticker['ticker'], ticker['status']) for ticker in ticker_list])
            sleep(config.INTERVAL * 60)
    elif config.SYMTYPE == "Portfolio":
        print("Implementation in progress.")
    else:
        print("Invalid ")


if __name__ == '__main__':  # Handle error when data isn't available for a specific stock because of market data subs
    while True:
        x = int(input("1. Run algorithm with standard configurations\n"
                      "2. Run algorithm with custom configurations\n"
                      "3. Edit watchlist\n"
                      "-1 EXIT\n"
                      "- "))
        if x == -1:
            break
        if x == 2:
            dbp = input('Path to database file or portfolio: ')
            dc = input('Dip calculation (Standard, Relative or Custom): ')
            ra = bool(input('Run auto (True or False): '))
            i = int(input('Interval (How often does the algorithm check): '))
            h = input("Host: ")
            p = int(input('Port: '))
            idd = int(input('id: '))
            configs = AlgoConfig(dbp, dc, ra, i, h, p, idd)
            dipper_start(configs)
        elif x == 1:
            configs = AlgoConfig()
            dipper_start(configs)
        elif x == 3:
            dbp = input('Path to database file, if empty, standard file will be used. ')
            if len(dbp) == 0:
                configs = AlgoConfig()
            else:
                configs = AlgoConfig(DATABASE_PATH=dbp)
            try:
                configs.db.present()
            except sqlite3.OperationalError:
                continue
            a = input("Add (1), remove (2), delete watchlist (-2), press any key to return to menu: ")
            if a == '1':
                configs.db.insert_tickers()
            elif a == '2':
                configs.db.remove_tickers()
            elif a == '-2':
                configs.db.delete_watchlist()
            else:
                continue
