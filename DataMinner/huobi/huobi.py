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


def get_deep_list_from_ele(depth_ele):
    result_list = []
    cur_html = etree.HTML(etree.tostring(depth_ele))
    inner_divs = cur_html.xpath("//div[@class='inner']")
    for cur_div in inner_divs:
        cur_h = etree.HTML(etree.tostring(cur_div))
        spans = cur_h.xpath("//span")
        cur_price = spans[1].text
        cur_amount = spans[3].text
        cur_deep = common.DeepUnit(price=cur_price, num=cur_amount)
        result_list.append(cur_deep)
    return result_list


def get_data():
    result = []
    connPool = urllib3.PoolManager()
    http = connPool.request(method='get', url=config.SITE_MAIN_ADDR["huobi"] +
           "/-/x/pro/v1/settings/symbols?r=y5syhk7spca4i1i270t3xr&language=en-us")
    coin_list = get_coin_list(http.data)

    total_num = len(coin_list)
    cur_num = 0
    for cur_coin in coin_list:
        cur_num = cur_num + 1
        cur_coin_name = cur_coin["base-currency"]
        trade_coin_name = cur_coin["quote-currency"]

        trade_url = "https://www.huobi.com/coin_coin/exchange/#s="+cur_coin_name+"_"+trade_coin_name
        http = common.phantom_get(trade_url)
        html = etree.HTML(http)
        cur_price = html.xpath("//span[@id='tickerClose']")[0].text

        depth_ele = html.xpath("//div[@id='market_depth']//dl")
        sell_list = get_deep_list_from_ele(depth_ele[0])
        buy_list = get_deep_list_from_ele(depth_ele[1])

        kline_list = []
        cur_data = common.CoinData(coin_name=cur_coin_name, trade_coin_name=trade_coin_name, buy_list=buy_list,
                                   sell_list=sell_list, cur_price=cur_price, kline_list=kline_list)
        result.append(cur_data)
        log.warning("huobi %s_%s:  " %(cur_coin_name, trade_coin_name) + str(cur_num) + "/" + str(total_num))
    return result


if __name__ == "__main__":
    get_data()
