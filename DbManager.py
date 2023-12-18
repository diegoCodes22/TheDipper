import sqlite3


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
        self.conn.commit()

    def update_ath(self, ath: float, ticker: str) -> None:
        self.cur.execute('UPDATE Watchlist SET all_time_high = ? WHERE ticker = ?', (ath, ticker))
        self.conn.commit()
