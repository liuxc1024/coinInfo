import os
import shutil
import time


class DeepUnit:
    def __init__(self, price, num):
        self.price = price
        self.num = num


class KlineUnit:
    def __init__(self, high, low, close):
        self.high = high
        self.low = low
        self.close = close


class CoinData:
    def __init__(self, coin_name, trade_coin_name, buy_list, sell_list, cur_price, kline_list):
        self.coin_name = coin_name
        self.trade_coin_nam = trade_coin_name
        self.buy_list = buy_list
        self.sell_list = sell_list
        self.cur_price = cur_price
        self.kline_list = kline_list


def phantom_get(url):
    url_file = open('d:/url.txt', 'w')
    url_file.write(url)
    url_file.flush()
    url_file.close()
    shutil.copy("phantomGet.js", "d:/phantomGet.js")
    time.sleep(1)
    os.system("phantomjs d:/phantomGet.js")


if __name__ == "__main__":
    phantom_get("https://www.baidu.com")
