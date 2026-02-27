def squaresFromAtoB(a, b):
    for i in range(a,b+1):
        yield i**2





a, b = map(int, input().split())
for num in squaresFromAtoB(a,b):
    print(num)