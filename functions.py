from Config import AlgoConfig
from ibapi.contract import Contract
from ibapi.order import Order
from TWSIBAPI_MODULES.DataStreams import reqAllTimeHigh


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


def buy(current_price: float, multiplier: float = 1.0) -> Order:
    order = Order()
    order.action = "BUY"
    order.orderType = "LMT"
    order.totalQuantity = multiplier
    order.lmtPrice = current_price
    return order
