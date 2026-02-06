n = int(input())
nums = list(map(int, input().split()))
l, r = map(int, input().split())

l -= 1
r -= 1

nums[l:r+1] = nums[l:r+1][::-1]

print(*nums)