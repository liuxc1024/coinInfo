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


def get_data(trade_coin_list):
    result = []
    connPool = urllib3.PoolManager()
    http = connPool.request(method='get', url="https://api.huobipro.com/v1/common/symbols")
    http = eval(http.data)

    total_num = len(http['data'])
    cur_num = 0
    for cur_coin in http['data']:
        cur_num = cur_num + 1
        cur_coin_name = cur_coin["base-currency"]
        trade_coin_name = cur_coin["quote-currency"]
        if trade_coin_name not in trade_coin_list:
            continue

        trade_url = "https://api.huobipro.com/market/detail?symbol="+cur_coin_name+trade_coin_name
        http = connPool.request(method='get', url=trade_url)
        http = eval(http.data)
        cur_price = http['tick']['close']

        sell_list = []
        buy_list = []
        deep_url = "https://api.huobipro.com/market/depth?symbol="+\
                   cur_coin_name+trade_coin_name+"&type=step1"
        http = connPool.request(method='get', url=deep_url)
        http = eval(http.data)
        cur_deep = http['tick']
        for cur_buy_deep in cur_deep['bids']:
            cur_price = cur_buy_deep[0]
            amount = cur_buy_deep[1]
            cur_deepcon = common.DeepUnit(price=cur_price, num=amount)
            buy_list.append(cur_deepcon)
        for cur_buy_deep in cur_deep['asks']:
            cur_price = cur_buy_deep[0]
            amount = cur_buy_deep[1]
            cur_deepcon = common.DeepUnit(price=cur_price, num=amount)
            sell_list.append(cur_deepcon)

        kline_list = []
        url = 'https://api.huobipro.com/market/history/kline?period=1min&size=200&symbol=' \
              + cur_coin_name + trade_coin_name
        kline_http = connPool.request(method='get', url=url)
        kline_con = eval(kline_http.data)
        for cur_k in kline_con['data']:
            cur_time = cur_k['id']
            high = cur_k['high']
            low = cur_k['low']
            close = cur_k['close']
            cur_k_data = common.KlineUnit(time=cur_time, high=high, low=low, close=close)
            kline_list.append(cur_k_data)
        cur_data = common.CoinData(coin_name=cur_coin_name, trade_coin_name=trade_coin_name, buy_list=buy_list,
                                   sell_list=sell_list, cur_price=cur_price, kline_list=kline_list)
        result.append(cur_data)
        log.warning("huobi %s_%s:  " %(cur_coin_name, trade_coin_name) + str(cur_num) + "/" + str(total_num))
    return result


if __name__ == "__main__":
    get_data()
