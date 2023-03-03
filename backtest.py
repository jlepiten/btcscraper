import numpy as np
import pandas as pd
from datetime import datetime
import vectorbt as vbt

num = 10
metric = "total_return"

btc_price = pd.read_csv("batusd2023-01-01to2023-01-31.csv")[["timestamp", "close"]]
btc_price["date"] = pd.to_datetime( btc_price["timestamp"], unit = "s")
btc_price = btc_price.set_index("date")["close"]

rsi = vbt.RSI.run(btc_price, window = 14, short_name="rsi")

entry_points = np.linspace(1,30, num=num)
exit_points = np.linspace(70,99, num=num)

entries = rsi.rsi_crossed_below(list(entry_points))
exits = rsi.rsi_crossed_above(list(exit_points))

pf = vbt.Portfolio.from_signals(btc_price, entries, exits)
pf_perf = pf.deep_getattr(metric)
pf_perf_matrix = pf_perf.vbt.unstack_to_df(index_levels = "rsi_crossed_above", column_levels = "rsi_crossed_below")

print(pf_perf_matrix)
heatmap = vbt.plotting.Heatmap(
    data=pf_perf_matrix,
    x_labels=exit_points,
    y_labels=entry_points
)
heatmap.fig