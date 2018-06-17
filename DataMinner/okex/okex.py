from lxml import etree
import DataMinner.config as config
import urllib3
import logging
log = logging.getLogger("bianceDataGet")
import DataMinner.common as common
import os


def get_data():
    result = []
    conn = urllib3.PoolManager()
    coin_list_url = "https://www.okex.com/marketList"
    #http = conn.request(method='get', url=coin_list_url).data
    http = common.phantom_get(url=coin_list_url)
    html = etree.HTML(http)
    usdt_tables = html.xpath("//div[@class='market-list-tickers']/table[@data-type='usdt']/tbody/tr/@data-product")
    btc_tables = html.xpath("//div[@class='market-list-tickers']/table[@data-type='btc']/tbody/tr/@data-product")
    eth_tables = html.xpath("//div[@class='market-list-tickers']/table[@data-type='eth']/tbody/tr/@data-product")
    okb_tables = html.xpath("//div[@class='market-list-tickers']/table[@data-type='okb']/tbody/tr/@data-product")
    total_num = len(usdt_tables+btc_tables+eth_tables+okb_tables)
    cur_num2 = 0
    for cur_pair in usdt_tables+btc_tables+eth_tables+okb_tables:
        cur_num2 = cur_num2 + 1
        names = cur_pair.split('_')
        coin_name = names[0]
        trade_coin_name = names[1]

        price_url = "https://www.okex.com/api/v1/ticker.do?symbol="+coin_name+"_"+trade_coin_name
        http = conn.request(method='get', url=price_url).data
        http = eval(http)
        cur_price = http['ticker']['last']

        deep_url = "https://www.okex.com/api/v1/depth.do?symbol="+coin_name+"_"+trade_coin_name
        http = eval(conn.request(method='get', url=deep_url).data)
        sell_list = []
        for cur_sell in http['asks']:
            cur_price = cur_sell[0]
            cur_amount = cur_sell[1]
            cur_deep = common.DeepUnit(price=cur_price, num=cur_amount)
            sell_list.append(cur_deep)
        buy_list = []
        for cur_buy in http['bids']:
            cur_price = cur_buy[0]
            cur_amount = cur_buy[1]
            cur_deep = common.DeepUnit(price=cur_price, num=cur_amount)
            buy_list.append(cur_deep)

        kline_url = "https://www.okex.com/api/v1/kline.do?symbol="+coin_name+"_"+trade_coin_name+"&type=1min"
        http = conn.request(method='get', url=kline_url).data
        http = eval(http)
        kline_list = []
        for cur_k in http:
            high = cur_k[2]
            low = cur_k[3]
            close = cur_k[4]
            cur_k_unit = common.KlineUnit(high=high, low=low, close=close)
            kline_list.append(cur_k_unit)

        cur_data = common.CoinData(coin_name, trade_coin_name, buy_list, sell_list, cur_price, kline_list)
        result.append(cur_data)
        log.warning("okex: "+coin_name + ":" + trade_coin_name + ":   " + str(cur_num2) + "/" + str(total_num))
    return result

if __name__ == "__main__":
    get_data()