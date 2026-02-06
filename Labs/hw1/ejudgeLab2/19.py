n = int(input())

d = {}

for i in range(n):
    key, value = input().split()
    value = int(value)

    if key in d:
        d[key] += value
    else:
        d[key] = value

for key in sorted(d):
    print(key, d[key])