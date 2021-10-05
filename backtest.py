import importlib
import warnings

import backtrader as bt
import pandas as pd

import helpers

pd.set_option('display.max_rows', None)
warnings.filterwarnings('ignore')


def get_winloss(analyzer):
    return analyzer.won.total, analyzer.lost.total, analyzer.pnl.net.total


def get_sqn(analyzer):
    return round(analyzer.sqn, 2)


def run(df, period, strategy, commission_val=None, portofolio=10000.0, stake_val=1, quantity=0.01):

    mod = importlib.import_module(f'strategies.{strategy}')

    cerebro = bt.Cerebro()
    cerebro.adddata(bt.feeds.PandasData(dataname=mod.apply(df, period)))
    cerebro.addstrategy(strategy=getattr(mod, helpers.to_clsname(strategy)))
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
    cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")
    cerebro.addsizer(bt.sizers.FixedSize, stake=stake_val)
    cerebro.broker.setcash(portofolio)

    if commission_val:
        cerebro.broker.setcommission(
            commission=commission_val/100)

    strat = cerebro.run()
    stratexe = strat[0]

    try:
        totalwin, totalloss, pnl_net = get_winloss(
            stratexe.analyzers.ta.get_analysis())
    except KeyError:
        totalwin, totalloss, pnl_net = 0, 0, 0

    sqn = get_sqn(stratexe.analyzers.sqn.get_analysis())

    return cerebro.broker.getvalue(), totalwin, totalloss, pnl_net, sqn
