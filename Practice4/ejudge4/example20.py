import sys

n_commands = int(sys.stdin.readline())

g = 0
n = 0

for _ in range(n_commands):
    scope, value = sys.stdin.readline().split()
    value = int(value)
    if scope == "global":
        g += value
    elif scope == "nonlocal":
        n += value

print(g, n)