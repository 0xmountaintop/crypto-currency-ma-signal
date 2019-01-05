#!/usr/bin/env python

import settings
import urllib2
import json
import time
import threading

sample_nums = [5, 10, 20, 50, 100, 200] # in ASC order
coin = "eth"

def main(regr_time):
    print "--------------------------"
    print time.ctime(regr_time)
    print "--------------------------"
    
    try:        
        price_url = "https://marketapi.blockmeta.com/kline/%s/%s_usd/1min?count=%d&format_type=all&end_time=%d" % (settings.exchange, coin, 1, regr_time)
        print "getting price from:", price_url
        contents = urllib2.urlopen(price_url).read()
        data = json.loads(contents)
        regr_price = data[0]["close"]
        print regr_price

        kline_url = "https://marketapi.blockmeta.com/kline/%s/%s_usd/1hour?count=%d&format_type=all&end_time=%d" % (settings.exchange, coin, max(sample_nums), regr_time)
        print "getting klines from:", kline_url
        contents = urllib2.urlopen(kline_url).read()
        data = json.loads(contents)
        data = data[::-1] # date DESC

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


        # make decision
        up_cnt = 0
        down_cnt = 0
        for ma_name in mas:
            if regr_price > mas[ma_name]:
                up_cnt += 1
            if regr_price < mas[ma_name]:
                down_cnt += 1
        print "up: %d/%d, down: %d/%d" % (up_cnt, len(mas), down_cnt, len(mas))
        if up_cnt > len(mas)*0.75:
            print "%s: BUY BUY BUY %s at price: %f" % (time.ctime(regr_time), coin, regr_price)
        if down_cnt > len(mas)*0.75:
            print "%s: SELL SELL SELL %s at price: %f" % (time.ctime(regr_time), coin, regr_price)
        return True
    except Exception as e:
        print "Error:", e
        return False

if __name__ == "__main__":
    print "Regression for", coin
    regr_time = 1530374470 # July 1, 2018 12:01:00 AM GMT+08:00
    now = int(time.time())
    while regr_time <= now:
        if main(regr_time):
            regr_time += 60*60 # move forward 1h