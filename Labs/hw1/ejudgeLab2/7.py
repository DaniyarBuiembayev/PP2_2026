n = int(input())
nums = input().split()
maximum = int(nums[0])
positionOfMaximum = 0
for i in range(n):
    if(maximum < int(nums[i])):
        maximum = int(nums[i])
        positionOfMaximum = i
print(positionOfMaximum+1)