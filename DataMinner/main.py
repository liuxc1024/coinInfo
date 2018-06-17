import DataMinner.binance.binance as binance
import DataMinner.huobi.huobi as huobi
import DataMinner.gate.gate as gate
import DataMinner.zb.zb as zb
import DataMinner.okex.okex as okex
import time


def get_data():
    start_sec = time.localtime()
    huobi_result = huobi.get_data()
    gate_result = gate.get_data()
    bin_result = binance.get_data()
    zb_result = zb.get_data()
    okex_result = okex.get_data()
    end_sec = time.localtime()
    print(start_sec)
    print(end_sec)

if __name__ == "__main__":
    get_data()