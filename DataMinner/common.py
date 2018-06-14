import pandas as pd
import logging as log


def get_df_from_address(site_addr):
    if site_addr is None:
        log.error("site addr error")


if __name__ == "__main__":
    get_df_from_address(None)