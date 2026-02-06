n = int(input())
names = []

for i in range(n):
    name = input().strip()
    names.append(name)

print(len(set(names)))
