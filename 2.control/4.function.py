def add(x, y):
    return x + y
result = add(1, 2)
print(result)

def say():
    return 'hi'
print(say())

#
def add(x, y):
    print(x + y)

add(1, 2)

#
def assign():
    a = 5

a = 0
assign()
print(a)

#
def assign2():
    global b
    b = 5

b = 0
assign2()
print(b)

#
def introduce(myName, age, gender=1):
    print(f'{age}살 {myName}입니다.', end=' ')
    if gender == 1: print('남자')
    else: print('여자')

# introduce('최한석')
introduce('최한석', 12)
introduce('최한석', 12, 2)