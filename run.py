import argparse
import os
import csv
import fnmatch
import importlib
import pandas as pd
import helpers
import backtrader as bt
import warnings

pd.set_option('display.max_rows', None)
warnings.filterwarnings('ignore')

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--strategy", type=str, default='buy_hold')
    parser.add_argument("--data_path", type=str, default='data/')
    parser.add_argument("--grep", type=str, default='*_1d.csv')
    parser.add_argument("--last_month", type=int, default=None)
    parser.add_argument("--last_days", type=int, default=None)
    args = parser.parse_args()

    mod = importlib.import_module(
        f'strategies.{args.strategy}')

    csvout = open(f'{args.strategy}.csv', 'w', newline='')
    result_writer = csv.writer(csvout, delimiter=',')
    result_writer.writerow(['Symbol', 'Start', 'End',
                            'Strategy', 'Initial value', 'Final value', 'ROI %'])  # init header

    for f in os.listdir(args.data_path):

        if not fnmatch.fnmatch(f, args.grep):
            continue

        try:

            df = pd.read_csv(f'{args.data_path}/{f}', index_col=0)
            df.set_index('close_time', inplace=True)
            df.index = pd.to_datetime(df.index, unit='ms')
            df, start, end = helpers.apply_filters(df, args)

            cerebro = bt.Cerebro()
            cerebro.adddata(bt.feeds.PandasData(dataname=mod.apply(df)))
            cerebro.addstrategy(strategy=getattr(
                mod, helpers.to_clsname(args.strategy)), verbose=True)

            initial = cerebro.broker.get_cash()
            cerebro.run()
            final = cerebro.broker.get_value()
            roi = (final / initial) - 1.0

            pair, _, _, _ = helpers.split_fname(f)

            result_writer.writerow(
                [pair, start, end, args.strategy, initial, round(final), round(roi, 3)])

            print(f'Symbol:     {f}')
            print('ROI:        {:.2f}%'.format(100.0 * roi))
            print('---------------------------------')

        except:
            print(f'problem with {f}')
            csvout.close()

    csvout.close()
