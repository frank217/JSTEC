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
            
            # Part 2 Fair trade BABA,BABZ:
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
                    trade = {"type": "add", "order_id":order_count , "symbol": "BABA", "dir": "BUY", "price": fv+1, "size": 10}
                    order_count +=1
                    write_to_exchange(exchange,trade)
                    trade = {"type": "add", "order_id":order_count , "symbol": "BABA", "dir": "SELL", "price": fv-1, "size": 10}
                    write_to_exchange(exchange,trade)
                    order_count+=1


if __name__ == "__main__":
    main()

