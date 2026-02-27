import sys
import math

r = float(sys.stdin.readline())
x1, y1 = map(float, sys.stdin.readline().split())
x2, y2 = map(float, sys.stdin.readline().split())

dx = x2 - x1
dy = y2 - y1

a = dx*dx + dy*dy
b = 2*(x1*dx + y1*dy)
c = x1*x1 + y1*y1 - r*r

disc = b*b - 4*a*c

if a == 0:
    if x1*x1 + y1*y1 <= r*r:
        print("0.0000000000")
    else:
        print("0.0000000000")
    sys.exit()

t0, t1 = 0.0, 1.0

if disc <= 0:
    if x1*x1 + y1*y1 <= r*r and x2*x2 + y2*y2 <= r*r:
        length = math.sqrt(a)
    else:
        length = 0.0
else:
    sqrt_disc = math.sqrt(disc)
    t_enter = (-b - sqrt_disc) / (2*a)
    t_exit = (-b + sqrt_disc) / (2*a)
    t_min = max(0.0, min(t_enter, t_exit))
    t_max = min(1.0, max(t_enter, t_exit))
    if t_max < t_min:
        length = 0.0
    else:
        length = math.sqrt(a) * (t_max - t_min)

print(f"{length:.10f}")