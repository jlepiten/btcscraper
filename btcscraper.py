import json
import requests
import pandas as pd
import datetime

currency_pair = "batusd"
url = f"https://www.bitstamp.net/api/v2/ohlc/{currency_pair}/"

start = "2023-01-01"
end = "2023-01-31"
dates = pd.date_range(start, end, freq = "1H")
dates = [ int(x.value/10**9) for x in list(dates)]
#print(dates)

master_data = []

for first, last in zip(dates, dates[1:]):
	print(first, last)

	params = {
		"step":60,
		"limit":60,
		"start":first,
		"end":last,
		}

	data = requests.get(url, params = params)

	data = data.json()["data"]["ohlc"]

	master_data += data



df = pd.DataFrame(master_data)
df["timestamp"] = df["timestamp"].astype(int)
df = df.sort_values(by="timestamp")
#df = df[ df["timestamp"] >= dates[0] ]

print(df)
df.to_csv(f"{currency_pair}{start}to{end}.csv", index=False)

