import pickle

box = [1, 3, 5, 4, 2]

f = open('myData.dat', 'wb')
pickle.dump(box, f)
f.close()