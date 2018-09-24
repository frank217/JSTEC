import argparse
import sys
import time
import errno
from socket import error as socket_error

from exchange import Exchange
from trading_bot import Trading_Bot


def main(strategies, test):
    exchange = Exchange(test)
    print ("Connected to exchange")
    trading_bot = Trading_Bot(exchange, strategies)
    print ("Bot initialized")
    trading_bot.trade()
    print ("Bot finished Trading")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('strategies')
    parser.add_argument('--test', action='store_true', default=False)
    parser.add_argument('-s',default=0)
    args = parser.parse_args()
    test = (args.test,args.s)
    print (args)

    strategies = args.strategies.split(',')
    while True:
        try:
            main(strategies, test)
        except socket_error as serr:
            if serr.errno != errno.ECONNREFUSED:
                raise serr
            # TODO metrics for each round
            print ("Sleeping...")
            time.sleep(1)