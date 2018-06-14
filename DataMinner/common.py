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
