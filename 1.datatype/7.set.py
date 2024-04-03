a = set([1, 2, 3])
print(a)

b = set('hello world')
print(b)

a = set([1, 2, 3])
b = set([3, 4, 5])
print(a & b)
print(a | b)
print(a - b)

a.add(7)
print(a)

b.update([7, 8])
print(b)

b.remove(7)
print(b)