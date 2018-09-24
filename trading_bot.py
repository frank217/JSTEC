import sys
import os.path as osp
import importlib
module_name = "bond_strategy"
sys.path.append(osp.join(osp.dirname(__file__), 'strategy'))
imports = importlib.import_module(module_name)


class Trading_Bot():
    def __init__(self, exchange, strategies):
        self.exchange = exchange
        self.strategies = [import_module(strategy) for strategy in strategies]
        self.data = {"latest_data":{},""}
        self.order_id = 0
        
    def trade(self):
        while True:
            lastest_data = self.exchange.read_from_exchange():
            self.process_data(lastest_data)
            for strategy in self.strategies:
                trades = strategy.trade(self.data)
                for trade in trades:
                    self.exchange.write_to_exchange(trade)
                    self.order_id+=1
        
    def process_data(self,lastest_data):
        if lastest_data["type"] == "book":
            self.data["latest_data"]=lastest_data
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
            # profic from sell
            if price!= cur_price:
                cur_profit = abs(price-cur_price)*size
                print ("Profit trade price difference : ", cur_profit)
                profit += cur_profit
                print ("Total profit: ",profit)

        

