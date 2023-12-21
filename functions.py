from Config import AlgoConfig
from ibapi.contract import Contract
from ibapi.order import Order
from time import sleep
from TWSIBAPI_MODULES.Contracts import stock
from TWSIBAPI_MODULES.Orders import place_order
from TWSIBAPI_MODULES.DataStreams import reqAllTimeHigh, reqCurrentPrice


def standard_calc(pdrop, perc_drop) -> int:
    if pdrop < perc_drop:
        return 0
    else:
        for x in range(1, 10):
            if (perc_drop * x) + 1 >= pdrop >= (perc_drop * x):
                return x
    return -1


def perc_dip(current_price: float, comp: float) -> float:
    return round(((current_price - comp) / comp) * 100, 1)


def dipper_algo(config: AlgoConfig, contract: Contract, current_price: float, perc_drop: float = 5.0) -> int:
    pdrop = 0
    if config.DIP_CALC == "Standard":
        ath = reqAllTimeHigh(config.CONN_VARS, contract)
        pdrop = perc_dip(current_price, ath)
    elif config.DIP_CALC == "Relative":
        r = config.db.select_rh(config.SYMBOL)
        rel = reqAllTimeHigh(config.CONN_VARS, contract) if r == 0 else r
        pdrop = perc_dip(current_price, rel)
    return standard_calc(pdrop, perc_drop)


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


def buy(current_price: float, multiplier: float = 1.0) -> Order:
    order = Order()
    order.action = "BUY"
    order.orderType = "LMT"
    order.totalQuantity = multiplier
    order.lmtPrice = current_price
    return order
