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
    except:
        log.error("get btc trade list from binance error")
        return btc_trade_list_url


def get_btc_trade_url_list():
    # get btc trade list
    connPool = urllib3.PoolManager()
    http = connPool.request(method='get', url=config.SITE_MAIN_ADDR["binance"] + "/cn")
    temp = etree.HTML(http.data)
    btc_trade_list = get_trade_url_list(temp)

    # get bnb trade list
    file = open("d:/coin/coinInfo/DataMinner/binanceBnb.txt", encoding="utf-8")
    content = file.read()
    bnb_trade_list = get_trade_url_list(content)

    # get


if __name__ == "__main__":
    None