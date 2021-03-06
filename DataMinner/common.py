import os
import shutil
import time


class DeepUnit:
    def __init__(self, price, num):
        self.price = price
        self.num = num


class KlineUnit:
    def __init__(self, time, high, low, close):
        self.time = time
        self.high = high
        self.low = low
        self.close = close


class CoinData:
    def __init__(self, coin_name, trade_coin_name, buy_list, sell_list, cur_price, kline_list):
        self.coin_name = coin_name
        self.trade_coin_name = trade_coin_name
        self.buy_list = buy_list
        self.sell_list = sell_list
        self.cur_price = cur_price
        self.kline_list = kline_list


class MediaCoinPrice:
    def __init__(self, coin_name, type, price):
        self.coin_name = coin_name
        self.type = type
        self.price = price


def phantom_get(url, is_wait=False):
    url_file = open('d:/url.txt', 'w')
    if os.path.exists('d:/flag'):
        os.remove('d:/flag')
    url_file.write(url)
    url_file.flush()
    url_file.close()
    if is_wait:
        js_name = "phantomGetWaitTime"
    else:
        js_name = "phantomGet"
    if not os.path.exists("d:/"+js_name+".js"):
        cur_path = os.path.dirname(__file__)
        shutil.copy(cur_path+"\\"+js_name+".js", "d:/"+js_name+".js")
        time.sleep(1)
    os.system("phantomjs d:/"+js_name+".js")
    ok = False
    for i in range(300):
        if os.path.exists('d:/flag'):
            os.remove('d:/flag')
            ok = True
            break
        else:
            time.sleep(1)
    if ok:
        file = open('d:/output.html', 'r', encoding='utf-8')
        return file.read()
    else:
        return None


if __name__ == "__main__":
    result = phantom_get("https://www.huobi.com")
    print(result)
