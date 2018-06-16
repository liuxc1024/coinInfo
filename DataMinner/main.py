import DataMinner.binance.binance as binance
import DataMinner.huobi.huobi as huobi
import DataMinner.gate.gate as gate
import DataMinner.zb.zb as zb


def get_data():
    huobi_result = huobi.get_data()
    gate_result = gate.get_data()
    bin_result = binance.get_data()
    zb_result = zb.get_data()

if __name__ == "__main__":
    get_data()