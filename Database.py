import sqlite3


class DbManager:
    def __init__(self, db_path, watchlist):
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        self.conn = conn
        self.cur = cur
        self.watchlist = watchlist

    def close_db(self) -> None:
        self.cur.close()

    def insert_tickers(self) -> None:
        tickers = input("Comma separated list of tickers ', ': ").split(', ')
        for ticker in tickers:
            if ticker in self.custom_query('SELECT ticker FROM {}'.format(self.watchlist)):
                print(f"{ticker} already exists in database")
                continue
            else:
                self.cur.execute('INSERT INTO {} (ticker) VALUES(?)'.format(self.watchlist), (ticker,))
        self.commit_operation()

    def remove_tickers(self) -> None:
        tickers = input("Comma separated list of tickers ', ': ").split(', ')
        print(tickers)
        x = input("Are you sure you want to delete these tickers from the database?\n"
                  "Your positions will NOT change but the algorithm will not take them into account (y/n): ")
        if x == 'y':
            for ticker in tickers:
                if ticker not in self.custom_query('SELECT ticker FROM {}'.format(self.watchlist)):
                    print(f"{ticker} not in database")
                    continue
                else:
                    self.cur.execute('DELETE FROM {} WHERE ticker = ?'.format(self.watchlist), (ticker, ))
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

    def exists(self) -> None:
        self.cur.execute('SELECT COUNT(*) FROM information_schema.tables WHERE table_name = ?', (self.watchlist, ))
        if self.cur.fetchone()[0] == 0:
            c = input("Watchlist does not exist, do you want to create a new one? (y/n) ")
            if c == 'y':
                self.create()

    def create(self):
        self.cur.execute('''CREATE TABLE {} (ticker TEXT NOT NULL CONSTRAINT ticker_key UNIQUE, 
        all_time_high REAL DEFAULT 0 NOT NULL, relative_high REAL DEFAULT 0, status INTEGER)'''.format(self.watchlist))

    def present(self):
        sa = self.select_all()
        print((q['ticker'], q['status']) for q in sa)

    def custom_query(self, query: str, params: tuple = ()) -> list:
        self.cur.execute(query, params)
        return self.cur.fetchall()

    def commit_operation(self) -> None:
        self.conn.commit()

