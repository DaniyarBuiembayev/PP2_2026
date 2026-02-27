def even_num(n):
    for i in range(0, n+1, 2):
        yield i

n = int(input("Enter a number: "))   
number = True
for x in even_num(n):
    if number:
        print(x, end="")
        number = False
    else:
        print(f",{x}", end="")