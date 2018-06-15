from lxml import etree
import DataMinner.config as config
import urllib3
import logging
log = logging.getLogger("huobiDataGet")
import DataMinner.common as common


def get_coin_list(html_content):
    html_content = html_content.decode()\
                .replace('false', '\"false\"')\
                .replace('true', '\"true\"')
    coin_list_dic = eval(html_content)
    return coin_list_dic["data"]


def get_data():
    connPool = urllib3.PoolManager()
    http = connPool.request(method='get', url=config.SITE_MAIN_ADDR["huobi"] +
           "/-/x/pro/v1/settings/symbols?r=y5syhk7spca4i1i270t3xr&language=en-us")
    coin_list = get_coin_list(http.data)

    print(len(coin_list))
    for cur_coin in coin_list:
        cur_coin_name = cur_coin["base-currency"]
        trade_coin_name = cur_coin["quote-currency"]
        print(cur_coin_name + ":" + trade_coin_name)

        trade_url = "https://www.huobi.com/coin_coin/exchange/#s="+cur_coin_name+"_"+trade_coin_name
        http = common.phantom_get(trade_url)
        html = etree.HTML(http)
        cur_price = html.xpath("//span[@class='ticker_close']")[0].text
        print(cur_price)


if __name__ == "__main__":
    get_data()
