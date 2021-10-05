import backtrader as bt
import pandas as pd
import math


class SuperTrend(bt.Strategy):

    params = dict(
        verbose=False
    )

    def __init__(self):
        self.order = None
        self.val_start = self.broker.get_cash()
        self.dataclose = self.datas[0].close
        self.data_openinterest = self.datas[0].openinterest

    def log(self, txt, dt=None):
        if self.p.verbose:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def next(self):
        if not self.position:
            if self.data_openinterest[0] == True and self.data_openinterest[-1] == False:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.size = math.floor((0.95 * self.broker.cash) / self.dataclose[0])
                self.buy(size=self.size)
        else:
            if self.data_openinterest[0] == False and self.data_openinterest[-1] == True:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.sell(size=self.size)


def apply(df, atr_period=14, atr_multiplier=3):

    df['previous_close'] = df['Close'].shift(1)
    df['high-low'] = df['High'] - df['Low']
    df['high-pc'] = abs(df['High'] - df['previous_close'])
    df['low-pc'] = abs(df['Low'] - df['previous_close'])
    df['tr'] = df[['high-low', 'high-pc', 'low-pc']].max(axis=1)

    # https://www.investopedia.com/terms/a/atr.asp
    # Average true range a.k.a ATR
    df['atr'] = df['tr'].rolling(atr_period).mean()

    hl2 = (df['High'] + df['Low']) / 2

    # Basic bands
    df['upperband'] = hl2 + (atr_multiplier * df['atr'])
    df['lowerband'] = hl2 - (atr_multiplier * df['atr'])
    df['in_uptrend'] = True

    for current in range(1, len(df.index)):
        previous = current - 1

        if df['Close'][current] > df['upperband'][previous]:
            df['in_uptrend'][current] = True
        elif df['Close'][current] < df['lowerband'][previous]:
            df['in_uptrend'][current] = False
        else:
            df['in_uptrend'][current] = df['in_uptrend'][previous]

            if df['in_uptrend'][current] and df['lowerband'][current] < df['lowerband'][previous]:
                df['lowerband'][current] = df['lowerband'][previous]

            if not df['in_uptrend'][current] and df['upperband'][current] > df['upperband'][previous]:
                df['upperband'][current] = df['upperband'][previous]

    df['openinterest'] = df['in_uptrend']

    return df
