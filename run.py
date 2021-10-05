import argparse
import os
import csv
import fnmatch
import importlib
import pandas as pd
import helpers
import backtrader as bt
import warnings

import helpers

pd.set_option('display.max_rows', None)
warnings.filterwarnings('ignore')

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--pair", type=str, default='ETHUSDT')
    parser.add_argument("--lookback", type=str, default='100')
    parser.add_argument("--interval", type=str, default='1d')
    parser.add_argument("--strategy", type=str, default='buy_hold')
    parser.add_argument("--strategy_param", type=int, default=14)
    args = parser.parse_args()

    pair = args.pair
    lookback = args.lookback
    interval = args.interval
    strategy = args.strategy
    strategy_param = args.strategy_param

    df = helpers.getdaydata(pair, interval, lookback)
    start, end = helpers.start_end_dates(df)

    mod = importlib.import_module(f'strategies.{strategy}')

    csvout = open(f'{strategy}.csv', 'w', newline='')
    result_writer = csv.writer(csvout, delimiter=',')
    result_writer.writerow(['Symbol', 'Start', 'End', 'Strategy', 'Initial value', 'Final value', 'ROI %'])

    cerebro = bt.Cerebro()
    cerebro.adddata(bt.feeds.PandasData(dataname=mod.apply(df, strategy_param)))
    cerebro.addstrategy(strategy=getattr(mod, helpers.to_clsname(strategy)), verbose=True)

    initial = cerebro.broker.get_cash()
    cerebro.run()
    final = cerebro.broker.get_value()
    roi = (final / initial) - 1.0

    result_writer.writerow([pair, start, end, args.strategy, initial, round(final), round(roi, 3)])
    csvout.close()

    print(f'Symbol:     {pair}')
    print('ROI:        {:.2f}%'.format(100.0 * roi))
    print('---------------------------------')

