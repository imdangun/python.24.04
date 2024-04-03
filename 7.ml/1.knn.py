import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split

samsung = pd.read_csv('full_samsung.csv', index_col='date')
samsung = samsung.sort_index()

data = []
target = []

for i in range(len(samsung) - 1):
    a = list(samsung.iloc[i])
    b = samsung.iloc[i+1, 0]
    data.append(a)
    target.append(b)    

data = np.array(data)
target = np.array(target)

train_input, test_input, train_target, test_target = train_test_split(data, target, test_size=0.2)

knn = KNeighborsRegressor()
knn.fit(train_input, train_target)
print(knn.score(test_input, test_target))