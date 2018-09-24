# 1. Bond exchange
# Process data with only bonds.
def trade(Data):
    latest_data = Data["latest_data"]
    symbol = latest_data["symbol"]
    trade = []

    # XLK trading
    if symbol == "AAPL":
        AAPL = Data[symbol]
        aapl_data = []
        max_appl = -float("inf")
        min_appl = float("inf")
        for price, amount in AAPL["sell"]:
            max_appl = max(price, max_appl)
        for price, amount in AAPL["buy"]:
            min_appl = min(price, min_appl)
        appl_fp = (max_appl + min_appl) / 2

    if symbol == "GOOG":
        GOOG = Data[symbol]
        goog_data = []
        max_goog = -float("inf")
        min_goog = float("inf")
        for price, amount in GOOG["sell"]:
            max_goog = max(price, max_goog)
        for price, amount in GOOG["buy"]:
            min_goog = min(price, min_goog)
        goog_fp = (max_goog + min_goog) / 2

    if symbol == "MSFT":
        MSFT = Data[symbol]
        msft_data = []
        max_msft = -float("inf")
        min_msft = float("inf")
        for price, amount in MSFT["sell"]:
            max_msft = max(price, max_msft)
        for price, amount in MSFT["buy"]:
            min_msft = min(price, min_msft)
        msft_fp = (max_msft + min_msft) / 2

    if symbol == "XLK":
        XLK = Data[symbol]
        xlk_data = []
        max_xlk = -float("inf")
        min_xlk = float("inf")
        for price, amount in XLK["sell"]:
            max_xlk = max(price, max_xlk)
        for price, amount in XLK["buy"]:
            min_xlk = min(price, min_xlk)
    
        
    if "GOOG" in Data and "XLK" in Data and "MSFT" in Data and "AAPL" in Data:
        xlk_min_comb = (3 * min_msft + 2 * min_goog + 2 * min_appl + 3000) / 10
        xlk_max_comb = (3 * max_msft + 2 * max_goog + 2 * max_appl + 3000) / 10

        fp_bound_1 = max(xlk_min_comb, min_xlk)
        fp_bound_2 = min(xlk_max_comb, max_xlk)

        if (fp_bound_1 > fp_bound_2):
            xlk_fp_max = fp_bound_1
            xlk_fp_min = fp_bound_2
        else:
            xlk_fp_max = fp_bound_2
            xlk_fp_min = fp_bound_1

        xlk_fp = (xlk_fp_min + xlk_fp_min) / 2


        trade.append({"type": "add", "order_id":order_count , "symbol": "XLK", "dir": "BUY", "price": xlk_fp+1, "size": 10})
        trade.append({"type": "add", "order_id":order_count , "symbol": "XLK", "dir": "SELL", "price": xlk_fp-1, "size": 10})
    #Todo : cancel trade
    return trade
    