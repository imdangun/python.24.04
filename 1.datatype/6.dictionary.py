ice = {'메로나': 1000, '월드콘': 2000}
print(ice)

ice['붕어'] = 3000
print(ice)

# indexing
print(ice['월드콘'])

# value write
ice['월드콘'] = 3100
print(ice['월드콘'])

# del
del ice['월드콘']
print(ice)

print(ice.keys())
print(ice.values())
print(ice.items())