# 1. Bond exchange
# Process data with only bonds.
def trade(Data):
    latest_data = Data["latest_data"]
    symbol = latest_data["symbol"]
    trade = []
    if symbol == "BABZ" or symbol == "BABA": 
        BABAZ = Data[symbol]
        # print(BABAZ)
        sell_value = float("inf")
        buy_value = -float("inf")
        for price, amount in BABAZ["sell"] :
            sell_value = min(sell_value,price)
        for price, amount in BABAZ["buy"] :
            buy_value = max(buy_value,price)
        mean = (sell_value+buy_value)/2
        # Base case
        if BABAZ_FV[0] == (0,0):
            BABAZ_FV[0] = (sell_value,buy_value)
        elif BABAZ_FV[0] == (0,0):
            BABAZ_FV[1] = (sell_value,buy_value)
        else:
            if symbol == "BABA":
                BABAZ_FV[0] = (sell_value,buy_value)
            else:
                BABAZ_FV[1] = (sell_value,buy_value)
            
            BABA = BABAZ_FV[0]
            BABZ = BABAZ_FV[1]
            # completely encompassing
            if BABA[0] >= BABZ[0] and BABA[1] <= BABZ[1]:
                fv = (BABZ[0]+BABZ[1])/2
            #BABZ is less.
            elif BABA[0] > BABZ[0]:
                fv = (BABZ[1]+BABA[0])/2
            else:
                fv = (BABZ[0]+BABA[1])/2
            #fv of BABZ
            trade.append({"type": "add", "order_id":order_count , "symbol": "BABA", "dir": "BUY", "price": fv+1, "size": 10})
            trade.append({"type": "add", "order_id":order_count , "symbol": "BABA", "dir": "SELL", "price": fv-1, "size": 10})
    #Todo : cancel trade
    return trade
    