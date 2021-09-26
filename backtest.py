import backtrader as bt
import pandas as pd
import importlib
import warnings
import helpers

pd.set_option('display.max_rows', None)
warnings.filterwarnings('ignore')


def get_winloss(analyzer):
    return analyzer.won.total, analyzer.lost.total, analyzer.pnl.net.total


def get_sqn(analyzer):
    return round(analyzer.sqn, 2)


def run(datapath, start, end, period, strategy, commission_val=None, portofolio=10000.0, stake_val=1, quantity=0.01, plt=False):

    cerebro = bt.Cerebro()

    df = pd.read_csv(datapath, index_col=0)
    df.set_index('close_time', inplace=True)
    df.index = pd.to_datetime(df.index, unit='ms')

    mod = importlib.import_module(f'strategies.{strategy}')

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

    if plt:
        cerebro.plot()

    return cerebro.broker.getvalue(), totalwin, totalloss, pnl_net, sqn
