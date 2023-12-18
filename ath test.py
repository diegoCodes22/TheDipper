from TWSIBAPI_MODULES.DataStreams import reqAllTimeHigh
from TWSIBAPI_MODULES.Contracts import stock

print(reqAllTimeHigh(["127.0.0.1", 7497, 0], stock("SPY")))
