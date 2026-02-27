def squares(N):
    for i in range(N):
        yield i**2

for x in squares(20):
    print(x)