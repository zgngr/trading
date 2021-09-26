import backtrader as bt
import pandas as pd
import math


class BuyHold(bt.Strategy):

    def start(self):
        self.val_start = self.broker.get_cash()

    def nextstart(self):
        size = math.floor((0.99 * self.broker.cash) / self.data.close)
        self.buy(size=size)


def apply(input):
    return input
