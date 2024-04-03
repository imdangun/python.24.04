money = 2000
if money > 1000:
    print('taxi')

if money > 3000:
    print('taxi')
else:
    print('bus')

if money > 3000:
    print('taxi')
elif money > 2100:
    print('bus')
else:
    print('walk')

#
money = 2000
card = 1
if money >= 3000 and card == 1:
    print('taxi')
else:
    print('walk')

if money >= 3000 or card == 1:
    print('taxi')
else:
    print('walk')

pocket = ['money', 'paper']
if 'card' in pocket:
    print('taxi')
elif 'card' not in pocket:
    print('walk')