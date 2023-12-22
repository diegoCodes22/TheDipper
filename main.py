import sqlite3
from functions import *


if __name__ == '__main__':  # Handle error when data isn't available for a specific stock because of market data subs
    while True:
        x = int(input("1. Run algorithm with standard configurations\n"
                      "2. Run algorithm with custom configurations\n"
                      "3. Edit watchlist\n"
                      "-1 EXIT\n"
                      "- "))
        if x == -1:
            try:
                configs.db.close_db()
            except NameError:
                pass
            break
        if x == 2:
            dbp = input('Path to database file: ')
            dc = input('Dip calculation (Standard or Relative): ')
            pd = float(input('Percentage drop: '))
            ra = bool(input('Run auto (True or False): '))
            i = int(input('Interval (How often does the algorithm check): '))
            h = input("Host: ")
            p = int(input('Port: '))
            idd = int(input('id: '))
            configs = AlgoConfig(dbp, dc, pd, ra, i, h, p, idd)
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
