import DataMinner.binance.binance as binance
import DataMinner.huobi.huobi as huobi
import DataMinner.gate.gate as gate
import DataMinner.zb.zb as zb
import DataMinner.okex.okex as okex
import time
import DataMinner.getcoinpullgetlist as getpullget

Data = None
GetPullGetData = None


def get_data(site_list, trade_coin_list):
    result = {}
    if len(site_list) == 0:
        site_list = ['binance', 'zb', 'okex', 'huobi', 'gate']
    start_sec = time.localtime()
    for cur_site in site_list:
        if cur_site == "zb":
            zb_result = zb.get_data(trade_coin_list)
            result['zb'] = zb_result
        if cur_site == "huobi":
            huobi_result = huobi.get_data(trade_coin_list)
            result['huobi'] = huobi_result
        if cur_site == "gate":
            gate_result = gate.get_data(trade_coin_list)
            result['gate'] = gate_result
        if cur_site == "binance":
            binance_result = binance.get_data(trade_coin_list)
            result['binance'] = binance_result
        if cur_site == "okex":
            okex_result = okex.get_data(trade_coin_list)
            result['okex'] = okex_result
    end_sec = time.localtime()
    print(start_sec)
    print(end_sec)
    return result


def init(site_list=[], trade_coin_list=[]):
    global GetPullGetData
    GetPullGetData = getpullget.get_pullget_table()
    global Data
    Data = get_data(site_list, trade_coin_list)


def check_pull(site, coin):
    return getpullget.check_pull(GetPullGetData, site, coin)


def check_get(site, coin):
    return getpullget.check_get(GetPullGetData, site, coin)


def select_coinlist_buy_trade_coin(coin_data_list, trade_coin_name):
    result = []
    for cur_data in coin_data_list:
        if cur_data.trade_coin_name == trade_coin_name:
            result.append(cur_data)
    return result


if __name__ == "__main__":
    get_data()
