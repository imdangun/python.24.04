import pandas as pd
from numpy import NaN, NAN, nan

print(nan == False)

print(pd.isnull(nan))
print(pd.isnull(0))

print(pd.notnull(nan))
print(pd.notnull(0))

df = pd.read_csv('country_timeseries.csv')
df.info()

print(df.iloc[0:5, 0:5])

print(df.fillna(0).iloc[:5, :5])

print(df.fillna(method='ffill').iloc[0:5, :5])
print(df.fillna(method='bfill').iloc[0:5, :5])

df['Date'] = pd.to_datetime(df['Date'])
print(df.fillna(df.mean()).iloc[:5, :5])

date = ['2024/03/01', '2024/03/02', '2024/03/09', '2024/03/10']
date = pd.to_datetime(date, format='%Y/%m/%d')

values = [1, nan, nan, 10]
series = pd.Series(values, index=date)
print(series)

series = series.interpolate()
print(series)

series = series.interpolate(method='time')
print(series)

df = pd.read_csv('country_timeseries.csv')
print(df.dropna())

idx = df[df['Day'] > 100].index
print(idx)

print(df.drop(idx).iloc[:, :3])