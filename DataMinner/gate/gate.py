import urllib3
import logging
log = logging.getLogger("bianceDataGet")
import DataMinner.common as common


def get_data():
    result = []
    connPool = urllib3.PoolManager()
    http = connPool.request(method='get', url="https://data.gateio.io/api2/1/tickers")
    con = eval(http.data)
    total_num = len(con.keys())
    cur_num = 0
    for cur_pair in con.keys():
        cur_num = cur_num + 1
        coin_names = cur_pair.split('_')
        coin_name = coin_names[0]
        trade_coin_name = coin_names[1]
        cur_price = con[cur_pair]['last']
        # get deep
        deep_url = "https://data.gateio.io/api2/1/orderBook/" + cur_pair
        http = connPool.request(method='get', url=deep_url)
        deep_con = eval(http.data)
        sell_con_list = deep_con['asks']
        buy_con_list = deep_con['bids']
        sell_list = []
        buy_list = []
        for cur_sell in sell_con_list:
            price = cur_sell[0]
            amount = cur_sell[1]
            cur_deep = common.DeepUnit(price=price, num=amount)
            sell_list.append(cur_deep)
        for cur_buy in buy_con_list:
            price = cur_buy[0]
            amount = cur_buy[1]
            cur_deep = common.DeepUnit(price=price, num=amount)
            buy_list.append(cur_deep)
        kline_list = []
        kline_url = "https://data.gateio.io/api2/1/candlestick2/" \
                    "%s?group_sec=30&range_hour=1" % cur_pair
        kline_data = eval(connPool.request(method='get', url=kline_url).data)
        for cur_kline in kline_data["data"]:
            high = cur_kline[3]
            low = cur_kline[4]
            close = cur_kline[2]
            cur_k = common.KlineUnit(high, low, close)
            kline_list.append(cur_k)
        cur_data = common.CoinData(coin_name, trade_coin_name, buy_list, sell_list, cur_price, kline_list)
        log.warning("gate :" + cur_pair + "  " + str(cur_num) + "/" + str(total_num))
        result.append(cur_data)
    return result

if __name__ == "__main__":
    get_data()
