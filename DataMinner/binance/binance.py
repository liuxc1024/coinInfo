from lxml import etree
import DataMinner.config as config
import urllib3
import logging as log
import DataMinner.common as common


def get_trade_url_list(html_content):
    btc_trade_list_url = []
    try:
        temp = etree.HTML(html_content)
        find = temp.xpath("//div[@class='s1ipci53-0 iFQrj']/a[@href]//@href")
        for cur_find in find:
            btc_trade_list_url.append(config.SITE_MAIN_ADDR["binance"] + cur_find)
        return btc_trade_list_url
    except :
        log.error("get btc trade list from binance error")
        return btc_trade_list_url


def get_coin_data_from_url(url):
    connPool = urllib3.PoolManager()
    http = connPool.request(method='get', url=url)
    html = etree.HTML(http.data)
    cur_node = html.xpath("//div[@class='s1d711xa-1 jgsWFi s1p4en3j-0 ghSPYW s62mpio-0 ecRduS']/div")[0]
    cur_node = cur_node.xpath("/span")
    print(cur_node)


def get_data():
    # get btc trade list
    connPool = urllib3.PoolManager()
    http = connPool.request(method='get', url=config.SITE_MAIN_ADDR["binance"] + "/cn")
    btc_trade_list = get_trade_url_list(http.data)
    connPool.clear()

    # get bnb trade list
    file = open("d:/coin/coinInfo/DataMinner/binance/binanceBnb.txt", encoding="utf-8")
    content = file.read()
    bnb_trade_list = get_trade_url_list(content)

    # get eth trade list
    file = open("d:/coin/coinInfo/DataMinner/binance/binanceEth.txt", encoding="utf-8")
    content = file.read()
    eth_trade_list = get_trade_url_list(content)

    # get usdt trade list
    file = open("d:/coin/coinInfo/DataMinner/binance/binanceUsdt.txt", encoding="utf-8")
    content = file.read()
    usdt_trade_list = get_trade_url_list(content)

    for cur_btc_coin_url in btc_trade_list:
        get_coin_data_from_url(cur_btc_coin_url)


if __name__ == "__main__":
    get_data()
