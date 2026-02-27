def cycle_list(lst, k):
    for _ in range(k):
        for item in lst:
            yield item


lst = input().split()
k = int(input())

for element in cycle_list(lst, k):
    print(element, end=" ")