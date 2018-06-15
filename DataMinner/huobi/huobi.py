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
    connPool.clear()

    for cur_coin in coin_list:
        cur_coin_name = cur_coin["base-currency"]
        trade_coin_name = cur_coin["quote-currency"]
        print(cur_coin_name + ":" + trade_coin_name)
        # https://www.huobi.com/wicc_usdt/depth/?trade=exchange
        deep_url = "https://www.huobi.com/"+cur_coin_name+"_"+trade_coin_name+"/depth/?trade=exchange"


if __name__ == "__main__":
    get_data()
