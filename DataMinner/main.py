import DataMinner.binance.binance as binance
import DataMinner.huobi.huobi as huobi
import DataMinner.gate.gate as gate
import DataMinner.zb.zb as zb
import DataMinner.okex.okex as okex
import time
import DataMinner.getcoinpullgetlist as getpullget

Data = None
GetPullGetData = None


def get_data():
    start_sec = time.localtime()
    zb_result = zb.get_data()
    huobi_result = huobi.get_data()
    gate_result = gate.get_data()
    binance_result = binance.get_data()
    okex_result = okex.get_data()
    end_sec = time.localtime()
    print(start_sec)
    print(end_sec)
    return {
        "zd": zb_result,
        "huobi": huobi_result,
        "gate_result": gate_result,
        "binance_result": binance_result,
        "okex_result": okex_result,
    }


def init():
    global Data
    Data = get_data()
    global GetPullGetData
    GetPullGetData = getpullget.get_pullget_table()


def check_pull(site, coin):
    return getpullget.check_pull(GetPullGetData, site, coin)


def check_get(site, coin):
    return getpullget.check_get(GetPullGetData, site, coin)

if __name__ == "__main__":
    get_data()
