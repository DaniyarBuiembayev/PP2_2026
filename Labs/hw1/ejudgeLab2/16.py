n = int(input())
names = list(map(int, input().split()))
seen = set()

for x in names:
    if x in seen:
        print("NO")
    else:
        print('YES')    
        seen.add(x)

