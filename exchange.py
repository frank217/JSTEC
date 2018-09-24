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

class Exchange:
    def __init__(self,test):
        team_name = "UNREGISTERED"
        # This variable dictates whether or not the bot is connecting to the prod
        # or test exchange. Be careful with this switch!
        test_mode = test[0]

        # This setting changes which test exchange is connected to.
        # 0 is prod-like
        # 1 is slower
        # 2 is empty
        test_exchange_index=test[1]
        prod_exchange_hostname="production"
        Data = {}
        self.port=25000 + (test_exchange_index if test_mode else 0)
        self.exchange_hostname = "test-exch-" + team_name if test_mode else prod_exchange_hostname
        self.exchange = self.connect()


    # ~~~~~============== NETWORKING CODE ==============~~~~~
    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.exchange_hostname, self.port))
        return s.makefile('rw', 1)

    def write_to_exchange(self,obj):
        json.dump(obj, exchange)
        self.exchange.write("\n")

    def read_from_exchange(self):
        return json.loads(self.exchange.readline())


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


if __name__ == "__main__":
    main()