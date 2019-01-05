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
            print "getting price from:", price_url
            contents = urllib2.urlopen(price_url).read()
            data = json.loads(contents)
            current_price = data["tickers"][0]["ticker"]["last"]
            print current_price

            kline_url = "https://marketapi.blockmeta.com/kline/%s/%s_usd/1hour?count=%d&format_type=all" % (settings.exchange, coin, max(sample_nums))
            print "getting klines from:", kline_url
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
                sample_num = sample_nums[i]
                ma = 0
                for j in range(sample_num):
                    ma += data[j]["close"]
                ma /= sample_num
                ma_name = "ma%d" % sample_num
                mas[ma_name] = ma

            # calc EMA
            for i in range(len(sample_nums)):
                sample_num = sample_nums[i]
                samples = data[0:sample_num][::-1] # ASC
                # alpha = 2/(sample_num+1)
                alpha = 1/sample_num
                ema = samples[0]["close"]
                for i in xrange(1,sample_num):
                    ema = alpha * samples[i]["close"] + (1-alpha) * ema
                ema_name = "ema%d" % sample_num
                mas[ema_name] = ema

            # make decision
            up_cnt = 0
            down_cnt = 0
            for ma_name in mas:
                print ma_name, mas[ma_name]
                if current_price > mas[ma_name]:
                    up_cnt += 1
                if current_price < mas[ma_name]:
                    down_cnt += 1
            if up_cnt > len(mas)*0.75:
                print "BUY BUY BUY %s at price: %f" % (coin, current_price)
            if down_cnt > len(mas)*0.75:
                print "SELL SELL SELL %s at price: %f" % (coin, current_price)
            print ""
        print "sleep for 1h"
        time.sleep(60*60)
    except Exception as e:
            print "Error:", e

if __name__ == "__main__":
    while True:
        main()