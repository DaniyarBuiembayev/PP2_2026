n = int(input())

freq = {}

for i in range(n):
    number = input().strip()
    if number in freq:
        freq[number] += 1
    else:
        freq[number] = 1

answer = 0
for count in freq.values():
    if count == 3:
        answer += 1

print(answer)
