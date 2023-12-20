from Database import DbManager


class AlgoConfig:
    def __init__(self, LIST: str, DATABASE_PATH: str = "watchlist.db", DIP_CALC: str = 'Standard',
                 RUN_AUTO: bool = True, INTERVAL: int = 30, HOST: str = "127.0.0.1", PORT: int = 7497, ID: int = 0):
        self.LIST = ''.join(ch for ch in LIST if ch.isalnum())
        self.DATABASE_PATH = DATABASE_PATH
        self.DIP_CALC = DIP_CALC
        self.RUN_AUTO = RUN_AUTO
        self.INTERVAL = INTERVAL
        self.CONN_VARS = [HOST, PORT, ID]

        self.SYMBOL = ''
        self.db = DbManager(self.DATABASE_PATH, self.LIST)
        self.SYMTYPE = ''
        if self.DATABASE_PATH.split('.')[1] == 'db':
            self.SYMTYPE = 'Watchlist'
        elif self.DATABASE_PATH == 'portfolio':
            self.SYMTYPE = 'Portfolio'
        self.db.exists()


