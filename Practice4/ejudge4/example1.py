def squaresOfNumbers(n):
    counter = 1
    for counter in range(1, n+1):
        yield counter**2
        




n = int(input())
for num in squaresOfNumbers(n):
    print(num)