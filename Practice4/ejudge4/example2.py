def evenGenerator(n):
    counter = 0
    while counter <= n:
        yield counter
        counter += 2


n = int(input())

for num in evenGenerator(n):
    if num + 2 <= n:
        print(num, end=",")
    else:
        print(num, end="")