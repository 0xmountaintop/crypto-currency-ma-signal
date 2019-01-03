#!/usr/bin/env python

import settings
import urllib2
import json

# https://marketapi.blockmeta.com/apidocs/#/

def main():
    url = "https://marketapi.blockmeta.com/kline/%s/eth_usd/1hour?count=2&format_type=all" % settings.exchange
    print "getting data from: ", url
    contents = urllib2.urlopen(url).read()
    print "raw_data:\n", contents

    data = json.loads(contents)
    print data[0]["close"]

if __name__ == "__main__":
    main()