import sqlite3
from TWSIBAPI_MODULES.Contracts import stock
from TWSIBAPI_MODULES.DataStreams import reqAllTimeHigh


class DbManager:
    def __init__(self, db_name):
        conn = sqlite3.connect(db_name)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        self.conn = conn
        self.cur = cur

    def close_db(self) -> None:
        self.cur.close()

    def insert_ticker(self, ticker: str) -> None:
        self.cur.execute('INSERT INTO Watchlist(ticker) VALUES(?)', (ticker,))

    def update_ath(self, ath: float, ticker: str) -> None:
        self.cur.execute('UPDATE Watchlist SET all_time_high = ? WHERE ticker = ?', (ath, ticker))

    def commit_opperation(self) -> None:
        self.conn.commit()

    def select_all(self) -> list:
        self.cur.execute('SELECT * FROM Watchlist')
        return self.cur.fetchall()

    def custom_query(self, query: str, params: tuple = ()) -> list:
        self.cur.execute(query, params)
        return self.cur.fetchall()


def ticker_insert(db: DbManager, CONN_VARS):
    t = input("Comma separated list of tickers ', ': ")
    t = t.split(", ")
    for ticker in t:
        db.insert_ticker(ticker)
        db.update_ath(reqAllTimeHigh(CONN_VARS, stock(ticker)), ticker)
    db.commit_opperation()
