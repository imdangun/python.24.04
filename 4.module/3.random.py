import random

box = [1, 2, 3, 4, 5]
random.shuffle(box)
print(box)

print(random.sample(box, 2))

print(random.randint(1, 5))