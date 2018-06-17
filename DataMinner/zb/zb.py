from lxml import etree
import DataMinner.config as config
import urllib3
import logging
import time
log = logging.getLogger("zbDataGet")
import DataMinner.common as common
false = False
true = True


def get_data(trade_coin_list):
    result = []
    conn_pool = urllib3.PoolManager()
    pairs_url = "http://api.zb.com/data/v1/markets"
    con = conn_pool.request(method='get', url=pairs_url)
    con = eval(con.data)

    all_price_url = "http://api.zb.com/data/v1/allTicker"
    all_price_con = eval(conn_pool.request(method='get', url=all_price_url).data)
    total_num = len(con.keys())
    cur_num2 = 0
    for cur_pair in con.keys():
        cur_num2 = cur_num2 + 1
        names = cur_pair.split('_')
        coin_name = names[0]
        trade_coin_name = names[1]
        if trade_coin_name not in trade_coin_list:
            continue
        cur_price = float(all_price_con[coin_name+trade_coin_name]['last'])
        deep_url = "http://api.zb.com/data/v1/depth?market=" + coin_name + "_" + trade_coin_name + "&size=20"
        deep_http = conn_pool.request(method='get', url=deep_url)
        deep_con = eval(deep_http.data)
        sell_list = []
        for cur_sell in deep_con['asks']:
            cur_price = cur_sell[0]
            cur_num = cur_sell[1]
            cur_sell_unit = common.DeepUnit(price=cur_price, num=cur_num)
            sell_list.append(cur_sell_unit)

        buy_list = []
        for cur_buy in deep_con['bids']:
            cur_price = cur_buy[0]
            cur_num = cur_buy[1]
            cur_buy_unit = common.DeepUnit(price=cur_price, num=cur_num)
            buy_list.append(cur_buy_unit)

        # get kline
        kline_url = "http://api.zb.com/data/v1/kline?market="+coin_name+"_"+trade_coin_name+"&type=1min"
        con = eval(conn_pool.request(method='get', url=kline_url).data)
        kline_list = []
        time.sleep(1)
        ok_flag = False
        for i in range(10):
            try:
                con['data']
                ok_flag = True
            except:
                time.sleep(5*i)
                con = eval(conn_pool.request(method='get', url=kline_url).data)
            else:
                break
        if not ok_flag:
            continue
        for cur_k in con['data']:
            cur_time = cur_k[0]
            high = cur_k[2]
            low = cur_k[3]
            close = cur_k[4]
            cur_k_unit = common.KlineUnit(time=cur_time, high=high, low=low, close=close)
            kline_list.append(cur_k_unit)
        cur_data = common.CoinData(coin_name, trade_coin_name, buy_list, sell_list, cur_price, kline_list)
        log.warning("zb:" + coin_name + ":" + trade_coin_name + ":  " + str(cur_num2) + "/" + str(total_num))
        result.append(cur_data)
    return result

if __name__ == "__main__":
    get_data()