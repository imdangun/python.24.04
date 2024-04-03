box = [1, 2, 3, 4]
print(box)

# indexing
print(box[0])
print(box[-1])

box[0] = 10
print(box)

# slicing
print(box[1:3])
print(box[1:])
print(box[:3])

# append
box.append(5)
print(box)

# insert
box.insert(1, 1)
print(box)

# del
del box[0]
print(box)

box.append(3)
print(box)
box.remove(3)
print(box)

# max, min
print(max(box))
print(min(box))

# sort
box = [3, 10, 4, 2]
box.sort()
print(box)

box.sort(reverse=True)
print(box)

box = ['car', 'apple', 'banana']
box.sort()
print(box)