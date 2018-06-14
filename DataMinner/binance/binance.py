from lxml import etree
import DataMinner.config as config
import urllib3
import logging as log


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


def get_data():
    # get btc trade list
    connPool = urllib3.PoolManager()
    http = connPool.request(method='get', url=config.SITE_MAIN_ADDR["binance"] + "/cn")
    btc_trade_list = get_trade_url_list(http.data)

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


if __name__ == "__main__":
    get_data()
