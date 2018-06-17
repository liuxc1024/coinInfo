import DataMinner.main as data


def time_average_predict(alpha, kline_list):
    if len(kline_list) < 2:
        return None
    if kline_list[0].time > kline_list[1].time:
        kline_list.reverse()
    pre_com = kline_list[0].close
    for i in range(1, len(kline_list)):
        pre_com = pre_com * (1-alpha) + kline_list[i].close * alpha
    return pre_com


def deep_intersect_gain(sell_list, buy_list):
    cur_max_buy = buy_list[0].price
    for i in range(1, len(buy_list)):
        if buy_list[i].price > cur_max_buy:
            cur_max_buy = buy_list[i].price
    cur_min_sell = sell_list[0].price
    for i in range(1, len(sell_list)):
        if sell_list[i].price < cur_min_sell:
            cur_min_sell = sell_list[i].price
    buy_check_mount = 0
    for i in range(len(buy_list)):
        cur_price = buy_list[i].price
        cur_amount = buy_list[i].num
        if cur_min_sell <= cur_price <= cur_max_buy:
            buy_check_mount = buy_check_mount + cur_price * cur_amount
    sell_check_mount = 0
    for i in range(len(sell_list)):
        cur_price = sell_list[i].price
        cur_amount = sell_list[i].num
        if cur_min_sell <= cur_price <= cur_max_buy:
            sell_check_mount = sell_check_mount + cur_price * cur_amount
    if buy_check_mount < sell_check_mount:
        return buy_check_mount
    else:
        return sell_check_mount


def compute_overgain_ratio(buy_price, sell_price):
    if buy_price == 0:
        return 0
    return (sell_price-buy_price)/buy_price*100


if __name__ == "__main__":
    data.init(["gate"])
    cur_data = data.Data['gate'][0]
    cur_kline = cur_data.kline_list
    pre = time_average_predict(0.6, cur_kline)
    None