import backtrader as bt
import pandas as pd
import numpy as np
import ta
import math


class StochMacdRsi(bt.Strategy):

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
                self.size = math.floor(
                    (0.95 * self.broker.cash) / self.data.close)
                self.buy(size=self.size)
        else:
            if self.data_openinterest[0] == False and self.data_openinterest[-1] == True:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.sell(size=self.size)

def apply(df, lags):
    
    df['%K'] = ta.momentum.stoch(df.high, df.low, df.close, window=14, smooth_window=3)
    df['%D'] = df['%K'].rolling(3).mean()
    df['rsi'] = ta.momentum.rsi(df.close, window=14)
    df['macd'] = ta.trend.macd_diff(df.close)
    df.dropna(inplace=True)

    dfx = pd.DataFrame()

    def gettrigger(lags):
        dfx = pd.DataFrame()
        for i in range(lags + 1):
            mask = (df['%K'].shift(i) < 20) & (df['%D'].shift(i) < 20)
            dfx = dfx.append(mask, ignore_index=True)
        return dfx.sum(axis=0)
    
    df['trigger'] = np.where(gettrigger(lags), 1, 0)
    df['buy'] = np.where((df.trigger) 
                            & (df['%K'].between(20,80)) 
                            & (df['%D'].between(20,80)) 
                            & (df.rsi > 50) 
                            & (df.macd > 0), 1, 0)
    
    df['openinterest'] = df['buy']


    return df
    