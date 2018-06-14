from lxml import etree
import DataMinner.config as config
import urllib3
import logging
log = logging.getLogger("bianceDataGet")
import DataMinner.common as common


def get_trade_url_list(html_content):
    btc_trade_list_url = []
    try:
        temp = etree.HTML(html_content)
        find = temp.xpath("//div[@class='s1ipci53-0 iFQrj']/a[@href]//@href")
        for cur_find in find:
            btc_trade_list_url.append(cur_find)
        return btc_trade_list_url
    except :
        log.error("get btc trade list from binance error")
        return btc_trade_list_url


def get_coin_data_from_tradecoin(tradecoin):
    tradecoin = tradecoin.split("/")[-1]
    names = tradecoin.split('_')
    tradecoin = tradecoin.replace('_', '')
    connPool = urllib3.PoolManager()
    deep_url = "https://www.binance.com/api/v1/depth?symbol=" + tradecoin
    # 1min kline
    kline_url = "https://www.binance.com/api/v1/klines?symbol="+tradecoin+"&interval=1m"
    deep_data = eval(connPool.request(method='get', url=deep_url).data)
    kline_data = eval(connPool.request(method='get', url=kline_url).data)
    connPool.clear()
    coin_name = names[0]
    trade_coin_name = names[1]
    sell_list = []
    buy_list = []
    kline_list = []
    for cur_sell in deep_data["asks"]:
        cur_price = cur_sell[0]
        cur_num = cur_sell[1]
        cur_deep_unit = common.DeepUnit(cur_price, cur_num)
        sell_list.append(cur_deep_unit)
    for cur_buy in deep_data["bids"]:
        cur_price = cur_buy[0]
        cur_num = cur_buy[1]
        cur_deep_unit = common.DeepUnit(cur_price, cur_num)
        buy_list.append(cur_deep_unit)
    for cur_kline in kline_data:
        cur_high = cur_kline[2]
        cur_low = cur_kline[3]
        cur_close = cur_kline[4]
        cur_kline_unit = common.KlineUnit(high=cur_high, low=cur_low, close=cur_close)
        kline_list.append(cur_kline_unit)
    cur_price = kline_data[-1][4]
    cur_data = common.CoinData(coin_name, trade_coin_name, buy_list, sell_list, cur_price, kline_list)
    return cur_data


def get_data():
    # get btc trade list
    connPool = urllib3.PoolManager()
    http = connPool.request(method='get', url=config.SITE_MAIN_ADDR["binance"] + "/cn")
    btc_trade_list = get_trade_url_list(http.data)
    connPool.clear()

    # get bnb trade list
    file = open("binanceBnb.txt", encoding="utf-8")
    content = file.read()
    bnb_trade_list = get_trade_url_list(content)

    # get eth trade list
    file = open("binanceEth.txt", encoding="utf-8")
    content = file.read()
    eth_trade_list = get_trade_url_list(content)

    # get usdt trade list
    file = open("binanceUsdt.txt", encoding="utf-8")
    content = file.read()
    usdt_trade_list = get_trade_url_list(content)

    result = []
    for cur_btc_coin in btc_trade_list + bnb_trade_list + eth_trade_list + usdt_trade_list:
        try:
            cur_data = get_coin_data_from_tradecoin(cur_btc_coin)
        except:
            log.error("getdata error of:  " + cur_btc_coin)
        else:
            log.info("getdata success of:" + cur_btc_coin)
            print(cur_btc_coin + ":: get data OK")
            result.append(cur_data)
    return result

if __name__ == "__main__":
    result = get_data()
    print(len(result))
