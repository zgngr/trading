import backtest
import csv
import os
import helpers

commission_val = 0.01  # 0.04% taker fees binance usdt futures
portofolio = 10000000.0  # amount of money we start with
stake_val = 1
quantity = 0.10  # percentage to buy based on the current portofolio amount

start = '2017-01-01'
end = '2020-12-31'
strategies = ['super_trend']
periods = range(10, 30)
plot = False


for strategy in strategies:

    for data in os.listdir("./data"):

        datapath = 'data/' + data

        print('\n ------------ ', datapath)
        print()

        pair, year_start, year_end, timeframe = helpers.split_fname(data)
        outfname = f'result/{strategy}_{pair}_{year_start}-{year_end}_{timeframe}.csv'
        csvout = open(outfname, 'w', newline='')
        result_writer = csv.writer(csvout, delimiter=',')
        result_writer.writerow(['Pair', 'Timeframe', 'Start', 'End', 'Strategy', 'Period',
                               'Final value', '%', 'Total win', 'Total loss', 'SQN'])  # init header

        for period in periods:

            end_val, totalwin, totalloss, pnl_net, sqn = backtest.run(
                datapath, start, end, period, strategy, commission_val, portofolio, stake_val, quantity, plot)
            backtest.run(datapath, start, end, period, strategy,
                         commission_val, portofolio, stake_val, quantity, plot)

            profit = (pnl_net / portofolio) * 100

            print('data processed: %s, %s (Period %d) --- Ending Value: %.2f --- Total win/loss %d/%d, SQN %.2f' %
                  (datapath[5:], strategy, period, end_val, totalwin, totalloss, sqn))

            result_writer.writerow([pair, timeframe, start, end, strategy, period, round(
                end_val, 3), round(profit, 3), totalwin, totalloss, sqn])

        csvout.close()
