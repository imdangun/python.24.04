from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np

samsung = pd.read_csv('full_samsung.csv', index_col='date')
samsung = samsung.sort_index()

data = []
target= []

for i in range(len(samsung) - 1):
    a = list(samsung.iloc[i])
    b = samsung.iloc[i+1, 0]
    data.append(a)
    target.append(b)

data = np.array(data)
target = np.array(target)

rf = RandomForestRegressor()
rf.fit(data, target)

price = rf.predict([[72200, 1300, 71700, 72200, 71600, 12161798]])
print(price)