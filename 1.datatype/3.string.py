str = 'hello world'
str = "hello world"
str = 'hello "world"'
str = "hello 'world'"
str = '''
    python can be ...
    whether 
    or your're
''' 
print(str)

# indexing
str = 'hello world'
print(str[0])
print(str[2])
print(str[-2])

# slicing
print(str[0:3])
print(str[3:])
print(str[:7])

# +
str1 = 'python'
str2 = ' is fun.'
print(str1 + str2)

# len()
print(len(str1))

# replace()
print(str1.replace('th', 'mo'))

# format()
print('I eat {} apples.'.format(5))
print('I love {} and {}.'.format('you', 'me'))
fruitName = 'banana'
print(f'I wash the {fruitName}.')

# split()
str = 'python,is,fun'
print(str.split(','))
str = 'python is fun.'
print(str.split())

# upper(), lower()
print(str.upper())
print(str.lower())

# strip
str = '   hello    '
print(f'|{str.lstrip()}|')
print(f'|{str.rstrip()}|')
print(f'|{str.strip()}|')

str = '--hello-'
print(str.strip('-'))