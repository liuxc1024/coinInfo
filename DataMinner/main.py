import DataMinner.binance.binance as binance
import DataMinner.huobi.huobi as huobi


def get_data():
    huobi_result = huobi.get_data()
    bin_result = binance.get_data()

if __name__ == "__main__":
    get_data()