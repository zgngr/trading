import backtrader as bt
import pandas as pd
import math


class BuyHold(bt.Strategy):
    
    params = dict(
        verbose=False
    )

    def __init__(self):
        self.order = None
        self.val_start = self.broker.get_cash()
        self.dataclose = self.datas[0].close

    def log(self, txt, dt=None):
        if self.p.verbose:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def start(self):
        self.val_start = self.broker.get_cash()

    def nextstart(self):
        size = math.floor((0.99 * self.broker.cash) / self.data.close)
        self.log('BUY CREATE, %.2f' % self.dataclose[0])
        self.buy(size=size)


def apply(df, *strategy_params):
    return df