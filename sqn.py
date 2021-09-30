import argparse
import csv
import fnmatch
import os
from datetime import datetime

from dateutil.relativedelta import relativedelta

import backtest
import helpers

commission_val = 0.01  # 0.04% taker fees binance usdt futures
portofolio = 10000000.0  # amount of money we start with
stake_val = 1
quantity = 0.10  # percentage to buy based on the current portofolio amount
plot = False

strategies = ['super_trend']
periods = range(10, 30)

parser = argparse.ArgumentParser()
parser.add_argument("--grep", type=str, default='*.csv')
parser.add_argument("--data_path", type=str, default='data/')
parser.add_argument("--last_month", type=int, default=None)
parser.add_argument("--last_days", type=int, default=None)
args = parser.parse_args()

time_frames = ['15min', '30min', '1h', '2h',
               '4h', '6h', '8h', '1d', '2d', '3d', '1w']

for strategy in strategies:

    for data in os.listdir(args.data_path):

        if not fnmatch.fnmatch(data, args.grep):
            continue

        sample = helpers.to_df(args.data_path + data)
        pair, _, _, _ = helpers.split_fname(data)

        print('\n ------------ ', f'{data}')
        print()

        for time_frame in reversed(time_frames):

            df = sample(time_frame)
            df, start, end = helpers.apply_filters(df, args)

            outfname = f'result/{strategy}_{pair}_{start}_{end}_{time_frame}.csv'
            csvout = open(outfname, 'w', newline='')
            result_writer = csv.writer(csvout, delimiter=',')
            result_writer.writerow(['Pair', 'Timeframe', 'Start', 'End', 'Strategy', 'Period',
                                    'Final value', '%', 'Total win', 'Total loss', 'SQN'])  # init header

            for period in periods:

                end_val, totalwin, totalloss, pnl_net, sqn = backtest.run(
                    df, period, strategy, commission_val, portofolio, stake_val, quantity, plot)

                profit = (pnl_net / portofolio) * 100

                print('processing: %s, %s (Period %d) --- Ending Value: %.2f --- Total win/loss %d/%d, SQN %.2f' %
                      (outfname, strategy, period, end_val, totalwin, totalloss, sqn))

                result_writer.writerow([pair, time_frame, start, end, strategy, period, round(
                    end_val, 3), round(profit, 3), totalwin, totalloss, sqn])

            csvout.close()
