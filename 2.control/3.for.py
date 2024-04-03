box = [1, 2, 3]
for num in box:
    print(num, end=' ')

print()
for num in [1, 2, 3]:
    print(num, end=',')

print()
for num in range(1, 4):
    print(num, end=' ')

print()
for num in range(1, 5, 2):
    print(num, end=' ')

print()
dic = {'월드콘': 2000, '붕어': 3000, '메로나': 1000}
for key in dic:
    print(key, end=' ')

print()
for key, val in dic.items():
    print(key, val, end='/')