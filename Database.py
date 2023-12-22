import sqlite3


class DbManager:
    def __init__(self, db_path: str):
        self.conn = None
        self.cur = None
        self.db_path = db_path
        self.watchlist = ''
        self.wlist = []

    def start_db(self) -> None:
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self.cur = self.conn.cursor()
        except sqlite3.OperationalError:
            print("Invalid database file, Operational Error raised.")
            exit(1)

    def close_db(self) -> None:
        self.cur.close()
        self.conn.close()

    def insert_tickers(self) -> None:
        tickers = input("Comma separated list of tickers ', ': ").upper().split(', ')
        for ticker in tickers:
            try:
                tl = self.custom_query('SELECT ticker FROM {}'.format(self.watchlist))[0]['ticker']
            except IndexError:
                tl = []
            if ticker in tl:
                print(f"{ticker} already exists in database")
                continue
            else:
                self.cur.execute('INSERT INTO {} (ticker) VALUES(?)'.format(self.watchlist), (ticker,))

        self.commit_operation()

    def remove_tickers(self) -> None:
        tickers = input("Comma separated list of tickers ', ': ").upper().split(', ')
        print(tickers)
        x = input("Are you sure you want to delete these tickers from the database?\n"
                  "Your positions will NOT change but the algorithm will not take them into account (y/n): ")
        if x == 'y':
            for ticker in tickers:
                if ticker not in self.custom_query('SELECT ticker FROM {}'.format(self.watchlist))[0]['ticker']:
                    print(f"{ticker} not in database")
                    continue
                else:
                    self.cur.execute('DELETE FROM {} WHERE ticker = ?'.format(self.watchlist), (ticker, ))
                    print(f"{ticker} deleted from database")
            self.commit_operation()
        else:
            return

    def update_ath(self, ticker: str, ath: float) -> None:
        self.cur.execute('UPDATE {} SET all_time_high = ? WHERE ticker = ?'.format(self.watchlist), (ath, ticker))

    def update_rh(self, ticker: str, rh: float) -> None:
        self.cur.execute('UPDATE {} SET relative_high = ? WHERE ticker = ?'.format(self.watchlist), (rh, ticker))

    def select_rh(self, ticker: str) -> float:
        self.cur.execute('SELECT relative_high FROM {} WHERE ticker = ?'.format(self.watchlist), (ticker, ))
        return self.cur.fetchone()[0]

    def update_status(self, ticker: str, status: int) -> None:
        self.cur.execute('UPDATE {} SET status = ? WHERE ticker = ?'.format(self.watchlist), (status, ticker))

    def select_status(self, ticker: str) -> int:
        self.cur.execute('SELECT status FROM {} WHERE ticker = ?'.format(self.watchlist), (ticker, ))
        return self.cur.fetchone()[0]

    def select_all(self) -> list:
        self.cur.execute('SELECT * FROM {}'.format(self.watchlist))
        return self.cur.fetchall()

    def show_all(self) -> None:
        self.cur.execute('SELECT * FROM sqlite_master WHERE type = "table"')
        self.wlist = [watchlist["name"] for watchlist in list(self.cur.fetchall())]
        print(self.wlist if len(self.wlist) > 0 else "This database is empty.")

    def exists(self, wname: str) -> None:
        if wname in self.wlist:
            self.watchlist = wname
        elif wname not in self.wlist:
            if input("This watchlist does not exist, do you want to create a new one? (y/n): ") == 'y':
                self.watchlist = wname
                self.create()

    def create(self) -> None:
        self.cur.execute('''CREATE TABLE {} (ticker TEXT NOT NULL CONSTRAINT ticker_key UNIQUE, 
        all_time_high REAL DEFAULT 0 NOT NULL, relative_high REAL DEFAULT 0, 
        status INTEGER DEFAULT 0)'''.format(self.watchlist))
        self.wlist.append(self.wlist)

    def present(self) -> None:
        sa = self.select_all()
        if len(list(sa)) == 0:
            print("Watchlist is empty")
        else:
            print([(q['ticker'], q['status']) for q in list(sa)])

    def custom_query(self, query: str, params: tuple = ()) -> list:
        self.cur.execute(query, params)
        return self.cur.fetchall()

    def delete_watchlist(self) -> None:
        if input("Are you sure you want to delete this watchlist? This action is permanent and all its "
                 "contents will be lost (y/n): ") == "y":
            self.cur.execute("DROP TABLE {}".format(self.watchlist))
            self.commit_operation()

    def commit_operation(self) -> None:
        self.conn.commit()

