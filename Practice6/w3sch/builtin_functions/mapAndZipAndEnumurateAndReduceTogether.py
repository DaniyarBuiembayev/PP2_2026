from functools import reduce

data = ["1", "2", "3", "four", "5"]


numbers = list(filter(lambda x: x.isdigit(), data))


numbers = list(map(int, numbers))

for i, n in enumerate(numbers):
    print(i, n)


total = reduce(lambda a, b: a + b, numbers)

print("Numbers:", numbers)
print("Total:", total)