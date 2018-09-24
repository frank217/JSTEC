# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x bot.py
# 3) Run in loop: while true; do ./bot.py; sleep 1; done

from __future__ import print_function

import sys
import socket
import json
import time
import math
from collections import deque
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


# Data Set of stock in action.
# Dictionary tree
# Symbol
#     set of data(100)
#     mean sell value 
#     mean buy value

Data = {}

# Trading in action(id)
order_id_inaction = {}   

# Trade trace:
trade_track = {}

# Track profit
profit = 0

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
    for symbol in symbols:
        Data[symbol] = {"latest_data":[],"sell_mean":0,"buy_mean":0,"data_set":deque(),"trading_inaction":{}}
    print (Data)
    # number to symbols. 
    symbol_dict = {}
    for i in range(len(symbols)):
        symbol_dict[i] = symbols[i]

    order_count =0


    #section 2 variable
    BABAZ_FV = [(0,0),(0,0)]
    while True:
        # Get data of market
        try:
            lastest_data = read_from_exchange(exchange)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        # print (lastest_data)
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
                    trade = {"type": "add", "order_id":order_count , "symbol": symbol, "dir": "SELL", "price": (sell_entire_mean + mean_sell)/2, "size": 2}
                    write_to_exchange(exchange,trade)
                    order_id_inaction[order_count] = trade
                    order_count += 1 

                buy_entire_mean = symbol_data["buy_mean"]
                buy_entire_mean = buy_entire_mean + (mean_buy - data_remove[1])
                # print ("buy:",buy_entire_mean,mean_buy)
                if buy_entire_mean < mean_buy:
                    trade = {"type": "add", "order_id":order_count , "symbol": symbol, "dir": "BUY", "price": (mean_buy + buy_entire_mean)/2, "size": 2}
                    write_to_exchange(exchange,trade)
                    order_count += 1 
            
            symbol_data["latest_data"] = lastest_data

            # 1. Bond exchange
            # Process data with only bonds.
            # if symbol =="Bond":
                
                


            # trade = {"type": "add", "order_id":order_count , "symbol": "BOND", "dir": "SELL", "price": 1001, "size": 10}
            # write_to_exchange(exchange,trade)
            # order_count += 1
            # trade = {"type": "add", "order_id":order_count , "symbol": "BOND", "dir": "BUY", "price": 999, "size": 10}
            # write_to_exchange(exchange,trade)
            # order_count += 1 
            
            # # Part 2 Fair trade BABA,BABZ:
            # if symbol == "BABZ" or symbol == "BABA": 
            #     BABAZ = Data[symbol]
            #     # print(BABAZ)
            #     sell_value = float("inf")
            #     buy_value = -float("inf")
            #     for price, amount in BABAZ["sell"] :
            #         sell_value = min(sell_value,price)
            #     for price, amount in BABAZ["buy"] :
            #         buy_value = max(buy_value,price)
            #     mean = (sell_value+buy_value)/2
            #     # Base case
            #     if BABAZ_FV[0] == (0,0):
            #         BABAZ_FV[0] = (sell_value,buy_value)
            #     elif BABAZ_FV[0] == (0,0):
            #         BABAZ_FV[1] = (sell_value,buy_value)
            #     else:
            #         if symbol == "BABA":
            #             BABAZ_FV[0] = (sell_value,buy_value)
            #         else:
            #             BABAZ_FV[1] = (sell_value,buy_value)
                    
            #         BABA = BABAZ_FV[0]
            #         BABZ = BABAZ_FV[1]
            #         # completely encompassing
            #         if BABA[0] >= BABZ[0] and BABA[1] <= BABZ[1]:
            #             fv = (BABZ[0]+BABZ[1])/2
            #         #BABZ is less.
            #         elif BABA[0] > BABZ[0]:
            #             fv = (BABZ[1]+BABA[0])/2
            #         else:
            #             fv = (BABZ[0]+BABA[1])/2
            #         #fv of BABZ
            #         trade = {"type": "add", "order_id":order_count , "symbol": "BABA", "dir": "BUY", "price": fv+1, "size": 10}
            #         order_count +=1
            #         write_to_exchange(exchange,trade)
            #         trade = {"type": "add", "order_id":order_count , "symbol": "BABA", "dir": "SELL", "price": fv-1, "size": 10}
            #         write_to_exchange(exchange,trade)
            #         order_count+=1


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
            
            


            

            print (Buy_sell, " price:",price," amount:",amount)
             



            
            {"type":"fill","order_id":N,"symbol":"SYM","dir":"BUY","price":N,"size":N}

        
                
                     


                    
                


if __name__ == "__main__":
    main()

