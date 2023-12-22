from Database import DbManager


class AlgoConfig:
    def __init__(self, DATABASE_PATH: str = "watchlist1.db", DIP_CALC: str = 'Standard', perc_drop: float = 5.0,
                 RUN_AUTO: bool = True, INTERVAL: int = 30, HOST: str = "127.0.0.1", PORT: int = 7497, ID: int = 0):
        self.DATABASE_PATH = DATABASE_PATH
        self.DIP_CALC = DIP_CALC
        self.perc_drop = perc_drop
        self.RUN_AUTO = RUN_AUTO
        self.INTERVAL = INTERVAL
        self.CONN_VARS = [HOST, PORT, ID]

        self.SYMBOL = ''

        self.db = DbManager(self.DATABASE_PATH)
        self.db.start_db()
        self.db.show_all()
        self.LIST = ''.join(ch for ch in input("Enter watchlist name: ") if ch.isalnum())
        self.db.exists(self.LIST)
