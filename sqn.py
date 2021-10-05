import argparse
import csv
import fnmatch
import os
from datetime import datetime

import backtest
import helpers

strategy_params = range(1, 30)

parser = argparse.ArgumentParser()
parser.add_argument("--pair", type=str, default='BTCUSDT')
parser.add_argument("--lookback", type=str, default='100')
parser.add_argument("--strategy", type=str, default='super_trend')
args = parser.parse_args()

# intervals = ['15m', '30m', '1h', '2h', '4h', '6h', '1d']
intervals = ['1d']

pair = args.pair
lookback = args.lookback
strategy = args.strategy

for interval in reversed(intervals):

    df = helpers.getdaydata(pair, interval, lookback)
    start, end = helpers.start_end_dates(df)

    output_name = f'{strategy}_{pair}_{start}_{end}_{interval}.csv'
    print('\n ------------ ', f'{output_name}')
    print()

    outfname = f'result/{output_name}'
    csvout = open(outfname, 'w', newline='')
    result_writer = csv.writer(csvout, delimiter=',')
    result_writer.writerow(['Pair', 'Interval', 'Start', 'End', 'Strategy', 'Parameter',
                            'Final value', '%', 'Total win', 'Total loss', 'SQN'])

    for strategy_param in strategy_params:

        end_val, totalwin, totalloss, pnl_net, sqn = backtest.run(df, strategy_param, strategy)

        profit = (pnl_net / 10000.0) * 100

        print('processing: %s, %s (Parameter %d) --- Ending Value: %.2f --- Total win/loss %d/%d, SQN %.2f' %
                (outfname, strategy, strategy_param, end_val, totalwin, totalloss, sqn))

        result_writer.writerow(
            [pair, interval, start, end, strategy, strategy_param, round(end_val, 3), round(profit, 3), totalwin, totalloss, sqn])

    csvout.close()
