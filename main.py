from TWSIBAPI_MODULES.DataStreams import reqAllTimeHigh, reqCurrentPrice
from TWSIBAPI_MODULES.Contracts import stock
from TWSIBAPI_MODULES.Orders import place_order
from ibapi.contract import Contract
from ibapi.order import Order
from Database import DbManager, ticker_insert


CONN_VARS: list = ["127.0.0.1", 7497, 0]
DIP_CALC: str = "standard"  # standard, relative, or custom
WATCHLIST: str = "watchlist1.db"  # path to watchlist db


def standard_calc(perc_dip, perc_drop):
    if perc_dip < perc_drop:
        return 0
    else:
        for x in range(1, 10):
            if (perc_drop * x) + 1 >= perc_dip >= (perc_drop * x):
                return x
    return -1


def dipper_algo(contract: Contract, current_price: float, perc_drop: float = 5.0):
    if DIP_CALC == "standard":
        ath = reqAllTimeHigh(CONN_VARS, contract)
        perc_dip = round(((current_price - ath) / ath) * 100, 1)
        dc = standard_calc(perc_dip, perc_drop)
        return dc


def buy(current_price: float, multiplier: float = 1.0):
    order = Order()
    order.action = "BUY"
    order.orderType = "LMT"
    order.totalQuantity = multiplier
    order.lmtPrice = current_price
    return order


def thedipper(run_auto: bool = True, watchlist: str = "", ticker: str = ""):
    if ticker != "" and watchlist == "":
        stk = stock(ticker)
        current_price = reqCurrentPrice(CONN_VARS, stk)
        da = dipper_algo(stk, current_price)
        if da > 0:
            if run_auto:
                place_order(CONN_VARS, stk, buy(current_price))
            else:
                print(f"Buy {ticker} at {current_price}. Dipper algo {da}")

    elif watchlist != "" and ticker == "":
        db = DbManager(watchlist)
        while True:
            x = input("Insert, Run, Present, Exit: ").upper()
            if x == 'E':
                break
            elif x == "I":
                ticker_insert(db, CONN_VARS)
            elif x == "R":
                ticker_list = db.select_all()
                for ticker in ticker_list:
                    thedipper(ticker=ticker[ticker])
            elif x == "P":
                z = db.custom_query('SELECT ticker, status FROM Watchlist')
                print(z)

    # elif mode == "portfolio":
    #     pass
    else:
        print("Invalid mode")


thedipper(watchlist=WATCHLIST)