def split_fname(fname):
    # splitting ETHUSDT_2020-2021_4h.csv
    parts = fname.split('_')
    pair = parts[0]
    year_start = parts[1].split('-')[0]
    year_end = parts[1].split('-')[1]
    timeframe = parts[2][:-4]

    return pair, year_start, year_end, timeframe


def to_clsname(underscore):
    return underscore.title().replace('_', '')
