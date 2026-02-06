n = int(input())
nums = input().split()
maximum = int(nums[0])
for i in range(n):
    if(maximum < int(nums[i])):
        maximum = int(nums[i])
print(maximum)