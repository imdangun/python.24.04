import pickle

f = open('myData.dat', 'rb')
data = pickle.load(f)

print(data)