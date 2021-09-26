import csv
from binance import Client

client = Client()

columns = [
    'open_time', 'open', 'high', 'low', 'close', 'volume',
    'close_time', 'quote_asset_volume', 'number_of_trades',
    'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume',
    'ignore'
]

symbols = ["AVAX", "ETH", "HNT", "CHZ", "LINK",
           "IOTA", "FIL", "AR", "BTC", "ORN"]

# symbols = ["1INCH", "1INCHDOWN", "1INCHUP", "AAVE", "AAVEDOWN", "AAVEUP", "ACM", "ADA", "ADADOWN", "ADAUP", "AION", "AKRO", "ALGO", "ALICE", "ALPACA", "ALPHA", "ANKR", "ANT", "AR", "ARDR", "ARPA", "ASR", "ATA", "ATM", "ATOM", "AUD", "AUDIO", "AUTO", "AVA", "AVAX", "AXS", "BADGER", "BAKE", "BAL", "BAND", "BAR", "BAT", "BCC", "BCH", "BCHABC", "BCHDOWN", "BCHSV", "BCHUP", "BEAM", "BEAR", "BEL", "BIDR", "BKRW", "BKRW", "BLZ", "BNB", "BNBBEAR", "BNBBULL", "BNBDOWN", "BNBUP", "BNT", "BOND", "BRL", "BRY", "BTC", "BTCDOWN", "BTCST", "BTCUP", "BTG", "BTS", "BTT", "BULL", "BURGER", "BUSD", "BVND", "BZRX", "C98", "CAKE", "CELO", "CELR", "CFX", "CHR", "CHZ", "CKB", "CLV", "COCOS", "COMP", "COS", "COTI", "CRV", "CTK", "CTSI", "CTXC", "CVC", "DAI", "DAI", "DASH", "DATA", "DCR", "DEGO", "DENT", "DEXE", "DF", "DGB", "DIA", "DNT", "DOCK", "DODO", "DOGE", "DOT", "DOTDOWN", "DOTUP", "DREP", "DUSK", "DYDX", "EGLD", "ELF", "ENJ", "EOS", "EOSBEAR", "EOSBULL", "EOSDOWN", "EOSUP", "EPS", "ERD", "ERN", "ETC", "ETH", "ETHBEAR", "ETHBULL", "ETHDOWN", "ETHUP", "EUR", "FARM", "FET", "FIL", "FILDOWN", "FILUP", "FIO", "FIRO", "FIS", "FLM", "FLOW", "FOR", "FORTH", "FTM", "FTT", "FUN", "GALA", "GBP", "GHST", "GNO", "GRT", "GTC", "GTO", "GXS", "GYEN", "HARD", "HBAR", "HC", "HIVE", "HNT", "HOT", "ICP", "ICX", "IDEX", "IDRT", "ILV", "INJ", "IOST", "IOTA", "IOTX", "IRIS", "JST", "JUV", "KAVA",
#            "KEEP", "KEY", "KLAY", "KMD", "KNC", "KSM", "LEND", "LINA", "LINK", "LINKDOWN", "LINKUP", "LIT", "LPT", "LRC", "LSK", "LTC", "LTCDOWN", "LTCUP", "LTO", "LUNA", "MANA", "MASK", "MATIC", "MBL", "MBOX", "MCO", "MDT", "MDX", "MFT", "MINA", "MIR", "MITH", "MKR", "MLN", "MTL", "NANO", "NBS", "NEAR", "NEO", "NGN", "NKN", "NMR", "NPXS", "NU", "NULS", "OCEAN", "OG", "OGN", "OM", "OMG", "ONE", "ONG", "ONT", "ORN", "OXT", "PAX", "PAXG", "PERL", "PERP", "PHA", "PNT", "POLS", "POLY", "POND", "PSG", "PUNDIX", "QNT", "QTUM", "QUICK", "RAMP", "RAY", "REEF", "REN", "REP", "REQ", "RIF", "RLC", "ROSE", "RSR", "RUB", "RUNE", "RVN", "SAND", "SC", "SFP", "SHIB", "SKL", "SLP", "SNX", "SOL", "SRM", "STMX", "STORJ", "STORM", "STPT", "STRAT", "STRAX", "STX", "SUN", "SUPER", "SUSD", "SUSHI", "SUSHIDOWN", "SUSHIUP", "SXP", "SXPDOWN", "SXPUP", "SYS", "TCT", "TFUEL", "THETA", "TKO", "TLM", "TOMO", "TORN", "TRB", "TRIBE", "TROY", "TRU", "TRX", "TRXDOWN", "TRXUP", "TRY", "TUSD", "TVK", "TWT", "UAH", "UMA", "UNFI", "UNI", "UNIDOWN", "UNIUP", "USDC", "USDP", "USDS", "USDSB", "UTK", "VEN", "VET", "VIDT", "VITE", "VTHO", "WAN", "WAVES", "WAXP", "WIN", "WING", "WNXM", "WRX", "WTC", "XEC", "XEM", "XLM", "XLMDOWN", "XLMUP", "XMR", "XRP", "XRPBEAR", "XRPBULL", "XRPDOWN", "XRPUP", "XTZ", "XTZDOWN", "XTZUP", "XVG", "XVS", "XZC", "YFI", "YFIDOWN", "YFII", "YFIUP", "YGG", "ZAR", "ZEC", "ZEN", "ZIL", "ZRX"]

for symbol in symbols:

    try:
        klines = client.get_historical_klines(
            f"{symbol}USDT", Client.KLINE_INTERVAL_45MINUTE, "1 Jan, 2021")
    except:
        print(f'{symbol} error')
        continue

    fname = f"{symbol}USDT_2021-2021_45m"

    with open(f'data/{fname}.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(columns)
        write.writerows(klines)
