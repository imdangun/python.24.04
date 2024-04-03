box = (1, 3, 5, 4, 2)

# indexing
print(box[0])
print(box[-1])

# slicing
print(box[2:4])
print(box[1:])
print(box[:3])

box = list(box)
box.append(10)
print(box)

box = tuple(box)
print(box)