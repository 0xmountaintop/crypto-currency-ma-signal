#!/usr/bin/env python

import settings
import urllib2
import json

# https://marketapi.blockmeta.com/apidocs/#/
# curl -X GET "https://marketapi.blockmeta.com/flash/ticker?symbols=huobipro-btc_usd" -H "accept: application/json"

# 5
# 10
# 20
# 50
# 100
# 200


def main():
    for coin in settings.coin:
        kline_url = "https://marketapi.blockmeta.com/kline/%s/%s_usd/1hour?count=200&format_type=all" % (settings.exchange, coin)
        print "getting data from: ", kline_url
        contents = urllib2.urlopen(kline_url).read()
        # print "raw_data:\n", contents
        data = json.loads(contents)
        # print len(data)
        for d in data:
            print d["date"], d["close"]
            break

if __name__ == "__main__":
    main()

