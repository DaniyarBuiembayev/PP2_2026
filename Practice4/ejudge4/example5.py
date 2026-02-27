def CountDown(n):
    while(n>=0):
        yield n
        n-=1






n =int(input())   
for num in CountDown(n):
    print(num)