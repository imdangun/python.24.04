weight = 90
jumpCnt = 0

while weight > 60:
    jumpCnt = jumpCnt + 1
    weight = weight - 1

print(f'{jumpCnt}번 줄넘기해서, {weight}kg이 되었습니다.')