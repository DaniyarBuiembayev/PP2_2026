n = int(input())
nums = input().split()

maxNum = int(nums[0])
minNum = int(nums[0])
for i in range(n):
    if(maxNum < int(nums[i])):
        maxNum = int(nums[i])
    if(minNum > int(nums[i])):
        minNum = int(nums[i])
for i in range(n):
    if int(nums[i]) == maxNum:
        nums[i] = str(minNum)
        
print(*nums)

