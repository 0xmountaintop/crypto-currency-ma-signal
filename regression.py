#!/usr/bin/env python

import settings
import urllib2
import json
import time
import threading

sample_nums = [5, 10, 20, 50, 100, 200] # in ASC order
coin = settings.regr_coin

def main(regr_time, file):
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
        file.write(time.ctime(regr_time) + ": regression_price "+ str(regr_price) + "\n")
        file.flush()

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
        for i in range(len(sample_nums)):
            sample_num = sample_nums[i]
            samples = data[0:sample_num][::-1] # ASC
            if settings.sensitive:
                alpha = 2/(sample_num+1)
            else:
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
            if regr_price > mas[ma_name]:
                up_cnt += 1
            if regr_price < mas[ma_name]:
                down_cnt += 1
        print "up: %d/%d, down: %d/%d" % (up_cnt, len(mas), down_cnt, len(mas))
        if up_cnt > len(mas)*settings.strenth_threshold:
            print "%s: BUY BUY BUY %s at price: %f" % (time.ctime(regr_time), coin, regr_price)
            file.write(time.ctime(regr_time) + ": BUY at "+ str(regr_price) + "\n")
            file.flush()
        if down_cnt > len(mas)*settings.strenth_threshold:
            print "%s: SELL SELL SELL %s at price: %f" % (time.ctime(regr_time), coin, regr_price)
            file.write(time.ctime(regr_time) + ": SELL at "+ str(regr_price) + "\n")
            file.flush()

        return True

    except Exception as e:
        print "Error:", e
        return False

if __name__ == "__main__": 
    print "Regression for", coin
    regr_time = settings.regr_start_timestamp
    filename = "regression_" + coin + "_" + str(regr_time) + ".log"
    file = open(filename, "w")
    file.flush()
    now = int(time.time())
    while regr_time <= now:
        if main(regr_time, file):
            regr_time += 60*60 # move forward 1h
    file.close()