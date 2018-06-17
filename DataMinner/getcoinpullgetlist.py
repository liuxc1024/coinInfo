import os
import pandas as pd


def get_pullget_table():
    config_file_path = os.path.dirname(__file__) + "/coinpullget.xlsx"
    dfs = pd.read_excel(config_file_path, sheet_name=None)
    return dfs


def check_pull(dfs, sitename, coinname):
    coinname = coinname.upper()
    cur_df = dfs[sitename]
    if cur_df[cur_df['coin_name']==coinname].empty:
        return False
    if cur_df[cur_df['coin_name']==coinname]['pull'].values[0] == 1:
        return True
    else:
        return False


def check_get(dfs, sitename, coinname):
    coinname = coinname.upper()
    cur_df = dfs[sitename]
    if cur_df[cur_df['coin_name']==coinname].empty:
        return False
    if cur_df[cur_df['coin_name']==coinname]['get'].values[0] == 1:
        return True
    else:
        return False


if __name__ == "__main__":
    dfs = get_pullget_table()
    check_pull(dfs, 'okex', 'btc')
    check_get(dfs, 'okex', 'btc')
