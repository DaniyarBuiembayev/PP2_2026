n = int(input())
nums = list(map(int, input().split()))

freq = {}

for x in nums:
    if x in freq:
        freq[x] += 1
    else:
        freq[x] = 1

max_count = max(freq.values())

answer = None
for key in freq:
    if freq[key] == max_count:
        if answer is None or key < answer:
            answer = key

print(answer)
