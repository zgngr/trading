import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta



def split_fname(fname):
    # splitting ETHUSDT_2020-2021_4h.csv
    parts = fname.split('_')
    pair = parts[0]
    year_start = parts[1].split('-')[0]
    year_end = parts[1].split('-')[1]
    timeframe = parts[2][:-4]

    return pair, year_start, year_end, timeframe


def to_clsname(underscore):
    return underscore.title().replace('_', '')


def to_df(datapath):
    def resample(timeframe):
        df = pd.read_csv(datapath, index_col=0)
        df.set_index('close_time', inplace=True)
        df.index = pd.to_datetime(df.index, unit='ms')
        df = df.close.resample(timeframe).ohlc()
        return df

    return resample


def apply_filters(df, args):
    now = datetime.now()

    if args.last_month:
        f = df.index >= (now - relativedelta(months=args.last_month))
        df = df.loc[f]

    if args.last_days:
        f = df.index >= (now - relativedelta(days=args.last_days))
        df = df.loc[f]

    start = df.index[0].strftime("%Y-%m-%d")
    end = df.index[-1].strftime("%Y-%m-%d")

    return df, start, end
