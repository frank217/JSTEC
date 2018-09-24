# 1. Bond exchange
# Process data with only bonds.
def trade(data):
    trade = []
    # print ("In bond strat")
    data = exchange.latest_data
    trade.append({"type": "add", "order_id":order_count , "symbol": "BOND", "dir": "SELL", "price": 1001, "size": 10})
    trade.append({"type": "add", "order_id":order_count , "symbol": "BOND", "dir": "BUY", "price": 999, "size": 10})
    # Todo: Cancel data when sell and buy price is stuck
    return trade