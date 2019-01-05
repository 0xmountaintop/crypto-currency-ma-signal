#!/usr/bin/env python

import settings
import urllib2
import json
import time
import threading

sample_nums = [5, 10, 20, 50, 100, 200] # in ASC order

def main():
    now = int(time.time())
    print "--------------------------------------"
    print "now: %s, %s\n" % (now, time.ctime(now))

    try:
        for coin in settings.coins:
            print "processing", coin
            
            price_url = "https://marketapi.blockmeta.com/flash/ticker?symbols=%s-%s_usd" % (settings.exchange, coin)
            print "getting price from: ", price_url
            contents = urllib2.urlopen(price_url).read()
            data = json.loads(contents)
            current_price = data["tickers"][0]["ticker"]["last"]
            print current_price

            kline_url = "https://marketapi.blockmeta.com/kline/%s/%s_usd/1hour?count=%d&format_type=all" % (settings.exchange, coin, max(sample_nums))
            print "getting klines from: ", kline_url
            contents = urllib2.urlopen(kline_url).read()
            # print "raw_data:\n", contents
            data = json.loads(contents)
            data = data[::-1] # date DESC
            # print len(data)
            # for d in data:
            #     print d["date"], d["close"]

            mas = {}

            # calc MA
            for i in range(len(sample_nums)):
                ma = 0
                for j in range(sample_nums[i]):
                    ma += data[j]["close"]
                ma /= sample_nums[i]
                ma_name = "ma%d" % sample_nums[i]
                print ma_name, ma
                mas[ma_name] = ma

            # calc EMA

            print ""
        print "sleep for 1h"
        time.sleep(60*60)
    except:
        print "network error\n"

if __name__ == "__main__":
    while True:
        main()