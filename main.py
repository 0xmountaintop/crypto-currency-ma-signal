#!/usr/bin/env python

import settings
import urllib2
import json
import time
import threading

# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API
# https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/timerbot.py

# https://marketapi.blockmeta.com/apidocs/#/

# 5
# 10
# 20
# 50
# 100
# 200

# [
#     {
#         "open": 132.05,
#         "high": 133.39,
#         "low": 131.09,
#         "close": 132.79,
#         "vol": 3228.0352636033,
#         "date": 1545800400
#     }
# ]


def main():
    now = int(time.time())
    print "now: %s, %s\n" % (now, time.ctime(now))

    for coin in settings.coins:
        print "processing", coin
        
        price_url = "https://marketapi.blockmeta.com/flash/ticker?symbols=%s-%s_usd" % (settings.exchange, coin)
        print "getting price from: ", price_url
        contents = urllib2.urlopen(price_url).read()
        data = json.loads(contents)
        print data["tickers"][0]["ticker"]["last"]

        kline_url = "https://marketapi.blockmeta.com/kline/%s/%s_usd/1hour?count=200&format_type=all" % (settings.exchange, coin)
        print "getting klines from: ", kline_url
        contents = urllib2.urlopen(kline_url).read()
        # print "raw_data:\n", contents
        data = json.loads(contents)
        # print len(data)
        for d in data:
            print d["date"], d["close"]
            break

        print ""

    time.sleep(60*60) # sleep for 1h



if __name__ == "__main__":
    while True:
        main()