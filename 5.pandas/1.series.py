import pandas as pd

s = pd.Series([10, 20, 30])
print(s)

s = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
print(s)

date = ['2024/04/01', '2024/04/02', '2024/04/03']
date = pd.to_datetime(date, format='%Y/%m/%d')

price = [50000, 55000, 60000]

stock = pd.Series(price, index=date)
print(stock)

print(stock.index)
print(stock.values)