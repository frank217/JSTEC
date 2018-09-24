
# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x bot.py
# 3) Run in loop: while true; do ./bot.py; sleep 1; done

from __future__ import print_function

import sys
import socket
import json
import time
# ~~~~~============== CONFIGURATION  ==============~~~~~
# replace REPLACEME with your team name!
team_name="UNREGISTERED"
# This variable dictates whether or not the bot is connecting to the prod
# or test exchange. Be careful with this switch!
test_mode = True

# This setting changes which test exchange is connected to.
# 0 is prod-like
# 1 is slower
# 2 is empty
test_exchange_index=0
prod_exchange_hostname="production"
Data = {}


port=25000 + (test_exchange_index if test_mode else 0)
exchange_hostname = "test-exch-" + team_name if test_mode else prod_exchange_hostname
print (exchange_hostname)
# ~~~~~============== NETWORKING CODE ==============~~~~~
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((exchange_hostname, port))
    return s.makefile('rw', 1)

def write_to_exchange(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def read_from_exchange(exchange):
    return json.loads(exchange.readline())


# ~~~~~============== MAIN LOOP ==============~~~~~

def main():
    exchange = connect()
    write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
    hello_from_exchange = read_from_exchange(exchange)
    # A common mistake people make is to call write_to_exchange() > 1
    # time for every read_from_exchange() response.
    # Since many write messages generate marketdata, this will cause an
    # exponential explosion in pending messages. Please, don't do that!
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)
    symbols  = read_from_exchange(exchange)["symbols"]
    # for symbol in symbols:
    #     Data[symbol] = []
    # print (Data)
    # number to symbols.
    symbol_dict = {}
    for i in range(len(symbols)):
        symbol_dict[i] = symbols[i]

    order_count =0


    #section 2 variable
    BABAZ_FV = [0,0]
    BABA_FV = 0
    BABZ_FV = 0
    # BABZ_FV = 0
    #
    while True:
        # Get data of market
        lastest_data = read_from_exchange(exchange)
        print (lastest_data)
        if lastest_data["type"] == "book" :
            symbol = lastest_data["symbol"]
            Data[symbol] = lastest_data

            # 1. Bond exchange
            # Process data with only bonds.

            trade = {"type": "add", "order_id":order_count , "symbol": "BOND", "dir": "SELL", "price": 1001, "size": 10}
            write_to_exchange(exchange,trade)
            order_count += 1
            trade = {"type": "add", "order_id":order_count , "symbol": "BOND", "dir": "BUY", "price": 999, "size": 10}
            write_to_exchange(exchange,trade)
            order_count += 1


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
                xlk_fp_comb = (3 * msft_fp + 2 * goog_fp + 2 * appl_fp + 3000) / 10


                trade = {"type": "add", "order_id":order_count , "symbol": "XLK", "dir": "BUY", "price": xlk_fp+1, "size": 10}
                order_count +=1
                write_to_exchange(exchange,trade)
                trade = {"type": "add", "order_id":order_count , "symbol": "XLK", "dir": "SELL", "price": xlk_fp-1, "size": 10}
                write_to_exchange(exchange,trade)
                order_count+=1

                # Converting XLK
                if (xlk_fp_comb - xlk_fp) * 10 > 100:
                    conversion = {"type": "convert", "order_count":order_count, "symbol": "XLK", "dir": "SELL", "size": 10}
                    write_to_exchange(exchange, conversion)
                    order_count += 1
                    trade = {"type": "add", "order_id":order_count , "symbol": "GOOG", "dir": "SELL", "price": goog_fp-1, "size": 20}
                    write_to_exchange(exchange, trade)
                    order_count += 1

                    trade = {"type": "add", "order_id":order_count , "symbol": "MSFT", "dir": "SELL", "price": msft_fp-1, "size": 30}
                    write_to_exchange(exchange, trade)
                    order_count += 1

                    trade = {"type": "add", "order_id":order_count , "symbol": "APPL", "dir": "SELL", "price": appl_fp-1, "size": 20}
                    write_to_exchange(exchange, trade)
                    order_count += 1

                    trade = {"type": "add", "order_id":order_count , "symbol": "BOND", "dir": "SELL", "price": 1001, "size": 30}
                    write_to_exchange(exchange, trade)
                    order_count += 1
                elif (xlk_fp - xlk_fp_comb) * 10 > 100:
                    conversion = {"type": "convert", "order_count": order_count, "symbol": "XLK", "dir": "BUY", "size": 10}
                    write_to_exchange(exchange, conversion)
                    order_count += 1

                    trade = {"type": "add", "order_id":order_count , "symbol": "XLK", "dir": "SELL", "price": xlk_fp-1, "size": 10}
                    write_to_exchange(exchange,trade)
                    order_count+=1

                if (xlk_fp_comb - xlk_fp) * 20 > 100:
                    conversion = {"type": "convert", "order_count":order_count, "symbol": "XLK", "dir": "SELL", "size": 20}
                    write_to_exchange(exchange, conversion)
                    order_count += 1
                    trade = {"type": "add", "order_id":order_count , "symbol": "GOOG", "dir": "SELL", "price": goog_fp-1, "size": 40}
                    write_to_exchange(exchange, trade)
                    order_count += 1

                    trade = {"type": "add", "order_id":order_count , "symbol": "MSFT", "dir": "SELL", "price": msft_fp-1, "size": 60}
                    write_to_exchange(exchange, trade)
                    order_count += 1

                    trade = {"type": "add", "order_id":order_count , "symbol": "APPL", "dir": "SELL", "price": appl_fp-1, "size": 40}
                    write_to_exchange(exchange, trade)
                    order_count += 1

                    trade = {"type": "add", "order_id":order_count , "symbol": "BOND", "dir": "SELL", "price": 1001, "size": 60}
                    write_to_exchange(exchange, trade)
                    order_count += 1
                elif(xlk_fp - xlk_fp_comb) * 20 > 100:
                    conversion = {"type": "convert", "order_count": order_count, "symbol": "XLK", "dir": "BUY", "size": 20}
                    write_to_exchange(exchange, conversion)
                    order_count += 1
                    
                    trade = {"type": "add", "order_id":order_count , "symbol": "XLK", "dir": "SELL", "price": xlk_fp-1, "size": 20}
                    write_to_exchange(exchange,trade)
                    order_count+=1


            # # Part 2 Fair trade BABA,BABZ:

            # if symbol == "BABZ":
            #     BABA = Data[symbol]
            #     print(BABZ)
            #     babz_min_value = float("inf")
            #     max_value = -float("inf")
            #     for price, amount in BABA["sell"] :
            #         babz_min_value = min(babz_min_value,price)
            #     for price, amount in BABA["buy"] :
            #         babz_max_value = max(babz_max_value,price)
            #     mean = (babz_min_value + babz_max_value)/2

            # if symbol == "BABA":
            #     BABA = Data[symbol]
            #     print(BABA)
            #     baba_min_value = float("inf")
            #     baba_max_value = -float("inf")
            #     for price, amount in BABAZ["sell"] :
            #         baba_min_value = min(baba_min_value,price)
            #     for price, amount in BABAZ["buy"] :
            #         baba_max_value = max(baba_max_value,price)
            #     mean = (min_value+max_value)/2

            # if symbol == "BABZ" or symbol == "BABA":
            #     BABAZ = Data[symbol]
            #     print(BABAZ)
            #     min_value = float("inf")
            #     max_value = -float("inf")
            #     for price, amount in BABAZ["sell"] :
            #         min_value = min(min_value,price)
            #     for price, amount in BABAZ["buy"] :
            #         max_value = max(min_value,price)
            #     mean = (min_value+max_value)/2
            #     # Base case
            #     if BABAZ_FV[0] == 0:
            #         BABAZ_FV = [mean,mean]
            #     elif symbol == "BABA":
            #         BABAZ_FV[0] == mean
            #     else:
            #         BABA_FV[1] = mean


            #     fv = (BABAZ_FV[0] + BABAZ_FV[1]) / 2

            #     # IF BABA is higher:
            #     if BABAZ_FV[0] >= BABAZ_FV[1]:
            #         if (BABA_FV[1] + fv)/2 >(BABA_FV[0]+fv)/2 +10:
            #             sell_to = ["BABZ", (BABA_FV[1]+fv)/2]
            #             buy_from = ["BABA", (BABA_FV[0]+fv)/2]
            #             trade = {"type": "add", "order_id":order_count , "symbol": buy_from[0], "dir": "BUY", "price": buy_from[1], "size": 10}
            #             write_to_exchange()
            #             trade = {"type": "add", "order_id":order_count , "symbol": sell_from[0], "dir": "SELL", "price": sell_from[1], "size": 10}
            #             write_to_exchange()
            #     else:
            #         sell_to = ["BABA", (BABA_FV[0]+fv)/2]
            #         buy_from = ["BABZ", (BABA_FV[1]+fv)/2]
            #         trade = {"type": "add", "order_id":order_count , "symbol": buy_from[0], "dir": "BUY", "price": buy_from[1], "size": 10}
            #         write_to_exchange()
            #         trade = {"type": "add", "order_id":order_count , "symbol": sell_from[0], "dir": "SELL", "price": sell_from[1], "size": 10}
            #         write_to_exchange()
            #     #BABA -> BABZ  for $BABZ
        
        elif lastest_data["type"] == "error":
            print ("Error processing Order")
        elif lastest_data["type"] == "reject":
            order_id = order_id_inaction.pop(latest_data["order_id"])
        elif lastest_data["type"] == "fill":
            order_id = latest_data["order_id"]
            price = lastest_data["price"]
            size = lastest_data["size"]
            Buy_sell = lastest_data["dir"]
            symbol = lastest_data["symbol"]

            cur_order  = order_id_inaction[order_id]
            cur_size = cur_order["size"]
            cur_price = cur_order["size"]
            
            trade_track["price"]

            cur_size -= size
            if cur_size == 0:
                order_id_inaction.pop(order_id)
            if price!= cur_price:
                cur_profit = abs(price-cur_price)*size
                print ("Profit trade price difference : ", cur_profit)
                profit += cur_profit
                print ("Total profit: ",profit)









if __name__ == "__main__":
    main()