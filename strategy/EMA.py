# 1. Bond exchange
# Process data with only bonds.
def trade(Data):
    latest_data = Data["latest_data"]
    trade = []

    if lastest_data["type"] == "book" :
    # Set Data
    symbol = lastest_data["symbol"]
    symbol_data = Data[symbol]

    data_set = symbol_data["data_set"]
    count = 0
    sum_buy = 0
    sum_sell = 0
    # Get mean of sell
    for price,amount in lastest_data["sell"]:
        sum_sell = price*amount
    if len(lastest_data["sell"]):
        mean_sell = sum_sell/len(lastest_data["sell"]) 
    else:
        mean_sell = symbol_data["sell_mean"]
    # Get mean of buy
    for price,amount in lastest_data["buy"]:
        sum_buy = price*amount
    if len(lastest_data["buy"]):
        mean_buy = sum_buy/len(lastest_data["buy"])
    else:
        mean_buy = symbol_data["buy_mean"]

    data_set.append([mean_sell,mean_buy])
    data_remove = data_set.popleft()


    # No data set 
    if not symbol_data["latest_data"]:
        symbol_data["sell_mean"] = mean_sell
        symbol_data["buy_mean"] = mean_buy
        
    else:
        sell_entire_mean = symbol_data["sell_mean"]
        sell_entire_mean = sell_entire_mean + (mean_sell - data_remove[0])
        # print ("sell:",sell_entire_mean,mean_sell)
        if sell_entire_mean > mean_sell :
            trade.append({"type": "add", "order_id":order_count , "symbol": symbol, "dir": "SELL", "price": (sell_entire_mean + mean_sell)/2, "size": 2})
            order_id_inaction[order_count] = trade

        buy_entire_mean = symbol_data["buy_mean"]
        buy_entire_mean = buy_entire_mean + (mean_buy - data_remove[1])
        # print ("buy:",buy_entire_mean,mean_buy)
        if buy_entire_mean < mean_buy:
            trade.append(){"type": "add", "order_id":order_count , "symbol": symbol, "dir": "BUY", "price": (mean_buy + buy_entire_mean)/2, "size": 2})
            order_id_inaction[order_count] = trade
    #Todo : cancel trade
    return trade
    