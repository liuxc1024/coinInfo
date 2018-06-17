import DataMinner.main as Data
import Model.common as model
from itertools import combinations


while True:
    site_list = ['binance', 'gate', 'huobi', 'zb', 'okex']
    trade_coin_list = ['usdt']
    Data.init(site_list, trade_coin_list)

    cur_comb_list = list(combinations(site_list, 2))
    for cur_comb in cur_comb_list:
        cur_first_site = cur_comb[0]
        cur_sec_site = cur_comb[1]
        gate_data = Data.select_coinlist_buy_trade_coin(Data.Data[cur_first_site], 'usdt')
        huobi_data = Data.select_coinlist_buy_trade_coin(Data.Data[cur_sec_site], 'usdt')
        for cur_gate in gate_data:
            for cur_huobi in huobi_data:
                if cur_gate.coin_name == cur_huobi.coin_name:
                    #cur_gate_pre_price = model.time_average_predict(0.6, cur_gate.kline_list)
                    #cur_huobi_pre_price = model.time_average_predict(0.6, cur_huobi.kline_list)
                    cur_gate_pre_price = cur_gate.cur_price
                    cur_huobi_pre_price = cur_huobi.cur_price
                    if cur_gate_pre_price > cur_huobi_pre_price:
                        if Data.check_get('huobi', cur_huobi.coin_name) == True \
                                and Data.check_pull('gate', cur_gate.coin_name) == True:
                            sell_list = cur_huobi.sell_list
                            buy_list = cur_gate.buy_list
                            deep_interact = model.deep_intersect_gain(sell_list, buy_list)
                            ratio = model.compute_overgain_ratio(cur_huobi_pre_price, cur_gate_pre_price)
                            print("coin:" + cur_gate.coin_name + "-" + "buy:" + cur_sec_site
                                  + "   sell:" + cur_first_site + "   data:"
                                  + str(ratio) + "    " + str(deep_interact))
                    else:
                        if Data.check_pull('huobi', cur_huobi.coin_name) == True \
                                and Data.check_get('gate', cur_gate.coin_name) == True:
                            sell_list = cur_gate.sell_list
                            buy_list = cur_huobi.buy_list
                            deep_interact = model.deep_intersect_gain(sell_list, buy_list)
                            ratio = model.compute_overgain_ratio(cur_gate_pre_price, cur_huobi_pre_price)
                            print("coin:" + cur_gate.coin_name + "-" + "buy:" + cur_first_site
                                  + "   sell:" + cur_sec_site + "   data:"
                                  + str(ratio) + "    " + str(deep_interact))
